# GRT Transit Data Pipeline & Reliability Analysis

> **Status:** Work in progress. The data pipeline and first reliability analysis are complete; more analysis questions may be added.

This project collects and analyzes Grand River Transit (GRT) GTFS data. It combines GRT's static schedule data with live GTFS-Realtime trip updates to measure how closely routes run to schedule.

## What It Does

1. Downloads GRT's static GTFS schedule data.
2. Collects live trip updates every 60 seconds.
3. Saves the raw Protocol Buffer (`.pb`) files locally.
4. Decodes the updates and stores them in a SQLite database.
5. Joins live updates with scheduled trip and stop-time data.
6. Calculates delay metrics by route and creates visualizations.

## Tools Used

- Python and SQL
- SQLite
- GTFS static data and GTFS-Realtime Protocol Buffers
- pandas, matplotlib, seaborn, JupySQL, SQLAlchemy

## Project Structure

```text
.
├── src/
│   ├── run_pipeline.py                # Runs the download, collect and decode steps in order
│   ├── Static_Feed_Downloader.py      # Downloads the static GRT feed
│   ├── Trip_Updates_Collector.py      # Collects live trip-update snapshots
│   └── Trip_Updates_Decoder.py        # Decodes snapshots into SQLite
├── GRT_GTFS/                          # Generated data and database files
├── notebook.ipynb                     # Analysis and charts
├── requirements.txt
└── README.md
```

The collected data and database are ignored by Git because they are generated locally and can become large.

## Setup

Run the commands below from the project root.

### Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows Command Prompt**

```bash
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If you are not opening the notebook in VS Code, install Jupyter as well:

```bash
pip install jupyter
```

## Run the Pipeline

### 1. Collect and decode the data

```bash
python src/run_pipeline.py
```

This runs three steps in order:

1. **Downloads the static schedule** into `GRT_GTFS/Static_Feed/`. This runs first so the schedule matches the trips you collect. If the static feed already exists, this step is skipped so it stays consistent with data you already collected. To force a fresh download, run `python src/Static_Feed_Downloader.py`.
2. **Collects live trip updates** every 60 seconds and saves timestamped `.pb` files in `GRT_GTFS/Trip_Updates/`. Let it run for as long as you want to collect data, then press `Ctrl+C` to stop.
3. **Decodes the collected data** into `GRT_GTFS/Trip_Updates_Static_Feed.db`. This starts automatically after you stop collecting. Snapshots that were already decoded are skipped, so it is safe to run the pipeline more than once; new snapshots are added to the existing database.

### 2. Run the analysis

Open `notebook.ipynb` in VS Code or Jupyter and run the cells in order. The notebook loads the static schedule data into SQLite, creates indexes, runs the analysis, and generates the charts.

### Running the steps individually

Each step can also be run on its own:

```bash
python src/Static_Feed_Downloader.py
python src/Trip_Updates_Collector.py
python src/Trip_Updates_Decoder.py
```

## Analysis

### Question

**How well does GRT run on schedule, and which routes are least reliable?**

The notebook joins real-time trip updates with the static trip schedule and calculates stop-level departure delay in minutes. It then calculates each route's average and maximum delay.

Because the collector saves a new snapshot every minute, the same trip-stop event can appear more than once. A SQL CTE keeps only the latest update for each trip-stop event so repeated observations do not affect the results.

Indexes were added to the main join keys. In the documented six-day collection, `trip_update` contained more than 50 million rows. The main route-delay query went from more than 10 minutes without indexes to about 1 minute with indexes.

## Current Results

The current notebook uses data collected from **September 1–6, 2026**. Results will change if the project is run over a different time period.

- Most routes were close to schedule on average.
- The analysis covers 45+ routes.
- The correlation between average and maximum delay by route was **r = 0.47**, which is moderate.
- Route 6 averaged 3.4 minutes late but had the largest observed maximum delay: nearly 64 minutes.

The notebook includes charts for average delay by route, maximum delay by route, and the relationship between average and maximum delay.

## Notes

- This is a sample of live data collected over a limited period, not a complete history of GRT service.
- Route rankings and delay values can change when the pipeline is run again.
- More analysis questions may be added later.

## Data Sources

- Grand River Transit static GTFS feed
- Grand River Transit GTFS-Realtime trip-updates feed
