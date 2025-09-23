# Real vs Nominal Return Calculator

## Project Overview

The **Real vs Nominal Return Calculator** is a Python program designed to help users understand the **true growth of their investments** after adjusting for inflation. While the **nominal return** shows the stated interest or investment gain, the **real return** reflects the **actual increase in purchasing power**, taking inflation into account.

This tool is useful for personal finance planning, investment evaluation, and understanding how inflation affects wealth over time.

---

## Features

### **Core Features**

* Calculate **real return** from nominal return and inflation rate using the formula:

  $$
  \text{Real Return} = \frac{1 + \text{Nominal Return}}{1 + \text{Inflation Rate}} - 1
  $$
* Take user input for **nominal return** (%) and **inflation rate** (%).
* Output the **real return** with interpretation:

  * Positive → investment grew in purchasing power
  * Zero → kept pace with inflation
  * Negative → investment lost value

### **Extra Features**

* Multi-year projection of real returns with compounding.
* Comparison table: Year | Nominal Return | Inflation | Real Return.
* Graphical visualization using Matplotlib: Nominal vs Real returns over time.
* Scenario analysis with different inflation rates.
* Break-even inflation calculation (real return = 0).
* Portfolio mode for multiple assets with weighted average real return.
* Live inflation data integration from APIs.
* “What-if” simulations for inflation and nominal return ranges.
* Interactive dashboard using Streamlit or Plotly Dash.
* Inflation-adjusted goal calculator.
* Country comparison of real returns with varying inflation rates.

---

## Getting Started

### **Requirements**

* Python 3.x
* Optional libraries for extra features:

  * `matplotlib` → Graphs/plots
  * `seaborn` → Enhanced visualizations
  * `requests` → Fetch live inflation data from APIs
  * `streamlit` or `plotly` → Interactive dashboards

### **Installation**

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project folder:

   ```bash
   cd Real_vs_Nominal_Return_Calculator
   ```
3. Install required packages (if using extra features):

   ```bash
   pip install matplotlib seaborn requests streamlit plotly
   ```

### **Usage**

1. Run the Python program:

   ```bash
   python real_vs_nominal_return.py
   ```
2. Enter the **nominal return** (%) when prompted.
3. Enter the **inflation rate** (%) when prompted.
4. View the **real return** and interpretation.
5. (Optional) Explore advanced features like multi-year projections, graphs, or portfolio mode.

---

## Screenshots

*(Add your program output screenshots here)*

* Example 1: Single-year calculation
* Example 2: Multi-year projection graph
* Example 3: Portfolio mode / weighted real return

---

## Learning Outcomes

### **Programming Concepts Learned**

* User input and output handling.
* Type conversion (`str` → `float`).
* Arithmetic operations and formula implementation.
* Functions and return values.
* Conditional statements for interpreting results.
* Output formatting with f-strings.
* Optional: Matplotlib, lists, loops, API calls.

### **Finance Concepts Learned**

* Difference between **Nominal Return** and **Real Return**.
* Understanding **inflation** and its impact on purchasing power.
* Compounding effect on real returns.
* Portfolio-level weighted real return calculations (if portfolio mode implemented).
* Practical investment insights: when an investment grows or loses value in real terms.

---

## Author

* Name: Chris Fernandes
* Email: chriscric17@gmail.com
* GitHub: \[Your GitHub Profile]


### Financial Dashboard
