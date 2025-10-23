import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs('visuals', exist_ok=True)
df = pd.read_csv('data/raw_311_requests.csv', parse_dates=['CREATED_DATE','CLOSED_DATE'])
df['ResponseDays'] = (df['CLOSED_DATE'] - df['CREATED_DATE']).dt.days
avg_resp = df['ResponseDays'].mean()
within_sla = (df['ResponseDays'] <= 3).mean() * 100
with open('visuals/kpi_summary.txt','w') as f:
    f.write(f'Average Response Days: {avg_resp:.2f}\n')
    f.write(f'Within SLA (<=3 days): {within_sla:.1f}%\n')
by_dist = df['DISTRICT'].value_counts().sort_values(ascending=False)
plt.figure(); by_dist.plot(kind='bar'); plt.title('Requests by District'); plt.ylabel('Count'); plt.tight_layout(); plt.savefig('visuals/requests_by_district.png'); plt.close()
df['Month'] = df['CREATED_DATE'].dt.to_period('M').astype(str)
cat_month = df.groupby(['Month','SERVICE_NAME']).size().unstack(fill_value=0)
plt.figure(); cat_month.rolling(2).mean().plot(); plt.title('Category Trend Over Time (Smoothed)'); plt.xlabel('Month'); plt.ylabel('Requests'); plt.tight_layout(); plt.savefig('visuals/category_trend.png'); plt.close()
plt.figure(); df['ResponseDays'].plot(kind='hist', bins=30); plt.title('Response Time Distribution (Days)'); plt.xlabel('Days'); plt.tight_layout(); plt.savefig('visuals/response_time_hist.png'); plt.close()
print('Done')