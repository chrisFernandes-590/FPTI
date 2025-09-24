import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
from datetime import datetime
import json

# --- Helper Functions and Data Simulation ---

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

def generate_report_text(transactions_df, monthly_cash_flow, net_worth_df, portfolio_df):
    """
    Generates a comprehensive text report of the financial data.
    """
    report = "--- Personal Finance Report ---\n\n"
    report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # Financial Overview
    if not transactions_df.empty and not net_worth_df.empty:
        total_income = transactions_df[transactions_df['Type'] == 'Income']['Amount'].sum()
        total_expenses = transactions_df[transactions_df['Type'] == 'Expense']['Amount'].sum()
        net_worth_change = net_worth_df['Net Worth'].iloc[-1] - net_worth_df['Net Worth'].iloc[0]

        report += "--- Financial Overview ---\n"
        report += f"Total Income: ${total_income:,.2f}\n"
        report += f"Total Expenses: ${total_expenses:,.2f}\n"
        report += f"Net Worth Change: ${net_worth_change:,.2f}\n\n"

    # Monthly Cash Flow
    if not monthly_cash_flow.empty:
        report += "--- Monthly Cash Flow ---\n"
        report += monthly_cash_flow.to_string(index=False)
        report += "\n\n"
    
    # Net Worth
    if not net_worth_df.empty:
        report += "--- Net Worth Over Time ---\n"
        report += net_worth_df.to_string(index=False)
        report += "\n\n"

    # Investment Portfolio
    if not portfolio_df.empty:
        total_portfolio_value = portfolio_df['Current Value ($)'].sum()
        report += "--- Investment Portfolio ---\n"
        report += portfolio_df.to_string(index=False)
        report += f"\n\nTotal Portfolio Value: ${total_portfolio_value:,.2f}\n"
    else:
        report += "--- Investment Portfolio ---\n"
        report += "No investment portfolio data provided.\n"
    
    return report

# --- Core Logic Functions ---

def load_and_preprocess_transactions(df):
    """
    Loads, cleans, and categorizes transaction data.
    """
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        return pd.DataFrame(), "Invalid transaction file. It must contain 'Date' and 'Amount' columns."

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    if 'Type' not in df.columns:
        df['Type'] = 'Expense'
        df.loc[df['Amount'] >= 0, 'Type'] = 'Income'
    
    df['Amount'] = df['Amount'].abs()
    
    if 'Category' not in df.columns:
        df['Category'] = 'Other'
        df.loc[df['Type'] == 'Income', 'Category'] = 'Income'
        df.loc[df['Description'].str.contains('Groceries|Shopping|Dinner', case=False), 'Category'] = 'Food & Shopping'
        df.loc[df['Description'].str.contains('Rent|Bill|Subscription', case=False), 'Category'] = 'Bills & Utilities'

    return df, ""

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
    if 'Investment' not in portfolio_df.columns or 'Shares' not in portfolio_df.columns:
        if 'Asset' in portfolio_df.columns and 'Quantity' in portfolio_df.columns:
            portfolio_df.rename(columns={'Asset': 'Investment', 'Quantity': 'Shares'}, inplace=True)
        else:
            return pd.DataFrame(), "Invalid portfolio file. It must contain 'Investment' and 'Shares' columns (or 'Asset' and 'Quantity')."
    
    portfolio_df['Current Price ($)'] = portfolio_df['Investment'].apply(mock_get_stock_price)
    portfolio_df['Current Value ($)'] = portfolio_df['Shares'] * portfolio_df['Current Price ($)']
    
    return portfolio_df, ""

# --- Streamlit Application ---

