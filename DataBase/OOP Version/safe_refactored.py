import sys
import os
import uu
import sqlite3
import base64
import cv2


class EncodeDecode:
    """
    Use: Encodes specified file type into binary format for database to store.
    """

    def __init__(self):
        pass

    @staticmethod
    def _strip_filename(filename_with_extension):
        fn_w_e = filename_with_extension
        filename = fn_w_e.split(".")[0]
        extension = fn_w_e.split(".")[1]
        return filename, extension

    def _process_file_type(self, filename_with_extension, mode):
        self.file_name = self._strip_filename(filename_with_extension)[0]
        self.extension = self._strip_filename(filename_with_extension)[1]
        self.file_path = os.getcwd() + "\\" + filename_with_extension
        self.database_file_directory = os.getcwd()

        try:
            self.extension = DataBase.file_types[self.extension]
        except Exception as e:
            print(e)

        if self.extension == "IMAGE":
            if mode == 'encode':
                self._encode_image()
            elif mode == 'decode':
                self._decode_image(filename_with_extension)

        elif self.extension == "TEXT":
            if mode == 'encode':
                self._encode_text()
            elif mode == 'decode':
                self._decode_text(filename_with_extension)

        elif self.extension == "VIDEO" or self.extension == "AUDIO":
            if mode == 'encode':
                self._encode_video_audio()
            elif mode == 'decode':
                try:
                    self._decode_video_audio(filename_with_extension)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)

        self.extension = self._strip_filename(filename_with_extension)[1]

    def remove_uu_text_file(self, file_name=None):
        if file_name is None:
            encoded_uu_text_file = self.file_name + ".txt"
            os.remove(encoded_uu_text_file)
        else:
            os.remove(file_name)

    def _encode_video_audio(self):
        self._encode_uu_to_b64()
        print("Audio/Video file successfully stored!")

    def _encode_uu_write(self):
        uu_file_out = self.file_name + ".txt"
        uu_file_encoded_write = uu.encode(self.file_path, uu_file_out)
        return uu_file_encoded_write

    def _encode_uu_read(self):
        self._encode_uu_write()
        uu_file_in = self.file_name + ".txt"
        with open(uu_file_in, "r") as f:
            return f.read()

    def _encode_uu_to_b64(self):
        uu_file_read = self._encode_uu_read()
        self.file_string = base64.b64encode(uu_file_read.encode("utf-8"))
        self.remove_uu_text_file()

    def _decode_video_audio(self, filename_with_extension):
        self._decode_uu_to_b64(filename_with_extension)

    def _decode_uu_write(self):
        uu_file_out = self.file_name + ".txt"
        uu_file_decode_write = uu.encode(self.file_path, uu_file_out)
        return uu_file_decode_write

    def _decode_uu_to_video_audio(self, filename_with_extension):
        filename = filename_with_extension.split(".")[0]
        uu.decode(filename + ".txt", filename_with_extension)
        self.remove_uu_text_file(filename + ".txt")
        print("File {} successfully recovered!".format(filename_with_extension))

    def _decode_uu_to_b64(self, filename_with_extension):
        filename = filename_with_extension.split(".")[0]
        with open(filename + ".txt", 'wb') as f_output:
            f_output.write(base64.b64decode(self.file_string))
        return self._decode_uu_to_video_audio(filename_with_extension)

    def _read_text(self):
        with open(self.file_path, "r") as f:
            return f.read()

    def _encode_text(self):
        text = self._read_text()
        self.file_string = base64.b64encode(text.encode("utf-8"))
        # print("file_string\t", cls.file_string)
        print("Text file successfully stored!")
        return self.file_string

    def _decode_text(self, filename_with_extension):
        with open(filename_with_extension, 'wb') as f_output:
            f_output.write(base64.b64decode(self.file_string))

    def _read_image(self):
        image_read = cv2.imread(self.file_path)
        return image_read

    def _encode_image(self):
        image = self._read_image()
        self.file_string = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode().encode("utf-8")
        print("Image file successfully stored!")

    def _decode_image(self, filename_with_extension):
        with open(filename_with_extension, 'wb') as f_output:
            f_output.write(base64.b64decode(self.file_string))
        print("File {} successfully recovered!".format(filename_with_extension))


