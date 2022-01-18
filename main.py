from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import configparser
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import Button, Select, SelectOption, ComponentsBot
from discord_components import *
import pytesseract
import cv2
import os

config = configparser.ConfigParser()

if os.path.exists('config.ini') == False:
    config['DEFAULT'] = {'bot_token': '123xyz','bot_prefix': '!','guild_ids': '123456789101234567,123456789012345678'}
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

bot_prefix = config['DEFAULT']['bot_prefix']
bot_token = config['DEFAULT']['bot_token']

database_username = config['DATABASE']['db_username']
database_password = config['DATABASE']['db_password']
database_ip = config['DATABASE']['db_ip']
database_port = config['DATABASE']['db_port']

bot = ComponentsBot(bot_prefix)

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#guild_ids = config['DEFAULT']['guild_ids'].split(',')
guild_ids = 713068366419722300

@bot.event
async def on_ready():
    """On ready event!"""
    print("Logged in as " + str(bot.user))
    print("User ID: " + str(bot.user.id))
    
    await bot.change_presence(activity=discord.Game(name="!analyse"))

@bot.command()
async def analyse(ctx):
    await ctx.send('Analyse command called')

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    

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

    team_one_LEFT = 740
    team_one_RIGHT = 1102

    team_one_TOP_one = 300
    team_one_BOTTOM_one = 321

    red_lower_limit_one = 83
    red_upper_limit_one = 91

    red_lower_limit_two = 110
    red_upper_limit_two = 120

    green_lower_limit_one = 91
    green_upper_limit_one = 105

    green_lower_limit_two = 150
    green_upper_limit_two = 160

    blue_lower_limit_one = 117
    blue_upper_limit_one = 130

    blue_lower_limit_two = 41
    blue_upper_limit_two = 45


    for x in range(6):

        im1 = im.crop((team_one_LEFT, team_one_TOP_one, team_one_RIGHT, team_one_BOTTOM_one))
        im1.save("name.png")

        rgb_im = im1.convert('RGB')
        r, g, b = rgb_im.getpixel((1, 1))
        r2, g2, b2 = rgb_im.getpixel((1, 2))
        r3, g3, b3 = rgb_im.getpixel((2, 1))
        r4, g4, b4 = rgb_im.getpixel((2, 2))
        r5, g5, b5 = rgb_im.getpixel((330, 4))
        r6, g6, b6 = rgb_im.getpixel((330, 5))
        r7, g7, b7 = rgb_im.getpixel((332, 4))
        r8, g8, b8 = rgb_im.getpixel((332, 5))

        r = (r + r2 + r3 + r4 + r5 + r6 + r7 + r8) / 8
        g = (g + g2 + g3 + g4 + g5 + g6 + g7 + g8) / 8
        b = (b + b2 + b3 + b4 + b5 + b6 + b7 + b8) / 8

        if ((r >= red_lower_limit_one and r <= red_upper_limit_one) or  (r >= red_lower_limit_two and r <= red_upper_limit_two)) and ((g >= green_lower_limit_one and g <= green_upper_limit_one) or (g >= green_lower_limit_two and g <= green_upper_limit_two)) and ((b >= blue_lower_limit_one and b <= blue_upper_limit_one) or (b >= blue_lower_limit_two and b <= blue_upper_limit_two)):

            img = cv2.imread("name.png")
            text = pytesseract.image_to_string(img)

            await ctx.send(text)
        else:
            await ctx.send("Failed RGB test:\nRGB = " + str(r) + " " +  str(g) + " " + str(b),file=discord.File('name.png'))

        team_one_TOP_one += 80
        team_one_BOTTOM_one += 80


    


bot.run(bot_token)