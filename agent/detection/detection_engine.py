
import time
from collections import defaultdict


class DetectionEngine:

    def __init__(self):
        self.file_events = []
        self.decoy_alerts = []
        self.modification_times = []

    # Receive events from the file monitor
    def process_file_event(self, event_type, file_path):

        event = {
            "type": event_type,
            "path": file_path,
            "timestamp": time.time()
        }

        self.file_events.append(event)

        if event_type == "MODIFIED":
            self.modification_times.append(event["timestamp"])

        self.analyse_activity()

    # Receive alerts from decoy manager
    def process_decoy_alert(self, alert):

        self.decoy_alerts.append(alert)

        print(f"\n[HIGH PRIORITY] {alert}")

        self.analyse_activity()

    # Analyse collected activity
    def analyse_activity(self):

        current_time = time.time()

        # Consider only modifications in the last 10 seconds
        recent_modifications = [
            timestamp for timestamp in self.modification_times
            if current_time - timestamp <= 10
        ]

        self.modification_times = recent_modifications

        # Count modifications in the time window
        modification_count = len(recent_modifications)

        if self.decoy_alerts and modification_count >= 3:

            print("\n[CRITICAL] Strong ransomware indicators detected!")
            print("[SnapBack] Multiple files modified and decoy triggered.")

        elif self.decoy_alerts:

            print("\n[WARNING] Decoy activity detected.")

        elif modification_count >= 5:

            print("\n[WARNING] Unusually high file modification activity.")

        else:

            print("\n[INFO] File activity recorded.")


if __name__ == "__main__":

    engine = DetectionEngine()

    engine.process_file_event("MODIFIED", "file1.txt")
    engine.process_file_event("MODIFIED", "file2.txt")
    engine.process_file_event("MODIFIED", "file3.txt")

    engine.process_decoy_alert(
        "Decoy modified: employee_records.txt"
    )
