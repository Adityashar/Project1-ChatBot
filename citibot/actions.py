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


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_payment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        ID = ""

        for dic in entities:
            if(dic['entity'] == 'account_id'):
                ID = dic['value']
                break
            # print(dic['entity']+ " : "+ dic['value'])
        print(ID)

        dataset = pd.read_csv('dataset.csv')
        PS = dataset[dataset['Account ID'] == int(ID)]['Payment Status']
        LE = dataset[dataset['Account ID'] == int(ID)]['Legal Entity']

        data = "Payment Status: {} , Legal Entity: {}".format(PS, LE) 

        print(data)

        dispatcher.utter_message(text="Hi here are the details: " + (data))

        return []