import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
from datetime import datetime
import json

# --- Helper Functions and Data Simulation ---

def get_dummy_transaction_data():
    """Generates dummy transaction data as a CSV string."""
    csv_data = """Date,Description,Amount,Type
2023-01-05,Paycheck,5000.00,Income
2023-01-10,Groceries,250.00,Expense
2023-01-15,Internet Bill,75.00,Expense
2023-01-20,Dinner with friends,60.00,Expense
2023-02-05,Paycheck,5200.00,Income
2023-02-10,Rent,1500.00,Expense
2023-02-18,Gasoline,40.00,Expense
2023-03-05,Paycheck,5100.00,Income
2023-03-12,Phone Bill,50.00,Expense
2023-03-25,Shopping,120.00,Expense
2023-04-05,Paycheck,5300.00,Income
2023-04-10,Groceries,280.00,Expense
2023-04-15,Subscription,10.00,Expense
"""
    return pd.read_csv(StringIO(csv_data))

def get_dummy_net_worth_data():
    """Generates dummy net worth data as a CSV string."""
    csv_data = """Date,Net Worth
2023-01-01,15000
2023-02-01,15500
2023-03-01,16000
2023-04-01,16200
2023-05-01,16500
2023-06-01,17000
"""
    return pd.read_csv(StringIO(csv_data))

def get_dummy_portfolio_data():
    """Generates a dummy investment portfolio."""
    return pd.DataFrame({
        'Investment': ['AAPL', 'MSFT', 'GOOGL'],
        'Shares': [10.0, 5.0, 8.0]
    })

def mock_get_stock_price(ticker):
    """
    Mocks fetching a stock price for demonstration.
    In a real app, you would use a financial API (e.g., Alpha Vantage, Finnhub).
    """
    # Dummy prices for demonstration
    prices = {
        'AAPL': 175.50,
        'MSFT': 325.75,
        'GOOGL': 130.20
    }
    return prices.get(ticker, 0.0)

# --- Core Logic Functions ---

def load_and_preprocess_transactions(df):
    """
    Loads, cleans, and categorizes transaction data.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    # Handle different CSV formats:
    # If the CSV does not have a 'Type' column, infer it from the 'Amount'
    if 'Type' not in df.columns:
        df['Type'] = 'Expense'
        df.loc[df['Amount'] >= 0, 'Type'] = 'Income'
    
    # The uploaded file might have 'Amount' as a negative value for expenses.
    # We convert it to a positive value for consistent calculations.
    df['Amount'] = df['Amount'].abs()
    
    # If a 'Category' column does not exist, create a basic one based on descriptions.
    if 'Category' not in df.columns:
        df['Category'] = 'Other'
        df.loc[df['Type'] == 'Income', 'Category'] = 'Income'
        df.loc[df['Description'].str.contains('Groceries|Shopping|Dinner', case=False), 'Category'] = 'Food & Shopping'
        df.loc[df['Description'].str.contains('Rent|Bill|Subscription', case=False), 'Category'] = 'Bills & Utilities'

    return df

def calculate_monthly_cash_flow(df):
    """
    Calculates monthly income and expenses from transactions.
    """
    df['Signed_Amount'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1)
    monthly_summary = df.groupby('Month')['Signed_Amount'].sum().reset_index()
    monthly_summary['Month'] = monthly_summary['Month'].astype(str)
    
    income_by_month = df[df['Type'] == 'Income'].groupby('Month')['Amount'].sum().reset_index()
    expense_by_month = df[df['Type'] == 'Expense'].groupby('Month')['Amount'].sum().reset_index()
    
    return monthly_summary, income_by_month, expense_by_month

def update_portfolio_value(portfolio_df):
    """
    Calculates the current value of the investment portfolio.
    """
    portfolio_df['Current Price'] = portfolio_df['Investment'].apply(mock_get_stock_price)
    portfolio_df['Current Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']
    return portfolio_df

# --- Streamlit Application ---

def main():
    st.set_page_config(layout="wide", page_title="Personal Finance Dashboard")

    st.title("💰 Personal Finance Dashboard")
    st.markdown("### A simple command-line finance tracker with a Streamlit interface.")

    # File Upload Section
    st.sidebar.header("Data Upload")
    trans_file = st.sidebar.file_uploader("Upload Transactions CSV", type=["csv"], help="e.g., transactions.csv")
    net_worth_file = st.sidebar.file_uploader("Upload Net Worth CSV", type=["csv"], help="e.g., net_worth.csv")

    # Load data, using dummy data if no file is uploaded
    transactions_df = get_dummy_transaction_data()
    if trans_file:
        try:
            transactions_df = pd.read_csv(trans_file)
        except Exception as e:
            st.error(f"Error loading transactions file: {e}. Please check the format.")
            return

    net_worth_df = get_dummy_net_worth_data()
    if net_worth_file:
        try:
            net_worth_df = pd.read_csv(net_worth_file)
        except Exception as e:
            st.error(f"Error loading net worth file: {e}. Please check the format.")
            return

    # Process Data
    transactions_df = load_and_preprocess_transactions(transactions_df)
    monthly_cash_flow, income_df, expenses_df = calculate_monthly_cash_flow(transactions_df)
    
    net_worth_df['Date'] = pd.to_datetime(net_worth_df['Date'])

    portfolio_df = get_dummy_portfolio_data()
    portfolio_df = update_portfolio_value(portfolio_df)

    st.header("Financial Overview")
    
    col1, col2, col3 = st.columns(3)
    
    total_income = transactions_df[transactions_df['Type'] == 'Income']['Amount'].sum()
    total_expenses = transactions_df[transactions_df['Type'] == 'Expense']['Amount'].sum()
    
    with col1:
        st.metric(label="Total Income", value=f"${total_income:,.2f}")
    with col2:
        st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")
    with col3:
        net_worth_change = net_worth_df['Net Worth'].iloc[-1] - net_worth_df['Net Worth'].iloc[0]
        st.metric(label="Net Worth Change", value=f"${net_worth_change:,.2f}")

    # --- Cash Flow Analysis ---
    st.subheader("Cash Flow Analysis")
    st.dataframe(transactions_df, use_container_width=True)
    
    cash_flow_fig = px.bar(monthly_cash_flow, x='Month', y='Signed_Amount',
                           title="Monthly Cash Flow", labels={'Signed_Amount': 'Net Cash Flow ($)'})
    st.plotly_chart(cash_flow_fig, use_container_width=True)

    # --- Net Worth Tracking ---
    st.subheader("Net Worth Over Time")
    st.dataframe(net_worth_df, use_container_width=True)
    
    net_worth_fig = px.line(net_worth_df, x='Date', y='Net Worth',
                            title="Net Worth Trend", labels={'Net Worth': 'Net Worth ($)'})
    st.plotly_chart(net_worth_fig, use_container_width=True)

    # --- Investment Performance ---
    st.subheader("Investment Portfolio")
    st.dataframe(portfolio_df, use_container_width=True)
    
    total_portfolio_value = portfolio_df['Current Value'].sum()
    st.markdown(f"**Total Portfolio Value:** ${total_portfolio_value:,.2f}")

if __name__ == "__main__":
    main()
