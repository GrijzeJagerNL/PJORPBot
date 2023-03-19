import os
import sys
import flask
import random
import discord
import threading
from replit import db
from discord.utils import get
from cmds import Commands as cmd
from cmds import DevCommands as Dcmd
from cmds import OwnerCommands as Ocmd

global debugMode

if len(sys.argv) >= 2:
    global debugMode
    debugMode = bool(sys.argv[1])
else:
    debugMode = None

debugMode = debugMode

vRoles = {
    "zeus": "⚡️zeus",  #1056134117219123220
    "poseidon": "🌊poseidon",  #1056134486812803084
    #"hera": "hera", #1056134631570800650
    "dementer": "🌷demeter",  #1056134771333419138
    "ares": "⚔️Ares",  #1056134882289528842
    "athena": "🗺️ Athena",  #1056135002712190976
    "apollo": "🏹 Apollo",  #1056135146773950504
    #"artemis": "🚺 Artemis", #1056135235739336704
    "hephaustus": "🛠️ hephaustus",  #1056135414035001414
    "aphrodite": "❤️ Aphrodite",  #1056135564862173216
    "hermes": "🌬️hermes",  #1056135696219390032
    "dionysus": "🍷 Dionysus",  #1056135820630831114
    "hades": "💀 Hades"  #1056135933029777408
}

clr = {"dev": [673509755196801057], "owner": [1002956183721758730]}

client = discord.Client(intents=discord.Intents.all())


def decorater1(data1, data2):
    def clearance(func):
        if data2.author.id not in clr[data1]: return
        func()
    return clearance


async def dbH(data1, data2):
    if data1 == "get":
        end = []
        for i in db[data2]:
            end.append(i)
        return end

async def cClr(data1, data2):
    if data2 in clr[data1]: return True
    else: return False

async def check(msg):
    if debugMode == True:
        if msg.author.id != 673509755196801057: await msg.channel.send("Bot is in restricted mode and will not process your command."); return False
        else: await msg.channel.send("Bot is in restricted mode."); return True

@client.event
async def on_ready():
    print(f"{client.user} has connected.")

@client.event
async def on_message(msg):
    global debugMode

    if msg.author == client.user: return

    split = str.split(msg.content, " ")

    if split[0] == "random":
        if await check(msg) == False: return
        if split[1] == "character":
            await cmd.random(msg, split[1], None)
        if len(split) != 3:
            await msg.channel.send("> Incorrect number of arguments."); return
        await cmd.random(msg, split[1], split[2])

    if split[0] == "jointeam":
        if await cClr("dev", msg.author.id) == True:
            if db["teams"].__contains__(split[1]): team = split[1]
            else:
                await msg.channel.send("> Team doesn't exsist."); return
            if db["teams"][team].__contains__(str.lower(split[2])):
                await msg.channel.send("> You're already in that team."); return
            else:
                db["teams"][team].append(split[2])
                await msg.channel.send(f"> {split[2]} join team {team}")

    if split[0] == "leaveteam":
        if await cClr("dev", msg.author.id) == True:
            if db["teams"].__contains__(split[1]): team = split[1]
            else:
                await msg.channel.send("> Team doesn't exsist."); return
            if db["teams"][team].__contains__(str.lower(split[2])) == False:
                await msg.channel.send("> You're not in that team."); return
            else:
                db["teams"][team].remove(split[2])
                await msg.channel.send(f"> {split[2]} left team {team}")

    if split[0] == "join":
        if await check(msg) == False: return
        await cmd.join(msg, split[1])

    if split[0] == "leave":
        if await check(msg) == False: return
        await cmd.leave(msg, split[1])

    if split[0] == "playing":
        if await check(msg) == False: return
        await msg.channel.send(await dbH("get", "active"))

    if split[0] == "name":
        if await check(msg) == False: return
        await msg.author.edit(nick=split[1])

    if split[0] == "role":
        if await check(msg) == False: return
        if split[1] == "add":
            if vRoles.get(str.lower(split[2])) == None:
                await msg.channel.send("> Role doesn't exsist."); return
            role = get(msg.author.guild.roles, name=vRoles[str.lower(split[2])])
            await msg.author.add_roles(role)

        if split[1] == "remove":
            if vRoles.get(str.lower(split[2])) == None:
                await msg.channel.send("> Role doesn't exsist.")
                return
            role = get(msg.author.guild.roles, name=vRoles[str.lower(split[2])])
            await msg.author.remove_roles(role)

    if split[0] == "cmds" or msg.content == "help":
        if await check(msg) == False: return
        await msg.channel.send("""```
cmds, shows a list of all possible commands and basic usage.
help, shows a list of all possible commands and basic usage.
        
random [number] [number], this gives a random number between the first and second one.
random character, this gives a random name from everybody in the "playing" list.

join [name], this adds a name to the list of characters being played.
leave [name], removes a namve from the list of characters being played.
playing, says all characters currently playing.

name [name], sets your nickname to the given name.

role [add/remove] [role name], removes or adds a role from a god(ess)

list of possible gods to get roles from:
    zeus,
    poseidon,
    dementer,
    ares,
    athena,
    apollo,
    hephaustus,
    aphrodite,
    hermes,
    dionysus,
    hades
```""")

    @decorater1("dev", msg)
    def exitF():
        if msg.content == "exit":
            Dcmd.exit(msg, False)

def start():
    client.run(os.getenv("BOT_KEY"))

th = threading.Thread(target=start, name="test")
th.start()

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Bot up and running"

@app.route("/404")
def index1():
    return "Page not found"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=debugMode, port=80)