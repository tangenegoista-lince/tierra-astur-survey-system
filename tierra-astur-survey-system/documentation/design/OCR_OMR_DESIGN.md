# Diseño de Procesamiento OCR/OMR

## Visión General
Este documento detalla el enfoque para el Reconocimiento Óptico de Caracteres (OCR) y el Reconocimiento Óptico de Marcas (OMR) del procesamiento de tarjetas de encuesta de Tierra Astur.

## Pipeline de Procesamiento

1. **Preprocesamiento de Imagen**
2. **Detección de Diseño y Alineación**
3. **Extracción de Región de Interés (ROI)**
4. **Reconocimiento de Texto (OCR) para Áreas Manuscritas**
5. **Detección de Marcas (OMR) para Casillas/Botones**
6. **Ensamblaje y Validación de Datos**
7. **Puntuación de Confianza y Marcado**

## 1. Preprocesamiento de Imagen

### Objetivos:
- Normalizar iluminación y contraste
- Corregir rotaciones y sesgos menores
- Mejorar la claridad de texto y marcas
- Preparar para detección precisa de regiones

### Pasos:
- Convertir a escala de grises
- Aplicar ecualización de histograma adaptativa (CLAHE)
- Desruido usando medias no locales o filtro bilateral
- Detectar y corregir sesgo usando Transformada de Hough o perfilado de proyección
- Redimensionar a DPI estándar (300 DPI recomendado para OCR)

## 2. Detección de Diseño y Alineación

### Enfoque:
- Usar coincidencia de plantilla o alineación basada en características (ORB, SIFT) para alinear la tarjeta escaneada con una plantilla maestra
- Plantilla maestra definida por versión de tarjeta (frontal/trasera)
- Si la coincidencia de plantilla falla, volver a detección de contornos para los límites de la tarjeta
- Aplicar transformación de perspectiva para obtener una vista superior, alineada

### Plan B:
- Si no hay coincidencia de plantilla, usar técnicas de escaneo de documentos (detección de bordes, aproximación de contornos) para encontrar el cuadrilátero de la tarjeta

## 3. Extracción de Región de Interés (ROI)

Basado en el PRD, necesitamos extraer datos de zonas específicas:
- Nombre del restaurante/encabezado
- Zona/sector
- Fecha y hora
- Grupos de calificaciones (Cocina, Personal, Sidra, Estado de la sidrería)
- Preguntas Sí/No
- Observaciones/sugerencias
- Información de contacto (nombre completo, ciudad, teléfono, email)

### Método:
- Definir coordenadas de ROI relativas a la plantilla alineada
- Usar un archivo de configuración (JSON) que mapee nombres de campos a:
  - Caja delimitadora (x, y, ancho, alto) como porcentaje de dimensiones de la tarjeta
  - Tipo de campo (texto, omr, fecha, etc.)
  - Formato esperado/reglas de validación
  - Parámetros del motor OCR/OMR por región

### Ejemplo de Configuración de ROI:
```json
{
  "nombre_restaurante": {
    "bbox": [0.1, 0.05, 0.8, 0.1],
    "tipo": "texto",
    "preprocesamiento": ["umbral", "invertir"],
    "config_ocr": "--psm 6",
    "validacion": "requerido"
  },
  "fecha_encuesta": {
    "bbox": [0.1, 0.2, 0.3, 0.05],
    "tipo": "fecha",
    "preprocesamiento": ["umbral"],
    "config_ocr": "--psm 7 -c tessedit_char_whitelist=0123456789/-",
    "validacion": "formato_fecha"
  }
}
```

## 4. Reconocimiento de Texto (OCR) para Áreas Manuscritas

### Elección de Motor:
- Principal: Tesseract OCR (código abierto, bueno para formularios estructurados)
- Alternativa/Piloto: Google Cloud Vision API o Azure Computer Vision para mayor precisión si es necesario

### Específicos de Escritura a Mano:
- Tesseract tiene capacidad limitada para escritura a mano; entrenaremos modelos personalizados si la precisión es insuficiente
- Para el MVP, asumimos escritura a mano estructurada (campos con cuadros o guías) que Tesseract puede manejar con preprocesamiento adecuado
- Usar listas blancas y ajuste de PSM (Modo de Segmentación de Página) por campo:
  - Fechas: `--psm 7 -c tessedit_char_whitelist=0123456789/-`
  - Números de teléfono: `--psm 7 -c tessedit_char_whitelist=0123456789+()-`
  - Email: `--psm 7` (menos restrictivo, luego validar con regex)
  - Texto general: `--psm 6` (asumir bloque uniforme de texto)

