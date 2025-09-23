def inflation_impact(current_value, inflation_rate, years):
    
    future_value = current_value / ((1 + inflation_rate) ** years)
    return future_value


# --- Main Program ---
print("💰 Inflation Impact Calculator 💰")
current_money = float(input("Enter the current amount of money (₹): "))
inflation = float(input("Enter annual inflation rate (in %): ")) / 100
years = int(input("Enter the number of years: "))

future_value = inflation_impact(current_money, inflation, years)

print(f"\n₹{current_money:.2f} today will only be worth about ₹{future_value:.2f} in {years} years at {inflation*100:.1f}% inflation.")
