
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from monitoring.file_monitor import FileMonitor
from detection.detection_engine import DetectionEngine
from decoys.decoy_manager import DecoyManager


class SnapBackAgent(FileSystemEventHandler):

    def __init__(self, engine, decoy_manager):
        self.engine = engine
        self.decoy_manager = decoy_manager
        self.reported_alerts = set()

    def on_any_event(self, event):

        if event.is_directory:
            return

        if os.path.basename(event.src_path) == "decoy_baseline.json":
            return

        event_type = event.event_type.upper()

        if event_type not in ["CREATED", "MODIFIED", "DELETED", "MOVED"]:
            return

        if event_type == "MOVED":
            path = f"{event.src_path} -> {event.dest_path}"
        else:
            path = event.src_path

        # Send file activity to detection engine
        self.engine.process_file_event(event_type, path)

        # Check decoy integrity
        alerts = self.decoy_manager.check_decoys()

        for alert in alerts:
            if alert not in self.reported_alerts:
                self.reported_alerts.add(alert)
                self.engine.process_decoy_alert(alert)


if __name__ == "__main__":

    print("\n========== SNAPBACK AGENT ==========\n")

    monitor_path = input("Enter test directory to monitor: ")
    decoy_path = input("Enter decoy directory: ")

    if not os.path.isdir(monitor_path):
        print("[ERROR] Monitoring directory does not exist.")
        exit()

    if not os.path.isdir(decoy_path):
        print("[ERROR] Decoy directory does not exist.")
        exit()

    # Initialize components
    engine = DetectionEngine()
    decoy_manager = DecoyManager(decoy_path)

    if not os.path.exists(decoy_manager.baseline_file):
        print("[ERROR] Decoy baseline not found. Initialize decoys first.")
        exit()

    handler = SnapBackAgent(engine, decoy_manager)
    observer = Observer()

    # Monitor both directories
    observer.schedule(handler, monitor_path, recursive=True)

    if os.path.abspath(monitor_path) != os.path.abspath(decoy_path):
        observer.schedule(handler, decoy_path, recursive=True)

    observer.start()

    print("\n[SnapBack] Agent started successfully.")
    print("[SnapBack] Monitoring:", monitor_path)
    print("[SnapBack] Monitoring decoys:", decoy_path)
    print("[SnapBack] Press CTRL+C to stop.\n")

    try:
        while True:
            engine.collect_training_sample()
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        print("\n[SnapBack] Stopping agent...")

    observer.join()
    print("[SnapBack] Agent stopped.")
