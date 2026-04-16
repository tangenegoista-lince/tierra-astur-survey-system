# OCR/OMR Processing Design

## Overview
This document details the approach for Optical Character Recognition (OCR) and Optical Mark Recognition (OMR) processing of Tierra Astur survey cards.

## Processing Pipeline

1. **Image Preprocessing**
2. **Layout Detection and Alignment**
3. **Region of Interest (ROI) Extraction**
4. **Text Recognition (OCR) for Handwritten Areas**
5. **Mark Detection (OMR) for Checkboxes/Ratings**
6. **Data Assembly and Validation**
7. **Confidence Scoring and Flagging**

## 1. Image Preprocessing

### Goals:
- Normalize lighting and contrast
- Correct minor rotations and skews
- Enhance text and mark clarity
- Prepare for accurate region detection

### Steps:
- Convert to grayscale
- Apply adaptive histogram equalization (CLAHE)
- Denoise using non-local means or bilateral filter
- Detect and correct skew using Hough Line Transform or projection profiling
- Resize to standard DPI (300 DPI recommended for OCR)

## 2. Layout Detection and Alignment

### Approach:
- Use template matching or feature-based alignment (ORB, SIFT) to align scanned card to a master template
- Master template defined per card version (front/back)
- If template matching fails, fall back to contour detection for card boundaries
- Apply perspective transform to get a top-down, aligned view

### Fallback:
- If no template match, use document scanning techniques (edge detection, contour approximation) to find the quadrilateral of the card

## 3. Region of Interest (ROI) Extraction

Based on the PRD, we need to extract data from specific zones:
- Restaurant name/header
- Zone/sector
- Date and time
- Rating groups (Cocina, Personal, Sidra, Estado de la sidrería)
- Yes/No questions
- Observations/suggestions
- Contact information (full name, city, phone, email)

### Method:
- Define ROI coordinates relative to the aligned template
- Use a configuration file (JSON) that maps field names to:
  - Bounding box (x, y, width, height) as percentage of card dimensions
  - Field type (text, omr, date, etc.)
  - Expected format/validation rules
  - OCR/OMR engine parameters per region

### Example ROI Configuration:
```json
{
  "restaurant_name": {
    "bbox": [0.1, 0.05, 0.8, 0.1],
    "type": "text",
    "preprocessing": ["threshold", "invert"],
    "ocr_config": "--psm 6",
    "validation": "required"
  },
  "survey_date": {
    "bbox": [0.1, 0.2, 0.3, 0.05],
    "type": "date",
    "preprocessing": ["threshold"],
    "ocr_config": "--psm 7 -c tessedit_char_whitelist=0123456789/-",
    "validation": "date_format"
  }
}
```

## 4. Text Recognition (OCR) for Handwritten Areas

### Engine Choice:
- Primary: Tesseract OCR (open source, good for structured forms)
- Alternative/Pilot: Google Cloud Vision API or Azure Computer Vision for higher accuracy if needed

### Handwriting Specifics:
- Tesseract has limited handwriting capability; we will train custom models if accuracy is insufficient
- For MVP, we assume structured handwriting (boxed or guided fields) which Tesseract can handle with proper preprocessing
- Use whitelists and PSM (Page Segmentation Mode) tuning per field:
  - Dates: `--psm 7 -c tessedit_char_whitelist=0123456789/-`
  - Phone numbers: `--psm 7 -c tessedit_char_whitelist=0123456789+()-`
  - Email: `--psm 7` (less restrictive, then validate with regex)
  - General text: `--psm 6` (assume uniform block of text)

### Preprocessing for OCR:
- Binarization (Otsu or adaptive threshold)
- Inversion if text is light on dark background
- Dilation/erosion to connect broken characters
- Despeckling

## 5. Mark Detection (OMR) for Checkboxes/Ratings

### Approach:
- For each rating group (1-5 scale) and yes/no questions, detect which box is marked
- Steps per ROI:
  a. Extract the ROI (containing the row of boxes)
  b. Binarize (invert if marks are dark)
  c. Find contours of individual boxes
  d. For each box, calculate the percentage of dark pixels (fill ratio)
  e. Apply threshold to determine if marked (e.g., >30% fill = marked)
  f. Handle edge cases:
     - No marks -> empty/null
     - Multiple marks -> flag as inconsistent
     - Ambiguous marks -> low confidence

### Configuration per OMR ROI:
```json
{
  "cocina_elaboracion_en_cocina": {
    "bbox": [0.2, 0.4, 0.6, 0.05],
    "type": "omr",
    "omr_config": {
      "box_count": 5,
      "box_spacing": "equal",
      "mark_threshold": 0.3,
      "invert": true
    },
    "validation": "single_mark_per_row"
  }
}
```

### Post-Processing:
- Map marked box to value (leftmost=1, rightmost=5)
- For yes/no: left=no (0), right=yes (5) per normalization rules
- Calculate confidence based on fill ratio difference between top choice and second choice

## 6. Data Assembly and Validation

