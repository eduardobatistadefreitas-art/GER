"""
============================================================
GER

L3.1 Correlation Matrix

Configuration

============================================================
"""

from pathlib import Path

# ============================================================
# Version
# ============================================================

VERSION = "1.0"

# ============================================================
# Correlation Methods
# ============================================================

CORRELATION_METHODS = [

    "pearson",

    "spearman",

    "kendall",

]

# ============================================================
# Thresholds
# ============================================================

STRONG_THRESHOLD = 0.70

VERY_STRONG_THRESHOLD = 0.90

CERTIFICATE_TOLERANCE = 1e-10

# ============================================================
# Folder Names
# ============================================================

TABLE_FOLDER = "tables"

JSON_FOLDER = "json"

REPORT_FOLDER = "report"

CERTIFICATE_FOLDER = "certificate"

# ============================================================
# File Names
# ============================================================

SUMMARY_JSON = "summary.json"

REPORT_FILE = "L3_1_report.txt"

CERTIFICATE_FILE = "certificate.json"

# ============================================================
# Matrix Files
# ============================================================

PEARSON_MATRIX = "pearson_matrix.csv"

SPEARMAN_MATRIX = "spearman_matrix.csv"

KENDALL_MATRIX = "kendall_matrix.csv"

# ============================================================
# Table Files
# ============================================================

PEARSON_TABLE = "pearson_table.csv"

SPEARMAN_TABLE = "spearman_table.csv"

KENDALL_TABLE = "kendall_table.csv"
