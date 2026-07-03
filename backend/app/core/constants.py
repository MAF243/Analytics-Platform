"""
Compile-time constants for the Enterprise Analytics Platform.
"""

# File constraints
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
MIN_NUMERIC_COLUMNS = 2
SUPPORTED_EXTENSIONS = {".csv"}
SUPPORTED_MIME_TYPES = {"text/csv", "application/vnd.ms-excel"}
DEFAULT_ENCODING = "utf-8"

# Storage paths
TEMP_STORAGE_PATH = "data"
RAW_DIR_NAME = "raw"
METADATA_DIR_NAME = "metadata"
RESULTS_DIR_NAME = "results"
RAW_FILE_NAME = "raw.csv"
METADATA_FILE_NAME = "metadata.json"

# Limits
MAX_K_CLUSTERS = 15
MIN_K_CLUSTERS = 2
DATASET_EXPIRATION_HOURS = 1
