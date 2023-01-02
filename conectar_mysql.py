#----------------------------------------------------------------------------
# Created By  : Trevisolli
# Created Date: 16/12/2022
# version     : '1.0'
# ---------------------------------------------------------------------------
""" Read records from a MySQL database and write the result in a text file, 
    using the Python language. 
"""
# ---------------------------------------------------------------------------
# Imports 
# ---------------------------------------------------------------------------
import boto3
import mysql.connector as mysql 
import os 
from pys3 import create_bucket, delete_bucket, generate_download_link, get_vars, list_objects
from pys3 import prevent_public_access, print_objects_list, upload_file
from pys3 import DIR, F1, PRI_BUCKET_NAME

column_separator = ";"

def load_db_properties():
    """
    Read MySQL database connection settings
    """
    try:
        d = dict()
        file_name = "db.properties"
        file = open(file_name, "r", encoding="utf8")
        for line in file:
            # Remove Newline character
            prop = line.replace("\n", "")
            prop = prop.split("=")
            d[prop[0]] = prop[1]
        file.close()
        return d
    except mysql.Error as err:
        print(f"Error reading properties from {file_name} file. Error: {err}.")
        exit(1)

def write_file(employees_list):
    """
    Write records to a file
    """
    try:
        if len(employees_list) != 0:
            header = ""
            i = 0 
            file_name = "employees_list.txt"
            if not os.path.exists(file_name):
                header = "Id"+ column_separator + \
                        "First Name" + column_separator + \
                        "Last Name "
            file = open(file_name, "a")
            # Header 
            if header != None:
                file.write(header)
            for l in employees_list:
                file.write("\n"+l)
                emp_id = employees_list[i].split(";")
                print("emp added: " + str(emp_id[0]))
                update_record(emp_id[0])
                i += 1 
            print(f"The file {file_name} was successfully written/updated.")    
            file.close()
        else:
            print("There is no record to be updated in the file.")
    except mysql.Error as err:
        print(f"Writting file error. Error: {err}.")
        exit(1)

def open_db_cur():
    """    
    Opens connection and cursor in database
    """
    try:
        prop = load_db_properties() 
        db = mysql.connect(host=prop["host"], user=prop["user"], password=prop["password"], database=prop["database"])    
        cur = db.cursor(prepared=True)
        return db, cur
    except mysql.Error as err:
        print(f"Could not connect to MySQL. Error: {err}.\nVerify your [db.properties] file.")
        exit(1)


def close_db_cur(db, cur):
    """
    Closes the connection and the cursor in the database
    """
    try:
        cur.close()
        db.close()
    except mysql.Err as err:
        print(f"Could not close the connection to MySQL. Error: {err}.")
        exit(1)

def update_record(employee_id):
    """
    Marks the record as sent after it is written to the file.
    """
    try:
        db, cur = open_db_cur()
        cmd = "update employees set exported = 'S' where id = ? "
        cur.execute(cmd, (employee_id,))
        db.commit()
        close_db_cur(db, cur)
    except Exception as err:
        if db.isopen():
            close_db_cur(db, cur)
        print(f"Error when trying to update record [{employee_id}]. Error: {err}.")
        exit(1)


def db_version():
    """
    Displays the DB Version
    """
    try:
        separator = '-'*100
        db, cur = open_db_cur()    
        cur.execute("select version()")
        # return the first element of the tuple 
        version = cur.fetchone()[0]
        print(separator)
        # DB Version 
        print(f"MySQL Version: {version}")
        print(separator)
        close_db_cur(db, cur)
    except Exception as err:
        print(f"Error when trying to display Database Version. Error: {err}.")
        exit(1)

  
def list_employees(employee_id=None):
    """
    Returns the list of employees, registered in the employees table, 
    in the MySQL database
    """
    try:
        return_list = list()
        separator = '-'*100
        cur_count = 0
        SQL = "select id, first_name, last_name, birth_date from employees where exported = 'N' "
    
        if employee_id != None:
            SQL = SQL + " and id = ? "    

        prop = load_db_properties()

        db, cur = open_db_cur()
        cur = db.cursor(prepared=True)
        if employee_id != None:
            cur.execute(SQL,
                        (employee_id,))
        else:
            cur.execute(SQL)
    
        row = cur.fetchone()

        employees_dict = dict()

        while row:        
            employees_dict[row[0]] = [row[1], row[2]]
            row = cur.fetchone()
    
        cur_count = cur.rowcount 

        if cur_count != 0:
            for i in employees_dict:
                return_list.append( str(i) + column_separator + \
                                    employees_dict[i][0] + column_separator + \
                                    employees_dict[i][1] )
        
        close_db_cur(db, cur)

        return return_list

    except Exception as err:
        print(f"Error when trying to display Employees list. Error: {err}.")
        exit(1)

# ---------------------------------------------------------------------------
# Execution  
# ---------------------------------------------------------------------------     
if __name__ == "__main__":
   db_version()   
   l = list_employees()
   write_file(l)
   """aws entry point"""
   access, secret = get_vars()
   s3 = boto3.resource('s3', aws_access_key_id=access, aws_secret_access_key=secret)
   create_bucket(PRI_BUCKET_NAME, s3, True)
   list_obj = list_objects(PRI_BUCKET_NAME, s3)
   if F1 not in list_obj:
       upload_file(PRI_BUCKET_NAME, DIR, F1, s3 )   
   print_objects_list(PRI_BUCKET_NAME, list_obj) 