class DataBase(EncodeDecode):
    """
    DataBase class is a Sub-Class of Encode Class - inherits methods

    Use:  Initializes database file in given directory if specified (default is current directory)
    """
    file_types = {
        "txt": "TEXT",
        "java": "TEXT",
        "dart": "TEXT",
        "py": "TEXT",
        "jpg": "IMAGE",
        "png": "IMAGE",
        "jpeg": "IMAGE",
        "mp4": "VIDEO",
        "mp3": "AUDIO",
    }

    def __init__(self, sql_file=None, directory=None):
        self.sql_file = sql_file
        self.directory = directory
        self.file_string = ''
        super().__init__()

    @property
    def sql_file(self):
        return self._sql_file

    @sql_file.setter
    def sql_file(self, value):
        self._sql_file = value

    @property
    def directory(self):
        return self._sql_file

    @directory.setter
    def directory(self, value):
        self._directory = value

    @staticmethod
    def _print_creating_file(sql_file, directory):
        if directory is None:
            directory = "current directory"
        print("Creating file: {} in {} \n\nDatabase file created.".format(sql_file, directory))

    def create_database_file(self, sql_file=None, directory=None):
        if sql_file is None:
            sql_file = self.sql_file
        if directory is not None:
            os.chdir(directory)
            self._print_creating_file(sql_file, directory)
            self.initialize_database_file(sql_file)
        elif directory is None:
            directory = os.getcwd()
            self._print_creating_file(sql_file, directory)
            sqlite3.connect(self.sql_file)
            self.initialize_database_file(sql_file)

    def initialize_database_file(self, sql):
        database = self.connect_to_database_file(sql)

        try:
            database.execute('''CREATE TABLE SAFE
                (FILE_NAME TEXT PRIMARY KEY NOT NULL,
                DIRECTORY TEXT NOT NULL,
                NAME TEXT NOT NULL,
                EXTENSION TEXT NOT NULL,
                FILES TEXT NOT NULL);''')

        except Exception as e:
            cursor = database.cursor()
            cursor.execute('SELECT * FROM SAFE')
            rows = cursor.fetchall()
            print("Database found!\nSee contents below\n")
            for row in rows:
                print('\t' + row[1] + '\\' + row[0])
            print('\n')

    @staticmethod
    def connect_to_database_file(sql_file=None, directory=None):
        if directory is not None:
            os.chdir(directory)
        try:
            # database_connect = sqlite3.connect(filename)
            return sqlite3.connect(sql_file)
        except Exception as e:
            print(e)
            print("Could not connect to database.\n")

    def store_file_in_database(self, sql_file):
        store_file_command = self._create_store_file_command()
        database = self.connect_to_database_file(sql_file)
        database.execute(store_file_command)
        database.commit()

    def _create_store_file_command(self):
        sql_file_name = str(self.file_name)
        sql_file_extension = str(self.extension)
        sql_full_filename = str(self.file_name) + "." + str(self.extension)
        sql_file_string = str(self.file_string, "utf-8")
        sql_database_file_dir = str(self.database_file_directory)
        store_file_command = 'INSERT or REPLACE INTO SAFE (FILE_NAME, DIRECTORY, NAME, EXTENSION, FILES)' \
                             ' VALUES (%s, %s, %s, %s, %s);' % ('"' + sql_full_filename + '"',
                                                                '"' + sql_database_file_dir + '"',
                                                                '"' + sql_file_name + '"',
                                                                '"' + sql_file_extension + '"',
                                                                '"' + sql_file_string + '"')
        return store_file_command

    def recover_directory(self, recover_directory, sql_file):
        database = sqlite3.connect(sql_file)
        cursor = database.execute("SELECT * from SAFE WHERE DIRECTORY=" + '"' + recover_directory + '"')
        recovered_files = self._database_file_recovery(cursor)
        for file in recovered_files:
            self.recover_file(file, sql_file)

    @staticmethod
    def _database_file_recovery(cursor):
        recovered_files = []
        for row in cursor:
            recovered_files.append(row[1] + "\\" + row[0])
        return recovered_files

    def recover_file(self, recover_file, sql_file):
        self._collect_binary_data(recover_file, sql_file)
        self._process_file_type(recover_file, mode="decode")

    def _collect_binary_data(self, recover_file, sql_file):
        database = DataBase.connect_to_database_file(sql_file)
        filename = recover_file.split('\\')[-1]
        cursor = database.execute("SELECT * from SAFE WHERE FILE_NAME=" + '"' + filename + '"')
        self.file_string = ''
        for row in cursor:
            self.file_string += row[4]

    @staticmethod
    def delete_all_recovered_files(delete_all_recovered_confirmation, sql_file):
        if delete_all_recovered_confirmation.lower().startswith("y"):
            protected_files = ["safe.py", sql_file, "DataBase_Shell.py", "safe_refactored.py"]
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name not in protected_files:
                        os.remove(os.path.join(root, name))

    def delete_one_database_file(self, delete_file, sql_file):
        database = self.connect_to_database_file(sql_file)
        cursor = database.cursor()
        delete_file_command = "DELETE FROM SAFE WHERE FILE_NAME = " + '"' + delete_file + '"'
        cursor.execute(delete_file_command)
        database.commit()
        print('\n\n...\n\n')
        self.list_stored_directories(sql_file)

    def delete_all_database_files(self, delete_all_database_files_confirmation, sql_file):
        if delete_all_database_files_confirmation.lower() == "y":
            database = self.connect_to_database_file(sql_file)
            cursor = database.cursor()
            delete_all_files_command = "DELETE FROM SAFE"
            cursor.execute(delete_all_files_command)
            database.commit()
            print('\n\n...\n\n')
            self.list_stored_directories(sql_file)

    def list_stored_directories(self, sql_file):
        self.initialize_database_file(sql_file)

    def store_file(self, filename_with_extension, file_directory=None, sql_file=None):
        if file_directory is not None:
            os.chdir(file_directory)
        if os.path.exists(filename_with_extension):
            print("File {} found!\nNow storing in {}...\n".format(filename_with_extension, sql_file))
            self._process_file_type(filename_with_extension, mode="encode")
            self.store_file_in_database(sql_file)
        else:
            print("File {} not found!\n".format(filename_with_extension))

    def store_directory(self, store_directory_file_path, sql_file):
        protected_files = ["safe.py", sql_file, "DataBase_Shell.py", "safe_refactored.py"]
        for root, dirs, files in os.walk(store_directory_file_path):
            for name in files:
                if name not in protected_files:
                    self.store_file(name, sql_file=sql_file)
