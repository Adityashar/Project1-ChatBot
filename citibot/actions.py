# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from dbconnect import query_formation, getData
import pandas as pd
import sys, os, pickle


## database code 
            ##table = ""
            #intent = tracker.latest_message['intent']
            #query = query_formation(entities, table, intent)
            #lis = getData(query)

            #info = lis[0][0]

            #dispatcher.utter_message(text="Hi here are the details: {}".format(info))


#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# rasa data convert nlu --data ./data/nlu.md --out ./data/data.json --format json

# rasa run -m models --enable-api --cors "*" --debug
# ps -fA | grep python



FEATURES = ['Client_Name', 'Account_ID', 'Legal_Entity', 'Currency', 
            'Payment_Type', 'Paid_Amount', 'Payment_Date', 'Payment_Status', 
            'Pending_Amount','Comments', 'Source']

ENTITY_LIST = {'legal_entity':'Legal_Entity',
              'client_name':'Client_Name',
              'currency':'Currency',
              'payment_date':'Payment_Date',
              'amountpaid':'Paid_Amount',
              'amountpending':'Pending_Amount',
              'account_id':'Account_ID'}

initial_table = {'Payment_table':['payment_status', 'paid_amount', 'pending_amount']}

if 'dict.pkl' not in os.listdir('/home/aditya/Documents/citibot/data'):
    information_table = {}
else:
    information_table = pickle.load(open('/home/aditya/Documents/citibot/data/dict.pkl', 'rb'))

final_table = {**initial_table, **information_table}

def get_table(intent):
    tab = ""
    for table in final_table.keys():
        if intent in final_table[table]:
            tab = table
            break

    return tab

def query_maker(entities):
    string = ""
    for e in entities:
        if e['entity'] in FEATURES and e['extractor'] == 'CRFEntityExtractor':
            string = string + e['entity'] + " == \"" + e['value'] + "\" and " 
    print(string)
    return string[:-5]

def record_finder(entities):
    query = query_maker(entities)
    dataset = pd.read_csv('dataset.csv')
    records = dataset.query(query)
    print(records['Payment_Status'].item())

    return records

class ActionPayment(Action):

    def name(self) -> Text:
        return "action_payment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            table = get_table(tracker.latest_message['intent'])
            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_payment')
                return []

            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this query !!!")
    
            print(records)
            dispatcher.utter_message(text="The payment is "+records['Payment_Status'].item()+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("Account_ID", records['Account_ID'].item()),
                    SlotSet("Legal_Entity", records['Legal_Entity'].item()),
                    SlotSet("Client_Name", records['Client_Name'].item()),
                    SlotSet("Paid_Amount", records['Paid_Amount'].item()),
                    SlotSet("Pending_Amount", records['Pending_Amount'].item()),
                    SlotSet("Currency", records['Currency'].item()),
                    SlotSet("Source", records['Source'].item()),
                    SlotSet("Payment_Date", records['Payment_Date'].item())
                    ]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []

#       dispatcher.utter_message("utter_name", tracker, Var=data)
#       utter_name -> []{Var}


#
class ActionAmountPaid(Action):

    def name(self) -> Text:
        return "action_amount_paid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            table = get_table(tracker.latest_message['intent'])
            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_paidamount')
                return []

            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this query !!!")
            records = records
            dispatcher.utter_message(text="The payment amount is {} {}".format(records['Currency'].item(), records['Paid_Amount'].item())+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("Account_ID", records['Account_ID'].item()),
                    SlotSet("Legal_Entity", records['Legal_Entity'].item()),
                    SlotSet("Client_Name", records['Client_Name'].item()),
                    SlotSet("Paid_Amount", records['Paid_Amount'].item()),
                    SlotSet("Pending_Amount", records['Pending_Amount'].item()),
                    SlotSet("Currency", records['Currency'].item()),
                    SlotSet("Source", records['Source'].item()),
                    SlotSet("Payment_Date", records['Payment_Date'].item())
                    ]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []        


class ActionAmountPending(Action):

    def name(self) -> Text:
        return "action_amount_pending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            table = get_table(tracker.latest_message['intent'])
            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_pendingamount')
                return []
            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this statement !!!")
            records = records
            dispatcher.utter_message(text="The payment pending is {} {}".format(records['Currency'].item(),records['Pending_Amount'].item()) + "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("Account_ID", records['Account_ID'].item()),
                    SlotSet("Legal_Entity", records['Legal_Entity'].item()),
                    SlotSet("Client_Name", records['Client_Name'].item()),
                    SlotSet("Paid_Amount", records['Paid_Amount'].item()),
                    SlotSet("Pending_Amount", records['Pending_Amount'].item()),
                    SlotSet("Currency", records['Currency'].item()),
                    SlotSet("Source", records['Source'].item()),
                    SlotSet("Payment_Date", records['Payment_Date'].item())
                    ]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []        










# class ActionCheckRestaurants(Action):
#    def name(self) -> Text:
#       return "action_check_restaurants"

#    def run(self,
#            dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#       cuisine = tracker.get_slot('cuisine')
#       q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
#       result = db.query(q)

#       return [SlotSet("matches", result if result is not None else [])]
