import discord
import requests
from datetime import timedelta
import os

# ====== Configs

try:
  token = os.environ["BOT_TOKEN"]
except KeyError as e:
  raise Exception("Missing env var BOT_TOKEN: You need to specify a bot token")
try:
  server_id = os.environ["SERVER_ID"]
except KeyError as e:
  raise Exception("Missing env var SERVER_ID: You need to specify a server id")
channel_category = os.getenv("CHANNEL")
mclogs = "https://api.mclo.gs/1/log"
paste_site_api = "http://blazing-coop.net/paste/"
paste_site = "http://blazing-coop.net/paste"
allowed_files = (".txt", ".json", ".toml", ".log")

# ======

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

'''
    Sends the content to a paste site. Adjust for paste site api
'''
def send_paste(filename, content):
    data = {"text": content, "filename": filename, "expires": int(timedelta(days=30).total_seconds())}
    # Send content to paste site
    send = requests.post(paste_site_api, json=data)
    if send.ok:
        result = send.json()
        id = result["path"].removeprefix("/")
        return (filename, f'{paste_site}/{id}')
    else:
        print("Error sending to paste: ", send.raise_for_status())

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    if str(message.guild.id) != server_id:
        return
    if channel_category != None and str(message.channel.category) != channel_category:
        return
    if len(message.attachments) > 0:
        print(f'{message.created_at} - Attempting processing message with attachments: {message.attachments}')
        urls = []
        for attachment in message.attachments:
            if not attachment.filename.endswith(allowed_files):
                continue
            output = await attachment.to_file()
            attachment_content = output.fp.read().decode('UTF-8')

            # Send logfiles to mclogs since they have better synatx highlighting
            if attachment.filename.endswith(".log"):
                data = {"content": attachment_content}
                send = requests.post(mclogs, data=data)
                if send.ok:
                    result = send.json()
                    if result["success"] == "True":
                        urls.append((attachment.filename, f'{result["url"]}'))
                else:
                    print("Error sending to paste: ", send.raise_for_status())
            else:
                result = send_paste(attachment.filename, attachment_content)
                if result is not None:
                    urls.append(result)

        if len(urls) > 0:
            attachment_files = ", ".join([f'`{file}`' for (file,_) in urls])
            msg = f'Created paste version of {attachment_files} from {message.author.mention}!'
            view = discord.ui.View()
            for (file, url) in urls:
                view.add_item(discord.ui.Button(url=url, label=f'View {file}'))
            await message.channel.send(msg, view=view)

client.run(token)
