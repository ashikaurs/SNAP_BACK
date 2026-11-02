
import os
import hashlib
import json


class DecoyManager:

    def __init__(self, decoy_directory):
        self.decoy_directory = decoy_directory
        self.baseline_file = os.path.join(
            decoy_directory, "decoy_baseline.json"
        )

        os.makedirs(decoy_directory, exist_ok=True)

    def calculate_hash(self, file_path):
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def create_decoys(self):

        decoys = {
            "employee_records.txt": "Confidential employee records",
            "financial_report.txt": "Confidential financial report",
            "company_credentials.txt": "Dummy credentials - NOT REAL"
        }

        for filename, content in decoys.items():

            file_path = os.path.join(
                self.decoy_directory, filename
            )

            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    file.write(content)

        self.save_baseline()

    def save_baseline(self):

        baseline = {}

        for filename in os.listdir(self.decoy_directory):

            file_path = os.path.join(
                self.decoy_directory, filename
            )

            if os.path.isfile(file_path):
                if filename == "decoy_baseline.json":
                    continue

                baseline[filename] = self.calculate_hash(file_path)

        with open(self.baseline_file, "w") as file:
            json.dump(baseline, file, indent=4)

    def check_decoys(self):

        with open(self.baseline_file, "r") as file:
            baseline = json.load(file)

        alerts = []

        for filename, original_hash in baseline.items():

            file_path = os.path.join(
                self.decoy_directory, filename
            )

            if not os.path.exists(file_path):
                alerts.append(f"[ALERT] Decoy deleted: {filename}")
                continue

            current_hash = self.calculate_hash(file_path)

            if current_hash != original_hash:
                alerts.append(f"[ALERT] Decoy modified: {filename}")

        return alerts


if __name__ == "__main__":

    manager = DecoyManager("decoy_test")

    if not os.path.exists(manager.baseline_file):
        manager.create_decoys()
        print("[SnapBack] Decoy files and baseline created.")

    alerts = manager.check_decoys()

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("[SnapBack] All decoy files are intact.")