# Esquema de Base de Datos

## Visión General
Este documento describe el esquema de base de datos para el Sistema de Extracción de Datos de Tarjetones de Encuesta de Tierra Astur.

## Entidades Principales

### 1. Encuestas
Representa cada tarjeta de encuesta individual procesada.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada encuesta |
| card_image_url | TEXT | NOT NULL | URL/ruta a la imagen original de la tarjeta escaneada |
| ocr_raw_text | TEXT | | Texto bruto extraído del proceso OCR |
| processed_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Cuándo se procesó la encuesta |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de última actualización del registro |
| status | VARCHAR(20) | DEFAULT 'pending' | Estado: pendiente, procesando, validado, error, archivado |
| validation_score | DECIMAL(3,2) | | Puntuación de confianza de la validación (0.00 a 1.00) |
| batch_id | UUID | FOREIGN KEY | Referencia al lote de procesamiento |

### 2. Preguntas de Encuesta
Define las preguntas que aparecen en las tarjetas de encuesta.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada pregunta |
| question_text | TEXT | NOT NULL | El texto real de la pregunta |
| question_type | VARCHAR(50) | NOT NULL | Tipo: multiple_choice, texto, rating, fecha, etc. |
| options | JSONB | | Para multiple choice: array de opciones posibles |
| validation_rules | JSONB | | Reglas para validar respuestas |
| required | BOOLEAN | DEFAULT false | Indica si la respuesta es requerida |
| display_order | INTEGER | | Orden en el que aparece la pregunta en la tarjeta |
| section | VARCHAR(100) | | Sección/agrupación de la pregunta en la tarjeta |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

### 3. Respuestas de Encuesta
Almacena respuestas individuales a las preguntas de la encuesta.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada respuesta |
| survey_id | UUID | FOREIGN KEY (surveys.id) | Referencia a la encuesta |
| question_id | UUID | FOREIGN KEY (survey_questions.id) | Referencia a la pregunta |
| answer_value | TEXT | | El valor real de la respuesta |
| answer_type | VARCHAR(20) | | Tipo detectado: texto, número, fecha, opción |
| confidence_score | DECIMAL(3,2) | | Confianza OCR para esta respuesta específica |
| validated | BOOLEAN | DEFAULT false | Indica si la respuesta pasó la validación |
| validation_notes | TEXT | | Notas del proceso de validación |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

### 4. Lotes de Procesamiento
Agrupa encuestas procesadas juntas para seguimiento y gestión.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada lote |
| batch_name | VARCHAR(200) | NOT NULL | Nombre descriptivo para el lote |
| total_surveys | INTEGER | DEFAULT 0 | Número total de encuestas en el lote |
| processed_surveys | INTEGER | DEFAULT 0 | Número de encuestas procesadas correctamente |
| failed_surveys | INTEGER | DEFAULT 0 | Número de encuestas que fallaron el procesamiento |
| started_at | TIMESTAMP | | Cuando comenzó el procesamiento del lote |
| completed_at | TIMESTAMP | | Cuando terminó el procesamiento del lote |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

### 5. Usuarios / Operadores
Usuarios del sistema que pueden subir, monitorear y gestionar encuestas.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada usuario |
| username | VARCHAR(100) | UNIQUE NOT NULL | Nombre de usuario para iniciar sesión |
| email | VARCHAR(255) | UNIQUE NOT NULL | Dirección de correo electrónico |
| full_name | VARCHAR(200) | NOT NULL | Nombre completo del usuario |
| role | VARCHAR(50) | NOT NULL | Rol: admin, operador, visualizador |
| is_active | BOOLEAN | DEFAULT true | Indica si la cuenta está activa |
| last_login | TIMESTAMP | | Marca de tiempo del último inicio de sesión |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de última actualización del registro |

### 6. Registro de Auditoría
Rastrea acciones importantes para cumplimiento y depuración.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PRIMARY KEY | Identificador único para cada entrada de registro |
| user_id | UUID | FOREIGN KEY (users.id) | Usuario que realizó la acción |
| action_type | VARCHAR(100) | NOT NULL | Tipo de acción: subir, validar, exportar, etc. |
| entity_type | VARCHAR(50) | | Tipo de entidad afectada: encuesta, lote, etc. |
| entity_id | UUID | | ID de la entidad afectada |
| details | JSONB | | Detalles adicionales sobre la acción |
| ip_address | INET | | Dirección IP del usuario |
| user_agent | TEXT | | Cadena de agente de usuario |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de la acción |

