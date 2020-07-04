# Telegram-TicketOs-Bot

You can now create tickets on TicketOS directly from Telegram!

## Installation

You will need pip to install the script requirements. The safer way to get your requirements installed without affecting any other Python project you have is using virtualenv

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
git clone https://github.com/saulo-m/telegramticketos.git
cd telegramticketos
virtualenv .venv
source activate .venv/bin/activate
pip install -r requirements.txt

```

## Usage

Edit the **.env** file, located at the project root directory,  using your settings, then run this script.

```
example:
TELEGRAM_APIKEY=121231313:AAaabbbb123 #Telegram API Key. Message @botfather on telegram to get one.
CLIENTS_FILE=users.csv # Semicolon delimited CSV file containing the TicketOS Users and their respective e-mail addresses (format: name;email)
TICKETOS_URL=http://example.domain.com/api/tickets.json #URL to TicketOS API
MACHINE_IP=172.16.0.1 #IP address of the machine running this script
API_KEY=123BB12313013 #TicketOS Api Key - This key should be generated in TicketOS and assigned to the same IP address set in MACHINE_IP
```

To create a new ticket, send a message in the following format:
```/newticket Name, Ticket Subject, Issue```. 

You can also edit a */newticket* message and the bot will redo the search using the new parameters.


## Generating a CSV users's file from Active Directory

If your TicketOS is integrated with an Active Directory server, you may use the following command in PowerShell to export Active Directory Users to a suitable file.

```get-aduser –filter * -property * | Select-object Name, mail  | Export-Csv users.csv -Delimiter ";" -NoTypeInformation```

**IMPORTANT**: You can't create tickets for users that don't exist in your TicketOS installation, even if you have it integrated with an Active Directory server.  You need first to confirm those AD users using the web interface, then you may create tickets directly from Telegram.

## TODO
Active directory integration.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
