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
import mariadb
import sys
import base64
import datetime

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
database_port = int(config['DATABASE']['db_port'])

bot = ComponentsBot(bot_prefix)

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#guild_ids = config['DEFAULT']['guild_ids'].split(',')
guild_ids = 713068366419722300

class connect():
    def __init__(self):
        # Connect to MariaDB Platform
        try:
            self.db = mariadb.connect(
                user=database_username,
                password=database_password,
                host=database_ip,
                port=database_port,
                database="overwatch"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        # Get Cursor
        self.cursor = self.db.cursor()
    
def disconnect(database):

    try:
        # Disconnect from MariaDB Platform
        cur = database.cursor
        d = database.db
        cur.close()
        d.close()
    except mariadb.Error as e:
        print(f"Error disconnecting from MariaDB Platform: {e}")


@bot.event
async def on_ready():
    """On ready event!"""
    print("Logged in as " + str(bot.user))
    print("User ID: " + str(bot.user.id))
    
    await bot.change_presence(activity=discord.Game(name="!analyse"))

@bot.command(aliases=['a'])
async def analyse(ctx):
    await ctx.send('Analyse command called')

    # connect to database
    database = connect()
    cursor = database.cursor
    db = database.db

    
    # get the last row in the games table
    cursor.execute("SELECT game_id FROM games ORDER BY game_id DESC LIMIT 1")
    last_game = cursor.fetchone()

    if last_game is None:
        game_id = 0
    else:

        game_id = int(last_game[0]) + 1

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

    level_top_tune = 28
    level_bottom_tune = 23
    level_left_tune = 12
    level_right_tune = 60

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

            level_buttom = bottom+level_bottom_tune
            level_top = top + level_top_tune
            level_left = pfp_right + level_left_tune
            level_right = pfp_right + level_right_tune

            red_lower_limit_one = 80
            red_upper_limit_one = 91

            red_lower_limit_two = 110
            red_upper_limit_two = 124

            green_lower_limit_one = 91
            green_upper_limit_one = 105

            green_lower_limit_two = 148
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

            level_buttom = bottom+level_bottom_tune
            level_top = top + level_top_tune
            level_left = pfp_right + level_left_tune
            level_right = pfp_right + level_right_tune

            red_lower_limit_one = 155
            red_upper_limit_one = 170

            green_lower_limit_one = 35
            green_upper_limit_one = 48

            blue_lower_limit_one = 50
            blue_upper_limit_one = 62


        for x in range(6):

            im1 = im.crop((left, top, right, bottom))

            # generate a random number between 0 and 999999999999999, padding the left with zeros to keep them all the same length
            random_number = str(rand.randint(0, 999999999999999)).zfill(15)
            name_image = f"name-{random_number}.png"


            im1.save(name_image)

            # checking colours to rule out missing players
            rgb_im = im1.convert('RGB')
            r, g, b = rgb_im.getpixel((1, 1))
            r2, g2, b2 = rgb_im.getpixel((1, 2))
            r3, g3, b3 = rgb_im.getpixel((2, 1))
            r4, g4, b4 = rgb_im.getpixel((2, 2))
            r5, g5, b5 = rgb_im.getpixel((330, 4))
            r6, g6, b6 = rgb_im.getpixel((330, 5))
            r7, g7, b7 = rgb_im.getpixel((332, 4))
            r8, g8, b8 = rgb_im.getpixel((332, 5))

            # finding the avg
            r = (r + r2 + r3 + r4 + r5 + r6 + r7 + r8) / 8
            g = (g + g2 + g3 + g4 + g5 + g6 + g7 + g8) / 8
            b = (b + b2 + b3 + b4 + b5 + b6 + b7 + b8) / 8

            if ((r >= red_lower_limit_one and r <= red_upper_limit_one) or  (r >= red_lower_limit_two and r <= red_upper_limit_two)) and ((g >= green_lower_limit_one and g <= green_upper_limit_one) or (g >= green_lower_limit_two and g <= green_upper_limit_two)) and ((b >= blue_lower_limit_one and b <= blue_upper_limit_one) or (b >= blue_lower_limit_two and b <= blue_upper_limit_two)):


                pfp_image = f"pfp-{random_number}.png"
                lvl_image = f"lvl-{random_number}.png"
                full_image = f"full-{random_number}.png"

                img = cv2.imread(name_image)
                text = pytesseract.image_to_string(img)

                im2 = im.crop((pfp_left, pfp_top, pfp_right, pfp_bottom))
                im2.save(pfp_image)

                #im3 = im.crop((level_left-10, top, right-30, level_buttom))
                #im3.save(lvl_image)

                im4 = im.crop((pfp_left, pfp_top, right, pfp_bottom))
                im4.save(full_image)
                

                # remove anything after any spaces (such as the users full name if they're friends)
                try:
                    text = (text.split())[0]
                except:
                    text = text
                
                with open(full_image,'rb') as f:
                    fileData=f.read()



                users.append([text, random_number])
                cursor.execute("INSERT INTO temp_user (local_id, name, image, time, game_id) VALUES (%s, %s, %s, %s, %s)", (str(random_number), text, fileData, time.time(), str(game_id)))
                db.commit()

                # select users from the table users who have the same name as the one we just found
                cursor.execute("SELECT * FROM users WHERE name = %s", (text,))
                result = cursor.fetchall()

                users = []
                # generate random number between 0 and 99999, padding the left with zeros to keep them all the same length
                random_number_comps = str(rand.randint(0, 99999)).zfill(5)

                multiple = True
                opts = []
                descript = ""


                if len(result) == 0:
                    print("New user found: " + text)
                    multiple = False
                else:
                    
                    i = 2

                    for user in result:
                        
                        name_of_image = f"comp-{random_number_comps}-{user[0]}.png"

                        # count the number of times the userID user[0] is in the games table
                        cursor.execute("SELECT COUNT(*) FROM games WHERE user_id = %s", (user[0],))
                        result_count = cursor.fetchone()

                        # get the time value from the users table where the userID is user[0]
                        cursor.execute("SELECT time FROM users WHERE local_id = %s", (user[0],))
                        result_time = cursor.fetchone()

                        # convert the time value from epoch to a readable format
                        result_time = datetime.datetime.fromtimestamp(result_time[0]).strftime('%Y-%m-%d %H:%M:%S')

                        with open(name_of_image, "wb") as fh:
                            fh.write(user[2])
                        
                        if i == 2:
                            opts.append(SelectOption(label=f"{i}nd user", value=f"{random_number},{int(user[0])}"))
                            descript = descript + f"{i}nd user has been logged {result_count[0]} times, last logged {result_time}\n\n"
                        elif i == 3:
                            opts.append(SelectOption(label=f"{i}rd user", value=f"{random_number},{int(user[0])}"))
                            descript = descript + f"{i}rd user has been logged {result_count[0]} times, last logged {result_time}\n\n"
                        else:
                            opts.append(SelectOption(label=f"{i}th user", value=f"{random_number},{int(user[0])}"))
                            descript = descript + f"{i}th user has been logged {result_count[0]} times, last logged {result_time}\n\n"
                        
                        i += 1
                        

                        users.append([user[0], name_of_image,result_count])
                
                
                # stich the image 'full_image' with the images of the users just found, if there is any
                if len(users) > 0:
                    # stitch all the users images together into one image vertically
                    i = 0
                    images = [Image.open(full_image)]
                    for user in users:
                        images.append(Image.open(user[1]))
                    result = Image.new('RGB', (images[0].width, (images[0].height * len(images)) + 10))
                    for i, image in enumerate(images):
                        if i == 0:
                            result.paste(image, (0, (i * images[0].height)))
                            i = 1
                        else:
                            result.paste(image, (0, (i * images[0].height) + 10))
                    result.save(full_image)

                # create a selection for the embed

                buttons = [Button(label="Incorrect Name", custom_id=f"{random_number},IN",style=4,disabled=False),Button(label="Correct Name", custom_id=f"{random_number},CN",style=3,disabled=False)]

                if multiple == True:

                    opts.append(SelectOption(label="None of the above (new user)", value=f"{random_number},New"))

                    # create a button asking if the name is correct
                    comps = [
                        Select(
                            placeholder="Select which user this matches",
                            options=opts,
                            custom_id=f"{game_id}"
                        ),
                        buttons
                        ]
                else:
                    comps = [buttons]

                # send embed to discord, with the image pfp_image as the thumbnail, the image name_image as the image, and the text as the title
                embed = discord.Embed(title=text, url="https://www.overbuff.com/search?q=" + text, description =descript, color=0x00ff00)
                #file = discord.File(pfp_image, filename="image.png")
                #file1 = discord.File(name_image, filename="image2.png")
                #file1 = discord.File(lvl_image, filename="image2.png")
                file1 = discord.File(full_image, filename="image2.png")
                embed.set_image(url="attachment://image2.png")
                await ctx.send(files=[file1], embed=embed, components=comps)
                #embed.set_thumbnail(url="attachment://image.png")
                #await ctx.send(files=[file1,file], embed=embed, components=comps)
            else:
                await ctx.send("Failed RGB test:\nRGB = " + str(r) + " " +  str(g) + " " + str(b),file=discord.File(name_image))

            next_user_in_image = 80

            top += next_user_in_image
            bottom += next_user_in_image
            pfp_top += next_user_in_image
            pfp_bottom += next_user_in_image
            level_top += next_user_in_image
            level_buttom += next_user_in_image
    
    disconnect(database)


    

    '''
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
    '''

# on button press
@bot.event
async def on_button_click(interaction):
    print(interaction.custom_id)

    custom_id = interaction.custom_id

    temp = custom_id.split(",")
    id = temp[0]
    button = temp[1]

    # connect to database
    database = connect()
    cursor = database.cursor
    db = database.db

    # get the  row from the table temp_user based on the id
    cursor.execute("SELECT * FROM temp_user WHERE local_id = %s", (id,))
    row = cursor.fetchone()

    if "CN" in custom_id:
        
        # insert the row into the table user
        cursor.execute("INSERT INTO users (name, image, time) VALUES ( %s, %s, %s)", (row[1], row[2], row[3]))
        db.commit()

        # get the id of the row just inserted
        cursor.execute("SELECT local_id FROM users WHERE name = %s", (row[1],))
        new_id = cursor.fetchone()[0]


        # delete the row from the table temp_user
        cursor.execute("DELETE FROM temp_user WHERE local_id = %s", (id,))
        db.commit()

        # insert the row into the table user
        cursor.execute("INSERT INTO games (game_id, user_id, time) VALUES ( %s, %s, %s)", (row[4], new_id, row[3]))
        db.commit()


        # delete the interaction
        # await interaction.send("User added to the database!", delete_after=5)
        await (interaction.message).delete()
    elif "IN" in custom_id:

        desc = f"Please enter the correct name, as shown in the image below,\n\n this can be done with the command `!correct {id} <name>` eg. `!correct {id} Morgan`"

        # generate random number
        randint = rand.randint(1, 1000000)

        with open(f"temp-{randint}.png", "wb") as fh:
            fh.write(row[2])

        # create an embed
        embed = discord.Embed(title="Name correction", description=desc)
        embed.set_image(url=f"attachment://temp-{randint}.png")

        # send the embed
        await interaction.send(embed=embed, file=discord.File(f"temp-{randint}.png"))
        await (interaction.message).delete()

    
    disconnect(database)
        
# on select option
@bot.event
async def on_select_option(interaction):
    game_id = interaction.custom_id
    
    temp = interaction.values[0].split(",")
    id = temp[0]
    user = temp[1]

    # connect to database
    database = connect()
    cursor = database.cursor
    db = database.db

    if "New" in user:
        # get the  row from the table temp_user based on the id
        cursor.execute("SELECT * FROM temp_user WHERE local_id = %s", (id,))
        row = cursor.fetchone()

        # insert the row into the table user
        cursor.execute("INSERT INTO users (name, image, time) VALUES ( %s, %s, %s)", (row[1], row[2], row[3]))
        db.commit()

        # get the id of the row just inserted
        cursor.execute("SELECT local_id FROM users WHERE name = %s", (row[1],))
        new_id = cursor.fetchone()[0]

        # delete the row from the table temp_user
        cursor.execute("DELETE FROM temp_user WHERE local_id = %s", (id,))
        db.commit()

        # insert the row into the table user
        cursor.execute("INSERT INTO games (game_id, user_id, time) VALUES ( %s, %s, %s)", (row[4], new_id, row[3]))
        db.commit()

        # delete the interaction
        #await interaction.send("User added to the database!", delete_after=5)
        await (interaction.message).delete()
    else:
        # get the  row from the table temp_user based on the id
        cursor.execute("SELECT * FROM temp_user WHERE local_id = %s", (id,))
        row = cursor.fetchone()

        # insert the row into the table user

        cursor.execute("UPDATE users SET image = %s, time = %s WHERE local_id = %s", (row[2], row[3], int(user)))
        db.commit()

        # delete the row from the table temp_user
        cursor.execute("DELETE FROM temp_user WHERE local_id = %s", (id,))
        db.commit()

        # insert the row into the table user
        cursor.execute("INSERT INTO games (game_id, user_id, time) VALUES ( %s, %s, %s)", (row[4], user, row[3]))
        db.commit()

        # delete the interaction
        # await interaction.send("Database Updated!", delete_after=5)
        await (interaction.message).delete()

@bot.command()
async def correct(ctx, id: str = None, name: str = None):
    if id == None or name == None:
        await ctx.send("Please enter a valid command, eg. `!correct <id> <name>`", delete_after=15)
        return

    # delete the message 
    await ctx.message.delete()

    # connect to database
    database = connect()
    cursor = database.cursor
    db = database.db

    # update the name of the user
    cursor.execute("UPDATE temp_user SET name = %s WHERE local_id = %s", (name, id))
    db.commit()

    # get the  row from the table temp_user based on the id
    cursor.execute("SELECT * FROM temp_user WHERE local_id = %s", (id,))
    row = cursor.fetchone()

    # select users from the table users who have the same name as the one we just found
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    result = cursor.fetchall()

    users = []
    # generate random number between 0 and 99999999, padding the left with zeros to keep them all the same length
    random_number_comps = str(rand.randint(0, 99999999)).zfill(5)

    multiple = True
    opts = []
    descript = ""


    full_image = f"full-{random_number_comps}.png"

    with open(full_image, "wb") as fh:
        fh.write(row[2])

    if len(result) == 0:
        print("New user found: " + name)
        multiple = False
    else:
        
        i = 2

        for user in result:
            
            name_of_image = f"comp-{random_number_comps}-{user[0]}.png"

            # count the number of times the userID user[0] is in the games table
            cursor.execute("SELECT COUNT(*) FROM games WHERE user_id = %s", (user[0],))
            result_count = cursor.fetchone()

            # get the time value from the users table where the userID is user[0]
            cursor.execute("SELECT time FROM users WHERE local_id = %s", (user[0],))
            result_time = cursor.fetchone()

            # convert the time value from epoch to a readable format
            result_time = datetime.datetime.fromtimestamp(result_time[0]).strftime('%Y-%m-%d %H:%M:%S')

            with open(name_of_image, "wb") as fh:
                fh.write(user[2])
            
            if i == 2:
                opts.append(SelectOption(label=f"{i}nd user", value=f"{random_number},{int(user[0])}"))
                descript = descript + f"{i}nd user has been logged {result_count[0]} times, last logged {result_time}\n\n"
            elif i == 3:
                opts.append(SelectOption(label=f"{i}rd user", value=f"{random_number},{int(user[0])}"))
                descript = descript + f"{i}rd user has been logged {result_count[0]} times, last logged {result_time}\n\n"
            else:
                opts.append(SelectOption(label=f"{i}th user", value=f"{random_number},{int(user[0])}"))
                descript = descript + f"{i}th user has been logged {result_count[0]} times, last logged {result_time}\n\n"
            
            i += 1
            users.append([user[0], name_of_image])
    
    
    # stich the image 'full_image' with the images of the users just found, if there is any
    if len(users) > 0:
        # stitch all the users images together into one image vertically
        i = 0
        images = [Image.open(full_image)]
        for user in users:
            images.append(Image.open(user[1]))
        result = Image.new('RGB', (images[0].width, (images[0].height * len(images)) + 10))
        for i, image in enumerate(images):
            if i == 0:
                result.paste(image, (0, (i * images[0].height)))
                i = 1
            else:
                result.paste(image, (0, (i * images[0].height) + 10))
        result.save(full_image)

    # create a selection for the embed

    buttons = [Button(label="Incorrect Name", custom_id=f"{row[0]},IN",style=4,disabled=False),Button(label="Correct Name", custom_id=f"{row[0]},CN",style=3,disabled=False)]

    if multiple == True:

        opts.append(SelectOption(label="None of the above (new user)", value=f"{row[0]},New"))

        # create a button asking if the name is correct
        comps = [
            Select(
                placeholder="Select which user this matches",
                options=opts,
                custom_id=f"{row[4]}"
            ),
            buttons
            ]
    else:
        comps = [buttons]

    # send embed to discord, with the image pfp_image as the thumbnail, the image name_image as the image, and the text as the title
    embed = discord.Embed(title=name, url="https://www.overbuff.com/search?q=" + name, description =descript, color=0x00ff00)
    #file = discord.File(pfp_image, filename="image.png")
    #file1 = discord.File(name_image, filename="image2.png")
    #file1 = discord.File(lvl_image, filename="image2.png")
    file1 = discord.File(full_image, filename="image2.png")
    embed.set_image(url="attachment://image2.png")
    await ctx.send(files=[file1], embed=embed, components=comps)
    #embed.set_thumbnail(url="attachment://image.png")
    #await ctx.send(files=[file1,file], embed=embed, components=comps)



bot.run(bot_token)