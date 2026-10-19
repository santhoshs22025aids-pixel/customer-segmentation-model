# Task 4 — Segmentation and Recommendation Model

## Objective
Group synthetic customers into understandable segments and apply a transparent rule-based churn-risk score to help prioritise retention outreach.

## Files
- `segmentation_analysis.py` — reproducible analysis and validation checks.
- `customer_churn_cleaned.csv` — supplied synthetic dataset used by this project.
- `segmented_customer_table.csv` — each customer with segment, score, risk level, and reason.
- `segment_summary.csv` — counts, observed churn rate, average tenure/support tickets/charges, and high-risk counts by segment.
- `key_metrics.txt` — overall summary metrics.
- `risk_level_counts.png`, `churn_by_segment.png` — charts.
- `recommendation_memo.md` — short decision memo and limitations.

## Run it
Install Python 3 and the required packages:
```bash
pip install pandas matplotlib
python segmentation_analysis.py
```

## Rule-based score
- Tenure 0–6 months: +2; 7–12 months: +1.
- Support tickets 4 or more: +2; 2–3 tickets: +1.
- Month-to-month contract: +1.
- Score 4+: High risk; 2–3: Medium risk; 0–1: Low risk.

The score is intentionally explainable. It is a prioritisation heuristic, not a trained or validated predictive model. `Churn` is not used to calculate the score; it is only used to summarise observed outcomes after scoring.

## Customer segments
1. New + high support needs: tenure <=12 months and >=3 support tickets.
2. Flexible contract: remaining customers on month-to-month contracts.
3. Established long-term: tenure >=25 months and two-year contract.
4. Other / developing: all remaining customers.

## Important caveat
The supplied data is a tiny synthetic sample (15 rows). Any rates are descriptive only and can change sharply with one customer. Do not generalise these findings to real customers without a larger representative dataset and validation.
