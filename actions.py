# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import Action
from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
import requests
import json
import sqlite3 

class StudentForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "student_form"
        
        
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["roll", "class"]
        
    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"roll": [self.from_entity(entity="roll",
                                            intent=["roll"])],
                "class": [self.from_entity(entity="class",
                                                intent=["class"])]}
                                                
    @staticmethod
    def class_db():
        # type: () -> List[Text]
        """Database of supported class"""
        return ["1st",
                "2nd",
                "3rd",
                "4th",
                "5th",
                "6th",
                "7th",
                "8th",
                "9th",
                "10th"]
    
    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False
            
    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        print("1")
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        print(slot_values)
        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        print(REQUESTED_SLOT)
        print(slot_to_fill)
        if slot_to_fill:
            #print(self.extract_requested_slot(dispatcher,tracker, domain))
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            print(slot_values)
            
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        print("3")

        for slot, value in slot_values.items():
            print("Slot : ",slot," Value :",value)
            if slot == 'class':
                if value.lower() not in self.class_db():
                    dispatcher.utter_template('utter_wrong_class', tracker)
                    # validation failed, set slot to None
                    print("qqqqq")
                    slot_values[slot] = None
                
                

            elif slot == 'roll':
                if not self.is_int(value) or int(value) <= 0:
                    dispatcher.utter_template('utter_wrong_roll',
                                              tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None
            

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
        
    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []
        
class ShowMarks(Action):
    def name(self): 
     return "action_marks"
    
    def run(self, dispatcher, tracker, domain):
    
    # connect with database 
     connection = sqlite3.connect("students.db") 
 
     rl = tracker.slots['roll'] 
     cl = tracker.slots['class'] 
     print("roll=",rl)
     print("class=",cl)     
     cursor = connection.execute("SELECT Class FROM students WHERE Roll_No ={}".format(rl))
     for row in cursor:
                     #print ("Class = ", row[0])
                     if(row[0]==cl):
                                    temp = connection.execute("SELECT Marks FROM students WHERE Roll_No ={}".format(rl))
                                    for row in temp:
                                                     dispatcher.utter_message ("Marks = {}".format(row[0]))
 
                     else:
                          dispatcher.utter_message("Not a valid Entry")
     connection.close()       
     dispatcher.utter_template("utter_choice", tracker)   
     return[]
class ActionChoice(Action):
    def name(self):
        return "action_choice"

    def run(self, dispatcher, tracker, domain):
        print("Running")
        x = tracker.slots['choice']
        print("x=",x)
       
        if x=="YES":
                    dispatcher.utter_message("Okk..We will inform u")
        if x=="NO":
                   dispatcher.utter_message("Okk")
        return[]
class ActionImage(Action):
    def name(self):
        return "action_image"
    def run(self, dispatcher, tracker, domain):
        #request = json.loads(requests.get('http://127.0.0.1:5000/res').text)
        #st = ""
        #i=1
        #for item in request:
            #st += str(i) + ". Name : " + item['name'] + "\tRating : " + item['rating'] + "\tDistance : " + item['distance'] + "\n"
            #i+=1
            #dispatcher.utter_message(st)
        #request = json.loads(requests.get('http://127.0.0.1:5000/get_image/image').text)
        return [SlotSet("image_url","http://d1kkg0o175tdyf.cloudfront.net/large/53973_food_1_app.jpg")]
       
        
class ActionShow(Action):
    def name(self):
        return "action_show"
    def run(self, dispatcher, tracker, domain):
        print("running")
        print(tracker.slots["image_url"])
        #dispatcher.utter_template("utter_menu",tracker, image=tracker.slots["image_url"])
        dispatcher.utter_template("utter_marks",tracker, image=tracker.slots["image_url"])
        #response=requests.get('http://127.0.0.1:5000/get_image/image')
        #dispatcher.utter_template("utter_marks",tracker, image=response)
        #dispatcher.utter_template("utter_marks",tracker, image="http://127.0.0.1:5000/get_image/image")
        #dispatcher.utter_attachment("http://127.0.0.1:5000/get_image/image")
        return []
        
