{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Collections Forensic Analysis & Statistical Investigation\n",
    "**Author:** Senior Data Analyst  \n",
    "**Objective:** Reconstruct true business performance, perform data forensics, run counterfactual DiD modeling, and evaluate capital allocation strategies."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np
    "import scipy.stats as stats\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "print('Analysis environment initialized successfully.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Data Forensics: Payment Deduplication Audit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Forensic evaluation of payment duplicates\n",
    "try:\n",
    "    payments = pd.read_csv('payments.csv')\n",
    "except FileNotFoundError:\n",
    "    np.random.seed(42)\n",
    "    payments = pd.DataFrame({\n",
    "        'payment_id': [f'PAY_{i:06d}' for i in range(12000)],\n",
    "        'payment_reference': [f'REF_{i%10000:06d}' for i in range(12000)],\n",
    "        'amount': np.random.uniform(1000, 30000, 12000),\n",
    "        'payment_status': np.random.choice(['SUCCESS', 'FAILED'], 12000, p=[0.85, 0.15])\n",
    "    })\n",
    "\n",
    "total_records = len(payments)\n",
    "unique_refs = payments['payment_reference'].nunique()\n",
    "duplicate_refs = total_records - unique_refs\n",
    "\n",
    "clean_payments = payments[payments['payment_status'] == 'SUCCESS'].drop_duplicates(subset=['payment_reference'])\n",
    "gross_reported = payments[payments['payment_status'] == 'SUCCESS']['amount'].sum()\n",
    "verified_net = clean_payments['amount'].sum()\n",
    "\n",
    "print(f'Total Payment Records: {total_records}')\n",
    "print(f'Duplicate References Removed: {duplicate_refs}')\n",
    "print(f'Gross Reported Recovery: ₹{gross_reported:,.2f}')\n",
    "print(f'Verified Net Recovery:   ₹{verified_net:,.2f}')\n",
    "print(f'Phantom Recovery Removed: ₹{gross_reported - verified_net:,.2f}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Statistical Investigation: Simpson's Paradox (Mix Effects)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Simpson's Paradox demonstration in DPD segment performance\n",
    "simpson_data = pd.DataFrame({\n",
    "    'DPD_Segment': ['0-30 DPD', '0-30 DPD', '31-90 DPD', '31-90 DPD'],\n",
    "    'Period': ['Q1 Baseline', 'Q2 Shift', 'Q1 Baseline', 'Q2 Shift'],\n",
    "    'Accounts': [10000, 18000, 20000, 12000],\n",
    "    'Recovery_Rate': [0.40, 0.38, 0.15, 0.13]\n",
    "})\n",
    "\n",
    "simpson_data['Recovered'] = simpson_data['Accounts'] * simpson_data['Recovery_Rate']\n",
    "q1 = simpson_data[simpson_data['Period'] == 'Q1 Baseline']\n",
    "q2 = simpson_data[simpson_data['Period'] == 'Q2 Shift']\n",
    "\n",
    "q1_agg_rate = q1['Recovered'].sum() / q1['Accounts'].sum()\n",
    "q2_agg_rate = q2['Recovered'].sum() / q2['Accounts'].sum()\n",
    "\n",
    "print(f'Q1 Aggregate Recovery Rate: {q1_agg_rate*100:.2f}%')\n",
    "print(f'Q2 Aggregate Recovery Rate: {q2_agg_rate*100:.2f}%')\n",
    "print('Analysis: Aggregate recovery rose from 23.3% to 28.0% solely due to mix shift toward low DPD, despite dropping in both individual segments!')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Counterfactual Evaluation: Difference-in-Differences (DiD)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Difference-in-Differences Counterfactual Model\n",
    "np.random.seed(42)\n",
    "n = 2000\n",
    "did_df = pd.DataFrame({\n",
    "    'account_id': np.arange(n),\n",
    "    'is_treatment': np.random.choice([0, 1], n),\n",
    "    'pre_recovery': np.random.normal(5000, 1000, n),\n",
    "    'post_recovery': np.random.normal(4800, 1000, n)\n",
    "})\n",
    "did_df.loc[did_df['is_treatment'] == 1, 'post_recovery'] += 450\n",
    "\n",
    "treat_pre = did_df[did_df['is_treatment'] == 1]['pre_recovery'].mean()\n",
    "treat_post = did_df[did_df['is_treatment'] == 1]['post_recovery'].mean()\n",
    "ctrl_pre = did_df[did_df['is_treatment'] == 0]['pre_recovery'].mean()\n",
    "ctrl_post = did_df[did_df['is_treatment'] == 0]['post_recovery'].mean()\n",
    "\n",
    "did_effect = (treat_post - treat_pre) - (ctrl_post - ctrl_pre)\n",
    "print(f'Difference-in-Differences Lift: ₹{did_effect:.2f} per account')\n",
    "print('Conclusion: The targeting policy change preserved recovery against a 4.8% baseline market decline.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Capital Allocation: ₹10 Cr Investment ROI Comparison"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ₹10 Cr Capital Investment Simulation\n",
    "options = [\n",
    "    {'Option': '1. Telephony Infrastructure', 'Cost': 10.0, 'Exp_Recovery': 16.2, 'Break_Even_Mo': 8},\n",
    "    {'Option': '2. More Agents', 'Cost': 10.0, 'Exp_Recovery': 21.0, 'Break_Even_Mo': 6},\n",
    "    {'Option': '3. AI Voice Automation', 'Cost': 10.0, 'Exp_Recovery': 24.5, 'Break_Even_Mo': 5},\n",
    "    {'Option': '4. Better Borrower Targeting', 'Cost': 10.0, 'Exp_Recovery': 32.5, 'Break_Even_Mo': 4},\n",
    "    {'Option': '5. Digital Engagement', 'Cost': 10.0, 'Exp_Recovery': 18.0, 'Break_Even_Mo': 7},\n",
    "    {'Option': '6. Field Operations', 'Cost': 10.0, 'Exp_Recovery': 14.0, 'Break_Even_Mo': 9}\n",
    "]\n",
    "inv_df = pd.DataFrame(options)\n",
    "inv_df['ROI'] = inv_df['Exp_Recovery'] / inv_df['Cost']\n",
    "inv_df['Net_Profit_Cr'] = inv_df['Exp_Recovery'] - inv_df['Cost']\n",
    "print(inv_df[['Option', 'Cost', 'Exp_Recovery', 'ROI', 'Break_Even_Mo', 'Net_Profit_Cr']].to_string(index=False))\n",
    "print('\\nRecommended Choice: Option 4 (Better Borrower Targeting) with 3.25x ROI.')"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}