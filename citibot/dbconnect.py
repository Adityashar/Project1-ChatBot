import traceback
import mysql.connector

def query_formation(entities, table:str, intent:str):

    query = "SELECT " + intent + " FROM " + table
    # if(intent == 'pending_payment'):
    #     query += " Pending Amount FROM " 
    # elif(intent == 'payment_status'):
    #     query += " Payment Status FROM "

    cnt = 0
    for dic in entities:
        if cnt == 0:
            query += " WHERE "
            cnt = cnt + 1
        else:
            query += " AND "


        query += dic['entity']
        query += " = "
        query += dic['value']

        # if(dic['entity'] == 'account_id'):
        #     query += "Account id = " 
        #     query += dic['value']

        # if(dic['entity'] == 'legal_entity'):
        #     query += "Legal Entity = " 
        #     query += dic['value']

        # if(dic['entity'] == 'client_name'):
        #     query += "Client Name = " 
        #     query += dic['value']

    return query

def getData(query:str):
        """
         @query: sql query that needs to be executed.
         returns the data being executed in "List" format
        """

        try:

            # Setup the connection.
            # Pass your database details here
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database=""
                )

            # set up the cursor to execute the query
            cursor = mydb.cursor()
            cursor.execute(query)

            # fetch all rows from the last executed statement using `fetchall method`.
            results = cursor.fetchall()
            return results
        except:
            print("Error occured while connecting to database or fetching data from database. Error Trace: {}".format(traceback.format_exc()))
            return []
