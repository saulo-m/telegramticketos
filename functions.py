import csv
import re
import requests
import json
from decouple import config
from telebot import types

def csv_to_array(source):
    array = []
    with open(source, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            array.append(row)
    return array


def get_clients(word, source, f_index, r_index):
    result_set = {}

    for row in source:
        if bool(re.match(r".*" + word + ".*", row[f_index], re.I)) == True:
            result_set[row[r_index-1]] = row[r_index]

        else:
            pass
    return result_set


def create_ticket_ticketos(email,tsubject,tmessage):
    ticketmessagef = "data:text/html, " + tmessage
    data = {
        "email": email,
        "subject": tsubject,
        "source": "API",
        "ip": config("MACHINE_IP"),
        "message": ticketmessagef,
    }
    headers = {"X-API-Key": config("API_KEY") }
    r = requests.post(config("TICKETOS_URL"), data=json.dumps(data), headers=headers)
    if r.ok:
        return f"Ticket created. {email}"
    else:
        return f"The ticket for user {email} couldn't be created."


def clear_commands(string,*commands):
    pattern = ''
    for command in commands:
        pattern += f"/{command} |"
    cleared_message = re.sub(
        pattern, "", str.lower(string), flags=re.IGNORECASE
    )
    return cleared_message

def create_keyboard(result):
    if len(result) > 0:
        buttons=[]
        keyboard = types.InlineKeyboardMarkup()
        for user, mail in result.items():
            buttons.append(types.InlineKeyboardButton(text=f"{user[:10]} {mail}", callback_data=mail))
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text='Cancelar', callback_data='cancel'))
        return keyboard
    else:
        return None