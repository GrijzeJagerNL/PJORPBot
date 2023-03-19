import os
import random
from replit import db

class Commands():
    async def random(msg, data1, data2):
        if data1 == "character":
            await msg.channel.send(db["active"][random.randint(0, len(db["active"])-1)]); return
        if data1.isdigit() == False:
            await msg.channel.send("> 1st argument isn't a number."); return
        if data2.isdigit() == None:
            await msg.channel.send("> 2nd argument isn't a number."); return
        if int(data1) > int(data2):
            await msg.channel.send("> 1st number must be lower as the 2nd."); return
        await msg.channel.send(f"> {random.randint(int(data1), int(data2))}")

    async def join(msg, data1):
        if db["active"].__contains__(str.lower(data1)):
            await msg.channel.send(f"{data1} is already in the RP."); return
        db["active"].append(str.lower(data1))
        await msg.channel.send(f"> {data1} joined the RP."); return

    async def leave(msg, data1):
        if db["active"].__contains__(str.lower(data1)) == False:
            await msg.channel.send(f"> {data1} isn't in the RP."); return
        db["active"].remove(str.lower(data1))
        await msg.channel.send(f"> {data1} left the RP.")

class OwnerCommands:
    pass

class DevCommands:
    def exit(msg, data1):
        if data1 == False:
            os._exit(1)

    async def restart(msg, data1):
        pass