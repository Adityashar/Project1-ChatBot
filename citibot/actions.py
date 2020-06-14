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

import pandas as pd
import sys

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

def query_maker(entities):
    string = ""
    for e in entities:
        if e['entity'] in ENTITY_LIST.keys() and e['extractor'] == 'CRFEntityExtractor':
            string = string + ENTITY_LIST[e['entity']] + " == \"" + e['value'] + "\" and " 
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
            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this query !!!")
    
            print(records)
            dispatcher.utter_message(text="The payment is "+records['Payment_Status'].item()+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("account_id", records['Account_ID'].item()),
                    SlotSet("legal_entity", records['Legal_Entity'].item()),
                    SlotSet("client_name", records['Client_Name'].item()),
                    SlotSet("amountpaid", records['Paid_Amount'].item()),
                    SlotSet("amountpending", records['Pending_Amount'].item()),
                    SlotSet("currency", records['Currency'].item()),
                    SlotSet("source", records['Source'].item()),
                    SlotSet("payment_date", records['Payment_Date'].item())
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
            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this query !!!")
            records = records
            dispatcher.utter_message(text="The payment amount is {}".format(records['Paid_Amount'].item())+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("account_id", records['Account_ID'].item()),
                    SlotSet("legal_entity", records['Legal_Entity'].item()),
                    SlotSet("client_name", records['Client_Name'].item()),
                    SlotSet("amountpaid", records['Paid_Amount'].item()),
                    SlotSet("amountpending", records['Pending_Amount'].item()),
                    SlotSet("currency", records['Currency'].item()),
                    SlotSet("source", records['Source'].item()),
                    SlotSet("payment_date", records['Payment_Date'].item())
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
            records = record_finder(entities)

            if(records.empty):
                raise ValueError("No record for this statement !!!")
            records = records
            dispatcher.utter_message(text="The payment pending is {}".format(records['Pending_Amount'].item()) + "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
            return [SlotSet("account_id", records['Account_ID'].item()),
                    SlotSet("legal_entity", records['Legal_Entity'].item()),
                    SlotSet("client_name", records['Client_Name'].item()),
                    SlotSet("amountpaid", records['Paid_Amount'].item()),
                    SlotSet("amountpending", records['Pending_Amount'].item()),
                    SlotSet("currency", records['Currency'].item()),
                    SlotSet("source", records['Source'].item()),
                    SlotSet("payment_date", records['Payment_Date'].item())
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
