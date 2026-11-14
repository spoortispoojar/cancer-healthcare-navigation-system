
# Exploratory Data Analysis Report

## 1. Dataset Overview
- Total records: 7000
- Total columns: 18
- Cancer types: Breast Cancer and Lung Cancer
- Duplicate records: 0
- Missing values: 1056 cells across two symptom columns

## 2. Target Distribution
- Low: 1890 (27.00%)
- Moderate: 2727 (38.96%)
- High: 2383 (34.04%)

## 3. Cancer Type Analysis
Lung cancer records have a higher proportion of High labels
than breast cancer records.

## 4. Age Analysis
The proportion of High labels increases across older age
groups, particularly for patients aged 70 and above.

## 5. Cancer Stage Analysis
Stage IV has a high proportion of High labels, while
Stage I has a high proportion of Low labels.

## 6. Treatment Analysis
Treatment categories show different support-label
distributions. Palliative/supportive care and combined
treatment categories have relatively high proportions
of High labels.

## 7. Symptom Analysis
Fatigue, shortness of breath, nausea and bone pain are
among the frequently reported symptoms.

Higher symptom severity is associated with a greater
proportion of High synthetic labels.

## 8. Caregiver Support
Patients reporting caregiver support have a higher
proportion of High labels.

## 9. Transport Availability
Patients without transport have a higher proportion
of High labels.

## 10. Insurance
Insurance analysis is excluded from the current
semester implementation and reserved for future work.

## 11. EDA Conclusion
The dataset contains useful patterns across cancer type,
age, stage, treatment, symptoms and patient support factors.

The target labels are generated using a predefined
synthetic scoring rule. Consequently, observed
relationships and future model performance reflect
that synthetic rule rather than real-world clinical validity.

## 12. Limitations
- All patient records are synthetic.
- Target labels are rule-generated.
- No clinical validation has been performed.
- EDA associations do not establish causation.
