# Database Schema

## Overview
This document outlines the database schema for the Tierra Astur Survey Card Data Extraction System.

## Core Entities

### 1. Surveys
Represents each individual survey card processed.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each survey |
| card_image_url | TEXT | NOT NULL | URL/path to the original scanned card image |
| ocr_raw_text | TEXT | | Raw text extracted from OCR process |
| processed_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the survey was processed |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |
| status | VARCHAR(20) | DEFAULT 'pending' | Status: pending, processing, validated, error, archived |
| validation_score | DECIMAL(3,2) | | Confidence score from validation (0.00 to 1.00) |
| batch_id | UUID | FOREIGN KEY | Reference to processing batch |

### 2. Survey Questions
Defines the questions that appear on the survey cards.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each question |
| question_text | TEXT | NOT NULL | The actual question text |
| question_type | VARCHAR(50) | NOT NULL | Type: multiple_choice, text, rating, date, etc. |
| options | JSONB | | For multiple choice: array of possible options |
| validation_rules | JSONB | | Rules for validating responses |
| required | BOOLEAN | DEFAULT false | Whether answer is required |
| display_order | INTEGER | | Order in which question appears on card |
| section | VARCHAR(100) | | Section/grouping of question on card |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

### 3. Survey Responses
Stores individual answers to survey questions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each response |
| survey_id | UUID | FOREIGN KEY (surveys.id) | Reference to the survey |
| question_id | UUID | FOREIGN KEY (survey_questions.id) | Reference to the question |
| answer_value | TEXT | | The actual response value |
| answer_type | VARCHAR(20) | | Detected type: text, number, date, choice |
| confidence_score | DECIMAL(3,2) | | OCR confidence for this specific answer |
| validated | BOOLEAN | DEFAULT false | Whether answer passed validation |
| validation_notes | TEXT | | Notes from validation process |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

### 4. Processing Batches
Groups surveys processed together for tracking and management.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each batch |
| batch_name | VARCHAR(200) | NOT NULL | Descriptive name for the batch |
| total_surveys | INTEGER | DEFAULT 0 | Total number of surveys in batch |
| processed_surveys | INTEGER | DEFAULT 0 | Number of surveys successfully processed |
| failed_surveys | INTEGER | DEFAULT 0 | Number of surveys that failed processing |
| started_at | TIMESTAMP | | When batch processing started |
| completed_at | TIMESTAMP | | When batch processing completed |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

### 5. Users / Operators
System users who can upload, monitor, and manage surveys.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each user |
| username | VARCHAR(100) | UNIQUE NOT NULL | Login username |
| email | VARCHAR(255) | UNIQUE NOT NULL | Email address |
| full_name | VARCHAR(200) | NOT NULL | Full name of user |
| role | VARCHAR(50) | NOT NULL | Role: admin, operator, viewer |
| is_active | BOOLEAN | DEFAULT true | Whether account is active |
| last_login | TIMESTAMP | | Last login timestamp |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

### 6. Audit Log
Tracks important actions for compliance and debugging.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier for each log entry |
| user_id | UUID | FOREIGN KEY (users.id) | User who performed action |
| action_type | VARCHAR(100) | NOT NULL | Type of action: upload, validate, export, etc. |
| entity_type | VARCHAR(50) | | Type of entity affected: survey, batch, etc. |
| entity_id | UUID | | ID of entity affected |
| details | JSONB | | Additional details about the action |
| ip_address | INET | | IP address of user |
| user_agent | TEXT | | User agent string |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp of action |

## Indexes
For performance with high volume (7000-8000 surveys/week):

1. **Surveys table:**
   - Index on `status` for filtering pending/processing surveys
   - Index on `processed_at` for time-based queries
   - Index on `batch_id` for batch-related queries
   - Composite index on `(status, processed_at)` for queue processing

2. **Survey Responses table:**
   - Index on `survey_id` for retrieving all responses for a survey
   - Index on `question_id` for analytics across questions
   - Composite index on `(survey_id, question_id)` for lookups

3. **Batches table:**
   - Index on `started_at` for time-based batch queries
   - Index on `completed_at` for completed batch analysis

## Relationships
- One Survey has Many Survey Responses (one-to-many)
- One Survey Question can be answered in Many Survey Responses (one-to-many)
- One Batch contains Many Surveys (one-to-many)
- One User can perform Many Audit Log entries (one-to-many)
- One User can upload/process Many Surveys (one-to-many)

## Constraints and Validation
1. **Survey Status Constraints:**
   - Valid values: 'pending', 'processing', 'validated', 'error', 'archived'
   - Automatic transitions based on processing workflow

2. **Data Integrity:**
   - Foreign key constraints enforce relationships
   - NOT NULL constraints on essential fields
   - CHECK constraints for valid enum values where applicable

3. **Volume Considerations:**
   - Partitioning strategy for Surveys table by month (for 7000-8000/week ≈ 30k-35k/month)
   - Archiving strategy for old completed surveys
   - Batch processing to manage workload peaks

## Sample Queries
### Get pending surveys for processing:
```sql
SELECT * FROM surveys 
WHERE status = 'pending' 
ORDER BY created_at ASC 
LIMIT 100;
```

### Get survey with all responses:
```sql
SELECT s.*, sr.*, sq.question_text, sq.question_type
FROM surveys s
LEFT JOIN survey_responses sr ON s.id = sr.survey_id
LEFT JOIN survey_questions q ON sr.question_id = q.id
WHERE s.id = 'survey-uuid-here';
```

### Get batch processing statistics:
```sql
SELECT 
    b.*,
    COUNT(s.id) as total_surveys,
    COUNT(CASE WHEN s.status = 'validated' THEN 1 END) as validated_surveys,
    COUNT(CASE WHEN s.status = 'error' THEN 1 END) as failed_surveys
FROM batches b
LEFT JOIN surveys s ON b.id = s.batch_id
WHERE b.id = 'batch-uuid-here'
GROUP BY b.id;
```

## Migration Considerations
For handling the expected volume:
1. **Horizontal partitioning** of surveys table by date ranges
2. **Read replicas** for reporting queries
3. **Connection pooling** for database connections
4. **Caching layer** for frequently accessed reference data (questions, etc.)
5. **Backup strategy** with point-in-time recovery

## Technologies Considered
- **Primary Database**: PostgreSQL (for reliability, JSONB support, and scalability)
- **Alternative**: MySQL/MariaDB if PostgreSQL expertise not available
- **ORM/Query Builder**: Prisma, TypeORM, or raw SQL with query builder
- **Connection Pooling**: PgBouncer or built-in pool