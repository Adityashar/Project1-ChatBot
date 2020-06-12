# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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


class ActionPayment(Action):

    def name(self) -> Text:
        return "action_payment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            print(entities)

            ID = ""

            for dic in entities:
                if(dic['entity'] == 'account_id'):
                    ID = dic['value']
                #     break
                print(dic['entity']+ " : "+ dic['value'])
            print(ID)

            dataset = pd.read_csv('dataset.csv')
            PS = dataset[dataset['Account ID'] == int(ID)]['Payment Status']
            LE = dataset[dataset['Account ID'] == int(ID)]['Legal Entity']

            record = dataset[dataset['Account ID'] == int(ID)]

            if(record.empty):
                raise ValueError("No record for this ID !!!")

            print((record))

            dispatcher.utter_message(text="Hi here are the details: {}  {}".format(PS, LE))
            return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []

#       dispatcher.utter_message("utter_name", tracker, Var=data)
#       utter_name -> []{Var}



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
