import numpy as np
import pandas as pd
import mysql.connector
import traceback,json

def isfound(data):
    mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="password",
		database="Rasadatabases"
		)

# set up the cursor to execute the query
    cursor = mydb.cursor()
    cursor.execute("SHOW TABLES;")
    rows = cursor.fetchall()
    for row in rows:
        chk = True
        cursor.execute('DESC ' + row[0])
        table_cols = cursor.fetchall()
        o_cols = []
        for entry in table_cols:
            o_cols.append(entry[0])
        print(o_cols)
        for col in data.columns:
            if col.lower() not in o_cols:
                chk = False
                break
        if chk == False:
            continue
        else:
            return row[0]
        
    return "what"

def loadtheModule(filename):
    
    data = pd.read_csv(filename)
#     data = data.drop(['Unnamed: 0'], axis = 1)
#     data = data[ : 10]
    table = isfound(data)
    
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database="Rasadatabases"
                )
    cursor = mydb.cursor()
    #data = data.drop(['Unnamed: 0'], axis = 1)
    if(table == "what"):
        table = filename.split('.')[0]
        create = "CREATE TABLE " + table + "("
        cnt = 0
        for cols in data.columns:
            create += (cols.lower())
            if(data[cols].dtype == 'int64'):
                create += ' int'
            elif 'date' in cols.lower():
                create += ' date'
            else:
                create += ' varchar(30)'
    
            if cnt < len(data.columns)-1 :
                create += ','
            cnt = cnt + 1
    
        create += ');'
        
        cursor.execute(create)
        mydb.commit()
    
    query = []
    ins = "INSERT INTO " + table + " VALUES("
    for ix in range(len(data)):
        #print(data['Account_ID'][ix])
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
    
    

# set up the cursor to execute the query
    
    for q in query:
        cursor.execute(q)
        mydb.commit()
    

def loadJson(filename):
    # dataxy = pd.read_json(filename, typ='series')
    dataxy = pd.DataFrame(json.load(open(filename, 'r')))
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database="Rasadatabases"
                )
    cursor = mydb.cursor()
    
   
    
    table = filename.split('.')[0]
    create = "CREATE TABLE " + table + "("
    cnt = 0
    for cols in dataxy.columns:
        create += (cols.replace(' ', '_').lower())
        if(dataxy[cols].dtype == 'int64'):
            create += ' int'
        else:
            create += ' varchar(300)'
    
        if cnt < len(dataxy.columns)-1 :
            create += ','
        cnt = cnt + 1
    
    create += ');'
        
    cursor.execute(create)
    mydb.commit()
    
    
    query = []
    ins = "INSERT INTO " + table + " VALUES("
    # for ix in range(len(dataxy)):
    #     #print(data['Account_ID'][ix])
    #     res = ins
    #     cnt = 0
    #     for iy in range(len(dataxy)):
    #         if ix == iy:
    #             res += str("\"" + dataxy[ix] + "\"")
    #         else:
    #             res += "NULL"
        
    #         if cnt < len(dataxy) -  1: 
    #             res += ','
    #         cnt = cnt + 1
    #     res += ");"
    #     query.append(res)
    
    for ix in range(len(dataxy)):
        res = ins
        cnt = 0
        for cols in dataxy.columns:
            if dataxy[cols].dtype == 'object':
                res += str("\"" + dataxy[cols][ix] + "\"")
            else:
                res += str(dataxy[cols][ix])
        
            if cnt < len(dataxy.columns) -  1: 
                res += ','
            cnt = cnt + 1    
        res += ");"
        query.append(res)

# set up the cursor to execute the query
    
    for q in query:
        cursor.execute(q)
        mydb.commit()
    

def loadExcel(filename):
    dataex = pd.read_excel(filename)
    dataex.to_csv(filename.split('.')[0], index = False)
    loadtheModule(filename.split('.')[0] + '.csv')


def loadData(data_name):
    if data_name.endswith('.csv'):
        loadtheModule(data_name)
    elif data_name.endswith('.xlx') or data_name.endswith('.xlsx'):
        loadExcel(data_name)
    elif data_name.endswith('.json'):
        loadJson(data_name)

if __name__=='__main__':
    loadData('dataset.csv')
