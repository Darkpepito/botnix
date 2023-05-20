import nextcord
from nextcord.ext import commands
from nextcord import message
import subprocess
import datetime
from nextcord import Interaction


import os

intents = nextcord.Intents.default()

TOKEN = "YOUR_TOKEN"
CHANNEL_ID = 1068901309148823683 #Replace with your channel ID
LOG_CHANNEL = 1069237276112081017 #Replace with your log channel ID

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
    await bot.get_channel(1069237276112081017).send(embed=startembed)
    await bot.change_presence(status=nextcord.Status.online)
    await bot.change_presence(activity = nextcord.Game(name="/commands-fr"))

@bot.slash_command(name="info-en", description="Infos about the bot")
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

@bot.slash_command(name="info-fr", description="Infos sur le bot")
async def info_fr(interaction: Interaction):
    infoembed = nextcord.Embed(title="**Infos**", description= 
        "**À quoi sert-il :**\n\n" +
        "Ce bot vous permet d'__interargir avec une session Linux__ directement en utilisant un salon Discord comme terminal.\n" +
        "(pour l'instant, toutes les commandes ne sont pas supportées et certaines sont restreintes)\n\n" +
        "**Qui l'a créé :**\n\n" +
        "Ce bot a été créé par __**Darkpepito**__, avec l'aide d' __**OmégaXx**__ (créateur du bot Demona)."
        , color= 0x00ff00
    )
    await interaction.response.send_message(embed=infoembed)

@bot.slash_command(name="comands-en", description="Show base commands you will surely need")
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

@bot.slash_command(name="comands-fr", description="Montre les commandes de bases dont vous aurez suremnt besoin")
async def commands_fr(interaction: Interaction):
    helpembed = nextcord.Embed(title="**Commandes**", description= 
        "__**Quelques commandes pour débuter avec le terminal Linux :**__\n" + "\n" +
        "`pwd` : Montre le répertoire actuel.\n\n" + 
        "`cd [DIR]` : Permet de naviguer entre les répertoires.\n\n" +
        "`ls [OPTION] [Dir]` : Liste le contenu d'un répertoire. Si le répertoire n'est pas spécifié, il list le contenu du répertoire actuel. Les options peuvent être `-a` pour lister les répertoires et fichiers cachés ou `-l` pour lister beaucoup d'infos sur chaque fichier et répertoire.\n" + "\n" +
        "`mkdir [DIR]` : Créer un répertoire vide.\n\n" + 
        "`touch [FILE]` : Créer un fichier vide.\n\n" +
        "`cp [OPTION] [DIR or FILE]` : Cpie-colle un fichier (ou un répertoire si vous utilisez l'option `-r` ).\n\n" +
        "`cat [FILE]` : Montre le contenu d'un fichier.\n\n" +
        "__**Nous ne pouvont pas être exaustif, donc n'hésitez pas à faire vos propres recherches si vous en avez besoin. Vous pouvez également savoir ce que fait une commande en faisant `[COMMAND] --help` !**__", color= 0x00ff00
    )
    await interaction.response.send_message(embed=helpembed)


# mainfunction start here :
@bot.event
async def on_message(message):
    if message.author != bot.user and message.channel.id == CHANNEL_ID:
        
        # Print general infos in terminal
        timeget()
        print(date)
        print("User      : ", message.author)
        print("Input     : ", message.content)


        # Verify for unexecutable commands                                                                                                                                                                                                                                                                                                                                                                                                                                 ...yeah it's very long.
        if "cd " not in message.content and "poweroff" not in message.content and "shutdown" not in message.content and "sleep" not in message.content and "dd " not in message.content and message.content != "dd" and "sudo " not in message.content and "su " not in message.content and message.content != "su" and ".botnix.py" not in message.content and ".private" not in message.content and message.content != "clear" and "nano " not in message.content and message.content != "nano":
            
            # Setup message as command
            cmd_input = message.content
            
            # Setup command process and get output and error code
            cmd = subprocess.Popen(cmd_input,stdout=subprocess.PIPE, shell=True)
            (output, err) = cmd.communicate()
            cmd_status = cmd.wait()
            
            # Reformat output to utf-8
            output=str(output, "utf-8")
            

            if output and len(output) <= 3999:
                print("Output    : ", output)

            elif len(output) >= 3999:
                # Print info if no output
                print("Action terminated.")
                output = "Action terminated"
                
            print("Exit code : ", cmd_status)
            print("--------------------------------")
            
            # Send message for normal output
            if output and len(output) <= 3999 and cmd_status != 1 and cmd_status != 2:
                await message.channel.send(output)
            
            elif output and len(output) > 3999:
                await message.channel.send("Output is too long.")


            # Send message for unknown command
            elif cmd_status == 127:
                await message.channel.send("Unknown command.")
            
            # Send message for permission denied or path doesn't exist
            elif cmd_status == 1 or cmd_status == 2:
                await message.channel.send("Permission denied or file/path doesn't exist.")
            else:
                await message.channel.send("Action terminated.")
            
        # Instead of real cd command, we change the script's active dir
        elif "cd " in message.content:
        
            # Slice input to get only the path name
            directory = message.content[:0] + message.content[3:]
            
            # Change active dir
            os.chdir(directory)
            
            # Print infos etc.
            print("Action terminated.")
            output = "Action terminated."
            cmd_status = 0
            print("--------------------------------")
            await message.channel.send("Action terminated.")
       
        # Check for forbidden commands or files they don't have to edit
        elif "poweroff" in message.content or "shutdown" in message.content or "sleep" in message.content or "dd " in message.content or message.content == "dd" or "sudo " in message.content or "su " in message.content or message.content == "su" or ".botnix.py" in message.content or ".private" in message.content:
            
            # Print infos etc.
            print("Impossible action.")
            output = "Impossible action."
            cmd_status = 127
            print("--------------------------------")
            
            # Mock them
            await message.channel.send("Stop being a script kiddie lmao.")
            
        # Check for not working commands
        elif message.content == "clear" or "nano " in message.content or message.content == "nano":
            
            # Print infos etc.
            print("Impossible action.")
            output = "Impossible action."
            cmd_status = 127
            print("--------------------------------")
            
            # Send a message
            await message.channel.send("This command isn't usable for now, maybe in the future...")
       
        # In case of, to avoid error below
        else:
            output = "?"
            cmd_status = 127
    
        # Here we setup embed message...
        if len(output) <= 39999:
            embed = nextcord.Embed(title = date , description ="User : " + str(message.author) + "\n" + "Input : " + str(message.content) +"\n"+"Output : " + output +"\n"+ "Exit code : "+ str(cmd_status), color = 0x00ff00)
        else:
            embed = nextcord.Embed(title = date , description ="User : " + str(message.author) + "\n" + "Input : " + str(message.content) +"\n"+"Output : " + "too long" +"\n"+ "Exit code : "+ str(cmd_status), color = 0x00ff00)
        # And send it to the log channe1068901309148823683l
        await bot.get_channel(LOG_CHANNEL).send(embed=embed)

bot.run(TOKEN)

