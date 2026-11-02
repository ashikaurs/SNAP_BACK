
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class FileMonitor(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED] {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED] {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED] {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[MOVED] {event.src_path} -> {event.dest_path}")


if __name__ == "__main__":

    path = input("Enter directory to monitor: ")

    event_handler = FileMonitor()
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    print(f"\n[SnapBack] Monitoring started: {path}")
    print("[SnapBack] Press CTRL+C to stop monitoring.\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