## Índices
Para rendimiento con alto volumen (7000-8000 encuestas/semana):

1. **Tabla de Encuestas:**
   - Índice en `status` para filtrar encuestas pendientes/procesando
   - Índice en `processed_at` para consultas basadas en tiempo
   - Índice en `batch_id` para consultas relacionadas con lotes
   - Índice compuesto en `(status, processed_at)` para procesamiento de cola

2. **Tabla de Respuestas de Encuesta:**
   - Índice en `survey_id` para obtener todas las respuestas de una encuesta
   - Índice en `question_id` para análisis entre preguntas
   - Índice compuesto en `(survey_id, question_id)` para búsquedas

3. **Tabla de Lotes:**
   - Índice en `started_at` para consultas de lotes basadas en tiempo
   - Índice en `completed_at` para análisis de lotes completados

## Relaciones
- Una Encuesta tiene Muchas Respuestas de Encuesta (uno a muchos)
- Una Pregunta de Encuesta puede ser respondida en Muchas Respuestas de Encuesta (uno a muchos)
- Un Lote contiene Muchas Encuestas (uno a muchos)
- Un Usuario puede realizar Muchas Entradas de Registro de Auditoría (uno a muchos)
- Un Usuario puede subir/procesar Muchas Encuestas (uno a muchos)

## Restricciones y Validación
1. **Restricciones de Estado de Encuesta:**
   - Valores válidos: 'pendiente', 'procesando', 'validado', 'error', 'archivado'
   - Transiciones automáticas basadas en el flujo de procesamiento

2. **Integridad de Datos:**
   - Las restricciones de clave externa imponen relaciones
   - Restricciones NOT NULL en campos esenciales
   - Restricciones CHECK para valores enum válidos donde aplique

3. **Consideraciones de Volumen:**
   - Estrategia de particionamiento horizontal para la tabla de Encuestas por mes (para 7000-8000/semana ≈ 30k-35k/mes)
   - Estrategia de archivo para encuestas antiguas completadas
   - Procesamiento por lotes para gestionar picos de carga

## Consultas de Ejemplo
### Obtener encuestas pendientes para procesar:
```sql
SELECT * FROM encuestas 
WHERE estado = 'pendiente' 
ORDER BY created_at ASC 
LIMIT 100;
```

### Obtener encuesta con todas sus respuestas:
```sql
SELECT e.*, er.*, p.pregunta_texto, p.tipo_pregunta
FROM encuestas e
LEFT JOIN respuestas_encuesta er ON e.id = er.encuesta_id
LEFT JOIN preguntas_encuesta p ON er.pregunta_id = p.id
WHERE e.id = 'uuid-de-encuesta-aquí';
```

### Obtener estadísticas de procesamiento de lote:
```sql
SELECT 
    l.*,
    COUNT(e.id) as total_encuestas,
    COUNT(CASE WHEN e.estado = 'validado' THEN 1 END) as encuestas_validadas,
    COUNT(CASE WHEN e.estado = 'error' THEN 1 END) as encuestas_fallidas
FROM lotes l
LEFT JOIN encuestas e ON l.id = e.lote_id
WHERE l.id = 'uuid-de-lote-aquí'
GROUP BY l.id;
```

## Consideraciones de Migración
Para manejar el volumen esperado:
1. **Particionamiento horizontal** de la tabla de encuestas por rangos de fechas
2. **Réplicas de lectura** para consultas de informes
3. **Agrupamiento de conexiones** para conexiones a base de datos
4. **Capa de caché** para datos de referencia frecuentemente accesados (preguntas, etc.)
5. **Estrategia de respaldo** con recuperación punto en el tiempo

## Tecnologías Consideradas
- **Base de Datos Principal**: PostgreSQL (por confiabilidad, soporte JSONB y escalabilidad)
- **Alternativa**: MySQL/MariaDB si no hay experiencia en PostgreSQL
- **ORM/Constructor de Consultas**: Prisma, TypeORM, o SQL sin procesar con constructor de consultas
- **Agrupamiento de Conexiones**: PgBouncer o pool incorporado