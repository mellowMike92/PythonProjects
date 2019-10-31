This is a simple script that will create a database
(using Python's sqlite3 library) and allow the user
to store files (txt, mp3, mp4, jpg, etc) that he/she 
can later delete from the hard disk and recover from 
the database.

This script works by encoding the stored files 
(or folder) into a binary strings which are stored 
into a SQL table.  The user is then able to recover
the decoded files/folder from the database.
