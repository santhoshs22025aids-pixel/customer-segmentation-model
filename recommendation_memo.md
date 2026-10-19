# Recommendation Memo — Customer Segmentation and Churn Prioritisation

## Operational question
Which fictional customer groups should the subscription team contact first to reduce avoidable churn?

## Approach
Customers are segmented using tenure, support-ticket count, and contract type. A transparent rule-based score adds points for short tenure, repeated support tickets, and month-to-month contracts. The score provides a prioritisation queue, not a probability of churn.

## Recommended action
Start with **High-risk customers**, especially those with short tenure and multiple recent support tickets. Have the support team review unresolved issues and offer an appropriate follow-up before making a retention offer. Next, contact **Medium-risk customers** with a short satisfaction check. Do not treat the score as proof that a customer will leave.

## Supporting measures
Use `key_metrics.txt` for overall counts and `segment_summary.csv` for segment-level observed churn rates and characteristics. `segmented_customer_table.csv` explains each customer's score through `RiskReasons`.

## Uncertainty and limitations
The dataset contains only 15 synthetic customers, so segment rates are unstable and not representative. The rule weights are chosen for transparency, not learned from data. The fields do not capture customer satisfaction, unresolved issue status, competitor offers, or the reason for leaving. Association does not establish causation.

## Next measurement
For a real pilot, record outreach date, contact success, issue resolution, offer accepted, and churn status after 30/60 days. Compare retention and contact cost across risk groups, and revise the rules only after collecting a larger representative sample.
