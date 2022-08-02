import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print('I am ready to help people find game partner!')
  activity = discord.Game(name="letsgame [gamename] [time] [note]")
  await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_raw_reaction_add(payload):
  channel_id = payload.channel_id
  reacted_channel = client.get_channel(channel_id)
  message_id = payload.message_id
  reacted_message = await reacted_channel.fetch_message(message_id)

  if str(payload.emoji) == "🤚":
    for reaction in reacted_message.reactions:
      if str(reaction.emoji) == "🤚":
        if reaction.count > 1:
          if("Let's Game 一起开黑" in reacted_message.content):
            if("<@" + str(payload.member.id) + ">" not in reacted_message.content):
              if("已参与玩家：尚无" in reacted_message.content):
                updated = reacted_message.content
                updated = updated.replace("已参与玩家：尚无","已参与玩家："+"<@" + str(payload.member.id) + ">  ")
                await reacted_message.edit(content=updated)
              else:
                updated = reacted_message.content
                updated = updated +"<@" + str(payload.member.id) + ">  "
                await reacted_message.edit(content=updated)
            await reacted_message.remove_reaction(payload.emoji.name , payload.member)

  if str(payload.emoji) == "❎":
    for reaction in reacted_message.reactions:
      if str(reaction.emoji) == "❎":
        if reaction.count > 1:
          if("Let's Game 一起开黑" in reacted_message.content):
            if("<@" + str(payload.member.id) + ">" in reacted_message.content):
              updated = reacted_message.content
              updated = updated.replace("<@" + str(payload.member.id) + ">","")
              if updated.endswith('已参与玩家：'):
                updated = updated.replace('已参与玩家：','已参与玩家：尚无')
              await reacted_message.edit(content=updated)
            await reacted_message.remove_reaction(payload.emoji.name , payload.member)

          

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("letsgame"):
    command = message.content.replace('letsgame ','')
    args = command.split(" ")
    GameName = args[0]
    GameTime = args[1]
    GameNote = " ".join(args[2:])

    Announcement="""***---------------------------------
      Let's Game 一起开黑
---------------------------------***
*游戏：{}
时间：{}
备注：{}*
***---------------------------------***
`按🤚参与，按❎退出`  >已参与玩家：尚无
    """.format(GameName,GameTime,GameNote)
    announceM = await message.channel.send(Announcement.lstrip("\n"))
    await announceM.add_reaction("🤚")
    await announceM.add_reaction("❎")

#keep_alive()
client.run("<BOT TOKEN>")
