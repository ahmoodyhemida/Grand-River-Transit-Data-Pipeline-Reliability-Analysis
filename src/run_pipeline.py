import subprocess
import sys
from pathlib import Path

STATIC_FEED_FOLDER = Path("GRT_GTFS/Static_Feed")

def run(script):
    subprocess.run([sys.executable, script])

if (STATIC_FEED_FOLDER / "stop_times.txt").exists():
    print(f"Static feed already exists in {STATIC_FEED_FOLDER}, skipping download.")
    print("To refresh it, run: python src/Static_Feed_Downloader.py")
else:
    run("src/Static_Feed_Downloader.py")

print("Collecting live data. Press Control + C to stop and decode.")

try:
    run("src/Trip_Updates_Collector.py")
except KeyboardInterrupt:
    pass

print("Decoding collected data...")
run("src/Trip_Updates_Decoder.py")
