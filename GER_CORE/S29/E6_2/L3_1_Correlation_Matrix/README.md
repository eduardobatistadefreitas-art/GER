# L3.1 — Correlation Matrix

## Objective

Compute the complete pairwise correlation structure among all observables.

This experiment is purely observational.

No hypothesis testing, causal interpretation, or structural clustering is performed.

---

## Methods

- Pearson
- Spearman
- Kendall

---

## Inputs

A numerical observables dataset.

---

## Outputs

### tables/

- pearson_matrix.csv
- spearman_matrix.csv
- kendall_matrix.csv

- pearson_table.csv
- spearman_table.csv
- kendall_table.csv

---

### json/

summary.json

---

### report/

L3_1_report.txt

---

### certificate/

certificate.json

---

## Pipeline

Dataset

↓

Correlation computation

↓

Correlation tables

↓

Summary

↓

Report

↓

Certificate

---

## Dependencies

statistics/correlation.py

---

## Version

1.0
