from safe_refactored import *
import random
import getpass


class Main(DataBase):

    database_password = '123'
    database_file_directory = ''
    sql_file = ''

    def __init__(self, sql_file=None, directory=None):
        super().__init__(sql_file=None, directory=None)
        sql = Main._create_new_database()
        create_random_pw_check = input("Would you like to create a new random password?\t(Y\\N)\n")
        self._password_creation(create_random_pw_check)
        print("Database file created in {}".format(Main.database_file_directory))
        if self.check_password() is True:
            print("Password verified!\n")
            self._print_menu()

            while True:
                task = input("\nWhat would you like to do?\n").lower()
                try:

                    if task == "rf":
                        recover_file = input("Please enter the full file name to recover.  "
                                             "Include the file extension (e.g. myPhoto.jpg)\n")
                        sql.recover_file(recover_file, Main.sql_file)

                    if task == "rd":
                        recover_directory = input("Please enter the full folder directory to recover.\n")
                        sql.recover_directory(recover_directory, Main.sql_file)

                    if task == "sf":
                        filename_with_extension = input("Please enter the file name (including "
                                                        "the extension) to store.\n")
                        sql.store_file(filename_with_extension, Main.database_file_directory)

                    if task == "sd":
                        store_directory_file_path = input("Please enter the folder directory containing "
                                                          "the files to store.\n")
                        sql.store_directory(store_directory_file_path, Main.sql_file)

                    if task == "dr":
                        delete_all_recovered_confirmation = input(
                            "\nDelete all files from Recovery Directory? (Y/N)\n"
                            "(Files will not be deleted from Data Base)\n\n")
                        sql.delete_all_recovered_files(delete_all_recovered_confirmation, Main.sql_file)

                    if task == 'df':
                        delete_file = input("Type in the file name including the extension of the file "
                                            "you want to delete from the database.  Note: Case-sensitive"
                                            "\nExample: My_File.txt\n")
                        sql.delete_one_database_file(delete_file)

                    if task == 'da':
                        delete_all_database_files_confirmation = input("Are you sure you would like to delete all "
                                                                       "stored files from the database? (Y/N)\n")

                        sql.delete_all_database_files(delete_all_database_files_confirmation)

                    if task == 'ls':
                        sql.list_stored_directories(Main.sql_file)

                    if task == 'help':
                        Main._print_menu()

                    if task == 'cwd':
                        print(os.getcwd())
                        print(Main.database_file_directory)

                    if task == "cd":
                        sql = Main._create_new_database()

                    if task.startswith('q'):
                        break
                except Exception as e:
                    pass

    @classmethod
    def _create_new_database(cls):
        cls.sql_file = input("Enter a database filename to create.\n")
        if not cls.sql_file.endswith('.db'):
            cls.sql_file += '.db'
        Main.database_file_directory = input('Enter a directory to create the file in.\n'
                                             'Type "c" for current directory.\n')
        if Main.database_file_directory == "c":
            Main.database_file_directory = os.getcwd()
        sql = DataBase(cls.sql_file, Main.database_file_directory)
        sql.create_database_file(cls.sql_file, Main.database_file_directory)
        return sql


        # directory = input("Please enter directory name (press c for current directory)\n")
        # sql_file = input("Please enter a database name\n").strip()
        # if directory.lower() == 'c':
        #     directory = None
        # my_created_database = DataBase(sql_file, directory=directory)
        # my_created_database.create_database_file(directory)
        # return my_created_database

    @staticmethod
    def _print_menu():
        print("\n" + "*" * 15)
        print("Commands:")
        print("cd = Create Database")
        print("rf = Recover File")
        print("rd = Recover Directory")
        print("sf = Store File")
        print("sd = Store Directory")
        print("dr = Delete all Recovered files")
        print("df = Delete one data base File")
        print("da = Delete All data base files")
        print("ls = LiSt stored Directories")
        print("cwd = Current Working Directory")
        print("q = Quit program")
        print('\n')
        print("help = Show all commands")
        print("*" * 15, "\n")

    @classmethod
    def create_random_password(cls, password_length):
        selection = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?~=-><\"'[]{}:;"
        password = "".join(random.sample(selection, password_length))
        print("Write down this password!"+"*"*12+"{}\n"+"*"*12+"\n".format(str(password)))
        cls.database_password = password

    @staticmethod
    def _password_creation(input_value):
        create_random_pw_check = input_value
        if create_random_pw_check.lower() == "y":
            length = input("Specify password length and hit Enter (12 is recommended)\n").strip()
            while not length.isnumeric():
                length = input("Specify password length and hit Enter (12 is recommended)\n").strip()
            Main.create_random_password(length)

        elif create_random_pw_check.lower() == "n":
            create_specific_pw_check = input("Would you like to create your own password?\t(Y\\N)\n")
            if create_specific_pw_check.lower() == "y":
                specific_pw = input("Create your password and press Enter\n").strip()
                Main.database_password = specific_pw
            elif create_specific_pw_check.lower() == "n":
                print("Password creation skipped.\n"
                      "Using default password of 123\n")

    @classmethod
    def check_password(cls):
        connect = getpass.getpass(prompt="Please enter your password, or press q followed by Enter to quit:\n")
        while connect != cls.database_password:
            connect = getpass.getpass(prompt="Please enter your password, or press q followed by Enter to quit:\n")
            if connect == 'q':
                break
        if connect == cls.database_password:
            return True


if __name__ == '__main__':
    print(os.getcwd())
    Main()