### Preprocesamiento para OCR:
- Binarización (Otsu o umbral adaptativo)
- Inversión si el texto es claro sobre fondo oscuro
- Dilatación/erosión para conectar caracteres rotos
- Despeckling

## 5. Detección de Marcas (OMR) para Casillas/Botones

### Enfoque:
- Para cada grupo de calificaciones (escala 1-5) y preguntas sí/no, detectar qué casilla está marcada
- Pasos por ROI:
  a. Extraer el ROI (conteniendo la fila de casillas)
  b. Binarizar (invertir si las marcas son oscuras)
  c. Encontrar contornos de casillas individuales
  d. Para cada casilla, calcular el porcentaje de píxeles oscuros (ratio de llenado)
  e. Aplicar umbral para determinar si está marcada (ej. >30% de llenado = marcada)
  f. Manejar casos extremos:
     - Ninguna marca -> vacío/nulo
     - Múltiples marcas -> marcar como inconsistente
     - Marcas ambiguas -> baja confianza

### Configuración por ROI de OMR:
```json
{
  "cocina_elaboracion_en_cocina": {
    "bbox": [0.2, 0.4, 0.6, 0.05],
    "tipo": "omr",
    "config_omr": {
      "conteo_casillas": 5,
      "espaciado_casillas": "igual",
      "umbral_marca": 0.3,
      "invertir": true
    },
    "validacion": "una_marca_por_fila"
  }
}
```

### Post-Procesamiento:
- Mapear casilla marcada a valor (la más a la izquierda=1, la más a la derecha=5)
- Para sí/no: izquierda=no (0), derecha=sí (5) según reglas de normalización
- Calcular confianza basado en la diferencia de ratio de llenado entre la primera y segunda opción

## 6. Ensamblaje y Validación de Datos

### Estructura de Salida por Tarjeta:
```json
{
  "id_encuesta": "uuid",
  "extraido_crudo": {
    "nombre_restaurante": "EL VASCO - OVIEDO",
    "fecha_encuesta": "2026-04-15",
    ...
  },
  "normalizado": {
    "nombre_restaurante": "EL VASCO - OVIEDO",
    "fecha_encuesta": "2026-04-15",
    "cocina_elaboracion_en_cocina": 4,
    ...
  },
  "confianza": {
    "nombre_restaurante": 0.95,
    "fecha_encuesta": 0.87,
    "cocina_elaboracion_en_cocina": 0.92,
    ...
  },
  "banderas": {
    "fecha_encuesta": false,
    "cocina_elaboracion_en_cocina": false,
    "email": true  // ejemplo: baja confianza o formato inválido
  },
  "metadatos_procesamiento": {
    "motor_ocr": "tesseract 5.3.0",
    "tiempo_procesamiento_ms": 1200,
    "alineado": true,
    "plantilla_usada": "frontal_v2"
  }
}
```

### Reglas de Validación:
- **Campos requeridos**: nombre_restaurante, fecha_encuesta (al menos)
- **Validación de formato**:
  - Fecha: fecha de calendario válida
  - Teléfono: regex para formato español (+34 o prefijos 0/6/7/9)
  - Email: regex estándar
  - Calificaciones: debe ser 1-5 o nulo
  - Sí/no: debe ser 0 o 5 (después de normalización) o nulo
- **Comprobaciones de consistencia**:
  - Ninguna marca múltiple en la misma fila OMR
  - Si el grupo de sidra es todo nulo, es aceptable (el cliente no bebió sidra)
- **Umbrales de confianza**:
  - Marcar para revisión si la confianza de cualquier campo < 0.7
  - Marcar para revisión si la validación falla
  - Marcar para revisión si se detectan marcas múltiples

## 7. Puntuación de Confianza y Marcado

### Confianza Por Campo:
- **Campos OCR**: Usar salida de confianza de Tesseract (promedio de confianzas de palabras en ROI)
- **Campos OMR**: 
  - Confianza = 1 - (|ratio_llenado_primero - ratio_llenado_segundo| / ratio_llenado_primero) 
  - Si solo una marca está por encima del umbral, confianza basada en qué claramente destaca
  - Si no hay marcas o marcas múltiples, confianza = 0.0 (o valor bajo fijo)

### Confianza General de la Tarjeta:
- Promedio ponderado de confianzas de campos (pesos por importancia de campo)
- Alternativamente, confianza mínima entre campos críticos

### Lógica de Marcado:
Crear `esta_marcado_para_revisión` verdadero si:
- Cualquier campo requerido está vacío o es inválido
- Cualquier campo tiene confianza < umbral (ej. 0.7)
- Cualquier regla de validación falla (formato, consistencia)
- Se detectan marcas múltiples en cualquier fila OMR
- Baja confianza general (< 0.6)

## 8. Manejo de Variabilidades

