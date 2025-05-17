# Sales Dashboard

A Python-based interactive sales dashboard built with [Dash](https://dash.plotly.com/) and [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/). The dashboard visualizes sales data from `data/100 Sales Records.csv`, providing KPIs, trend analysis, and drill-down capabilities.

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
   git clone https://github.com/Xavious2604/sales-dashboard.git
   cd sales-dashboard
   ```

2. **Configure Git Identity**:
   - Set your Git name and email to avoid identity errors:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```
   - Replace `"Your Name"` and `"your.email@example.com"` with your name and GitHub-associated email.

3. **Configure Git Authentication**:
   - GitHub requires a Personal Access Token (PAT) for HTTPS authentication:
     - Go to GitHub **Settings > Developer settings > Personal access tokens > Tokens (classic)**.
     - Generate a token with `repo` scope.
     - When pushing, use your username (`Xavious2604`) and PAT as the password.
   - Alternatively, set up SSH authentication (see [GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)).

4. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Ensure CSV File**:
   - The dashboard uses `data/100 Sales Records.csv`. Ensure it’s present in the `data/` folder.
   - If you don’t have the file, replace it with your own CSV, but update the column mappings in `app.py` (e.g., `DATE_COL`, `SALES_COL`).

7. **Run the App**:
   ```bash
   python app.py
   ```
   - Open `http://127.0.0.1:8051/` in your browser.

## Adding Folders to the Repository

To add a new folder (e.g., `assets/` for images):
1. Create the folder locally:
   ```bash
   mkdir assets
   ```
2. Add at least one file (Git ignores empty folders):
   ```bash
   touch assets/placeholder.txt
   echo "Placeholder file" > assets/placeholder.txt
   ```
3. Stage, commit, and push:
   ```bash
   git add assets/
   git commit -m "Add assets folder"
   git push -u origin main
   ```
4. Use your username (`Xavious2604`) and PAT for authentication.
5. Verify the folder on GitHub: `https://github.com/Xavious2604/sales-dashboard`.

## Deployment Instructions

### Deploying the Dash App (Render)

The Dash application (`app.py`) requires a server and cannot be hosted on GitHub Pages. Use Render for deployment:

1. **Create a GitHub Repository**:
   - Ensure all files are pushed to `https://github.com/Xavious2604/sales-dashboard`:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/Xavious2604/sales-dashboard.git
     git push -u origin main
     ```
   - Use your username (`Xavious2604`) and PAT.

2. **Set Up Render**:
   - Sign up or log in to [Render](https://render.com/).
   - Click **New** → **Web Service**.
   - Connect your GitHub account and select the `sales-dashboard` repository.
   - Configure:
     - **Name**: `sales-dashboard`.
     - **Environment**: Python.
     - **Region**: Oregon (or your choice).
     - **Branch**: `main`.
     - **Root Directory**: `.`.
     - **Build Command**: `pip install -r requirements.txt`.
     - **Start Command**: `gunicorn app:server`.
   - Click **Create Web Service**.
   - Wait ~5 minutes. Access the app at the provided URL (e.g., `https://sales-dashboard.onrender.com`).

3. **Update the App**:
   - Commit and push changes:
     ```bash
     git add .
     git commit -m "Update app"
     git push origin main
     ```
   - Render redeploys automatically.

### Setting Up GitHub Pages (Static Site)

To host a static site (e.g., project documentation) on GitHub Pages instead of the default `README.md`:

1. **Create `index.html`**:
   ```bash
   echo '<!DOCTYPE html><html><head><title>Sales Dashboard</title></head><body><h1>Sales Dashboard</h1><p>Visit the app on <a href="https://sales-dashboard.onrender.com">Render</a>.</p></body></html>' > index.html
   ```

2. **Push to GitHub**:
   ```bash
   git add index.html
   git commit -m "Add index.html for GitHub Pages"
   git push -u origin main
   ```

3. **Configure GitHub Pages**:
   - Go to **Settings** → **Pages**.
   - Set **Source** to `main` branch, `/ (root)`.
   - Save and wait ~1-2 minutes.
   - Visit `https://xavious2604.github.io/sales-dashboard/`.

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
├── assets/                   # Static files (e.g., images)
│   └── placeholder.txt       # Placeholder file
├── index.html                # GitHub Pages static page
├── requirements.txt          # Python dependencies
├── Procfile                  # Render start command
├── .gitignore                # Files to ignore in Git
└── README.md                 # Project documentation
```

## Troubleshooting

- **Git Identity Error**:
  - Configure identity:
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

- **Git Push Error (Authentication Failed)**:
  - Use a PAT with `repo` scope:
    ```bash
    git push -u origin main
    ```
  - Enter username (`Xavious2604`) and PAT.

- **GitHub Pages Shows README.md**:
  - Ensure `index.html` exists in the `main` branch root.
  - Verify GitHub Pages is set to `main` branch, `/ (root)`.

- **CSV Loading Error**:
  - Check `data/100 Sales Records.csv`:
    ```bash
    chmod +r data/100\ Sales\ Records.csv
    python -c "import pandas as pd; print(pd.read_csv('data/100 Sales Records.csv').head())"
    ```

- **Render Deployment Fails**:
  - Check Render logs.
  - Ensure `requirements.txt` and `Procfile` are correct.

- **Port Conflict**:
  - Change port in `app.py` if 8051 is occupied:
    ```python
    app.run(debug=False, port=8052)
    ```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgments

- [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/) for the framework.
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) for UI styling.
- [Render](https://render.com/) for hosting.