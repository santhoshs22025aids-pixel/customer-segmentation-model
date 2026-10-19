"""Task 4: Customer Segmentation and Rule-Based Churn Risk
Run: python segmentation_analysis.py
Requirements: pandas, matplotlib
All records are synthetic. This is a transparent prioritisation rule, not a predictive model.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'customer_churn_cleaned.csv'
OUTPUT = BASE

df = pd.read_csv(INPUT)

# Basic validation
required = {'CustomerID','TenureMonths','MonthlyCharges','SubscriptionType','ContractType','SupportTickets','PaymentMethod','Churn'}
missing_columns = required - set(df.columns)
if missing_columns:
    raise ValueError(f'Missing required columns: {sorted(missing_columns)}')
if df['CustomerID'].duplicated().any():
    raise ValueError('CustomerID must be unique; inspect duplicates before analysis.')
if not set(df['Churn'].dropna().unique()).issubset({'Yes','No'}):
    raise ValueError('Churn must contain Yes/No values.')

# Segments are intentionally interpretable and based on supplied account/behavior fields.
def segment_customer(row):
    if row['TenureMonths'] <= 12 and row['SupportTickets'] >= 3:
        return 'New + high support needs'
    if row['ContractType'] == 'Month-to-Month':
        return 'Flexible contract'
    if row['TenureMonths'] >= 25 and row['ContractType'] == 'Two Year':
        return 'Established long-term'
    return 'Other / developing'

def score_customer(row):
    score = 0
    reasons = []
    if row['TenureMonths'] <= 6:
        score += 2; reasons.append('very short tenure (<=6 months)')
    elif row['TenureMonths'] <= 12:
        score += 1; reasons.append('short tenure (7-12 months)')
    if row['SupportTickets'] >= 4:
        score += 2; reasons.append('4+ recent support tickets')
    elif row['SupportTickets'] >= 2:
        score += 1; reasons.append('2-3 recent support tickets')
    if row['ContractType'] == 'Month-to-Month':
        score += 1; reasons.append('month-to-month contract')
    if score >= 4:
        level = 'High'
    elif score >= 2:
        level = 'Medium'
    else:
        level = 'Low'
    return pd.Series([score, level, '; '.join(reasons) if reasons else 'No rule-based risk flags'])

df['CustomerSegment'] = df.apply(segment_customer, axis=1)
df[['RiskScore','RiskLevel','RiskReasons']] = df.apply(score_customer, axis=1)
# Add observed outcome for evaluation only; do not use it to calculate the score.
df.to_csv(OUTPUT / 'segmented_customer_table.csv', index=False)

segment_summary = (df.groupby('CustomerSegment', dropna=False)
    .agg(Customers=('CustomerID','count'),
         Churned=('Churn', lambda s: (s == 'Yes').sum()),
         AverageTenureMonths=('TenureMonths','mean'),
         AverageSupportTickets=('SupportTickets','mean'),
         AverageMonthlyCharges=('MonthlyCharges','mean'),
         HighRiskCustomers=('RiskLevel', lambda s: (s == 'High').sum()))
    .reset_index())
segment_summary['ObservedChurnRatePct'] = (segment_summary['Churned'] / segment_summary['Customers'] * 100).round(1)
for c in ['AverageTenureMonths','AverageSupportTickets','AverageMonthlyCharges']:
    segment_summary[c] = segment_summary[c].round(2)
segment_summary.to_csv(OUTPUT / 'segment_summary.csv', index=False)

# Useful verified summary metrics
n = len(df)
churned = int((df['Churn'] == 'Yes').sum())
metrics = {
    'Total customers': n,
    'Observed churned customers': churned,
    'Observed churn rate (%)': round(churned / n * 100, 1) if n else 0,
    'High rule-based risk customers': int((df['RiskLevel'] == 'High').sum()),
    'Customers with 4+ support tickets': int((df['SupportTickets'] >= 4).sum()),
    'Month-to-month customers': int((df['ContractType'] == 'Month-to-Month').sum()),
}
with open(OUTPUT / 'key_metrics.txt','w', encoding='utf-8') as f:
    f.write('TASK 4 — KEY METRICS (synthetic sample)\n')
    for k,v in metrics.items(): f.write(f'{k}: {v}\n')

# Charts
plt.figure(figsize=(8,5))
order = ['Low','Medium','High']
counts = df['RiskLevel'].value_counts().reindex(order, fill_value=0)
counts.plot(kind='bar')
plt.title('Customers by Rule-Based Churn Risk')
plt.xlabel('Risk level'); plt.ylabel('Number of customers'); plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(OUTPUT/'risk_level_counts.png', dpi=160); plt.close()

plot = segment_summary.sort_values('ObservedChurnRatePct', ascending=False)
plt.figure(figsize=(9,5))
plt.bar(plot['CustomerSegment'], plot['ObservedChurnRatePct'])
plt.title('Observed Churn Rate by Customer Segment')
plt.xlabel('Customer segment'); plt.ylabel('Observed churn rate (%)')
plt.xticks(rotation=20, ha='right'); plt.tight_layout()
plt.savefig(OUTPUT/'churn_by_segment.png', dpi=160); plt.close()

print('Analysis complete. Created segmented_customer_table.csv, segment_summary.csv, key_metrics.txt and charts.')
print('\nKey metrics:')
for k,v in metrics.items(): print(f'- {k}: {v}')
print('\nSegment summary:')
print(segment_summary.to_string(index=False))
