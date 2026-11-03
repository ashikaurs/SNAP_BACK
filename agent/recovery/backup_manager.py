
import os
import json
import shutil
import hashlib


class BackupManager:

    def __init__(self, source_directory, backup_directory):

        self.source_directory = os.path.abspath(source_directory)
        self.backup_directory = os.path.abspath(backup_directory)

        # Prevent backups from being stored inside the monitored directory
        if os.path.commonpath([
            self.source_directory,
            self.backup_directory
        ]) == self.source_directory:

            raise ValueError(
                "Backup directory must be outside the monitored directory."
            )

        os.makedirs(self.backup_directory, exist_ok=True)

        self.manifest_file = os.path.join(
            self.backup_directory, "backup_manifest.json"
        )

    # Calculate SHA-256 hash
    def calculate_hash(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    # Create initial backups
    def create_backup(self):

        manifest = {}

        for root, dirs, files in os.walk(self.source_directory):

            for filename in files:

                source_path = os.path.join(root, filename)

                if os.path.islink(source_path):
                    continue

                relative_path = os.path.relpath(
                    source_path, self.source_directory
                )

                backup_path = os.path.join(
                    self.backup_directory, relative_path
                )

                os.makedirs(
                    os.path.dirname(backup_path),
                    exist_ok=True
                )

                shutil.copy2(source_path, backup_path)

                manifest[relative_path] = self.calculate_hash(
                    backup_path
                )

                print(f"[BACKUP CREATED] {relative_path}")

        with open(self.manifest_file, "w") as file:
            json.dump(manifest, file, indent=4)

        print("\n[SnapBack] Initial backup completed.")

    # Verify backup integrity
    def verify_backup(self, relative_path):

        with open(self.manifest_file, "r") as file:
            manifest = json.load(file)

        if relative_path not in manifest:
            print("[ERROR] No backup record found.")
            return False

        backup_path = os.path.join(
            self.backup_directory, relative_path
        )

        if not os.path.isfile(backup_path):
            print("[ERROR] Backup file is missing.")
            return False

        current_hash = self.calculate_hash(backup_path)

        if current_hash == manifest[relative_path]:
            print("[SnapBack] Backup integrity verified.")
            return True

        print("[ERROR] Backup integrity verification failed.")
        return False

    # Restore a selected file
    def restore_file(self, relative_path):

        if not self.verify_backup(relative_path):
            return

        source_path = os.path.join(
            self.backup_directory, relative_path
        )

        destination_path = os.path.join(
            self.source_directory, relative_path
        )

        os.makedirs(
            os.path.dirname(destination_path),
            exist_ok=True
        )

        shutil.copy2(source_path, destination_path)

        print(f"[RECOVERED] {relative_path}")



#creating a folder for backup and adding all the files to it. 

# if __name__ == "__main__":

#     source = input("Enter directory to back up: ")
#     backup = input("Enter backup directory: ")

#     manager = BackupManager(source, backup)

#     manager.create_backup()



if __name__ == "__main__":

    source = input("Enter directory to back up: ")
    backup = input("Enter backup directory: ")

    manager = BackupManager(source, backup)

    relative_path = input("Enter file to restore: ")

    manager.restore_file(relative_path)
