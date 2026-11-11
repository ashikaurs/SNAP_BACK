
import os
import time


class FeatureExtractor:
    def __init__(self, window_seconds=10):
        self.window_seconds = window_seconds

    def extract_features(self, events):
        """
        Extract numerical features from file events
        occurring within the rolling time window.
        """

        current_time = time.time()

        # Keep only events from the last 10 seconds.
        recent_events = [
            event for event in events
            if current_time - event["timestamp"] <= self.window_seconds
        ]

        # Count different event types.
        total_events = len(recent_events)

        modified_count = sum(
            1 for event in recent_events
            if event["type"] == "MODIFIED"
        )

        created_count = sum(
            1 for event in recent_events
            if event["type"] == "CREATED"
        )

        deleted_count = sum(
            1 for event in recent_events
            if event["type"] == "DELETED"
        )

        moved_count = sum(
            1 for event in recent_events
            if event["type"] == "MOVED"
        )

        # Identify distinct files and file extensions.
        unique_files = set()
        unique_extensions = set()

        for event in recent_events:
            file_path = event["path"]

            # MOVED events currently contain "source -> destination".
            # Treat the complete path string as one event identifier.
            unique_files.add(file_path)

            filename = os.path.basename(file_path)

            # Extract file extension.
            extension = os.path.splitext(filename)[1].lower()

            if extension:
                unique_extensions.add(extension)

        # Calculate final features.
        features = {
            "total_events": total_events,
            "modified_count": modified_count,
            "created_count": created_count,
            "deleted_count": deleted_count,
            "moved_count": moved_count,
            "unique_files": len(unique_files),
            "unique_extensions": len(unique_extensions)
        }

        return features
