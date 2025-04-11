import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv("/Users/rushabarram/Documents/archive (2)/P_L_March_2021.csv")

st.title("📊 Financial Dashboard - March 2021")

# Display raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Try to infer key columns
columns = df.columns.str.lower()

date_col = next((col for col in df.columns if 'date' in col.lower()), df.columns[0])
amount_col = next((col for col in df.columns if 'amount' in col.lower()), df.columns[-1])
category_col = next((col for col in df.columns if 'category' in col.lower() or 'desc' in col.lower()), None)

# Preprocess data
df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# Summary metrics
total_income = df[df[amount_col] > 0][amount_col].sum()
total_expense = df[df[amount_col] < 0][amount_col].sum()
net = total_income + total_expense

st.metric("💰 Total Income", f"${total_income:,.2f}")
st.metric("💸 Total Expenses", f"${total_expense:,.2f}")
st.metric("📈 Net Profit", f"${net:,.2f}")

# Charts
if category_col:
    st.subheader("📂 Breakdown by Category")
    summary = df.groupby(category_col)[amount_col].sum().reset_index()
    fig = px.pie(summary, names=category_col, values=amount_col, title="Expenses & Income by Category")
    st.plotly_chart(fig)

# Filter data
if category_col:
    selected = st.multiselect("Filter by Category", options=df[category_col].unique())
    if selected:
        filtered_df = df[df[category_col].isin(selected)]
    else:
        filtered_df = df
else:
    filtered_df = df

# Show filtered table
st.subheader("📋 Filtered Transactions")
st.write(filtered_df)

# Export option
st.download_button(
    label="Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_report.csv",
    mime="text/csv"
)
