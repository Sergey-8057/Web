import time
import uuid
import random
from collections import UserDict
from datetime import datetime
import json
from colorama import init, Fore, Back, Style#Сторонний пакет
from textmatch import fuzzy_match

init(autoreset=True)#Для Windows 10

#---------------------------------------------------------------------------------------------
class NoteBase(UserDict):
    def add_record(self, record):
        self.data[record.note_id] = record
    def __str__(self):
        return f"{self.values()}" 
  

class Marker:
    def __init__(self):
        self.note_id=str(uuid.uuid1()) #Автоматически будет присвоен уникальный токен UUID1 формата
        self.note_tag=[]
        self.note_keyword=""
    

class NoteRecord(Marker):
    def __init__(self):
        super().__init__() #Подтягиваем __init__ из Tag
        self.note_data: str  = "" 
        self.note_date=datetime.now() #Автоматически будет присвоено время создания
    def __str__(self):
        return f"\nID: {self.note_id}\nDate: {self.note_date}\nTag: {self.note_tag}\nKeyword: {self.note_keyword}\n\nNote:\n_________________________________\n\n{self.note_data}" 
    def __repr__(self):
        return f"{self}"

NOTEBASE=NoteBase()

#---------------------------------------------------------------------------------------------    
def flasher(text, speed=0.03):
    
    for i in text:
        time.sleep(speed)
        print(Fore.CYAN + Style.BRIGHT + i, end='', flush=True)
    
def add_note():
    input_data=input(Fore.BLUE +'Write your notes right here and press "Enter" when you are done:' + Fore.GREEN + '\n>>>'+ Style.RESET_ALL)

    new_note=NoteRecord()
    new_note.note_data=input_data

    particles_note=new_note.note_data.split(" ")
    new_note.note_keyword: str = 'No keyword (phrase).' if len(particles_note) == 0 else str(random.choices(particles_note, k=1))
    print(Fore.BLUE +"\n{:*^40}\n".format("Your note have random keyword") + Style.RESET_ALL)
    
    
    while True:
        input_data=input(Fore.BLUE +'Would you like to assign a tag?\nInput next: '+ Fore.GREEN + 'yes'+ Fore.BLUE + '/' + Fore.RED + 'no' + Fore.GREEN + '\n>>>' + Style.RESET_ALL)
        
        if input_data == "yes":
            new_note.note_tag.append(input(Fore.BLUE +'Assign first tag: '+ Style.RESET_ALL))
            print(Fore.BLUE +"\n{:*^40}\n".format("Your note have first tag") + Style.RESET_ALL)
            break
        elif input_data == "no":
            print(Fore.BLUE +"\n{:*^40}\n".format("Your note don\'t have any tags") + Style.RESET_ALL)
            break
        else:
            flasher('Something went wrong!',0.05)
           

    
    input_data_2=input(Fore.BLUE +'Would you like to save your note in stream? ' + Fore.GREEN + 'yes'+ Fore.BLUE + '/' + Fore.RED + 'no' + Fore.GREEN + '\n>>>' + Style.RESET_ALL)
    if input_data_2 == 'yes':
        cl_notebase_input=NOTEBASE.add_record(new_note)
        print(Fore.BLUE +"{:*^40}".format("Your note were saved in stream")+ Style.RESET_ALL)
        print(NOTEBASE)

