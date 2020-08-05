import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import tkinter as tk
from tkinter import filedialog,Text
from datetime import datetime
import shutil


class Watcher:
    def __init__(self):
        global DIRECTORY_TO_WATCH
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
        global DIRECTORY_TO_WATCH
        self.directory = DIRECTORY_TO_WATCH.replace('/', '\\') + '\\'

    def clean_up(self):
        global SVideos, sPDF,SExcel, SImages, SPrograms, SDocuments
        videoformats = ['.mp4', '.mov', '.webm', '.mgg', '.mp2','.mpeg', '.mpe', '.mpv',
                        '.ogg', '.m4p', '.m4v', '.avi', '.wmv', '.mov', '.qt',
                        '.flv', '.swf', '.avchd']
        excelformats = ['.xlsm', 'xls', 'xlsx', 'xlsm', 'xlsb', '.xltx']
        pdfformats = ['.pdf']
        docformats = ['.doc','.docm','.docx', '.dot', '.dotm', '.dotx', '.rtf', '.txt'
                      , '.wps', '.xml', '.xps']
        imageformats = ['.jpeg', '.jpg', '.png', '.gif', '.webp','.tiff', '.psd', '.raw', '.bmp'
            ,'.heif', '.indd', '.jpeg 2000', '.jpe', '.jif','.jfif', '.jfi']
        progformats = ['.exe', '.lnk']
        audioformats = []
        for f in os.listdir(self.directory):
            filename, file_ext = os.path.splitext(f)

            try:

                if not file_ext:
                    pass

                elif file_ext.lower() in (videoformats):
                    # if directory is set by user store
                    # in designated area otherwise save in current directory
                    if len(SVideos) != 0:
                        videopath = SVideos

                    else:
                        videopath = self.directory + '\\Videos'
                        if not os.path.exists(videopath):
                            os.makedirs(videopath)
                    if len(sPDF) != 0:
                        pdf_path = sPDF

                    print(videopath)
                    print(self.directory)
                    new_file = ""
                    num = 0
                    original_destination = f'{filename}{file_ext}'
                    # loop until we find a file that doesn't exist
                    while os.path.exists(videopath + '\\' + original_destination):
                        num += 1
                        print("stuck here")

                        # use rfind to find your file extension if there is one
                        period = filename.rfind('.')
                        # this ensures that it will work with files without extensions
                        if period == -1:
                            period = len(filename)

                        # create our new destination
                        # we could extract the number and increment it
                        # but this allows us to fill in the gaps if there are any
                        # it has the added benefit of avoiding errors
                        # in file names like this "test(sometext).pdf"
                        new_file = f'{filename[:period]}({num}){file_ext}'
                        print(os.path.exists(new_file))
                        original_destination = new_file
                    if len(new_file) == 0:
                        shutil.move(self.directory + f'{filename}{file_ext}',
                                videopath + '\\' + f'{filename}{file_ext}')
                    else:
                        print("OH FUCK")
                        print(new_file)
                        shutil.move(self.directory + f'{filename}{file_ext}',
                                    videopath + '\\' + new_file)

                    for f in os.listdir(videopath):
                        fname, filext = os.path.splitext(f)
                        if not filext:
                            pass
                        elif filext.lower() in videoformats:
                            timecreated = time.strftime('%m/%d/%Y', time.gmtime(
                                os.path.getctime(videopath + '\\' + f'{f}')))
                            month, day, year = str(timecreated).split('/', 2)
                            daycreated = month + '.' + day + '.' + year

                            if not os.path.exists(videopath + '\\' + f'{daycreated}'):
                                os.makedirs(videopath + '\\' + f'{daycreated}')
                            new_file = ""
                            num = 0
                            original_destination = f'{daycreated}' + '\\' + f'{f}'
                            # loop until we find a file that doesn't exist
                            while os.path.exists(videopath + '\\' + original_destination):
                                num += 1
                                print("stuck here 2")

                                # use rfind to find your file extension if there is one
                                period = fname.rfind('.')
                                # this ensures that it will work with files without extensions
                                if period == -1:
                                    period = len(fname)

                                # create our new destination
                                # we could extract the number and increment it
                                # but this allows us to fill in the gaps if there are any
                                # it has the added benefit of avoiding errors
                                # in file names like this "test(sometext).pdf"
                                new_file = f'{fname[:period]}({num}){filext}'
                                if (os.path.exists(videopath + '\\' + f'{daycreated}' + '\\' + new_file)):
                                    original_destination = videopath + '\\' + f'{daycreated}' + '\\' + new_file
                                else:
                                    original_destination = new_file
                            if len(new_file) == 0:
                                print("Overwrite")
                                shutil.move(videopath + '\\' + f'{f}',
                                            videopath + '\\' + f'{daycreated}' + '\\' + f'{f}')
                            else:
                                print("OH FUCK 2")
                                print(new_file)
                                shutil.move(videopath + '\\' + f'{f}',
                                            videopath + '\\' + f'{daycreated}' + '\\' + new_file)

                '''elif file_ext.lower() in ('.mp4'):
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
                                        self.directory + 'Gaming Videos\\' + f'{daycreated}' + '\\' + f'{f}')'''

            except(FileNotFoundError, PermissionError):
                pass
def start_watching():
    a = Actions()
    a.clean_up()
    w = Watcher()
    w.run()

def create_directory_path():
    global DIRECTORY_TO_WATCH
    foldername = filedialog.askdirectory()
    DIRECTORY_TO_WATCH = foldername
    f = open("watchdirectory.txt", "w+")
    f.write(foldername)
    f.close()

def gui():
    global DIRECTORY_TO_WATCH
    root = tk.Tk()
    canvas = tk.Canvas(root, height = 700, width = 700, bg="#263D42")
    canvas.pack()
    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight= 0.8, relx= 0.1, rely= 0.1)
    openFile = tk.Button(root, text ="Open File", padx=10, pady=5, bg="white",
                         command = create_directory_path)
    openFile.pack()
    root.mainloop()


DIRECTORY_TO_WATCH = ""
SVideos = r"C:\Users\tdphi\Desktop\Videos"
SPrograms = ""
SImages = ""
SDocuments = ""
SExcel = ""
sPDF = ""

if __name__ == '__main__':
    if not os.path.isfile(r'C:\Users\tdphi\PycharmProjects\pythonProject2\watchdirectory.txt'):
        gui()
    else:
        f = open("watchdirectory.txt", "r")
        if f.mode == 'r':
            contents = f.read()
            DIRECTORY_TO_WATCH = contents
        start_watching()

