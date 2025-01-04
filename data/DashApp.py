from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Example data for sales_per_day (replace with actual data source)
sales_per_day = pd.DataFrame({
    'date': ['2021-01-10', '2021-01-11', '2021-01-12', '2021-01-13', '2021-01-14', '2021-01-15'],
    'sales': [100, 150, 200, 130, 170, 180]
})

# Convert 'date' to datetime
sales_per_day['date'] = pd.to_datetime(sales_per_day['date'])

# Perform analysis to draw a conclusion
price_increase_date = pd.Timestamp("2021-01-15")
sales_before = sales_per_day[sales_per_day['date'] < price_increase_date]['sales'].mean()
sales_after = sales_per_day[sales_per_day['date'] >= price_increase_date]['sales'].mean()
total_change_percentage = ((sales_per_day['sales'].iloc[-1] - sales_per_day['sales'].iloc[0])
                           / sales_per_day['sales'].iloc[0]) * 100
conclusion = f"Sales increased by {total_change_percentage:.2f}% from {sales_per_day['date'].iloc[0].date()} to {sales_per_day['date'].iloc[-1].date()}. " \
             f"Average sales before the price increase were ${sales_before:.2f}, and after were ${sales_after:.2f}."

# Create the line chart
line_chart = px.line(
    sales_per_day,
    x='date',
    y='sales',
    title="Sales Over Time for Pink Morsels",
    labels={'date': 'Date', 'sales': 'Sales ($)'},
)

# Add vertical line for January 15, 2021 (price increase date)
line_chart.add_shape(
    type="line",
    x0='2021-01-15',
    x1='2021-01-15',
    y0=0,
    y1=sales_per_day['sales'].max(),
    line=dict(color="Red", width=2, dash="dash"),
)
line_chart.add_annotation(
    x='2021-01-15',
    y=sales_per_day['sales'].max(),
    text="Price Increase (Jan 15, 2021)",
    showarrow=True,
    arrowhead=2,
)

# Layout for our Dash app
app.layout = html.Div([
    html.H1("Pink Morsels Sales Data Visualizer", style={'textAlign': 'center'}),
    dcc.Graph(figure=line_chart),
    html.P(
        "This chart visualizes the Pink Morsels sales over time. "
        "The dashed vertical red line indicates the price increase on January 15, 2021.",
        style={'textAlign': 'center'}
    ),
    html.H3("Conclusion", style={'textAlign': 'center', 'marginTop': '20px'}),
    html.P(conclusion, style={'textAlign': 'center', 'fontSize': '18px'})
])

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)