### Variaciones de Tarjeta:
- Diferentes nombres/colores de restaurantes en el encabezado -> manejado por OCR en ROI de nombre_restaurante
- Ligeramente diferentes diseños -> coincidencia de plantilla con tolerancia; fallback a detección de ROI flexible
- Diferentes resoluciones de escaneo -> normalizar a 300 DPI temprano en el pipeline

### Variabilidades de Escritura a Mano:
- Cursiva vs impresión: Tesseract funciona mejor con caracteres aislados; preprocesamiento para romper cursiva conectada si es necesario
- Mayúsculas y minúsculas mezcladas: OCR es sensible a mayúsculas/minúsculas; convertiremos a mayúsculas/minúsculas deseadas post-OCR si es necesario
- Baja calidad: confiar en puntuación de confianza para marcar para revisión

## 9. Consideraciones de Rendimiento para Alto Volumen (7000-8000/semana)

### Optimizaciones:
- **Procesamiento paralelo**: Procesar múltiples tarjetas concurrentemente (limitado por CPU/RAM)
- **Caché**: Almacenar en caché resultados de coincidencia de plantilla si el lote tiene la misma versión de tarjeta
- **OCR eficiente**: 
  - Ejecutar OCR solo en ROIs definidas, no en toda la tarjeta
  - Usar `--psm` de Tesseract para limitar procesamiento
- **Procesamiento asíncrono**: 
  - Subir -> almacenar -> encolar -> procesar -> almacenar resultados
  - Usar cola de mensajes (Redis/RabbitMQ) o cola basada en archivos simple para MVP
- **Límites de recursos**: 
  - Establecer timeout por tarjeta (ej. 5 segundos) para evitar procesos bloqueados
  - Mecanismo de reintento con parámetros diferentes para tarjetas fallidas

### Monitoreo:
- Rastrear tiempo de procesamiento por tarjeta
- Rastrear tasas de éxito de OCR/OMR
- Rastrear tasas de marcado (para ajustar umbrales)
- Alertar sobre acumulación de procesamiento

## 10. Herramientas y Bibliotecas

### Principales:
- **Tesseract OCR** (vía envoltorio: pytesseract para Python, o tesseract.js para Node.js)
- **OpenCV** (para procesamiento de imagen, detección de contornos, coincidencia de plantilla)
- **NumPy** (para operaciones de arreglos en ratio de llenado OMR)

### Alternativas/Evaluaciones:
- **Google ML Kit** o **Azure Form Recognizer** para mayor precisión OCR/OMR (si el presupuesto lo permite)
- **TensorFlow/PyTorch** para modelos entrenados personalmente si el código abierto es insuficiente

### Elección de Lenguaje:
- Para MVP: Python (ecosistema rico para CV/ML)
- Para producción: Considerar Node.js si frontend/backend es JS para uniformidad

## 11. Integración con el Sistema

### Entrada:
- Archivo de imagen (JPG, PNG, primera página de PDF) o PDF multipágina (dividido en imágenes)

### Salida:
- Datos estructurados según `encuesta_encabezado_extracciones` y tablas relacionadas
- Imagen original almacenada en Almacenamiento de Supabase
- Metadatos de procesamiento y puntuaciones de confianza almacenados

### Manejo de Errores:
- Si la imagen no puede cargarse o alinearse -> marcar como fallido, almacenar error
- Si el motor OCR falla -> fallback a cola manual o reintentar con diferentes ajustes
- Siempre preservar la imagen original para reprocesamiento

## 12. Mejoras Futuras

### Mejora de Escritura a Mano:
- Recopilar datos etiquetados para entrenar modelo de escritura a mano personalizado (red neuronal recurrente o transformer)
- Usar aprendizaje semi-supervisado con revisiones marcadas

### Adaptabilidad de Diseño:
- Usar aprendizaje automático (layoutlm) para detectar campos sin plantillas fijas
- Permitir al usuario definir ROIs mediante arrastrar y soltar en interfaz de revisión

### Calibración de Confianza:
- Usar escalado de Platt o regresión isotónica para calibrar confianzas brutas a verdaderas probabilidades

### Verificaciones de Consistencia por Lote:
- Detectar combinaciones imposibles (ej. altas calificaciones pero comentarios negativos) para marcar

## Conclusión
Este diseño de OCR/OMR proporciona un pipeline robusto y configurable para extraer datos de tarjetas de encuesta de Tierra Astur. Equilibra herramientas de uso general (Tesseract, OpenCV) con configurabilidad para adaptarse al diseño específico de la tarjeta y variabilidades. El diseño incluye puntuación de confianza y marcado para asegurar la calidad de datos mientras mantiene un alto rendimiento para el volumen esperado.