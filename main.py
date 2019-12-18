from functions import csv_to_array, get_clients, create_ticket_ticketos, clear_commands, create_keyboard
from telebot import TeleBot
from decouple import config

""" This script creates tickets in the TicketOS from messages sent on Telegram.
This bot works on individuals chats or groups chats.

Please change the .env file with yours settings:

example:
TELEGRAM_APIKEY=121231313:AAaabbbb123 #Telegram API Key. Message @botfather on telegram to get one
CLIENTS_FILE=adusers.csv #File with the users and e-mail addresses used to create the tickets (format: name;email)
TICKETOS_URL=http://example.domain.com/api/tickets.json #URL to TicketOS API
MACHINE_IP=172.16.0.1 #IP of the machine running this script
API_KEY=123BB12313013 #TicketOS Api Key - This key should be generated in TicketOS and assigned to the same IP in MACHINE_IP
"""


bot = TeleBot(config("TELEGRAM_APIKEY")) 
clients = csv_to_array(config("CLIENTS_FILE"))
create_new_ticket_commands = ['newticket','novoticket'] # Commands accepted to create a new ticket.



@bot.message_handler(commands=["start"])
def hello_world(message):
    """First message sent by the bot, after receiving /start command"""
    bot.reply_to(message, f"""Hello, {message.from_user.first_name}!
    To create a new ticket, please use "/{create_new_ticket_commands[0]} Name, Ticket subject, description of the issue" to create a new ticket""")


@bot.message_handler(commands=create_new_ticket_commands)
def create_new_ticket(message):
    """" Creates a ticket, format: /newticket Name, ticket subject, description of the issue"""
    message_cleared = clear_commands(message.text,*create_new_ticket_commands)
    global ticketsubject
    global ticket_message
    clientname, ticketsubject, ticket_message = message_cleared.split(", ")
    result = get_clients(clientname,clients,0,1)
    keyboard = create_keyboard(result)
    if keyboard:
        bot.reply_to(message,'Choose the User', reply_markup=keyboard)

    else:
         bot.reply_to(message, 'No users were found using the specified search criteria')


@bot.callback_query_handler(func=lambda callback : '@' in callback.data)
def create_ticket_from_menu(call):
    """" Creates the ticket based on the user choice"""
    newticket = create_ticket_ticketos(call.data,ticketsubject,ticket_message)
    bot.edit_message_text(newticket,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="markdown"
    )

@bot.callback_query_handler(func=lambda callback : 'cancel' in callback.data)
def cancel_operation(call):
    """" Cancles the operation"""
    bot.edit_message_text('Operation aborted',
        call.message.chat.id,
        call.message.message_id,
        parse_mode="markdown"
    )

@bot.edited_message_handler(commands=create_new_ticket_commands)
def edited_message(message):
    """When a create ticket message is edited, the bot searches using the new parameters"""
    bot.reply_to(message,'Finding users using the edited message')
    create_new_ticket(message)

"""Displays the loaded Clients"""
print(clients)

"""Starts receiving message"""
bot.polling()


