from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Example data for sales_per_day (with a region column)
sales_per_day = pd.DataFrame({
    'date': ['2021-01-10', '2021-01-11', '2021-01-12', '2021-01-13', '2021-01-14', '2021-01-15'] * 4,
    'sales': [100, 150, 200, 130, 170, 180,
              120, 160, 210, 140, 180, 190,
              110, 155, 205, 135, 175, 185,
              90, 140, 180, 120, 150, 160],
    'region': ['north'] * 6 + ['east'] * 6 + ['south'] * 6 + ['west'] * 6
})
sales_per_day['date'] = pd.to_datetime(sales_per_day['date'])

# Calculate cumulative sales
sales_per_day['cumulative_sales'] = sales_per_day.groupby('region')['sales'].cumsum()

# Perform analysis for the conclusion
price_increase_date = pd.Timestamp("2021-01-15")
sales_before = sales_per_day[sales_per_day['date'] < price_increase_date]['sales'].mean()
sales_after = sales_per_day[sales_per_day['date'] >= price_increase_date]['sales'].mean()
total_change_percentage = ((sales_per_day['sales'].iloc[-1] - sales_per_day['sales'].iloc[0])
                           / sales_per_day['sales'].iloc[0]) * 100
conclusion = f"Sales increased by {total_change_percentage:.2f}% from {sales_per_day['date'].iloc[0].date()} to {sales_per_day['date'].iloc[-1].date()}. " \
             f"Average sales before the price increase were ${sales_before:.2f}, and after were ${sales_after:.2f}."

# App layout
app.layout = html.Div([
    html.H1("Pink Morsels Sales Data Visualizer",
            style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#123456', 'fontSize': '32px'}),

    html.Div([
        html.Label("Filter by Region:", style={'fontSize': '18px', 'color': '#333'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True,
            style={'fontSize': '16px', 'marginBottom': '10px'}
        )
    ], style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#f0f8ff', 'borderRadius': '8px'}),

    html.Div([
        dcc.RadioItems(
            id='chart-toggle',
            options=[
                {'label': 'Daily Sales', 'value': 'daily'},
                {'label': 'Cumulative Sales', 'value': 'cumulative'}
            ],
            value='daily',
            inline=True,
            style={'textAlign': 'center', 'marginBottom': '20px', 'fontSize': '16px', 'padding': '10px'}
        )
    ]),

    # Adjustable Graph
    html.Div([
        dcc.Graph(
            id='sales-chart',
            style={
                'width': '90%',  # Occupies 90% of the container width
                'height': '70vh',  # 70% of the viewport height
                'borderRadius': '8px',
                'padding': '10px',
                'margin': '0 auto'  # Center the graph horizontally
            }
        )
    ], style={'marginBottom': '20px', 'backgroundColor': '#fff', 'borderRadius': '10px', 'textAlign': 'center'}),

    # Conclusion
    html.Div(id='conclusion-text', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '20px'}),
    dcc.Markdown(
        children="**Tip:** Use the filters above to refine what you see.",
        style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '14px', 'color': '#666'}
    )
], style={
    'backgroundColor': '#f9f9f9',
    'padding': '30px',
    'margin': '0 auto',
    'width': '95%',  # Slightly less than full width for good visuals
    'maxWidth': '1200px',  # Prevents the layout from being too wide
    'display': 'block',
})


# Callback for updating the chart and conclusion text
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('conclusion-text', 'children')],
    [Input('chart-toggle', 'value'),
     Input('region-filter', 'value')]
)
def update_chart(selected_view, selected_region):
    # Filter data by region
    if selected_region == 'all':
        filtered_data = sales_per_day
    else:
        filtered_data = sales_per_day[sales_per_day['region'] == selected_region]

    # Generate the chart
    if selected_view == 'daily':
        figure = px.line(
            filtered_data,
            x='date',
            y='sales',
            color='region',
            title=f"Daily Sales Over Time ({selected_region.capitalize() if selected_region != 'all' else 'All Regions'})",
            labels={'date': 'Date', 'sales': 'Sales ($)', 'region': 'Region'}
        )
    else:
        figure = px.line(
            filtered_data,
            x='date',
            y='cumulative_sales',
            color='region',
            title=f"Cumulative Sales Over Time ({selected_region.capitalize() if selected_region != 'all' else 'All Regions'})",
            labels={'date': 'Date', 'cumulative_sales': 'Cumulative Sales ($)', 'region': 'Region'}
        )

    # Add a reference line for the price increase date
    figure.add_shape(
        type="line",
        x0='2021-01-15',
        x1='2021-01-15',
        y0=0,
        y1=filtered_data['sales'].max() if selected_view == 'daily' else filtered_data['cumulative_sales'].max(),
        line=dict(color="Red", width=2, dash="dash"),
    )
    figure.add_annotation(
        x='2021-01-15',
        y=filtered_data['sales'].max() if selected_view == 'daily' else filtered_data['cumulative_sales'].max(),
        text="Price Increase (Jan 15, 2021)",
        showarrow=True,
        arrowhead=2,
    )

    # Style the chart layout
    figure.update_layout(
        title_font_size=20,
        title_x=0.5,  # Center the title
        xaxis_title="Date",
        yaxis_title="Sales",
        legend_title="Region",
        plot_bgcolor="#f0f0f0",  # Light grey background
        paper_bgcolor="#ffffff",  # White background
        xaxis=dict(showline=True, linewidth=2, linecolor='black'),
        yaxis=dict(showline=True, linewidth=2, linecolor='black'),
    )

    return figure, f"Conclusion: {conclusion}"


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)