from DataBase_Tools import *
import random
import getpass


class Main(DataBase):

    def __init__(self):
        super().__init__(sql_file=None, directory=None)
        self.database_password = ''
        self._create_or_connect_database()

    def ui_task_exec(self, sql):
        while True:
            task = input("\nWhat would you like to do?\n").lower()
            try:

                if task == "rf":
                    recover_file = input("Please enter the full file name to recover.  "
                                         "Include the file extension (e.g. myPhoto.jpg)\n")
                    sql.recover_file(recover_file, self.sql_file)

                if task == "rd":
                    recover_directory = input("Please enter the full folder directory to recover.\n")
                    sql.recover_directory(recover_directory, self.sql_file)

                if task == "sf":
                    filename_with_extension = input("Please enter the file name (including "
                                                    "the extension) to store.\n\tFile must be in "
                                                    "same location as database file.\n")
                    sql.store_file(filename_with_extension,
                                   file_directory=self.database_file_directory, sql_file=self.sql_file)

                if task == "sd":
                    store_directory_file_path = input("Please enter the folder directory containing "
                                                      "the files to store.\n")
                    sql.store_directory(store_directory_file_path, sql_file=self.sql_file)

                if task == "dr":
                    delete_all_recovered_confirmation = input(
                        "\nDelete all files from Recovery Directory? (Y/N)\n"
                        "(Files will not be deleted from Data Base)\n\n")
                    sql.delete_all_recovered_files(delete_all_recovered_confirmation, self.sql_file)

                if task == "df":
                    delete_file = input("Type in the file name including the extension of the file "
                                        "you want to delete from the database.  Note: Case-sensitive"
                                        "\nExample: My_File.txt\n")
                    sql.delete_one_database_file(delete_file, self.sql_file)

                if task == "da":
                    delete_all_database_files_confirmation = input("Are you sure you would like to delete all "
                                                                   "stored files from the database? (Y/N)\n")

                    sql.delete_all_database_files(delete_all_database_files_confirmation, self.sql_file)

                if task == "ls":
                    sql.list_stored_directories(self.sql_file)

                if task == "help":
                    Main._print_menu()

                if task == "cwd":
                    print(os.getcwd())
                    print(self.database_file_directory)

                if task == "cd":
                    self._create_or_connect_database()

                if task.startswith("q"):
                    break

                else:
                    continue

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    def create_password_prompt(self):
        create_random_pw_check = input("Would you like to create a new random password?\t(Y\\N)\n")
        self.password_creation(create_random_pw_check)
        print("\nDatabase file created in {}".format(self.database_file_directory))

    def _create_or_connect_database(self):
        self.database_file_directory = input('\nEnter a directory to connect to an existing database file,'
                                             'or enter a directory to create a new database file.\n'
                                             'Type "c" for current directory.\n')
        self.sql_file = input("\nEnter an existing database filename to connect to "
                              "or a new database filename to create.\n")
        if self.database_file_directory == "c":
            self.database_file_directory = os.getcwd()
        else:
            self.database_file_directory = self.database_file_directory

        if not self.sql_file.endswith('.db'):
            self.sql_file = self.sql_file + '.db'

        if os.path.exists(self.database_file_directory+"\\"+self.sql_file):
            print("\nDatabase found!\nConnecting to {} in {}\n".format(self.sql_file, self.database_file_directory))
            sql = DataBase()
            sql.connect_create_database_file(sql_file=self.sql_file, directory=self.database_file_directory)
            self.database_password = sql.check_db_password(self.sql_file)
            if self.check_password() is True:
                print("Password verified!\n")
                self._print_menu()
                self.ui_task_exec(sql)

        else:
            print("\nCreating new database {} in {}".format(self.sql_file, self.database_file_directory))
            sql = DataBase()
            sql.connect_create_database_file(sql_file=self.sql_file, directory=self.database_file_directory)
            self.create_password_prompt()
            self._print_menu()
            self.ui_task_exec(sql)
            password = self.database_password



    @staticmethod
    def _print_menu():
        print("\n" + "*" * 15)
        print("Commands:")
        print("cd = Create new Database / Connect to other DataBase")
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

    def create_random_password(self, password_length):
        alphanum_selection = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        special_char_selection = "!@#$%^&*()?~=-><\"'[]{}:;"

        half_length = int(password_length)/2
        password_1 = "".join(random.sample(alphanum_selection, int(half_length)))
        password_2 = "".join(random.sample(special_char_selection, int(half_length)))
        password = "".join(random.sample(password_1 + password_2, int(password_length)))

        print("\nPassword created.\nSave this database password for next time!\n\n" + "*" * len(password) + "\n" +
              password + "\n" + "*" * len(password) + "\n")
        self.store_password_in_database(self.sql_file, password)

    def password_creation(self, input_value):
        create_random_pw_check = input_value
        if create_random_pw_check.lower() == "y":
            length = input("Specify password length and hit Enter (12 is recommended)\n").strip()
            while not length.isnumeric():
                length = input("Specify password length and hit Enter (12 is recommended)\n")
            self.create_random_password(int(length))

        elif create_random_pw_check.lower() == "n":
            create_specific_pw_check = input("Would you like to create your own password?\t(Y\\N)\n")
            if create_specific_pw_check.lower() == "y":
                specific_pw = input("Create your password and press Enter\n").strip()
                self.store_password_in_database(self.sql_file, specific_pw)
            elif create_specific_pw_check.lower() == "n":
                print("Password creation skipped.\nUsing default password: 123")
                self.store_password_in_database(self.sql_file, "123")

        self.database_password = self.check_db_password(self.sql_file)

    def check_password(self):
        connect = getpass.getpass(prompt="Please enter your password, or press q followed by Enter to quit:\n")
        while connect != self.database_password:
            connect = getpass.getpass(prompt="Please enter your password, or press q followed by Enter to quit:\n")
            if connect == 'q':
                break
        if connect == self.database_password:
            return True


if __name__ == '__main__':
    print("You are currently in this directory\t", os.getcwd())
    Main()
