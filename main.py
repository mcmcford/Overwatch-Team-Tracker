import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import configparser
import discord
import random as rand
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import Button, Select, SelectOption, ComponentsBot
from discord_components import *
import pytesseract
import cv2
import os
import time

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

    users = []


    for x in range(2):
        top = 300
        bottom = 321

        if x == 0:

            left = 740
            right = 1102

            pfp_left = 670
            pfp_right = 740
            pfp_bottom = bottom + 42
            pfp_top = top - 6

            red_lower_limit_one = 83
            red_upper_limit_one = 91

            red_lower_limit_two = 110
            red_upper_limit_two = 124

            green_lower_limit_one = 91
            green_upper_limit_one = 105

            green_lower_limit_two = 150
            green_upper_limit_two = 162

            blue_lower_limit_one = 117
            blue_upper_limit_one = 130

            blue_lower_limit_two = 41
            blue_upper_limit_two = 50
        
        else:
            left = 1290
            right = 1652
            
            pfp_left = 1220
            pfp_right = 1290
            pfp_bottom = bottom + 42
            pfp_top = top - 6

            red_lower_limit_one = 155
            red_upper_limit_one = 170

            green_lower_limit_one = 35
            green_upper_limit_one = 48

            blue_lower_limit_one = 50
            blue_upper_limit_one = 60


        for x in range(6):

            im1 = im.crop((left, top, right, bottom))

            # generate a random number between 0 and 9999999999, padding the left with zeros to keep them all the same length
            random_number = str(rand.randint(0, 9999999999)).zfill(10)
            name_image = f"name-{random_number}.png"


            im1.save(name_image)

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


                pfp_image = f"pfp-{random_number}.png"

                img = cv2.imread(name_image)
                text = pytesseract.image_to_string(img)

                im2 = im.crop((pfp_left, pfp_top, pfp_right, pfp_bottom))
                im2.save(pfp_image)

                # remove anything after any spaces (such as the users full name if they're friends)
                try:
                    text = (text.split())[0]
                except:
                    text = text

                users.append([text, random_number])

                #await ctx.send(text,file=discord.File(name_image))
                #await ctx.send(file=discord.File(pfp_image))
            else:
                await ctx.send("Failed RGB test:\nRGB = " + str(r) + " " +  str(g) + " " + str(b),file=discord.File(name_image))

            top += 80
            bottom += 80
            pfp_top += 80
            pfp_bottom += 80


    for x in users:
        print(x)  
    
    option = webdriver.ChromeOptions()
    # I use the following options as my machine is a window subsystem linux. 
    # I recommend to use the headless option at least, out of the 3
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')

    driver = webdriver.Chrome('C:\\Users\\morga\\Documents\\GitHub\\Overwatch-Team-Tracker\\chromedriver.exe', options=option)

    for x in range(len(users)):
        
        name = users[x][0]

        driver.get("https://www.overbuff.com/search?q=" + name) # Getting page HTML through request
        
        print(str(x) + " in " + str(len(users)))
        print(users)
        
        not_found = False
        multi_users = []
        
        # wait for page to load players
        try:
            elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'SearchResult')))
            time.sleep(10)
        except selenium.common.exceptions.TimeoutException:
            not_found = True
        finally:
            soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
        
        if not_found == False:
            #print(soup)

            title = soup.title.text
            links = soup.find_all('a')

            links_split = str(links).split("<a class=\"SearchResult\"")
            links_split = links_split[1:] # remove first index in the array
            
            if len(links_split) > 1:
                multi_users.append([])
            
            for y in range(len(links_split)):
                
                if y == len(links_split) -1:
                    
                    temp = links_split[y].split(", <a class=\"\" href=\"/about\">About</a>, ")
                    links_split[y] = temp[0]
                
                # get URL
                temp = links_split[y].split("href=\"")
                end = (temp[1].split("\">"))[0].replace(" ", "%20")
                url = "https://www.overbuff.com" + end
                
                # get icon
                temp = links_split[y].split("<img class=\"image-player image-icon\" src=\"")
                icon = (temp[1].split("\"/>"))[0]
                
                if "cloudfront" in icon:
                    print("")
                else:
                    icon = "https://www.overbuff.com" + icon
                
                # get level
                temp = links_split[y].split("player-level\">")
                level = (temp[1].split("</div>"))[0]
                
                try:
                    # get blizzard ID
                    temp = url.split("/")
                    temp = temp[-1].split("-")
                    name = temp[0] + "#" + temp[1].replace("%20", " ")
                except:
                    name = (url.split("/"))[-1]
                
                print("URL: " + url)
                print("icon: " + icon)
                print("level: " + level)
                print("name: " + name)
                
                if len(links_split) > 1:
                    multi_users[len(multi_users)-1].append([])
                    multi_users[len(multi_users)-1][y].append(url)
                    multi_users[len(multi_users)-1][y].append(icon)
                    multi_users[len(multi_users)-1][y].append(level)
                    multi_users[len(multi_users)-1][y].append(name)
                    
                else:

                    # send an embed

                    embed = discord.Embed(title=name, description="View this player [here](" + url +")")
                    embed.add_field(name='Level', value=level)
                    embed.set_thumbnail(url=icon)
                    embed.set_footer(text="Provided by Morgan")
                    await ctx.send(embed=embed)
                
                print("\n\n")
            
            if len(multi_users) > 0:
                for y in multi_users:
                    print(y)


bot.run(bot_token)