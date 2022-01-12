import configparser
import os

config = configparser.ConfigParser()

if os.path.exists('config.ini') == False:
    config['DEFAULT'] = {'bot_token': '123xyz'}
    config['DATABASE'] = {'db_username': 'defaultusername','db_password': 'defaultpassword','db_ip': 'dbip','db_port': '3306'}
    config['RESOURCES'] = {'tesseract_path': 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Please go to config.ini and enter your bots details and preferences")
    exit()

config.read('config.ini')

global db
global configdb
global db_ip

bot_token = config['DEFAULT']['bot_token']
bots_prefix = config['DEFAULT']['bots_prefix']

database_username = config['DATABASE']['db_username']
database_password = config['DATABASE']['db_password']
database_ip = config['DATABASE']['db_ip']
database_port = config['DATABASE']['db_port']