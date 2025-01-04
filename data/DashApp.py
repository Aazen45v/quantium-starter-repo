from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Example data for sales_per_day (replace with actual data source)
sales_per_day = pd.DataFrame({
    'date': ['2021-01-10', '2021-01-11', '2021-01-12', '2021-01-13', '2021-01-14', '2021-01-15'],
    'sales': [100, 150, 200, 130, 170, 180]
})
sales_per_day['date'] = pd.to_datetime(sales_per_day['date'])

# Calculate cumulative sales
sales_per_day['cumulative_sales'] = sales_per_day['sales'].cumsum()

# Perform analysis for the conclusion
price_increase_date = pd.Timestamp("2021-01-15")
sales_before = sales_per_day[sales_per_day['date'] < price_increase_date]['sales'].mean()
sales_after = sales_per_day[sales_per_day['date'] >= price_increase_date]['sales'].mean()
total_change_percentage = ((sales_per_day['sales'].iloc[-1] - sales_per_day['sales'].iloc[0])
                           / sales_per_day['sales'].iloc[0]) * 100
conclusion = f"Sales increased by {total_change_percentage:.2f}% from {sales_per_day['date'].iloc[0].date()} to {sales_per_day['date'].iloc[-1].date()}. " \
             f"Average sales before the price increase were ${sales_before:.2f}, and after were ${sales_after:.2f}."

# Initialize the app layout with radio buttons
app.layout = html.Div([
    html.H1("Pink Morsels Sales Data Visualizer",
            style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#333'}),
    dcc.RadioItems(
        id='chart-toggle',
        options=[
            {'label': 'Daily Sales', 'value': 'daily'},
            {'label': 'Cumulative Sales', 'value': 'cumulative'}
        ],
        value='daily',
        inline=True,
        style={'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '18px', 'padding': '10px'}
    ),
    dcc.Graph(id='sales-chart'),  # Dynamic chart based on radio button
    html.Div(id='conclusion-text', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '20px'}),
    dcc.Markdown(
        style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '16px', 'color': '#666'},
        children="**Tip:** Use the radio button above to switch between different views of the sales data."
    )
], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px'})


# Callback for updating the chart and conclusion text based on radio button selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('conclusion-text', 'children')],
    [Input('chart-toggle', 'value')]
)
def update_chart(selected_view):
    # Generate a chart based on the selected view
    if selected_view == 'daily':
        figure = px.line(
            sales_per_day,
            x='date',
            y='sales',
            title="Daily Sales Over Time",
            labels={'date': 'Date', 'sales': 'Sales ($)'}
        )
    elif selected_view == 'cumulative':
        figure = px.line(
            sales_per_day,
            x='date',
            y='cumulative_sales',
            title="Cumulative Sales Over Time",
            labels={'date': 'Date', 'cumulative_sales': 'Cumulative Sales ($)'}
        )
    else:
        return None, ""

    # Add a reference line and annotation for the price increase date
    figure.add_shape(
        type="line",
        x0='2021-01-15',
        x1='2021-01-15',
        y0=0,
        y1=sales_per_day['sales'].max() if selected_view == 'daily' else sales_per_day['cumulative_sales'].max(),
        line=dict(color="Red", width=2, dash="dash"),
    )
    figure.add_annotation(
        x='2021-01-15',
        y=sales_per_day['sales'].max() if selected_view == 'daily' else sales_per_day['cumulative_sales'].max(),
        text="Price Increase (Jan 15, 2021)",
        showarrow=True,
        arrowhead=2,
    )

    # Return the figure and conclusion
    return figure, f"Conclusion: {conclusion}"


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)