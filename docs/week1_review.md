# Week 1 Review — Spotify Million Playlist Data Engineering Pipeline

## Week 1 Goal

The goal of Week 1 was to set up the project foundation, understand the raw Spotify Million Playlist Dataset, and prepare the project for Bronze layer implementation.

---

## Completed Work

### 1. Project Goal Defined

The project goal is to build an end-to-end data engineering pipeline using:

- Python
- PySpark
- SQL
- Parquet
- AWS S3
- AWS Athena

The pipeline converts raw nested Spotify playlist JSON files into Bronze, Silver, and Gold analytical layers.

---

### 2. Project Folder Structure Created

The project uses a clean data engineering folder structure:

```text
spotify-million-playlist-pipeline/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── quality/
│   └── utils/
│
├── sql/
│   ├── athena_ddl/
│   └── analytics_queries/
│
├── notebooks/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

This structure separates data, processing code, validation code, SQL queries, notebooks, and documentation.

---

### 3. Local Environment Configured

A Python virtual environment was created and dependencies were installed from:

```text
requirements.txt
```

Important packages:

```text
pyspark
pandas
boto3
pyarrow
python-dotenv
```

Spark was tested using:

```text
src/utils/spark_test.py
```

Run command:

```bash
python src/utils/spark_test.py
```

---

### 4. Java and PySpark Issues Resolved

During setup, Java and Python environment issues were addressed.

Key environment decisions:

1. Use Java 17 for PySpark compatibility.
2. Use the same Python version for the PySpark driver and worker.
3. Run Spark inside the correct project directory.

---

### 5. Raw Spotify JSON Read Successfully

A Spotify Million Playlist slice file was placed under:

```text
data/raw/
```

Example:

```text
data/raw/mpd.slice.0-999.json
```

Raw reader script:

```text
src/ingestion/read_raw_json.py
```

Run command:

```bash
python src/ingestion/read_raw_json.py
```

This script reads the raw JSON file, prints the raw schema, previews playlist records, and inspects nested track records.

---

### 6. Raw Schema Analyzed

Raw schema documentation was created:

```text
docs/raw_schema_notes.md
```

Schema inspection script:

```text
src/quality/inspect_raw_schema.py
```

Run command:

```bash
python src/quality/inspect_raw_schema.py
```

Important raw schema findings:

1. Raw files contain a top-level `playlists` array.
2. Each playlist contains playlist-level metadata.
3. Each playlist contains a nested `tracks` array.
4. Track data must be flattened later for SQL analytics.

---

### 7. Bronze Layer Designed

Bronze layer design documentation was created:

```text
docs/bronze_layer_design.md
```

Bronze design decision:

```text
Raw JSON will be converted to Parquet while keeping one row per playlist.
```

The nested `tracks` array remains in Bronze and will be flattened in Silver.

---

## Week 1 Architecture Progress

Completed architecture stage:

```text
Raw JSON
   ↓
Raw schema inspection
   ↓
Bronze layer design
```

Prepared next architecture stage:

```text
Raw JSON → Bronze Parquet
```

---

## Key Week 1 Learning Outcomes

By the end of Week 1, the project established:

1. A professional folder structure.
2. A working PySpark environment.
3. Raw JSON ingestion capability.
4. Raw schema understanding.
5. Bronze layer design.
6. Clear data modeling direction.

---

## Week 1 Conclusion

Week 1 completed the project foundation. The local environment works, the raw Spotify JSON structure is understood, and the Bronze layer is designed.

The next step is to implement the Bronze ingestion job.
