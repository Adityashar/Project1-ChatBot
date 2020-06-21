import numpy as np
import pandas as pd
import mysql.connector
import traceback

def loadtheModule(filename, table):
    data = pd.read_csv(filename)
    #data = data.drop(['Unnamed: 0'], axis = 1)
    create = "CREATE TABLE " + table + "("
    cnt = 0
    for cols in data.columns:
        create += (cols.lower())
        if(data[cols].dtype == 'int64'):
            create += ' int'
        else:
            create += ' varchar(30)'
    
        if cnt < len(data.columns)-1 :
            create += ','
        cnt = cnt + 1
    
    create += ');'
    
    query = []
    ins = "INSERT INTO " + table + " VALUES("
    for ix in range(len(data)):
        print(data['Account_ID'][ix])
        res = ins
        cnt = 0
        for cols in data.columns:
            if data[cols].dtype == 'object':
                res += str("\"" + data[cols][ix] + "\"")
            else:
                res += str(data[cols][ix])
        
            if cnt < len(data.columns) -  1: 
                res += ','
            cnt = cnt + 1
        res += ");"
        query.append(res)
    
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="*Ritik22*",
                database="citi"
                )

# set up the cursor to execute the query
    cursor = mydb.cursor()
    cursor.execute(create)
    mydb.commit()
    for q in query:
        cursor.execute(q)
        mydb.commit()
    