This is a simple script that will create a database 
using Python's sqlite3 library and allow
the user to store files (txt, mp3, mp4, jpg, etc)
in the database - allowing the user to delete 
the stored files from the hard disk -
and recover the files from the database.

This script works by encoding the stored files 
(or folder) into a binary format, storing it into
a SQL table, and allows the recovery of the decoded 
files/folder from the database.