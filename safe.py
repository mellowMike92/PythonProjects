import os
import uu
import sqlite3
import base64
import cv2
import getpass

"""
This script will run in the terminal/shell and works in an interactive manner (input & output)
The 'encodeFiles' function below is used to gather directory & file information, input commands, and
store or recover files/folders in/from a created database by encoding files into binary format.
"""


def encodeFiles(PATH, conn):
    # Creating dictionary/hash table to relate file types with file extensions
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

    # Splitting off the file name from the directory name
    file_name = PATH.split("\\")
    file_name = file_name[len(file_name) - 1]

    # Creating an empty string to place binary information in
    file_string = ""

    NAME = file_name.split(".")[0]
    EXTENSION = file_name.split(".")[1]

    try:
        EXTENSION = FILE_TYPES[EXTENSION]
    except:
        Exception()

    # The below conditional statements are comparing the associated file extension that was input from the user
    # with the file type from the hash table/dictionary above to determine which block of logic to execute.

    if EXTENSION == "IMAGE":
        # Using Python library cv2 to encode image information into binary format with base64, a separate Python library.
        IMAGE = cv2.imread(PATH)
        file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode().encode("utf-8")

    elif EXTENSION == "TEXT":
        # Reading the file into memory as a string, then encoding the string into binary with utf-8 formatting.
        file_string = open(PATH, "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))

    elif EXTENSION == "VIDEO":
        # Using Python library uu to encode video files into utf-8 binary.
        uu.encode(PATH, PATH.split(".")[0] + ".txt")
        file_string = open(PATH.split(".")[0] + ".txt", "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))
        os.remove(PATH.split(".")[0] + ".txt")

    elif EXTENSION == "AUDIO":
        # Using Python library uu to encode audio files into utf-8 binary.
        uu.encode(PATH, PATH.split(".")[0] + ".txt")
        file_string = open(PATH.split(".")[0] + ".txt", "r").read()
        file_string = base64.b64encode(file_string.encode("utf-8"))
        os.remove(PATH.split(".")[0] + ".txt")

    EXTENSION = file_name.split(".")[1]

    # Storing the input directory into the database in case the user would like to associate the file to the directory
    db_directory = "\\".join(PATH.rsplit('\\')[:-1])

    # Creates SQL Command to store relevant data in database.

    command = 'INSERT or REPLACE INTO SAFE (FILE_NAME, DIRECTORY, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s, %s);' % (
        '"' + file_name + '"', '"' + db_directory + '"', '"' + NAME + '"', '"' + EXTENSION + '"',
        '"' + str(file_string, "utf-8") + '"')

    # Executes & Commits the SQL Command into the conn argument (passed in as a sqlite3 object)
    conn.execute(command)
    conn.commit()


# Create a secure password that you would like to set before compiling
PASSWORD = "password"

# Creating a name/variable defined as a password entry (without echoing the input)
connect = getpass.getpass(prompt="Please enter your password:\n")

# As long as each password entry is incorrect, the loop below will keep running
while connect != PASSWORD:
    # GetPass is a python library that does not echo the input from keystrokes into the terminal
    connect = getpass.getpass(prompt="Incorrect password.  Please try again:\n")

    # Quits the program if the user inputs the 'q' keystroke
    if connect == "q":
        break

# If the password is correct, a connection is established to a file named mySafe.db
if connect == PASSWORD:
    conn = sqlite3.connect('mySafe.db')
    # If mySafe.db does not exist, the try/except loop below will create it.
    try:
        conn.execute('''CREATE TABLE SAFE
            (FILE_NAME TEXT PRIMARY KEY NOT NULL,
            DIRECTORY TEXT NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("Database created.  What would you like to do?")
    except:
        print("Database found.  What would you like to do?")

    # Defining a list of commands that can be used in the terminal
    while True:
        print("\n" + "*" * 15)
        print("Commands:")
        print("rf = Recover File")
        print("rd = Recover Directory")
        print("sf = Store File")
        print("sd = Store Directory")
        print("dr = Delete all Recovered files")
        print("df = Delete data base File")
        print("da = Delete All data base files")
        print("ls = LiSt stored Directories ")
        print("q = Quit program")
        print("*" * 15)
        input_ = input(":")

        # If the user accidentally had caps lock on, the .lower() method will force the input into lowercase.
        # This is used to make an appropriate conditional assessment
        if input_.lower().startswith("q"):
            # Exits the program if 'q' is pressed on the keyboard.
            break
        if input_.lower() == "rf":
            # If the 'rf' command is placed, the block below will recover a single file based on the input
            # given by the user.
            # This is set in the file_type and file_name inputs.

            file_type = input("File type? (e.g. txt, jpg, mp3, mp4, py)\n")
            file_name = input("File name?\n")
            FILE_ = file_name + "." + file_type

            # Creates a SQL command to select the file that was requested by the user.
            cursor = conn.execute("SELECT * from SAFE WHERE FILE_NAME=" + '"' + FILE_ + '"')

            # Loops through the cursor object defined above
            # Appends the string found in the 4th column (file information in bytes) into the file_string container

            file_string = ""
            for row in cursor:
                file_string += row[4]

            # Performs check to decide whether or not to decode a bytes text file into a video or audio file.
            if file_type == "mp4" or file_type == "mp3":
                with open(file_name + ".txt", 'wb') as f_output:
                    f_output.write(base64.b64decode(file_string)) 
                # Decodes the requested audio or video file as the text file in which the byte information 
                # was initially stored using the 'uu' Python library.
                uu.decode(file_name + ".txt", FILE_)
                os.remove(file_name + ".txt")
            else:
                # Creates a file in the current working directory
                # and writes the decoded string information from the file_string container defined above.
                with open(FILE_, 'wb') as f_output:
                    f_output.write(base64.b64decode(file_string))

        if input_.lower() == "rd":
            # Recovers a directory by checking the database for the input placed by the user.
            directory = input("Please enter directory path containing previously stored files.\n")
            cursor = conn.execute("SELECT * from SAFE WHERE DIRECTORY=" + '"' + directory + '"')
            
            recovered_files = []
            
            # Appends files found in the database with the directory path that was intially stored.
            for row in cursor:
                # row[1] is the directory and row[0] is the file name.
                # The position of the elements in the cursor object were defined in the 'command' sqlite3 object 
                # which was executed in the encodeFiles function.
                
                recovered_files.append(row[1] + "\\" + row[0])
                
            for file in recovered_files:
                # Goes through each file stored in the recovered_files list to decode one-by-one.
                
                # Manipulates the files for easier management
                FILE_ = file.split('\\')[-1]
                file_type = FILE_.split(".")[-1]
                file_name = FILE_.split(".")[0]
                
                # Creates the sqlite3 cursor object which is used to recover the byte information from the 4th index of its array.
                cursor = conn.execute("SELECT * from SAFE WHERE FILE_NAME=" + '"' + FILE_ + '"')
                file_string = ""
                for row in cursor:
                    file_string += row[4]
                    
                
                if file_type == "mp4" or file_type == "mp3":
                with open(file_name + ".txt", 'wb') as f_output:
                    f_output.write(base64.b64decode(file_string))                         
                    # Decodes the requested audio or video file as the text file in which the byte information 
                    # was initially stored using the 'uu' Python library.
                    uu.decode(file_name + ".txt", FILE_)
                    os.remove(file_name + ".txt")
                else:
                     # Creates a file in the current working directory
                     # and writes the decoded string information from the file_string container defined above.
                    with open(FILE_, 'wb') as f_output:
                        f_output.write(base64.b64decode(file_string))
                        
                        
                # Since this if/else check is repeated in the 'rf' conditional block above, a function can be created for
                # ease of readability.

        if input_.lower() == "sd":
            # Stores all the files found within the directory input into the database.
            PATH = input(
                "Type in the path to the directory you want to store.\nExample: \\Users\\userName\\Desktop\\myFolder\n")
            
            for root, dirs, files in os.walk(PATH):
                for name in files:
                    # Walks through the directory that was input and creates a PATH name using the directory and file(s)
                    PATH = os.path.join(root, name)
                    
                    # Runs the encodeFiles function for each file found in the directory.
                    encodeFiles(PATH, conn)
                    

        if input_.lower() == "sf":
            # Stores a single file in the database.
            PATH = input(
                "Type in the full path to the file you want to store.\nExample: \\Users\\userName\\Desktop\\myFile.py\n")
            
            # Runs the encodeFiles function for the single file that was input in the terminal.
            encodeFiles(PATH, conn)

        if input_ == "dr":
            # Deletes all the recovered files from the current working directory in which this script is executed from.
            delete = input(
                "\nDelete all files from Recovery Directory? (Y/N)\n"
                "(Files will not be deleted from Data Base)\n\n")
            
            if delete.lower().startswith("y"): # In case caps-lock was on
                programFiles = ["safe.py", "mySafe.db"] # Ensures the main files (script and database) are not deleted.
                for root, dirs, files in os.walk(os.getcwd()):
                    for name in files:
                        if name not in programFiles:
                            # Deletes all files in the directory using the os.remove method.
                            os.remove(os.path.join(root, name))
        
        if input_ == "df":
            # Deletes a single file from the database
            PATH = input(
                "Type in the file name including the extension of the file you want to delete from the database."
                "Note: Case-sensitive"
                "\nExample: My_File.txt\n")
            
            PATH = str(PATH)
            cursor = conn.cursor()
            
            # Just showing another way in which you can execute a sqlite3 command
            deleteFile = "DELETE FROM SAFE WHERE FILE_NAME = " + '"' + PATH + '"'
            cursor.execute(deleteFile)
            
            conn.commit()

        if input_ == "da":
            # Deletes all files from the database
            PATH = input("Are you sure you would like to delete all stored files from the database? (Y/N)\n") 
            if PATH.lower() == "y": # Perform double-check to confirm deletion of all files.
                cursor = conn.cursor()
                
                # sqlite3 string command to delete all files from database
                deleteFile = "DELETE FROM SAFE"
                cursor.execute(deleteFile)
                conn.commit()

        if input_ == "ls":
            # Shows all files/directories currently stored in database.
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SAFE')
            
            rows = cursor.fetchall() # fetchall is a built-in method that retrieves all tables within the cursor object.
            
            for row in rows:
                print(row[1] + '\\' + row[0]) # Prints directory+filename

