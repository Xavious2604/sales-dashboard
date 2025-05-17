from dash import Dash, dcc, html, callback_context
from dash.dependencies import Input, Output, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import os

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CYBORG])
server = app.server  # Expose Flask server for deployment

# Load CSV file
csv_path = os.path.join(os.path.dirname(__file__), "data", "100 Sales Records.csv")
try:
    data = pd.read_csv(csv_path)
except Exception as e:
    print(f"Error loading CSV: {str(e)}")
    data = pd.DataFrame()

# Predefined column mappings
DATE_COL = "Order Date"
SALES_COL = "Total Revenue"
PROFIT_COL = "Total Profit"
REGION_COL = "Region"
CATEGORY_COL = "Item Type"
SUBCATEGORY_COL = "Country"
PRODUCT_COL = "Order ID"
SEGMENT_COL = "Sales Channel"

# Infer column types
def infer_columns(df):
    categorical = [col for col in df.columns if df[col].dtype == 'object' or df[col].nunique() < 20]
    numerical = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    date = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col]) or 'date' in col.lower()]
    return categorical, numerical, date

# Process data
categorical = []
if not data.empty:
    categorical, numerical, date = infer_columns(data)
    try:
        data[DATE_COL] = pd.to_datetime(data[DATE_COL], format='%m/%d/%Y', errors='coerce')
        if data[DATE_COL].isna().any():
            print("Warning: Some dates in 'Order Date' could not be parsed.")
        data['Year'] = data[DATE_COL].dt.year
        data['Month'] = data[DATE_COL].dt.to_period('M')
    except Exception as e:
        print(f"Error parsing date column: {str(e)}")
        data = pd.DataFrame()

# Main dashboard layout with Bootstrap
def dashboard_layout(categorical_cols):
    slicer_options = [col for col in categorical_cols if col not in [SALES_COL, PROFIT_COL, PRODUCT_COL]]
    return dbc.Container([
        # Title
        html.H1("Sales Dashboard", className="text-center mb-4"),
        # Slicers
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Filters:", className="form-label"),
                        dcc.Dropdown(
                            id='filter-dropdown',
                            options=[{'label': col, 'value': col} for col in slicer_options],
                            multi=True,
                            placeholder="Select columns to filter",
                            className="form-select"
                        ),
                        html.Div(id='dynamic-slicers', className="mt-3")
                    ])
                ], className="shadow-sm")
            ], width=12, lg=4, className="mx-auto")
        ], className="mb-4"),
        # KPI cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Revenue", className="card-title text-center"),
                        html.P(id='total-sales', className="card-text text-center fs-4")
                    ])
                ], className="shadow-sm text-white bg-dark")
            ], width=12, md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Profit", className="card-title text-center"),
                        html.P(id='total-profit', className="card-text text-center fs-4")
                    ])
                ], className="shadow-sm text-white bg-dark")
            ], width=12, md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Profit Margin", className="card-title text-center"),
                        html.P(id='profit-margin', className="card-text text-center fs-4")
                    ])
                ], className="shadow-sm text-white bg-dark")
            ], width=12, md=4)
        ], className="mb-4"),
        # Trend line
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='sales-trend')
                    ])
                ], className="shadow-sm")
            ], width=12)
        ], className="mb-4"),
        # Drill-down charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='category-chart')
                    ])
                ], className="shadow-sm")
            ], width=12, md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='subcategory-chart')
                    ])
                ], className="shadow-sm")
            ], width=12, md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='product-chart')
                    ])
                ], className="shadow-sm")
            ], width=12, md=4)
        ], className="mb-4"),
        # Additional charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='top-products')
                    ])
                ], className="shadow-sm")
            ], width=12, md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='customer-segments')
                    ])
                ], className="shadow-sm")
            ], width=12, md=6)
        ], className="mb-4")
    ], fluid=True)

# Initial layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    html.Div(id='dashboard-container', children=dashboard_layout(categorical) if not data.empty else html.Div("Error: Could not load CSV file.", style={'color': 'red', 'text-align': 'center', 'margin-top': '20px'})),
    html.Div(id='error-message', style={'color': 'red', 'text-align': 'center', 'margin-top': '20px'})
])

# Callback to generate dynamic slicers
@app.callback(
    Output('dynamic-slicers', 'children'),
    Input('filter-dropdown', 'value')
)
def update_slicers(selected_filters):
    if not selected_filters or data.empty:
        return []
    slicers = []
    for col in selected_filters:
        unique_vals = data[col].dropna().unique().tolist()
        slicers.append(
            html.Div([
                html.Label(f"Select {col}:", className="form-label"),
                dcc.Dropdown(
                    id={'type': 'dynamic-slicer', 'index': col},
                    options=[{'label': val, 'value': val} for val in unique_vals],
                    multi=True,
                    placeholder=f"Select {col} (all if empty)",
                    className="form-select"
                )
            ], className="mb-2")
        )
    return slicers

