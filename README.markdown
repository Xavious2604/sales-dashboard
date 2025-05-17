# Sales Dashboard

A Python-based interactive sales dashboard built with [Dash](https://dash.plotly.com/) and [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/). The dashboard visualizes sales data from `100 Sales Records.csv`, providing KPIs, trend analysis, and drill-down capabilities.

## Features

- **KPIs**: Displays Total Revenue, Total Profit, and Profit Margin.
- **Slicers**: Filter data by Region, Item Type, Sales Channel, or Order Priority.
- **Trend Line**: Shows monthly revenue trends from 2010 to 2017.
- **Drill-Down Charts**: Explore revenue by Item Type → Country → Order ID (top 10 orders).
- **Additional Charts**: Top 10 orders by revenue and sales channel distribution (Online vs. Offline).
- **Responsive UI**: Modern, dark-themed interface using Bootstrap's CYBORG theme, optimized for desktop and mobile.

## Prerequisites

- Python 3.8+
- Git
- A GitHub account
- (Optional) A [Render](https://render.com/) account for deployment

## Setup Instructions (Local)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sales-dashboard.git
   cd sales-dashboard
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure CSV File**:
   - The dashboard uses `data/100 Sales Records.csv`. Ensure it’s present in the `data/` folder.
   - If you don’t have the file, replace it with your own CSV, but update the column mappings in `app.py` (e.g., `DATE_COL`, `SALES_COL`).

5. **Run the App**:
   ```bash
   python app.py
   ```
   - Open `http://127.0.0.1:8051/` in your browser.

## Deployment Instructions (Render)

1. **Create a GitHub Repository**:
   - Go to [GitHub](https://github.com/) and create a new public repository named `sales-dashboard`.
   - Initialize with a `README.md` (optional, as it’s included here).
   - Push the project files:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/sales-dashboard.git
     git push -u origin main
     ```

2. **Set Up Render**:
   - Sign up or log in to [Render](https://render.com/).
   - Click **New** → **Web Service**.
   - Connect your GitHub account and select the `sales-dashboard` repository.
   - Configure the web service:
     - **Name**: `sales-dashboard` (or any unique name).
     - **Environment**: Python.
     - **Region**: Choose your preferred region (e.g., Oregon).
     - **Branch**: `main`.
     - **Root Directory**: Leave blank (or `.`).
     - **Build Command**: `pip install -r requirements.txt`.
     - **Start Command**: `gunicorn app:server`.
   - Click **Create Web Service**.
   - Wait ~5 minutes for deployment. Once complete, access the app via the provided URL (e.g., `https://sales-dashboard.onrender.com`).

3. **Update the App**:
   - Make changes to the code, commit, and push to GitHub:
     ```bash
     git add .
     git commit -m "Update app"
     git push origin main
     ```
   - Render automatically redeploys the app.

## Usage

- **Slicers**: Select filters (e.g., Region, Item Type) to update all components.
- **KPI Cards**: View Total Revenue (~$137,549,721.10), Total Profit (~$44,162,389.16), and Profit Margin (~32.11%) unfiltered.
- **Trend Line**: Analyze monthly revenue trends.
- **Drill-Down**:
  - Click an Item Type (e.g., Cosmetics) to filter the Country chart.
  - Click a Country (e.g., Switzerland) to see top 10 orders.
- **Charts**: Explore top 10 orders (bar chart) and sales channel distribution (pie chart).

## Project Structure

```
sales-dashboard/
├── app.py                    # Main Dash application
├── data/
│   └── 100 Sales Records.csv # Sales data CSV
├── requirements.txt          # Python dependencies
├── Procfile                  # Render start command
├── .gitignore                # Files to ignore in Git
└── README.md                 # Project documentation
```

## Troubleshooting

- **CSV Loading Error**:
  - Ensure `data/100 Sales Records.csv` exists.
  - Check file permissions: `chmod +r data/100\ Sales\ Records.csv`.
  - Test loading:
    ```python
    import pandas as pd
    print(pd.read_csv("data/100 Sales Records.csv").head())
    ```

- **Date Parsing Warning**:
  - If dates fail to parse, inspect `Order Date`:
    ```python
    print(data['Order Date'].unique())
    ```
  - Ensure dates match `MM/DD/YYYY`.

- **Deployment Fails on Render**:
  - Check Render logs for errors (e.g., missing dependencies).
  - Verify `requirements.txt` includes all packages.
  - Ensure `Procfile` is `web: gunicorn app:server`.

- **Port Conflict**:
  - Locally, the app uses port 8051. If occupied, change in `app.py`:
    ```python
    app.run(debug=False, port=8052)
    ```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgments

- [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/) for the framework.
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) for UI styling.
- [Render](https://render.com/) for free hosting.