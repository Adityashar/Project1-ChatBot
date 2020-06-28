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
import sys, os, pickle, json


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


helpFile = json.load(open('data/help.json', 'r'))

FEATURES = ['Client_Name', 'Account_ID', 'Legal_Entity', 'Currency', 
            'Payment_Type', 'Paid_Amount', 'Payment_Date', 'Payment_Status', 
            'Pending_Amount','Comments', 'Source']

table1 = 'Payment_table'
initial_table = {'Payment_table':FEATURES}

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

def query_maker(entities, table):
    string = ""
    if table == 'Payment_table':
	    for e in entities:	
	        if e['entity'] in FEATURES and e['extractor'] == 'CRFEntityExtractor':
	            string = string + e['entity'] + " == \"" + e['value'] + "\" and " 
	    print(string)
    else:
        for e in entities:	
	        if e['entity'] in final_table[table] and e['extractor'] == 'CRFEntityExtractor':
	            string = string + e['entity'] + " == \"" + e['value'] + "\" and " 
        print(string)
    return string[:-5]

def record_finder(entities, table):
    # print(table)
    query = query_maker(entities, table)
    # print(query)
    dataset = pd.read_csv(table+'.csv')
    records = dataset.query(query)
    print(records['Payment_Status'].item())

    return records

slots = ['Legal_Entity','Client_Name','Currency','Payment_Date','Paid_Amount','Pending_Amount','Account_ID','Source', 'Comments', 'Payment_Type', 'Payment_Status']

# class ActionPayment(Action):

#     def name(self) -> Text:
#         return "action_Payment_Status"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             entities = tracker.latest_message['entities']
#             intent = tracker.latest_message['intent']
#             table = get_table(intent['name'])
#             if(len(entities) == 0):
#                 dispatcher.utter_message(template = 'utter_Payment_Status')
#                 return []

#             records, features = getData(query_formation(entities, 'dataset'), table)

#             if(records.empty):
#                 raise ValueError("No record for this query !!!")
    
#             print(records)
#             dispatcher.utter_message(text="The payment is "+records['Payment_Status'].item()+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
#             return [SlotSet("{}".format(slot), records[slot].item()) for slot in slots]

#         except:
#             dispatcher.utter_message(text = str(sys.exc_info()[1]))
#             return []

# #       dispatcher.utter_message("utter_name", tracker, Var=data)
# #       utter_name -> []{Var}


# #
# class ActionAmountPaid(Action):

#     def name(self) -> Text:
#         return "action_Paid_Amount"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             entities = tracker.latest_message['entities']
#             intent = tracker.latest_message['intent']
#             table = get_table(intent['name'])
#             if(len(entities) == 0):
#                 dispatcher.utter_message(template = 'utter_Paid_Amount')
#                 return []

#             records, features = getData(query_formation(entities, 'dataset'), 'dataset')
#             features = {tup[0]:val for tup,val in zip(features,records[0])}
#             print(records, features)
#             if(len(records)==0 or len(records)>1):
#                 raise ValueError("No record for this query !!!")
#             records = records
#             # dispatcher.utter_message(text="The payment amount is {} {}".format(records['Currency'].item(), records['Paid_Amount'].item())+ "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
#             dispatcher.utter_message(text=str(features['Paid_Amount']))
#             return [SlotSet("{}".format(slot), records[slot].item()) for slot in slots]

#         except:
#             dispatcher.utter_message(text = str(sys.exc_info()[1]))
#             return []        


# class ActionAmountPending(Action):

#     def name(self) -> Text:
#         return "action_amount_pending"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             entities = tracker.latest_message['entities']
#             intent = tracker.latest_message['intent']
#             table = get_table(intent['name'])
#             if(len(entities) == 0):
#                 dispatcher.utter_message(template = 'utter_pendingamount')
#                 return []
#             # records = record_finder(entities)
#             records, features = getData(query_formation(entities, 'dataset'), table)
#             print(records)
#             if(records.empty):
#                 raise ValueError("No record for this statement !!!")
#             records = records
#             dispatcher.utter_message(text="The payment pending is {} {}".format(records['Currency'].item(),records['Pending_Amount'].item()) + "\nSource for this info is document number {}.".format(records['Source'].item()))# {}  {}".format(PS, LE))
#             return [SlotSet("{}".format(slot), records[slot].item()) for slot in slots]

