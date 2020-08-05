import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
import shutil


class Watcher:
    def __init__(self, DIRECTORY_TO_WATCH):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = DIRECTORY_TO_WATCH
        self.action = Actions()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("ERROR")
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        action = Actions()
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            action.clean_up()
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            action.clean_up()
        elif event.event_type == 'moved':
            print("Recieved moved event - %s." % event.src_path)
        elif event.event_type == 'deleted':
            print("Recieved deleted event - %s." % event.src_path)


class Actions:
    def __init__(self):
        self.directory = r"C:\Users\tdphi\Videos\\"

    def clean_up(self):
        for f in os.listdir(self.directory):
            filename, file_ext = os.path.splitext(f)

            try:
                if not file_ext:
                    pass
                elif file_ext.lower() in ('.mp4'):
                    if not os.path.exists(self.directory + 'Gaming Videos'):
                        os.makedirs(self.directory + 'Gaming Videos')
                    shutil.move(self.directory + f'{filename}{file_ext}',
                                self.directory + 'Gaming Videos\\' + f'{filename}{file_ext}')
                    for f in os.listdir(self.directory + 'Gaming Videos'):
                        fname, filext = os.path.splitext(f)
                        if not filext:
                            pass
                        elif filext.lower() in ('.mp4'):
                            timecreated = time.strftime('%m/%d/%Y', time.gmtime(
                                os.path.getctime(self.directory + 'Gaming Videos\\' + f'{f}')))
                            month, day, year = str(timecreated).split('/', 2)
                            daycreated = month + '.' + day + '.' + year

                            if not os.path.exists(self.directory + 'Gaming Videos\\' + f'{daycreated}'):
                                os.makedirs(self.directory + 'Gaming Videos\\' + f'{daycreated}')
                            shutil.move(self.directory + 'Gaming Videos\\' + f'{f}',
                                        self.directory + 'Gaming Videos\\' + f'{daycreated}' + '\\' + f'{f}')

            except(FileNotFoundError, PermissionError):
                pass


if __name__ == '__main__':
    a = Actions()
    a.clean_up()
    w = Watcher(r"C:\Users\tdphi\Videos")
    w.run()