### Output Structure per Card:
```json
{
  "survey_id": "uuid",
  "raw_extracted": {
    "restaurant_name": "EL VASCO - OVIEDO",
    "survey_date": "2026-04-15",
    ...
  },
  "normalized": {
    "restaurant_name": "EL VASCO - OVIEDO",
    "survey_date": "2026-04-15",
    "cocina_elaboracion_en_cocina": 4,
    ...
  },
  "confidence": {
    "restaurant_name": 0.95,
    "survey_date": 0.87,
    "cocina_elaboracion_en_cocina": 0.92,
    ...
  },
  "flags": {
    "survey_date": false,
    "cocina_elaboracion_en_cocina": false,
    "email": true  // example: low confidence or invalid format
  },
  "processing_metadata": {
    "ocr_engine": "tesseract 5.3.0",
    "processing_time_ms": 1200,
    "aligned": true,
    "template_used": "front_v2"
  }
}
```

### Validation Rules:
- **Required fields**: restaurant_name, survey_date (at least)
- **Format validation**:
  - Date: valid calendar date
  - Phone: regex for Spanish format (+34 or 0/6/7/9 prefixes)
  - Email: standard regex
  - Ratings: must be 1-5 or null
  - Yes/no: must be 0 or 5 (after normalization) or null
- **Consistency checks**:
  - No multiple marks in same OMR row
  - If sidra group all null, that's acceptable (customer didn't drink sidra)
- **Confidence thresholds**:
  - Flag for review if any field confidence < 0.7
  - Flag for review if validation fails
  - Flag for review if multiple marks detected

## 7. Confidence Scoring and Flagging

### Per-Field Confidence:
- **OCR fields**: Use Tesseract's confidence output (average of word confidences in ROI)
- **OMR fields**: 
  - Confidence = 1 - (|fill_ratio_top - fill_ratio_second| / fill_ratio_top) 
  - If only one mark above threshold, confidence based on how clearly it stands out
  - If no marks or multiple marks, confidence = 0.0 (or low fixed value)

### Overall Card Confidence:
- Weighted average of field confidences (weights by field importance)
- Alternatively, minimum confidence across critical fields

### Flagging Logic:
Create `is_flagged_for_review` true if:
- Any required field is empty or invalid
- Any field confidence < threshold (e.g., 0.7)
- Any validation rule fails (format, consistency)
- Multiple marks detected in any OMR row
- Low overall confidence (< 0.6)

## 8. Handling Variabilities

### Card Variations:
- Different restaurant names/colors in header -> handled by OCR in restaurant_name ROI
- Slightly different layouts -> template matching with tolerance; fallback to flexible ROI detection
- Different scan resolutions -> normalize to 300 DPI early in pipeline

### Handwriting Variabilities:
- Cursive vs print: Tesseract does best with isolated characters; preprocessing to break connected cursive if needed
- Mixed case: OCR is case-sensitive; we will convert to desired case post-OCR if needed
- Poor quality: rely on confidence scoring to flag for review

## 9. Performance Considerations for High Volume (7000-8000/week)

### Optimizations:
- **Parallel processing**: Process multiple cards concurrently (limited by CPU/RAM)
- **Caching**: Cache template matching results if same card version batch
- **Efficient OCR**: 
  - Only run OCR on defined ROIs, not whole card
  - Use Tesseract's `--psm` to limit processing
- **Asynchronous processing**: 
  - Upload -> store -> queue -> process -> store results
  - Use message queue (Redis/RabbitMQ) or simple file-based queue for MVP
- **Resource limits**: 
  - Set timeout per card (e.g., 5 seconds) to prevent stuck processes
  - Retry mechanism with different parameters for failed cards

### Monitoring:
- Track processing time per card
- Track OCR/OMR success rates
- Track flagging rates (to tune thresholds)
- Alert on processing backlog

## 10. Tools and Libraries

### Primary:
- **Tesseract OCR** (via wrapper: pytesseract for Python, or tesseract.js for Node.js)
- **OpenCV** (for image processing, contour detection, template matching)
- **NumPy** (for array operations in OMR fill ratio)

### Alternatives/Evaluations:
- **Google ML Kit** or **Azure Form Recognizer** for higher accuracy OCR/OMR (if budget allows)
- **TensorFlow/PyTorch** for custom trained models if open source insufficient

### Language Choice:
- For MVP: Python (rich ecosystem for CV/ML)
- For production: Consider Node.js if frontend/backend is JS for uniformity

## 11. Integration with System

### Input:
- Image file (JPG, PNG, PDF first page) or PDF multipage (split into images)

### Output:
- Structured data as per `survey_card_extractions` and related tables
- Original image stored in Supabase Storage
- Processing metadata and confidence scores stored

### Error Handling:
- If image cannot be loaded or aligned -> mark as failed, store error
- If OCR engine fails -> fallback to manual queue or retry with different settings
- Always preserve original image for re-processing

## 12. Future Enhancements

### Handwriting Improvement:
- Collect labeled data to train custom handwriting model (CRNN or Transformer)
- Use semi-supervised learning with flagged reviews

### Layout Adaptability:
- Use machine learning (layoutlm) to detect fields without fixed templates
- Allow user to define ROIs via drag-and-drop in review interface

### Confidence Calibration:
- Use Platt scaling or isotonic regression to calibrate raw confidences to true probabilities

### Batch Consistency Checks:
- Detect impossible combinations (e.g., high ratings but negative comments) for flagging

## Conclusion
This OCR/OMR design provides a robust, configurable pipeline for extracting data from Tierra Astur survey cards. It balances off-the-shelf tools (Tesseract, OpenCV) with configurability to adapt to the specific card layout and variabilities. The design includes confidence scoring and flagging to ensure data quality while maintaining high throughput for the expected volume.