#!/usr/bin/python3

import nextcord
from nextcord.ext import commands
from nextcord import message
import subprocess
import datetime
from nextcord import Interaction


import os

intents = nextcord.Intents.default()

TOKEN = "Your token"
TERMINAL_CHANNEL = 1109885908595003432 #Replace with your terminal channel ID
LOG_CHANNEL = 1109885938143871088 #Replace with your log channel ID

bot = commands.Bot(intents=intents)
intents.message_content = True


def timeget():
    global date
    date = datetime.datetime.now()


@bot.event
async def on_ready():
    timeget()
    print(f'We have logged in as {bot.user} at {date}\n')

    # Send ignition message in log channel
    startembed = nextcord.Embed(title = "**Ignition !**", description = "Started at " + str(date) , color = 0x0083FF)
    await bot.get_channel(LOG_CHANNEL).send(embed=startembed)
    await bot.change_presence(status=nextcord.Status.online)
    await bot.change_presence(activity = nextcord.Game(name="/commands"))

@bot.slash_command(name="infos", description="Infos about the bot")
async def info_en(interaction: Interaction):
    infoembed = nextcord.Embed(title="**Infos**", description= 
        "**What is it for :**\n\n" +
        "This bot allows you to __interact with a Linux session__ by directly using a Discord channel as a terminal.\n" +
        "(for now, not all commands are supported and some of them are restricted)\n\n" +
        "**Who made it :**\n\n" +
        "This bot was created by __**Darkpepito**__, with the help of __**OmégaXx**__ (creator of the Demona bot)."
        , color= 0x00ff00
    )
    await interaction.response.send_message(embed=infoembed)


@bot.slash_command(name="comands", description="Show base commands you will surely need")
async def commands_en(interaction: Interaction):
    helpembed = nextcord.Embed(title="**Commands**", description= 
        "__**Some commands to be started with the Linux terminal :**__\n" + "\n" +
        "`pwd`  Show the current active directory.\n\n" + 
        "`cd [DIR]` : Allow to navigate through directories.\n\n" +
        "`ls [OPTION] [Dir]` : List the content of a directory. If dir isn't specified, list content of current directory. Options can be `-a` to list hidden directories and files, or `-l` to list many info for each file and directory.\n" + "\n" +
        "`mkdir [DIR]` : Create an empty directory.\n\n" + 
        "`touch [FILE]` : Create an empty file.\n\n" +
        "`cp [OPTION] [DIR or FILE]` : Copy past a file (or a directory if you use the `-r` option).\n\n" + 
        "`cat [FILE]` : Show the content of a file.\n\n" +
        "__**We can't be exhaustive, so don't hesitate to mak your own researches if you need it. You can also know what a command does by doing `[COMMAND] --help` !**__", color= 0x00ff00
    )
    await interaction.response.send_message(embed=helpembed)


# mainfunction start here :
@bot.event
async def on_message(message):
    if message.author != bot.user and message.channel.id == TERMINAL_CHANNEL:
        
        user = message.author
        cmd_input = message.content


        # Verify for unexecutable commands                                                                                                                                                                                                                                                                                                                                                                                                                                 ...yeah it's very long.
        if "cd " not in message.content and "poweroff" not in message.content and "shutdown" not in message.content and "sleep" not in message.content and "dd " not in message.content and message.content != "dd" and "sudo " not in message.content and "su " not in message.content and message.content != "su" and ".botnix.py" not in message.content and ".private" not in message.content and message.content != "clear" and "nano " not in message.content and message.content != "nano":
            
            # Setup command process and get output and error code
            cmd = subprocess.Popen(cmd_input,stdout=subprocess.PIPE, shell=True)
            (output, err) = cmd.communicate()
            cmd_status = cmd.wait()
            
            # Reformat output to utf-8
            output=str(output, "utf-8")
            
            # Send message for long output
            if output and len(output) > 1999:
                output = "Output is too long."


            # Send message for unknown command
            elif cmd_status == 127:
                output= "Unknown command."
            
            # Send message for permission denied or path doesn't exist
            elif cmd_status == 1 or cmd_status == 2:
                output="Permission denied or file/path doesn't exist."
            
        # Instead of real cd command, we change the script's active dir
        elif "cd " in message.content:
        
            # Slice input to get only the path name
            directory = message.content[:0] + message.content[3:]
            
            # Change active dir
            os.chdir(directory)
            
            # Print infos etc.
            output = "Action ended."
            cmd_status = 0
        

        # Check for forbidden commands or files they don't have to edit
        elif "poweroff" in message.content or "shutdown" in message.content or "sleep" in message.content or "dd " in message.content or message.content == "dd" or "sudo " in message.content or "su " in message.content or message.content == "su" or ".botnix.py" in message.content or ".private" in message.content:
            
            # Print infos etc.
            cmd_status = 127
            
            # Mock them
            output="Stop being a script kiddie lmao."
            
        # Check for not working commands
        elif "nano" in message.content or message.content == "clear":
            
            # Print infos etc.
            output = "Impossible action."
            cmd_status = 127
            
            # Define terminal output
            output = "This command isn't usable for now, maybe in the future..."
       
        # In case of, to avoid error below
        else:
            output = "?"
            cmd_status = 127
        
        print("User : "+str(user))
        print("Input : "+cmd_input)
        print("Output: "+output)
        print("Exit code : "+str(cmd_status))
        print("--------------------------------")
        await message.channel.send(output)
    
        # Here we setup embed message...
        # And send it to the log channe1
        embed = nextcord.Embed(title = date , description ="User : " + str(message.author) + "\n" + "Input : " + str(message.content) +"\n"+"Output : " + output +"\n"+ "Exit code : "+ str(cmd_status), color = 0x00ff00)
        await bot.get_channel(LOG_CHANNEL).send(embed=embed)

bot.run(TOKEN)

