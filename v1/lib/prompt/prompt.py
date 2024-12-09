from lib import logger
from getpass import getpass

def yes_or_no(question:str, predefined_answer = ""):
    answer = ""
    
    while answer == "":
        answer = input(f"INPUT: {question}? (Y/N) > ")
        if answer.lower() != "y" and answer.lower() != "n":
            logger.error("Response must only be 'y' or 'n'")
            answer = ""
            continue

        return answer
    
def from_list(question:str, target_list:list, predefined_answer = ""):
    answer = ""
    list_length = len(target_list)
    
    while answer == "":
        print(f"INPUT: {question}")
        for i, list_entry in enumerate(target_list, start=1):
            print(f"{i}. {list_entry}")
            
        answer = input(f"INPUT: Select something from the list by typing its entry number. > ")
        if not answer.replace("-", "").replace("+", "").isnumeric():
            logger.error("Answer isn't a number.")
            continue
        
        if int(answer) > list_length or int(answer) < 0:
            logger.error("Answer is out of list range!")
            continue
        
        return target_list[int(answer) - 1]
    
def string(question:str, predefined_answer = ""):
    return input(f"INPUT: {question} > ")

def password(question:str):
    return getpass(f"INPUT: {question} > ")