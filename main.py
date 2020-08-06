import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import tkinter as tk
from tkinter import filedialog, Text
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

    def return_path(self, file_type, folder_name):
        if len(file_type) != 0:
            return file_type
        else:
            setpath = self.directory + '\\' + folder_name
            if not os.path.exists(setpath):
                os.makedirs(setpath)
            return setpath

    def get_next_filename(self, source, directory_path, destination, file_name):

        num = 0
        while os.path.exists(destination):
            num += 1
            # use rfind to find your file extension if there is one
            period = file_name.rfind('.')
            # this ensures that it will work with files without extensions
            if period == -1:
                period = len(file_name)

            # create our new destination
            # we could extract the number and increment it
            # but this allows us to fill in the gaps if there are any
            # it has the added benefit of avoiding errors
            # in file names like this "test(sometext).pdf"
            new_file = f'{file_name[:period]}({num}){file_name[period:]}'

            destination = directory_path + '\\' + new_file
        shutil.move(source + file_name,
                    destination)

    def fucking_moveit(self, bool_flag, sub_path, main_path, filename, file_ext):

        file_name = f'{filename}{file_ext}'
        destination = main_path + '\\' + file_name

        #if true move file to its first directory
        if bool_flag:
            if os.path.isfile(destination):
                self.get_next_filename(self.directory, main_path, destination, file_name)

            else:
                shutil.move(self.directory + f'{filename}{file_ext}',
                        destination)
        #if false then move file to sub directory
        else:
            destination = sub_path + "\\" + file_name
            if os.path.isfile(destination):
                self.get_next_filename(main_path + "\\" ,sub_path, destination, file_name)
            else:
                shutil.move(main_path + "\\" +file_name,
                            destination)




    def create_sub(self, diretory_path, f):
        #creating timestamp based subdirectory
        timecreated = time.strftime('%m/%d/%Y', time.gmtime(
            os.path.getctime(diretory_path + '\\' + f'{f}')))
        month, day, year = str(timecreated).split('/', 2)
        daycreated = month + '.' + day + '.' + year

        #checking to see if diretory already exists
        # if it doesn't create new directory and  return the path
        if not os.path.isdir(diretory_path + "\\"+ f'{daycreated}'):
            subdirect = diretory_path + '\\' + f'{daycreated}'
            os.makedirs(subdirect)
            return subdirect
        #if it does exist return path
        else:
           return diretory_path + "\\"+ f'{daycreated}'
    def clean_up(self):
        global SVideos, sPDF, SExcel, SImages, SPrograms, SDocuments
        videoformats = ['.mp4', '.mov', '.webm', '.mgg', '.mp2', '.mpeg', '.mpe', '.mpv',
                        '.ogg', '.m4p', '.m4v', '.avi', '.wmv', '.mov', '.qt',
                        '.flv', '.swf', '.avchd']
        excelformats = ['.xlsm',  '.xlsx', '.xlsb', '.xltx']
        pdfformats = ['.pdf']
        docformats = ['.doc', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.rtf', '.txt'
            , '.wps', '.xml', '.xps']
        imageformats = ['.jpeg', '.jpg', '.png', '.gif', '.webp', '.tiff', '.psd', '.raw', '.bmp'
            , '.heif', '.indd', '.jpeg 2000', '.jpe', '.jif', '.jfif', '.jfi']
        progformats = ['.exe', '.lnk']
        audioformats = []
        PowerPoints = ['.pptx', '.pptm', '.ppt', '.pps', '.ppa' ]
        for f in os.listdir(self.directory):
            filename, file_ext = os.path.splitext(f)
            try:

                if not file_ext:
                    pass

                elif file_ext.lower() in (videoformats):
                    print("Found Video")
                    videopath = self.return_path(SVideos, "Videos")
                    self.fucking_moveit(1,"", videopath, filename, file_ext)

                    #create sub directory

                    sub_directory = self.create_sub(videopath, f)

                    #move the file to subdirectory

                    self.fucking_moveit(0,sub_directory,videopath, filename, file_ext)



                elif file_ext.lower() in (excelformats):
                    excel_path = self.return_path(SExcel, "Excel")
                    self.fucking_moveit(1,"",excel_path, filename, file_ext)

                    # create sub directory

                    sub_directory = self.create_sub(excel_path, f)

                    # move the file to subdirectory

                    self.fucking_moveit(0, sub_directory, excel_path, filename, file_ext)


                elif file_ext.lower() in (docformats):
                    print("Found Document")
                    document_path = self.return_path(SDocuments, "Documents")
                    self.fucking_moveit(1,"",document_path, filename, file_ext)

                    # create sub directory

                    sub_directory = self.create_sub(document_path, f)
                    # move the file to subdirectory

                    self.fucking_moveit(0, sub_directory, document_path, filename, file_ext)

                elif file_ext.lower() in (imageformats):
                    print("Found Image")
                    image_path = self.return_path(SImages, "Images")
                    self.fucking_moveit(1,"",image_path, filename, file_ext)

                    # create sub directory

                    sub_directory = self.create_sub(image_path, f)

                    # move the file to subdirectory

                    self.fucking_moveit(0, sub_directory, image_path, filename, file_ext)

                elif file_ext.lower() in (pdfformats):
                    print("Found PDF")
                    pdf_path = self.return_path(sPDF, "PDF")
                    self.fucking_moveit(1,"",pdf_path, filename, file_ext)

                    # create sub directory

                    sub_directory = self.create_sub(pdf_path, f)

                    # move the file to subdirectory

                    self.fucking_moveit(0, sub_directory, pdf_path, filename, file_ext)

                elif file_ext.lower() in (progformats):
                    print("FOUND PROG")
                    program_path = self.return_path(SPrograms, "Programs")
                    self.fucking_moveit(1,"",program_path, filename, file_ext)

                    # create sub directory

                    sub_directory = self.create_sub(program_path, f)

                    # move the file to subdirectory

                    self.fucking_moveit(0, sub_directory, program_path, filename, file_ext)

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
def video_location():


def gui():
    global DIRECTORY_TO_WATCH
    root = tk.Tk()
    canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
    canvas.pack()
    frame = tk.Frame(root, bg="white")
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    openFile = tk.Button(root, text="Open File", padx=10, pady=5, bg="white",
                         command=create_directory_path)
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
    if not os.path.isfile(os.getcwd() + '\\' + 'watchdirectory.txt'):
        gui()
    else:
        f = open("watchdirectory.txt", "r")
        if f.mode == 'r':
            contents = f.read()
            DIRECTORY_TO_WATCH = contents
        start_watching()
