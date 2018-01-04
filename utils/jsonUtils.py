import json
def is_json(myjson):  
    try:  
        eval(myjson)  
    except ValueError:  
        return False  
    return True  