#         except:
#             dispatcher.utter_message(text = str(sys.exc_info()[1]))
#             return []        

class ActionPayCreation(Action):

    def name(self) -> Text:
        return "action_help_payment_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile['Payment creation']))

        return [SlotSet("Domain", "Payment creation link"),UserUtteranceReverted()]

class ActionMultiAcc(Action):

    def name(self) -> Text:
        return "action_help_multiple_accounts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile["Number of accounts"]))

        return [SlotSet("Domain", "Account setup link"),UserUtteranceReverted()]

class ActionPaySuccess(Action):

    def name(self) -> Text:
        return "action_help_payment_successful"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile['Payment Successful']))

        return [SlotSet("Domain", "payment status link"),UserUtteranceReverted()]

class ActionGetID(Action):

    def name(self) -> Text:
        return "action_help_get_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile['Transaction id of payment']))

        return [SlotSet("Domain", "get id link"),UserUtteranceReverted()]

class ActionCrossCountry(Action):

    def name(self) -> Text:
        return "action_help_cross_country"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile['Cross country accounts']))

        return [SlotSet("Domain", "cross country link"),UserUtteranceReverted()]

class ActionAddAcc(Action):

    def name(self) -> Text:
        return "action_help_add_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=str(helpFile['Add new fund and account details']))

        return [SlotSet("Domain", "add account link"),UserUtteranceReverted()]


class actionClientName(Action):

    def name(self) -> Text:
        return "action_Client_Name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])
            flag = [ 1 for e in entities if e['entity'] == 'Account_ID']
            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Client_Name')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The client name is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


# class actionAccountID(Action):

#     def name(self) -> Text:
#         return "action_Account_ID"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         try:
#             entities = tracker.latest_message['entities']
#             intent = tracker.latest_message['intent']
#             table = 'dataset'#get_table(intent['name'])

#             if(len(entities) == 0):
#                 dispatcher.utter_message(template = 'utter_Account_ID')
#                 return []

#             records, features = getData(query_formation(entities, table), table)
#             features = {tup[0]:val for tup,val in zip(features,records[0])}
#             print(records, features)

#             # why make two query calls when already have features

#             if(len(records)==0 or len(records)>1):
#                 raise ValueError("No record for this query !!!")
    
#             print(records)
#             #dispatcher.utter_message(text="yy")
#             dispatcher.utter_message(text="The account id is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
#             return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

#         except:
#             dispatcher.utter_message(text = str(sys.exc_info()[1]))
#             return []


class actionLegalEntity(Action):

    def name(self) -> Text:
        return "action_Legal_Entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Legal_Entity')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The legal entity is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionCurrency(Action):

    def name(self) -> Text:
        return "action_Currency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Currency')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The currency is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionPaymentType(Action):

    def name(self) -> Text:
        return "action_Payment_Type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Payment_Type')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The payment type is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionPaidAmount(Action):

    def name(self) -> Text:
        return "action_Paid_Amount"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Paid_Amount')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The paid amount is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionPaymentDate(Action):

    def name(self) -> Text:
        return "action_Payment_Date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Payment_Date')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The payment date is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionPaymentStatus(Action):

    def name(self) -> Text:
        return "action_Payment_Status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Payment_Status')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The payment status is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionPendingAmount(Action):

    def name(self) -> Text:
        return "action_Pending_Amount"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Pending_Amount')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The pending amount is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionComments(Action):

    def name(self) -> Text:
        return "action_Comments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name']))

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Comments')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The comments is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionSource(Action):

    def name(self) -> Text:
        return "action_Source"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']
            table = 'dataset'#get_table(intent['name'])

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_Source')
                return []

            records, features = getData(query_formation(entities, table), table)
            features = {tup[0]:val for tup,val in zip(features,records[0])}
            print(records, features)

            # why make two query calls when already have features

            if(len(records)==0 or len(records)>1):
                raise ValueError("No record for this query !!!")
    
            print(records)
            #dispatcher.utter_message(text="yy")
            dispatcher.utter_message(text="The source is  "+ str(features[intent['name'].lower()]) + " for the given record with id "+ str(features['account_id']) )
            return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table1]]

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