# Callback to update KPI cards
@app.callback(
    [Output('total-sales', 'children'),
     Output('total-profit', 'children'),
     Output('profit-margin', 'children')],
    Input({'type': 'dynamic-slicer', 'index': ALL}, 'value')
)
def update_kpis(slicer_values):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    total_sales = df[SALES_COL].sum()
    total_profit = df[PROFIT_COL].sum()
    profit_margin = total_profit / total_sales if total_sales > 0 else 0
    return f"${total_sales:,.2f}", f"${total_profit:,.2f}", f"{profit_margin:.2%}"

# Callback for sales trend line
@app.callback(
    Output('sales-trend', 'figure'),
    Input({'type': 'dynamic-slicer', 'index': ALL}, 'value')
)
def update_sales_trend(slicer_values):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    trend_df = df.groupby('Month')[SALES_COL].sum().reset_index()
    trend_df['Month'] = trend_df['Month'].astype(str)
    fig = px.line(trend_df, x='Month', y=SALES_COL, title='Revenue Trend Over Time')
    return fig

# Callback for category chart
@app.callback(
    Output('category-chart', 'figure'),
    Input({'type': 'dynamic-slicer', 'index': ALL}, 'value')
)
def update_category_chart(slicer_values):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    category_sales = df.groupby(CATEGORY_COL)[SALES_COL].sum().reset_index()
    fig = px.bar(category_sales, x=CATEGORY_COL, y=SALES_COL, title='Revenue by Item Type')
    return fig

# Callback for sub-category chart
@app.callback(
    Output('subcategory-chart', 'figure'),
    [Input({'type': 'dynamic-slicer', 'index': ALL}, 'value'),
     Input('category-chart', 'clickData')]
)
def update_subcategory_chart(slicer_values, clickData):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    if clickData:
        selected_category = clickData['points'][0]['x']
        df = df[df[CATEGORY_COL] == selected_category]
    
    subcategory_sales = df.groupby(SUBCATEGORY_COL)[SALES_COL].sum().reset_index()
    fig = px.bar(subcategory_sales, x=SUBCATEGORY_COL, y=SALES_COL, title='Revenue by Country')
    return fig

# Callback for product chart
@app.callback(
    Output('product-chart', 'figure'),
    [Input({'type': 'dynamic-slicer', 'index': ALL}, 'value'),
     Input('category-chart', 'clickData'),
     Input('subcategory-chart', 'clickData')]
)
def update_product_chart(slicer_values, category_clickData, subcategory_clickData):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    if category_clickData:
        selected_category = category_clickData['points'][0]['x']
        df = df[df[CATEGORY_COL] == selected_category]
    if subcategory_clickData:
        selected_subcategory = subcategory_clickData['points'][0]['x']
        df = df[df[SUBCATEGORY_COL] == selected_subcategory]
    
    product_sales = df.groupby(PRODUCT_COL)[SALES_COL].sum().reset_index().sort_values(SALES_COL, ascending=False).head(10)
    fig = px.bar(product_sales, x=PRODUCT_COL, y=SALES_COL, title='Top 10 Orders by Revenue')
    return fig

# Callback for top products chart
@app.callback(
    Output('top-products', 'figure'),
    Input({'type': 'dynamic-slicer', 'index': ALL}, 'value')
)
def update_top_products(slicer_values):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    top_products = df.groupby(PRODUCT_COL)[SALES_COL].sum().reset_index().sort_values(SALES_COL, ascending=False).head(10)
    fig = px.bar(top_products, x=PRODUCT_COL, y=SALES_COL, title='Top 10 Orders by Revenue')
    return fig

# Callback for customer segments
@app.callback(
    Output('customer-segments', 'figure'),
    Input({'type': 'dynamic-slicer', 'index': ALL}, 'value')
)
def update_customer_segments(slicer_values):
    if not callback_context.triggered or data.empty:
        raise PreventUpdate
    
    df = data.copy()
    slicer_cols = [prop['id']['index'] for prop in callback_context.inputs_list[0]]
    for col, vals in zip(slicer_cols, slicer_values):
        if vals:
            df = df[df[col].isin(vals)]
    
    segment_counts = df[SEGMENT_COL].value_counts().reset_index()
    segment_counts.columns = [SEGMENT_COL, 'Count']
    fig = px.pie(segment_counts, values='Count', names=SEGMENT_COL, title='Sales Channel Distribution')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=False, port=8051)