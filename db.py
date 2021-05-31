# importing module 
import sqlite3 
  
# connecting to the database  
connection = sqlite3.connect("students.db") 
  
# cursor  
crsr = connection.cursor() 
  
# SQL command to create a table in the database 
sql_command = """CREATE TABLE students (  
Roll_No INTEGER PRIMARY KEY,  
Sname VARCHAR(20),  
Class VARCHAR(30),  
Marks INTEGER);"""
  
# execute the statement 
crsr.execute(sql_command) 
  
# SQL command to insert the data in the table 
sql_command = """INSERT INTO students VALUES (1, "Payal", "10th", 100);"""
crsr.execute(sql_command) 
  
# another SQL command to insert the data in the table 
sql_command = """INSERT INTO students VALUES (2, "Devanshu", "9th", 98);"""
crsr.execute(sql_command)

# another SQL command to insert the data in the table 
sql_command = """INSERT INTO students VALUES (3, "Jagriti", "8th", 95);"""
crsr.execute(sql_command)

# another SQL command to insert the data in the table 
sql_command = """INSERT INTO students VALUES (4, "Ansh", "5th", 90);"""
crsr.execute(sql_command)

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
connection.commit() 
  
# close the connection 
connection.close() 
