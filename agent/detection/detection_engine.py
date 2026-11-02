
import time


class DetectionEngine:

    def __init__(self):
        self.file_events = []
        self.modification_times = []
        self.last_decoy_alert_time = None
        self.last_detection_state = None

    # Receive file events
    def process_file_event(self, event_type, file_path):

        event = {
            "type": event_type,
            "path": file_path,
            "timestamp": time.time()
        }

        self.file_events.append(event)

        print(f"\n[FILE EVENT] {event_type}: {file_path}")

        if event_type == "MODIFIED":
            self.modification_times.append(event["timestamp"])

        self.analyse_activity()

    # Receive decoy alerts
    def process_decoy_alert(self, alert):

        print(f"\n[HIGH PRIORITY] {alert}")

        self.last_decoy_alert_time = time.time()

        self.analyse_activity()

    # Analyse activity
    def analyse_activity(self):

        current_time = time.time()

        # Keep only modifications from the last 10 seconds
        self.modification_times = [
            timestamp for timestamp in self.modification_times
            if current_time - timestamp <= 10
        ]

        modification_count = len(self.modification_times)

        decoy_recently_triggered = (
            self.last_decoy_alert_time is not None
            and current_time - self.last_decoy_alert_time <= 10
        )

        # Determine current detection state
        if decoy_recently_triggered and modification_count >= 3:
            state = "CRITICAL"

        elif decoy_recently_triggered:
            state = "WARNING"

        elif modification_count >= 5:
            state = "SUSPICIOUS"

        else:
            state = "NORMAL"

        # Report only when the detection state changes
        if state != self.last_detection_state:

            if state == "CRITICAL":
                print("\n[CRITICAL] Strong ransomware indicators detected!")

            elif state == "WARNING":
                print("\n[WARNING] Decoy activity detected.")

            elif state == "SUSPICIOUS":
                print("\n[WARNING] Unusually high file modification activity.")

            self.last_detection_state = state
