import pandas as pd

# File paths for the three input CSV files
file1 = 'daily_sales_data_0.csv'
file2 = 'daily_sales_data_1.csv'
file3 = 'daily_sales_data_2.csv'

# Step 1: Load all CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

# Step 2: Combine all CSVs into one DataFrame
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# Step 3: Filter rows for only "Pink Morsels"
filtered_df = combined_df[combined_df['product'] == 'pink morsel']

# Step 4: Calculate the 'sales' column (quantity * price)
filtered_df['sales'] = filtered_df['price'].replace('[\$,]', '', regex=True).astype(float) * filtered_df['quantity']

# Step 5: Append '$' to 'sales' column
filtered_df['sales'] = filtered_df['sales'].apply(lambda x: f"${x}")

# Step 6: Extract required columns: 'sales', 'date', 'region'
final_df = filtered_df[['sales', 'date', 'region']]

# Step 7: Save the resulting DataFrame to a formatted output CSV file
output_file = 'Total_transactions.csv'
final_df.to_csv(output_file, index=False)

print(f"Formatted data saved to {output_file}")