# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:11:04 2020

@author: user
"""

def add_ques1(intent, entity , values):
    questions = []
    
    for value in values:
        questions.append("What is the {} for transaction with [{}]({})".format(intent,value,entity))
        questions.append("Give me the {} details about agreement with [{}]({})".format(intent,value,entity))
        questions.append("Tell me the {} for the [{}]({})".format(intent, value, entity))
        questions.append("Can you show me the {} for [{}] ({})".format(intent , value, entity))
        questions.append("I request you to provide me the {} made with [{}] ({})".format(intent , value, entity))
        questions.append("Could you please give me the {} insights regarding concurrence with [{}]({})".format(intent,value,entity))
        questions.append("For the {} disclose to me the {}".format(intent,value,entity))
        questions.append("Please check the {} of [{}] ({})".format(intent , value, entity))
        questions.append("Brief me about the {} for the accord with [{}]({})".format(intent,value,entity))
        questions.append("Please show me the {} for transaction with [{}] ({})".format(intent , value, entity))
    
    return questions



def add_ques2(intent, entity1 , values1, entity2 , values2):
    questions = []
    
    for value1 in values1:
        for value2 in values2:
            questions.append("What is the {} that [{}]({}) has to pay to [{}]({})?".format(intent,value1,entity1,value2,entity2))
            questions.append("Give me details about {} for transaction with [{}]({}) for agreement [{}]({})".format(intent,value1,entity1,value2,entity2))
            questions.append("Brief us about the {} for the agreement of [{}]({}) for transaction with [{}]({})".format(intent,value1,entity1,value2,entity2))     
            questions.append("For agreement with [{}]({}) give me the subtleties of the {} from [{}]({})".format(value2,entity2, intent, value1,entity1))
            questions.append("For [{}]({}) with id [{}]({}) tell me the {}.".format(value1, entity1, value2, entity2, intent))
            questions.append("for the concurrence with [{}]({}) give me report of {} from [{}]({})".format(value1,entity1, intent, value2, entity2))
    return questions

    
def get_questions(intents,entities):
    questions = []
    
    for intent in intents:
        for entity,value in entities.items():
            questions.extend(add_ques1(intent,entity,value))
    
    for intent in intents:
        for entity1,value1 in entities.items():
            for entity2,value2 in entities.items():
                if entity1 != entity2:
                    questions.extend(add_ques2(intent,entity1,value1,entity2,value2))
                    
    return questions

intents = ["payment status", "payment date"]
entities = {"Legal_name":["citi","pity"], "account_id":[1022,1033]}

q = get_questions(intents,entities)
