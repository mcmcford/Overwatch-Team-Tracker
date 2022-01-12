from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import configparser
import interactions
import pytesseract
import cv2
import os

config = configparser.ConfigParser()

if os.path.exists('config.ini') == False:
    config['DEFAULT'] = {'bot_token': '123xyz','guild_ids': '123456789101234567,123456789012345678'}
    config['DATABASE'] = {'db_username': 'defaultusername','db_password': 'defaultpassword','db_ip': 'dbip','db_port': '3306'}
    #config['RESOURCES'] = {'tesseract_path': 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Please go to config.ini and enter your bots details and preferences")
    exit()

config.read('config.ini')

global db
global configdb
global db_ip

bot_token = config['DEFAULT']['bot_token']

database_username = config['DATABASE']['db_username']
database_password = config['DATABASE']['db_password']
database_ip = config['DATABASE']['db_ip']
database_port = config['DATABASE']['db_port']

bot = interactions.Client(token=bot_token)

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#guild_ids = config['DEFAULT']['guild_ids'].split(',')
guild_ids = 713068366419722300

@bot.command(
    name='analyse',
    description='Analyse a given image',
    scope=guild_ids
)
async def _analyse(ctx, *args):
    await ctx.send('Analyse command called')

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    # get the image the user sent
    # for some reason this isn't getting attachments
    image = ctx.message.attachments
    print(image)
    # get the image url
    image_url = image.url

    try:
        print(ctx.message.attachments[0].url)
    except:
        await ctx.send("please upload a screenshot of your game")
        return
    
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    url = ctx.message.attachments[0].url
    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(url,None,headers) #The assembled request
    r = urllib.request.urlopen(request)
    with open("FULL_IMAGE.jpg", "wb") as f:
        f.write(r.read())
    
    
    image_to_process = 'FULL_IMAGE.jpg'

    im = Image.open(image_to_process)

    im.save("temp_1.png")

    img = cv2.imread("temp_1.png")
    text = pytesseract.image_to_string(img)

    print(text)
    await ctx.send(text)


bot.start()