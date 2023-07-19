import mysql.connector

#establishing the connection
conn = mysql.connector.connect(
   user='root', password='', host='127.0.0.1', database='facerecognition')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing SQL query to INSERT a record into the database.
insert_stmt = (
   "INSERT INTO students(ID, NAME,Time)"
   "VALUES (%s, %s, %s)"
)
data = (2, 'Ramapriya', '10:30')

try:
   # Executing the SQL command
   cursor.execute(insert_stmt, data)
   
   # Commit your changes in the database
   conn.commit()

except:
   # Rolling back in case of error
   conn.rollback()

print("Data inserted")

# Closing the connection
conn.close()
'''CREATE TABLE CUSTOMERS(
   ID   INT              NOT NULL,
   NAME VARCHAR (20)     NOT NULL,
   AGE  INT              NOT NULL,
   ADDRESS  CHAR (25) ,
   SALARY   DECIMAL (18, 2),       
   PRIMARY KEY (ID)
);'''
