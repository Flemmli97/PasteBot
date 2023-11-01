import discord
import requests

# ====== Configs

channel_category = ""
paste_site = "https://api.mclo.gs/1/log"
allowed_files = (".txt", ".json", ".toml", ".log")

# ======

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    if channel_category != "" and str(message.channel.category) != channel_category:
        return
    if len(message.attachments) > 0:
        urls = []
        for attachment in message.attachments:
            if not attachment.filename.endswith(allowed_files):
                continue
            output = await attachment.to_file()
            attachment_content = output.fp.read().decode('UTF-8')
            # Send content to paste site
            send = requests.post(paste_site, data= {"content": attachment_content})
            if send.ok:
                result = send.json()
                if result["success"]:
                    urls.append((attachment.filename, result["url"]))

        if len(urls) > 0:
            attachment_files = ", ".join([f'`{file}`' for (file,_) in urls])
            msg = f'Created paste version of {attachment_files} from {message.author.mention}!'
            view = discord.ui.View()
            for (file, url) in urls:
                view.add_item(discord.ui.Button(url=url, label=f'View {file}'))
            await message.channel.send(msg, view=view)

f = open(".secret", "r")
client.run(f.read())