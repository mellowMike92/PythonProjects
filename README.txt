Original script from:
https://github.com/KalleHallden/PythonProjects/blob/master/Database/safe.py

Overview of project:

I modified the database script from Kalle Hallden's github by adding extended functionality.
I have also created a refactored, OOP version of the script that can be compiled into an
executable.
Working on adding docstrings and will hopefully have a GUI version afterwards...

What the script does:

The program will generate a database (using Python's sqlite3 library) and allow the user
to store files (txt, mp3, mp4, jpg, etc) that he/she can later delete from the hard disk 
and still recover from the database.

This script works by encoding the stored files (or folder) into a binary strings which are
stored into a SQL table.  The user is then able to recover the decoded files/folder from 
the database.
