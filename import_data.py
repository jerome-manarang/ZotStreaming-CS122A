import os
import csv
import mysql.connector
from db_connection import connect_db  # Import the database connection function

###
# FUNCTION REQUIREMENT NUMBER ONE: IMPORT DATA
###

#this deletes existing tables, will be used when we import to create new table2
def reset_database():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    if not tables:
        return False
    else:
        for (table_name,) in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    db.commit()
    cursor.close()
    db.close()

#imports and creates tables based on csv files
def import_data(folder_name):
    #convert folder_name to absolute path ( both relative & absolute paths)
    folder_path = os.path.abspath(folder_name)

    if not os.path.isdir(folder_path):
        return False

    db = connect_db()
    cursor = db.cursor()


    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            table_name = filename.replace(".csv", "")
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r") as file:
                reader = csv.reader(file)
                headers = next(reader)  #read column names

                #define columns dynamically
                column_definitions = ", ".join([f"{col} TEXT" for col in headers])

                #create table dynamically
                create_table_sql = f"CREATE TABLE {table_name} ({column_definitions})"
                cursor.execute(create_table_sql)

                #insert data
                columns = ", ".join(headers)
                placeholders = ", ".join(["%s"] * len(headers))
                insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                for row in reader:
                    cursor.execute(insert_sql, row)

    db.commit()
    cursor.close()
    db.close()
    return True