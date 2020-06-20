
class ActionPayment(Action):

    def name(self) -> Text:
        return "lol_work"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            print(entities)


            ## database code 
            #table = ""
            # intent = tracker.latest_message['intent']
            #query = query_formation(entities, table, intent)
            #lis = getData(query)

            #info = lis[0][0]

            #dispatcher.utter_message(text="Hi here are the details: {}".format(info))

            ID = ""

            for dic in entities:
                if(dic['entity'] == 'account_id'):
                    ID = dic['value']
                #     break
                print(dic['entity']+ " : "+ dic['value'])
            print(ID)

            dataset = pd.read_csv('dataset.csv')
            PA = dataset[dataset['Account ID'] == int(ID)]['lol_work']
            LE = dataset[dataset['Account ID'] == int(ID)]['Legal Entity']

            record = dataset[dataset['Account ID'] == int(ID)]

            if(record.empty):
                raise ValueError("No record for this ID !!!")

            print((record))

            dispatcher.utter_message(text="Hi here are the details: {}  {}".format(PA, LE))
            return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []

class ActionPayment(Action):

    def name(self) -> Text:
        return "lol_work"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            print(entities)


            ## database code 
            #table = ""
            # intent = tracker.latest_message['intent']
            #query = query_formation(entities, table, intent)
            #lis = getData(query)

            #info = lis[0][0]

            #dispatcher.utter_message(text="Hi here are the details: {}".format(info))

            ID = ""

            for dic in entities:
                if(dic['entity'] == 'account_id'):
                    ID = dic['value']
                #     break
                print(dic['entity']+ " : "+ dic['value'])
            print(ID)

            dataset = pd.read_csv('dataset.csv')
            PA = dataset[dataset['Account ID'] == int(ID)]['lol_work']
            LE = dataset[dataset['Account ID'] == int(ID)]['Legal Entity']

            record = dataset[dataset['Account ID'] == int(ID)]

            if(record.empty):
                raise ValueError("No record for this ID !!!")

            print((record))

            dispatcher.utter_message(text="Hi here are the details: {}  {}".format(PA, LE))
            return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []
