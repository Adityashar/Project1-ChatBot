"""
Dynamically updating different files
"""
import os
import sys
import json
import pickle
import pandas as pd
from getQuestions import get_questions


def new_data(data_name, directory):
    """get the name of the new dataset file"""
    DATASET_LOC = os.path.join(directory, data_name)
    # read the data file - csv, excel and json
    if data_name.endswith('.csv'):
        DATASET = pd.read_csv(DATASET_LOC)
    elif data_name.endswith('.xlx') or data_name.endswith('.xlsx'):
        DATASET = pd.read_excel(DATASET_LOC)
    elif data_name.endswith('.json'):
        DATASET = pd.DataFrame(json.load(open(DATASET_LOC, 'r')), index=[1])
    return DATASET


def get_entities(threshold_value, FEATURES):
    """List all the possible entities"""
    PRIMARY_KEY = []
    ENTITIES = {}
    for col in FEATURES.keys():
        if (DATASET[col].unique().shape[0] == DATASET.shape[0]) and (FEATURES[col] == 'O' or FEATURES[col] == 'int64'):           
            PRIMARY_KEY.append(col)                                             # Make this the PRIMARY KEY
            ENTITIES[col] = DATASET[col].unique()[:threshold_value].tolist()

        elif DATASET[col].unique().shape[0] > threshold_value and (FEATURES[col] == 'O' or FEATURES[col] == 'int64'):
            ENTITIES[col] = DATASET[col].unique()[:threshold_value].tolist()

        elif FEATURES[col] == 'O' or FEATURES[col] == 'int64':
            ENTITIES[col] = DATASET[col].unique().tolist()        
    return ENTITIES, PRIMARY_KEY


# def get_questions(intent):
#     intent = intent.replace("_", " ").lower()
#     questions = []
#     questions.append("what is {} for ".format(intent))
#     questions.append("Tell me something about {} with ".format(intent))
#     questions.append("Give me information about {} for the ".format(intent))
#     return questions

# it contains a list of intents, actions, responses, entities, slots
def update_domain(intents, actions, entities, responses, data):
    """updating the domain.yml file"""
    # update intent list
    pointer_intent = data.find("intents:")
    string = ""
    for intent in intents:
        string += "  - {}\n".format(intent)
    data = data[:pointer_intent+9] + string + data[pointer_intent+9:]
    # update actions list 
    pointer_actions = data.find("actions:")
    string = ""
    for action in actions:
        string += "  - {}\n".format(action)
    data = data[:pointer_actions+9] + string + data[pointer_actions+9:]
    # update entity list
    pointer_ent = data.find("entities:")
    string = ""
    for entity in entities:
        string += "  - {}\n".format(entity)
    data = data[:pointer_ent+10] + string + data[pointer_ent+10:]
    # update responses
    pointer_resp = data.find("responses:")
    string = ""
    for resp in responses:
        text = "The {} for the given agreement is ".format(resp[6:].replace("_", " ")) + "{" + resp[6:] + "}."
        string += "  {}:\n  - text: \"{}\"\n\n".format(resp, text)
    data = data[:pointer_resp+11] + string + data[pointer_resp+11:]
    # update slots
    pointer_slot = data.find("slots:")
    if pointer_slot == -1:
        data = data + "\n\nslots:\n"
        pointer_slot = data.find("slots:")
    string = ""
    for slot in entities:
        string += "  {}:\n    type: unfeaturized\n    auto_fill: false\n".format(slot)
    data = data[:pointer_slot+7] + string + data[pointer_slot+7:]
    return data

# updating the actions file by addition of new actions based on an intent
# Each of the new intent is mapped to an action which will be triggered once the latter intent is predicted
# First open the given actions.py file in append mode, add the template text and voila new action is updated !
text = """

class {}(Action):

    def name(self) -> Text:
        return "{}"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            entities = tracker.latest_message['entities']
            intent = tracker.latest_message['intent']['name']
            table = get_table(intent)
            primary_key = final_pk[table][0]

            if(len(entities) == 0):
                dispatcher.utter_message(template = '{}')
                return []

            if(containsEntity(primary_key, entities)):
                val = '*'
            else:
                val = intent
                allrecords, features = getData(query_formation_dy(entities, "*",  final_table[table],table), table)

            records, features = getData(query_formation(entities, val, final_table[table], table), table)
            if val == "*":
                allrecords = records
            saveRecords(table, allrecords)
            if len(records) == 0:
                raise ValueError("No record for this query !!!")
            elif len(records) == 1:
                features = {{tup[0]:val for tup,val in zip(features,records[0])}}
                print(records, features)
                dispatcher.utter_message(text="{} "+ str(features[intent.lower()]) + " for the given record with id "+ str(features[primary_key.lower()]) )
                return [SlotSet("{{}}".format(slot), features[slot.lower()]) for slot in final_table[table]]
            else:
                print(records)
                return []

        except:
            dispatcher.utter_message(text = str(sys.exc_info()[1]))
            return []
"""
def add_action(Action, file):
    """updating the actions file by addition of new actions based on an intent"""
    utter = []
    for action in Action:
        # print(action)
        utterance = "utter" + action[6:]
        class_name = action.replace("_", "")
        intent = action[7:].replace("_", " ").lower()
        # sprint(intent)
        utter.append(utterance)
        template = text.format(class_name, action, utterance, "The {} is ".format(intent))
        file.write(template)
    return utter

# the current stories.md file has storylines with respect to a classified intent
# For the dynamic addition of data, contextual storylines cannot be added due to their increased complexity
# name : ## {intent} path
def new_stories(story, intent_dict):
    """the current stories.md file has storylines with respect to a classified intent"""
    story[-1] = story[-1] + '\n'
    data = []
    actions = []
    for intent in intent_dict:
        action = "action_{}".format(intent)
        string = " {} path 1\n* {}\n  - {}\n\n".format(intent, intent, action)
        data.append(string)
        actions.append(action) 
    story += data
    return story, actions

# the current nlu.md file has the following information : (1)intents, (2)lookup, (3)synonyms
# created three functions to update each of the these sections respectively
# optimisation for future instead of writing, just append new data
def synonyms_to_md(data_md, entity_dict):
    """add synonyms"""
    data = []
    for entity in entity_dict.keys():
        if FEATURES[entity] == 'int64' or entity in PRIMARY_KEY:
            continue
        # Now the only entities left are character dtype with limited uniques
        # For each value in entity add synonyms
        for val in entity_dict[entity]:
            string = " synonym:{}\n".format(val)
            synonyms = [val.lower(), val.upper(), val.title()]
            for sys in synonyms:
                string += "- {}\n".format(sys)
            string += "\n"
            data.append(string)
    data_md += data
    return data_md

# lookup should not include primary_key entity, integer entities
def lookups_to_md(data_md, entity_dict):
    """add lookups"""
    data = []
    for entity in entity_dict.keys():
        string_ent = " lookup:{}\n".format(entity)
        if FEATURES[entity] == 'int64' or entity in PRIMARY_KEY or 'date' in entity.lower():
            continue          
        for val in entity_dict[entity]:
            string_ent += "- {}\n".format(val)
        string_ent += "\n"
        data.append(string_ent)
    data_md += data
    return data_md

def intents_to_md(data_md, intent_dict):
    """intents add"""
    data_md[-1] = data_md[-1] + '\n'
    data = []
    for intent in intent_dict.keys():
        string_intent = " intent:{}\n".format(intent)
        for ques in intent_dict[intent]:
            string_intent += "- {}\n".format(ques)
        string_intent += "\n"
        data.append(string_intent)  
    data_md += data
    return data_md

def main():
    """This function should be triggered by a listener"""
    global DATASET, FEATURES, PRIMARY_KEY
    data_name = sys.argv[1]
    directory = '../botfiles'
    DATASET = new_data(data_name, directory)

    # dict of columns in new data with corresponding dtypes 
    DATASET.columns = [column.replace(" ", "_") for column in DATASET.columns] 

    FEATURES = {col: DATASET[col].dtype for col in DATASET}
    threshold_value = 20
    ENTITIES, PRIMARY_KEY = get_entities(threshold_value, FEATURES)

    # Dict of intents having a list of questions as their values.
    INTENTS = {col:get_questions(col, ENTITIES, PRIMARY_KEY) for col in FEATURES.keys()}

    # making a dictionary of tables with corresponding intents for query based retrieval
    table = os.path.splitext(data_name)[0]
    if 'dict.pkl' not in os.listdir('../data'):
        information_table = {}
    else:
        information_table = pickle.load(open('../data/dict.pkl', 'rb'))

    information_table[table] = list(INTENTS.keys())
    pickle.dump(information_table, open('../data/dict.pkl', 'wb'))
    # dictionary dumped
    if 'pk.pkl' not in os.listdir('../data'):
        primary_table = {}
    else:
        primary_table = pickle.load(open('../data/pk.pkl', 'rb'))

    primary_table[table] = list(PRIMARY_KEY)
    pickle.dump(primary_table, open('../data/pk.pkl', 'wb'))
    # invoke nlu
    nlu = open('../data/nlu.md', 'r')
    s = nlu.read().split('##')
    nlu_intent = intents_to_md(s, INTENTS)
    nlu_lookup = lookups_to_md(nlu_intent, ENTITIES)
    # nlu_synonyms = synonyms_to_md(nlu_lookup, ENTITIES)
    new_nlu = '##'.join(nlu_lookup)
    f = open('../data/nlu.md', "w")
    f.write(new_nlu)
    f.close()
    # invoke stories
    story = open('../data/stories.md', 'r')
    s = story.read().split('##')
    story_text, Actions = new_stories(s, INTENTS)
    new_story = '##'.join(story_text)
    f = open('../data/stories.md', "w")
    f.write(new_story)
    f.close()    
    # invoke actions
    current_actions = open('../actions.py', 'a', encoding='utf-8')
    utterances = add_action(Actions, current_actions)
    # invoke domain
    domain = open('../domain.yml', 'r').read()
    new_domain = update_domain(list(INTENTS.keys()), Actions, list(ENTITIES.keys()), utterances, domain)
    f = open('../domain.yml', "w")
    f.write(new_domain)
    f.close() 

if __name__ == '__main__':
    main()
	
