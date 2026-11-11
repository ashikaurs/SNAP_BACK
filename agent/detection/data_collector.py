
import csv
from datetime import datetime
from pathlib import Path


class DataCollector:
    def __init__(self):
        # Locate the SNAP_BACK project root.
        project_root = Path(__file__).resolve().parents[2]

        # Store training data in SNAP_BACK/data/
        self.output_file = project_root / "data" / "normal_activity.csv"

        # Create the data directory if it doesn't exist.
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        self.fieldnames = [
            "timestamp",
            "total_events",
            "modified_count",
            "created_count",
            "deleted_count",
            "moved_count",
            "unique_files",
            "unique_extensions"
        ]

        # Create the CSV file and its header if necessary.
        if not self.output_file.exists() or self.output_file.stat().st_size == 0:
            with open(self.output_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

        print(f"[DATA COLLECTOR] Saving data to: {self.output_file}")

    def save_sample(self, features):
        """
        Save one extracted feature vector as a CSV row.
        """

        sample = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            **features
        }

        with open(self.output_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(sample)

        print("[DATA COLLECTOR] Training sample saved.")
