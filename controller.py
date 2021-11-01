import requests
import model
import random

def find_cat(choice):
    cat = requests.get("https://wger.de/api/v2/exercisecategory/").json()['results']
    for i in cat:
        if i['name'].lower() == choice:
            return i['id']
    return "wrong choice"

def find_equipment(equipment):
    equipments = requests.get("https://wger.de/api/v2/equipment/").json()['results']
    for i in equipments:
        if i['name'].lower() == equipment:
            return i['id']
    return "wrong choice"

def check_history(category_data):
    cat_id = str(find_cat(category_data))
    if HistoryController.create(cat_id):
        return 'Come on dude,you need to train all the muscles!'
    return cat_id

def exercise(cat_id,equipment):
    eq_id= find_equipment(equipment)
    response = requests.get("https://wger.de/api/v2/exercise/?language=2&category="+cat_id)
    exercise_data = response.json()
    flag=False
    if eq_id ==7:
       for exercise in exercise_data["results"]:
            if exercise["equipment"]==[]:
                flag = True
                exe = exercise
                break
    else:
        for exercise in exercise_data["results"]:
            if eq_id in exercise["equipment"]:
                flag=True
                exe=exercise
                break
    if not flag:
        return "We did not find an exercise with the equipment in the category you selected."+"\n"+" Would you like to train without equipment in this category?"
    #exe = random.choice(exercise_data["results"])
    id = exe['id']
    return "https://wger.de/en/exercise/" + str(id) + "/view/"


class HistoryController:
    """
    warpped class to handle the bot history
    """

    @classmethod
    def create(cls, cat: int) :
        """ 
        connect to function from model     
        """
        return model.HistoryModelWrapper.create(cat)
        