def find_in_note():
    input_data=input(Fore.BLUE +'Please, input the phrase, you want to de finded:'+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
    matches_id_list=[]
    match_counter=0
    
    for value in NOTEBASE.values():
        
        if value.note_data.find(input_data) > -1:
            matches_id_list.append(value.note_id)
    
    if len(matches_id_list) > 0:
        for i in map(lambda id: id, matches_id_list):
            match_counter+=1
            print(Fore.BLUE +"{:=^70}".format("=")+ Style.RESET_ALL)
            print(Fore.MAGENTA + f"Match {match_counter} in NOTEBASE:"+ Style.RESET_ALL)
            print(Fore.RED +i+ Style.RESET_ALL)
            print(NOTEBASE[i].note_data)
    else:
        print(Fore.BLUE +"\n{:*^40}\n".format("No matches!") + Style.RESET_ALL)

def delete_note():
    input_data=input(Fore.BLUE +'Please, input the note ID, you want to de burned:'+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)

    if input_data in NOTEBASE.keys():
        NOTEBASE.pop(input_data)
    print(Fore.RED +f"\nRecord {input_data} sucсessfuly deleated."+ Style.RESET_ALL)

def burn_base():
    NOTEBASE.clear()
    print(Fore.RED +"{:-^70}".format("BASE TOTALY BURNED")+ Style.RESET_ALL)

def change_note():
    
    while True:
        input_data=input(Fore.BLUE +'Please, input the note ID, you want to de changed:'+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
        if input_data in NOTEBASE.keys():
            input_data_2=input(Fore.BLUE +'Please, input new content:'+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
            if input(Fore.BLUE +'You sure, you want to save changes? '+ Fore.GREEN + 'yes'+ Fore.BLUE + '/' + Fore.RED + 'no' + Fore.GREEN + '\n>>>' + Style.RESET_ALL) == "yes":
                NOTEBASE[input_data].note_data=input_data_2
                print(Fore.BLUE +f"\nRecord {input_data} sucsessfuly changed."+ Style.RESET_ALL)
                break
        else:
                print(Fore.RED +"\n{:*^40}\n".format("No ID in base!") + Style.RESET_ALL)
                break


def show_all():
    for i in map(lambda id: id, NOTEBASE):
        print(Fore.BLUE +"{:=^70}".format("=")+ Style.RESET_ALL)
        print(NOTEBASE[i])

def set_tag():
    input_data=input(Fore.BLUE +'Please, input the note ID, to add tag: '+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
    
    if input_data in NOTEBASE.keys():
        input_data_2=input(Fore.BLUE +'Please, input new tag: '+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
        NOTEBASE[input_data].note_tag.append(input_data_2)
        NOTEBASE[input_data].note_tag.sort() #Автоматически сортирует теги вниутри записи
        print(Fore.BLUE +f"\nRecord {input_data} have new tag."+ Style.RESET_ALL)

def clear_tags():
    
    while True:
        input_data=input(Fore.BLUE +'Please, input the note ID, to clear ALL tags: '+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
        if input_data in NOTEBASE.keys():
            if input(Fore.BLUE +'You sure, you want to delete tags? '+ Fore.GREEN + 'yes'+ Fore.BLUE + '/' + Fore.RED + 'no' + Fore.GREEN + '\n>>>' + Style.RESET_ALL) == "yes":
                NOTEBASE[input_data].note_tag.clear()
                print(Fore.RED +f"\nRecord {input_data} sucсessfuly cleaned from all tags."+ Style.RESET_ALL)
                break
        else:
                print(Fore.RED +"\n{:*^40}\n".format("No ID in base!") + Style.RESET_ALL)
                break
        

def save_handler(book=NOTEBASE):
    
    inner_val=[]
    json_dict_pattern={"note_base":inner_val} 
   
    for val_id, all_fields in book.data.items():         
        note_data={val_id:[
            {"Tag":str(all_fields.note_tag)},
            {"Keyword":str(all_fields.note_keyword)},
            {"Notes":str(all_fields.note_data)},
            {"Date":str(all_fields.note_date)}
            ]}
        inner_val.append(note_data)
        print(inner_val)
    with open("note_base.json", "w") as fh:
        json.dump(json_dict_pattern, fh)
        print(Fore.BLUE +"Saved on your HardDrive. Current directory."+ Style.RESET_ALL)

def find_tag_notes():
    input_data=input(Fore.BLUE +'Please, input the tag, you want to de finded:'+ Fore.GREEN + '\n>>>'+ Style.RESET_ALL)
    matches_id_list=[]
    match_counter=0
    
    for value in NOTEBASE.values():
        
        if input_data in value.note_tag:
            matches_id_list.append(value.note_id)
    
    if len(matches_id_list) > 0:
        for i in map(lambda id: id, matches_id_list):
            match_counter+=1
            print(Fore.BLUE +"{:=^70}".format("=")+ Style.RESET_ALL)
            print(Fore.MAGENTA + f"Match {match_counter} in NOTEBASE:"+ Style.RESET_ALL)
            print(Fore.RED +i+ Style.RESET_ALL)
            print(NOTEBASE[i].note_data)
    else:
        print(Fore.BLUE +"\n{:*^40}\n".format("No matches!") + Style.RESET_ALL)

def show_by_tags():

    for_sorting=[]
    non_sorting=[]
    sorted_output_id=[]

    for id, data in NOTEBASE.items():
        if len(data.note_tag)>0:
            for_sorting.append(f'{data.note_tag[0]}_{id}')
            print(for_sorting)
        else:
            non_sorting.append(id)
            print(non_sorting)

    for_sorting.sort()
   
    for el in for_sorting:
        devided_el=el.split("_") #Без слайсов чтоб избежать проблем с длинной UUID
        sorted_output_id.append(devided_el[1])
    sorted_output_id.extend(non_sorting)

    for id in sorted_output_id:
        print(Fore.BLUE +"{:=^70}".format("=")+ Style.RESET_ALL)
        print(NOTEBASE[id])   
                 
#---------------------------------------------------------------------------------------------
def call_notebook():
    notebook_commands={
        "add note":add_note,
        "find in note":find_in_note, #Поиск внутри заметок, согласно пункту №7 ТЗ, ищет в тексте и выдает ID
        "find by tag":find_tag_notes,
        "delete":delete_note,
        "burn":burn_base,
        "change":change_note,
        "show base":show_all,
        "show by tags":show_by_tags,
        "tag":set_tag,
        "clear tags":clear_tags,
        "save on HD":save_handler 
    }
    print("\n")
    flasher('Welcome on board "Notepad 1.0" !')

    while True:

        input_data=input(Fore.BLUE +'''\n\nPlease, choose your command regarding to:
"add note"- create new note
"stop notes"- exit from notebook
"find in note"- can find lines in base
"find by tag" - can find notes by tag
"delete"- delete note
"burn" - burn base
"change" - change note
"show base" - show all positions in base
"show by tags" - return sorting by tags base
"tag" - add tag to note
"clear tags" - clear ALL tags in note
"save on HD" - exactly that'''
+ Fore.GREEN + '\n>>>' + Style.RESET_ALL)
        
        if input_data == "stop notes":
            return ('\nYou finished with notes.\n')
            #break
            
        for command, action in notebook_commands.items():

            if input_data == command:
                push=notebook_commands[command]
                push()

            elif input_data not in notebook_commands.keys():
                flasher(fuzzy_match(input_data, notebook_commands.keys()))
                break
                

def main():

    call_notebook()
    
if __name__ == '__main__':  
    exit(main())
