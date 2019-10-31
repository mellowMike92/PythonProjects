import os
import uu
import sqlite3
import base64
import cv2
import getpass

def encodeFiles(PATH):
    FILE_TYPES = {
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

    file_name = PATH.split("\\")
    file_name = file_name[len(file_name) - 1]
    file_string = ""

    NAME = file_name.split(".")[0]
    EXTENSION = file_name.split(".")[1]

    try:
        EXTENSION = FILE_TYPES[EXTENSION]
    except:
        Exception()
    if EXTENSION == "IMAGE":
        IMAGE = cv2.imread(PATH)
        file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode().encode("utf-8")

    elif EXTENSION == "TEXT":
        file_string = open(PATH, "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))

    elif EXTENSION == "VIDEO":
        uu.encode(PATH, PATH.split(".")[0] + ".txt")
        file_string = open(PATH.split(".")[0] + ".txt", "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))
        os.remove(PATH.split(".")[0] + ".txt")

    elif EXTENSION == "AUDIO":
        uu.encode(PATH, PATH.split(".")[0] + ".txt")
        file_string = open(PATH.split(".")[0] + ".txt", "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))
        os.remove(PATH.split(".")[0] + ".txt")


    EXTENSION = file_name.split(".")[1]

    db_directory = "\\".join(PATH.rsplit('\\')[:-1])

    command = 'INSERT or REPLACE INTO SAFE (FULL_NAME, DIRECTORY, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s, %s);' % (
        '"' + file_name + '"', '"' + db_directory + '"', '"' + NAME + '"', '"' + EXTENSION + '"', '"' + str(file_string, "utf-8") + '"')

    conn.execute(command)
    conn.commit()

PASSWORD = "123"

connect = getpass.getpass(prompt="Enter Password\n")

while connect != PASSWORD:
    connect = getpass.getpass(prompt="What is your password?\n")
    if connect == "q":
        break

if connect == PASSWORD:
    conn = sqlite3.connect('mySafe.db')
    try:
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            DIRECTORY TEXT NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print("\n" + "*" * 15)
        print("Commands:")
        print("rf = Recover File")
        print("rd = Recover Directory")
        print("sf = Store File")
        print("sd = Store Directory")
        print("d = Delete recovered files")
        print("ls = LiSt stored Directories ")
        print("q = Quit program")
        print("*" * 15)
        input_ = input(":")

        if input_.lower().startswith("q"):
            break
        if input_.lower() == "rf":
            file_type = input("File type? (e.g. txt, jpg, mp3, mp4, py)\n")
            file_name = input("File name?\n")
            FILE_ = file_name + "." + file_type

            cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            file_string = ""
            for row in cursor:
                file_string += row[4]

            if file_type == "mp4" or file_type == "mp3":
                with open(file_name+".txt", 'wb') as f_output:
                    f_output.write(base64.b64decode(file_string))
                uu.decode(file_name+".txt", FILE_)
                os.remove(file_name+".txt")
            else:
                with open(FILE_, 'wb') as f_output:
                    f_output.write(base64.b64decode(file_string))


        if input_.lower() == "rd":
            directory = input("Please enter directory path containing previously stored files.\n")
            cursor = conn.execute("SELECT * from SAFE WHERE DIRECTORY=" + '"' + directory + '"')
            recovered_files = []
            for row in cursor:
                recovered_files.append(row[1] + "\\" + row[0])
            for file in recovered_files:
                FILE_ = file.split('\\')[-1]
                file_type = FILE_.split(".")[-1]
                file_name = FILE_.split(".")[0]
                cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')
                file_string = ""
                for row in cursor:
                    file_string += row[4]
                if file_type == "mp4" or file_type == "mp3":
                    with open(file_name+".txt", 'wb') as f_output:
                        f_output.write(base64.b64decode(file_string))
                    uu.decode(file_name+".txt", FILE_)
                    os.remove(file_name+".txt")
                else:
                    with open(FILE_, 'wb') as f_output:
                        f_output.write(base64.b64decode(file_string))

        if input_.lower() == "sd":
                # store file
            PATH = input(
                "Type in the path to the directory you want to store.\nExample: \\Users\\userName\\Desktop\\myFolder\n")
            for root, dirs, files in os.walk(PATH):
                for name in files:
                    PATH = os.path.join(root, name)
                    encodeFiles(PATH)
                # encodeFiles(i)

        if input_.lower() == "sf":
            # store file
            PATH = input(
                "Type in the full path to the file you want to store.\nExample: \\Users\\userName\\Desktop\\myFile.py\n")
            encodeFiles(PATH)

        if input_ == "d":
            # store file
            delete = input(
                "\nDelete files from Recovery Directory? (Y/N)\n"
                "(Files will not be deleted from Data Base)\n\n")
            if delete.lower().startswith("y"):
                programFiles = ["safe.py", "mySafe.db"]
                for root, dirs, files in os.walk(os.getcwd()):
                    for name in files:
                        if name not in programFiles:
                            os.remove(os.path.join(root, name))

        if input_ == "ls":
            def sql_fetch(con):

                cursorObj = con.cursor()

                cursorObj.execute('SELECT * FROM SAFE')

                rows = cursorObj.fetchall()

                for row in rows:
                    print(row[1]+'\\'+row[0])


            sql_fetch(conn)
