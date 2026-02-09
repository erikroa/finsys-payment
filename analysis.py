"""
Payment Processing Operations Analysis
Author: Erik Roa
Purpose: Identify operational bottlenecks in payment processing for fintech
"""

import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("PAYMENT PROCESSING OPERATIONS ANALYSIS")
print("=" * 60)

# ============================================
# 1. LOAD 
# ============================================
print("\n[1/5] Downloading dataset...")
path = kagglehub.dataset_download("ealaxi/banksim1")
print(f"✓ Dataset downloaded to: {path}")

# CSV 
import os
csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
df = pd.read_csv(os.path.join(path, csv_file))

print(f"✓ Loaded {len(df):,} transactions")

# ============================================
# 2. DATA OVERVIEW
# ============================================
print("\n[2/5] Analyzing transaction patterns...")

print(f"\nDataset Shape: {df.shape}")
print(f"\nTransaction Types:")
print(df['category'].value_counts())

# ============================================
# 3. KEY METRICS
# ============================================
print("\n[3/5] Calculating operational metrics...")

# Metric 1: Volume by payment type
volume_by_type = df['category'].value_counts()
print("\n--- Transaction Volume by Type ---")
print(volume_by_type)

# Metric 2: Average transaction value
avg_by_type = df.groupby('category')['amount'].agg(['mean', 'count', 'sum'])
avg_by_type.columns = ['Avg Amount', 'Count', 'Total Volume']
avg_by_type['Avg Amount'] = avg_by_type['Avg Amount'].round(2)
print("\n--- Financial Metrics by Type ---")
print(avg_by_type.sort_values('Total Volume', ascending=False))

# Metric 3: Fraud analysis
fraud_rate = df.groupby('category')['fraud'].agg(['sum', 'count', 'mean'])
fraud_rate.columns = ['Fraud Count', 'Total Trans', 'Fraud Rate']
fraud_rate['Fraud Rate'] = (fraud_rate['Fraud Rate'] * 100).round(3)
print("\n--- Operational Risk (Fraud Rate %) ---")
print(fraud_rate.sort_values('Fraud Rate', ascending=False))

# ============================================
# 4. BUSINESS IMPACT
# ============================================
print("\n[4/5] Calculating business impact...")

total_volume = df['amount'].sum()
fraud_volume = df[df['fraud'] == 1]['amount'].sum()
fraud_count = df['fraud'].sum()

print(f"\n{'='*60}")
print("REVENUE IMPACT ANALYSIS")
print(f"{'='*60}")
print(f"Total Transaction Volume: ${total_volume:,.2f}")
print(f"Total Transactions: {len(df):,}")
print(f"Fraud Incidents: {fraud_count:,} ({fraud_count/len(df)*100:.2f}%)")
print(f"Fraud Volume: ${fraud_volume:,.2f}")
print(f"Revenue at Risk: ${fraud_volume:,.2f} ({fraud_volume/total_volume*100:.2f}%)")
print(f"\n💡 Potential Annual Savings (30% reduction): ${fraud_volume * 0.30:,.2f}")

# ============================================
# 5. VISUALIZATIONS
# ============================================
print("\n[5/5] Generating visualizations...")

# Create images directory
os.makedirs('images', exist_ok=True)

# Chart 1: Transaction Volume
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

volume_by_type.plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Transaction Volume by Payment Type', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Payment Type')
axes[0, 0].set_ylabel('Number of Transactions')
axes[0, 0].tick_params(axis='x', rotation=45)

# Chart 2: Fraud Rate
fraud_rate['Fraud Rate'].plot(kind='bar', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Fraud Rate by Payment Type (%)', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Payment Type')
axes[0, 1].set_ylabel('Fraud Rate (%)')
axes[0, 1].tick_params(axis='x', rotation=45)

# Chart 3: Transaction Amount Distribution
df['amount'].hist(bins=50, ax=axes[1, 0], color='green', alpha=0.7)
axes[1, 0].set_title('Transaction Amount Distribution', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Amount ($)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_yscale('log')

# Chart 4: Volume vs Risk
scatter_data = avg_by_type.copy()
scatter_data['Fraud Rate'] = fraud_rate['Fraud Rate']
axes[1, 1].scatter(scatter_data['Count'], scatter_data['Fraud Rate'], 
                   s=scatter_data['Total Volume']/1000, alpha=0.6, color='purple')
axes[1, 1].set_title('Transaction Volume vs Fraud Risk', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Transaction Count')
axes[1, 1].set_ylabel('Fraud Rate (%)')

for idx, cat in enumerate(scatter_data.index):
    axes[1, 1].annotate(cat, (scatter_data['Count'].iloc[idx], scatter_data['Fraud Rate'].iloc[idx]))

plt.tight_layout()
plt.savefig('images/operations_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: images/operations_dashboard.png")

# Chart 5: Summary chart
fig, ax = plt.subplots(figsize=(10, 6))
summary_data = avg_by_type[['Total Volume']].sort_values('Total Volume', ascending=True)
summary_data.plot(kind='barh', ax=ax, color='teal', legend=False)
ax.set_title('Total Transaction Volume by Payment Type', fontsize=16, fontweight='bold')
ax.set_xlabel('Total Volume ($)')
ax.set_ylabel('Payment Type')
plt.tight_layout()
plt.savefig('images/volume_summary.png', dpi=300, bbox_inches='tight')
print("✓ Saved: images/volume_summary.png")

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE!")
print("="*60)
print("\nNext steps:")
print("1. Check the 'images/' folder for charts")
print("2. Update README.md with these findings")
print("3. Push to GitHub: git add . && git commit -m 'Complete analysis' && git push")
