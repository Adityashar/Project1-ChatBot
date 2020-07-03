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
from dbconnect import query_formation, getData, query_formation_dynamic
import pandas as pd
import sys, os, pickle, json, datetime


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


helpFile = json.load(open('./data/help.json', 'r'))

FEATURES = ['Client_Name', 'Account_ID', 'Legal_Entity', 'Currency', 
            'Payment_Type', 'Paid_Amount', 'Payment_Date', 'Payment_Status', 
            'Pending_Amount','Comments', 'Source']
Table = ""
initial_table = {'dataset':FEATURES}
initial_pk = {'dataset': ["Account_ID"]}

if 'pk.pkl' not in os.listdir('./data'):
    primary_table = {}
else:
    primary_table = pickle.load(open('./data/pk.pkl', 'rb'))
final_pk = {**initial_pk, **primary_table}

if 'dict.pkl' not in os.listdir('./data'):
    information_table = {}
else:
    information_table = pickle.load(open('./data/dict.pkl', 'rb'))
final_table = {**initial_table, **information_table}


helpFile = json.load(open('./data/help.json', 'r'))

def get_table(intent):
    global Table
    tab = ""
    for table in final_table.keys():
        if intent in final_table[table]:
            tab = os.path.basename(table)
            break
    Table = tab
    print(tab)
    return tab

def containsEntity(e, entities):
    for ent in entities:
        if e == ent['entity']:
            return True;
    return False;

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

# def getstring(val, tup):
#     if 'date' in tup.lower():
#         val = val.strftime('%Y-%m-%d')
#         print(type(val))
#     # print((str(val)))
#     return val

def saveRecords(table, records):
    features = final_table[table]
    store = {i:{tup:val for tup,val in zip(features,records[i])} for i in range(len(records))}
    with open('./botfiles/records.json', 'w') as fp:
        json.dump(store, fp)
    return 

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
        global Table
        Table = ""
        dispatcher.utter_message(text=str(helpFile['Payment creation'][0]))

        return [SlotSet("Domain", "Payment creation link"), SlotSet("Source", "'Help.json'")]

class ActionMultiAcc(Action):

    def name(self) -> Text:
        return "action_help_multiple_accounts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Table
        Table = ""
        dispatcher.utter_message(text=str(helpFile["Number of accounts"][0]))

        return [SlotSet("Domain", "Account setup link"), SlotSet("Source", "'Help.json'")]

class ActionPaySuccess(Action):

    def name(self) -> Text:
        return "action_help_payment_successful"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Table
        Table = ""
        dispatcher.utter_message(text=str(helpFile['Payment Successful'][0]))

        return [SlotSet("Domain", "payment status link"), SlotSet("Source", "'Help.json'")]

class ActionGetID(Action):

    def name(self) -> Text:
        return "action_help_get_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Table
        Table= ""
        dispatcher.utter_message(text=str(helpFile['Transaction id of payment'][0]))

        return [SlotSet("Domain", "get id link"), SlotSet("Source", "'Help.json'")]

class ActionCrossCountry(Action):

    def name(self) -> Text:
        return "action_help_cross_country"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Table
        Table= ""
        dispatcher.utter_message(text=str(helpFile['Cross country accounts'][0]))

        return [SlotSet("Domain", "cross country link"), SlotSet("Source", "'Help.json'")]

class ActionAddAcc(Action):

    def name(self) -> Text:
        return "action_help_add_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global Table 
        Table= ""
        dispatcher.utter_message(text=str(helpFile['Add new fund and account details'][0]))

        return [SlotSet("Domain", "add account link"), SlotSet("Source", "'Help.json'")]



class actionClientName(Action):

    def name(self) -> Text:
        return "action_Client_Name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Client_Name')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The client name is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
                # return []
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The Client names are {}.".format(', '.join(records)))
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionAccountID(Action):

    def name(self) -> Text:
        return "action_Account_ID"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Account_ID')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The account id is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The ids are {}.".format(', '.join(records)))
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionLegalEntity(Action):

    def name(self) -> Text:
        return "action_Legal_Entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Legal_Entity')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The legal entity is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                print(records)
                dispatcher.utter_message(text="The legal entities are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Currency')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The currency is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The Currenies are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Payment_Type')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The payment type is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The Status are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Paid_Amount')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)

            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The paid amount is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The amounts are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Payment_Date')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The payment date is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The dops are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Payment_Status')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The payment status is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The status are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Pending_Amount')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The pending amount is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The amounts are {}.".format(', '.join(records)))
                return []

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
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                if(tracker.get_slot('Account_ID') is not None):    
                    dispatcher.utter_message(template = 'utter_Comments')
                else:
                    dispatcher.utter_message(text = "Please enter a valid transaction ID !")
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,allrecords[0])}
                print(allrecords, features)
                dispatcher.utter_message(text="The comments is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                records = [rec[0] for rec in records]
                records = list(set(records))
                dispatcher.utter_message(text="The Comments are {}.".format(', '.join(records)))
                return []

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
            # entities = tracker.latest_message['entities']
            # intent = tracker.latest_message['intent']['name']
            # table = get_table(intent)
            # primary_key = final_pk[table][0]
            print(Table)
            # if(len(entities) == 0):
            #     print(Table)
            dispatcher.utter_message(template = 'utter_Source')
                # if(Table != ""):
                #     dispatcher.utter_message(template = 'utter_table')
            return []

            # if(containsEntity(primary_key, entities)):
            #     val = '*'
            # else:
            #     val = intent
            #     allrecords, features = getData(query_formation(entities, "*",  final_table[table],table), table)

            # records, features = getData(query_formation(entities, val,  final_table[table],table), table)
            # if val == "*":
            #     allrecords = records
            # saveRecords(table, allrecords)
            # if len(records) == 0:
            #     raise ValueError("No record for this query !!!")
            # elif len(records) == 1:
            #     features = {tup[0]:val for tup,val in zip(features,records[0])}
            #     print(records, features)
            #     dispatcher.utter_message(text="The source is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
            #     return [SlotSet("{}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            # else:
            #     records = [rec[0] for rec in records]
            #     records = list(set(records))
            #     dispatcher.utter_message(text="The sources are {}.".format(', '.join(records)))
            #     return []

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



class actionid(Action):

    def name(self) -> Text:
        return "action_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_id')
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation_dynamic(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation_dynamic(entities, val, final_table[table], table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,records[0])}
                print(records, features)
                features['Source'] = features.pop('source')
                dispatcher.utter_message(text="The id is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot]) for slot in features.keys()]
            else:
                print(records)
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionestablishment(Action):

    def name(self) -> Text:
        return "action_establishment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_establishment')
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation_dynamic(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation_dynamic(entities, val, final_table[table], table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,records[0])}
                print(records, features)
                features['Source'] = features.pop('source')
                dispatcher.utter_message(text="The establishment is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot]) for slot in features.keys()]
            else:
                print(records)
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []


class actionipoyear(Action):

    def name(self) -> Text:
        return "action_ipo_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                dispatcher.utter_message(template = 'utter_ipo_year')
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation_dynamic(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation_dynamic(entities, val, final_table[table], table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {tup[0]:val for tup,val in zip(features,records[0])}
                print(records, features)
                features['Source'] = features.pop('source')
                dispatcher.utter_message(text="The ipo year is  "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{}".format(slot), features[slot]) for slot in features.keys()]
            else:
                print(records)
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []
