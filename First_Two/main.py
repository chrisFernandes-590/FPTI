# Get user input
print("Real vs Nominal Return Calculator")
nominal_return_percentage = float(input("Enter Nominal return (%): "))
inflation_percentage = float(input("Enter Inflation Rate (%): "))

# print(f"nominal return: {nominal_return_percentage}")

def calculate_real_return(nominal_percent, inflation_percent):
    # Convert to decimal
    nominal = nominal_return_percentage / 100 
    print(nominal)
    inflation = inflation_percentage / 100
    print(inflation)
    real_return = ((1 + nominal) / (1 + inflation)) - 1
    real_return_percent = real_return * 100
    print(f"Real return: {real_return_percent:.2f}%")

calculate_real_return(nominal_return_percentage, inflation_percentage)