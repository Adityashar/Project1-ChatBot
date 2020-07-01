"""
Query Formation and retrieval script
"""

import traceback
import mysql.connector
import datetime

#systemctl status mysql.service
#sudo mysql -u root -ppassword
def query_formation(entities, val, features, table:str):
    """
    Query formation
    """
    query = "SELECT {} FROM {} WHERE".format(val,table)
    flag = False
    count = 0
    dates = []
    for e in entities:
        if e['entity'] == 'daterange':
            query += " (payment_date BETWEEN '{}' and '{}') and".format(e['value']['start_date'], e['value']['end_date'])
            flag = True
        if 'date' == e['entity'].lower() and e['extractor'] == 'MSRTExtractor':
            count += 1
            dates.append(e['value'])

    if flag == False and count == 1:
        query += " payment_date = '{}' and".format(dates[0])
    if flag == False and count == 2:
        query += " (payment_date BETWEEN '{}' and '{}') and".format(dates[0], dates[1])

    for e in entities:
        if query.find(e['entity']) == -1 and e['entity'] in features and ('date' not in e['entity'].lower()):
            if (e['entity'] == 'Account_ID' and len(e['value']) != 6):
                continue;       
            if e['extractor'] == 'CRFEntityExtractor' and len(e['value'].split()) > 3:
                continue
            query += " {} = '{}' and".format(e['entity'], e['value'])
    
    print(query)
    return query[:-3]

def query_formation_dy(entities, val:str, features):

    query = "SELECT {} FROM {} WHERE".format(val, table)
    for e in entities:
        # if e['extractor'] == 'CRFEntityExtractor':
        if query.find(e['entity']) == -1 and e['entity'] in features:      
            query += " {} = '{}' and".format(e['entity'], e['value'])
    print(query)
    return query[:-3]

def getData(query:str, table):
    """
    get data from database
    """
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="Rasadatabases"
            )
        cursor = mydb.cursor()
        cursor.execute(query)

        results = cursor.fetchall()
        final = []
        for result in results:
            li = []
            for tup in result:
                if isinstance(tup, datetime.date):
                    tup = "{:%Y-%m-%d}".format(tup)#tup.strftime('%Y-%m-%d')
                    li.append(tup)
                else:
                    li.append(tup)
            final.append(li)
        # print(final)
        # features = cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='Rasadatabases' AND `TABLE_NAME`={}".format(table)).fetchall()
        cursor.execute("show columns from {}".format(table))
        features = cursor.fetchall()
        return final, features
    except:
        print("Error occured while connecting to database or fetching data from database. Error Trace: {}".format(traceback.format_exc()))
        return []