def main():
    st.set_page_config(layout="wide", page_title="Personal Finance Dashboard")
    st.title("💰 Personal Finance Dashboard")

    if 'trans_df' not in st.session_state:
        st.session_state.trans_df = pd.DataFrame()
        st.session_state.trans_error = ""
    if 'net_worth_df' not in st.session_state:
        st.session_state.net_worth_df = pd.DataFrame()
        st.session_state.net_worth_error = ""
    if 'portfolio_df' not in st.session_state:
        st.session_state.portfolio_df = pd.DataFrame()
        st.session_state.portfolio_error = ""
    if 'page' not in st.session_state:
        st.session_state.page = "Overview"

    # Sidebar for navigation and file upload
    with st.sidebar:
        st.header("Navigation")
        st.session_state.page = st.radio("Go to", ["Overview", "Transactions", "Net Worth", "Portfolio"])
        
        st.header("Data Upload")
        trans_file = st.file_uploader("Upload Transactions CSV", type=["csv"], help="e.g., transactions.csv")
        net_worth_file = st.file_uploader("Upload Net Worth CSV", type=["csv"], help="e.g., net_worth.csv")
        portfolio_file = st.file_uploader("Upload Portfolio CSV", type=["csv"], help="e.g., portfolio.csv")

    # --- File Upload and Processing ---
    if trans_file:
        try:
            temp_df = pd.read_csv(trans_file)
            st.session_state.trans_df, st.session_state.trans_error = load_and_preprocess_transactions(temp_df)
        except Exception as e:
            st.session_state.trans_error = f"Error loading transactions file: {e}. Please check the format."
            
    if net_worth_file:
        try:
            temp_df = pd.read_csv(net_worth_file)
            if 'Date' not in temp_df.columns or 'Net Worth' not in temp_df.columns:
                if len(temp_df.columns) >= 2:
                    temp_df.rename(columns={temp_df.columns[0]: 'Date', temp_df.columns[1]: 'Net Worth'}, inplace=True)
                else:
                    st.session_state.net_worth_error = "Uploaded Net Worth file must contain 'Date' and 'Net Worth' columns."
            
            if not st.session_state.net_worth_error:
                st.session_state.net_worth_df = temp_df
                try:
                    st.session_state.net_worth_df['Date'] = pd.to_datetime(st.session_state.net_worth_df['Date'])
                except Exception as e:
                    st.session_state.net_worth_error = f"Error converting 'Date' column: {e}. Ensure dates are in a valid format (e.g., YYYY-MM-DD)."
        except Exception as e:
            st.session_state.net_worth_error = f"Error loading net worth file: {e}. Please check the format."
            
    if portfolio_file:
        try:
            temp_df = pd.read_csv(portfolio_file)
            st.session_state.portfolio_df, st.session_state.portfolio_error = update_portfolio_value(temp_df)
        except Exception as e:
            st.session_state.portfolio_error = f"Error loading portfolio file: {e}. Please check the format."
            
    # --- Page Rendering ---
    
    if st.session_state.page == "Overview":
        st.header("Financial Overview")
        if not st.session_state.trans_df.empty and not st.session_state.net_worth_df.empty:
            col1, col2, col3 = st.columns(3)
            
            total_income = st.session_state.trans_df[st.session_state.trans_df['Type'] == 'Income']['Amount'].sum()
            total_expenses = st.session_state.trans_df[st.session_state.trans_df['Type'] == 'Expense']['Amount'].sum()
            net_worth_change = st.session_state.net_worth_df['Net Worth'].iloc[-1] - st.session_state.net_worth_df['Net Worth'].iloc[0]
            
            with col1:
                st.metric(label="Total Income", value=f"${total_income:,.2f}")
            with col2:
                st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")
            with col3:
                st.metric(label="Net Worth Change", value=f"${net_worth_change:,.2f}")
                
            report_text = generate_report_text(st.session_state.trans_df, pd.DataFrame(), st.session_state.net_worth_df, pd.DataFrame())
            st.download_button(
                label="Download Financial Report",
                data=report_text,
                file_name="financial_report.txt",
                mime="text/plain",
            )
        else:
            st.info("Please upload both Transactions and Net Worth files to see a full financial overview.")

    elif st.session_state.page == "Transactions":
        st.header("Transactions and Cash Flow")
        if st.session_state.trans_error:
            st.error(st.session_state.trans_error)
        elif st.session_state.trans_df.empty:
            st.info("Please upload a Transactions CSV file to view your cash flow analysis.")
        else:
            st.dataframe(st.session_state.trans_df, use_container_width=True)
            monthly_cash_flow, _, _ = calculate_monthly_cash_flow(st.session_state.trans_df)
            cash_flow_fig = px.bar(monthly_cash_flow, x='Month', y='Signed_Amount',
                                   title="Monthly Cash Flow", labels={'Signed_Amount': 'Net Cash Flow ($)'})
            st.plotly_chart(cash_flow_fig, use_container_width=True)

    elif st.session_state.page == "Net Worth":
        st.header("Net Worth Over Time")
        if st.session_state.net_worth_error:
            st.error(st.session_state.net_worth_error)
        elif st.session_state.net_worth_df.empty:
            st.info("Please upload a Net Worth CSV file to track your net worth trend.")
        else:
            st.dataframe(st.session_state.net_worth_df, use_container_width=True)
            net_worth_fig = px.line(st.session_state.net_worth_df, x='Date', y='Net Worth',
                                    title="Net Worth Trend", labels={'Net Worth': 'Net Worth ($)'})
            st.plotly_chart(net_worth_fig, use_container_width=True)

    elif st.session_state.page == "Portfolio":
        st.header("Investment Portfolio")
        if st.session_state.portfolio_error:
            st.error(st.session_state.portfolio_error)
        elif st.session_state.portfolio_df.empty:
            st.info("Please upload a Portfolio CSV file to see your investment performance.")
        else:
            st.dataframe(st.session_state.portfolio_df, use_container_width=True)
            total_portfolio_value = st.session_state.portfolio_df['Current Value ($)'].sum()
            st.markdown(f"**Total Portfolio Value:** ${total_portfolio_value:,.2f}")

if __name__ == "__main__":
    main()
