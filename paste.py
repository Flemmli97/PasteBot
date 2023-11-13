import discord
import requests
from datetime import datetime, timedelta, timezone

# ====== Configs

channel_category = ""
paste_site_api = "https://api.paste.gg/v1/pastes"
paste_site = "https://paste.gg/"
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
        print(f'{message.created_at} - Attempting processing message with attachments: {message.attachments}')
        urls = []
        for attachment in message.attachments:
            if not attachment.filename.endswith(allowed_files):
                continue
            output = await attachment.to_file()
            attachment_content = output.fp.read().decode('UTF-8')
            exp = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            file = [{"name": attachment.filename, "content": {"format": "text", "value": attachment_content}}]
            data = {"visibility": "public", "expires": exp, "files": file}
            # Send content to paste site
            send = requests.post(paste_site_api, json=data)
            if send.ok:
                result = send.json()
                if result["status"] == "success":
                    id = result["result"]["id"]
                    urls.append((attachment.filename, f'{paste_site}/{id}'))
            else:
                print("Error sending to paste: ", send.raise_for_status())

        if len(urls) > 0:
            attachment_files = ", ".join([f'`{file}`' for (file,_) in urls])
            msg = f'Created paste version of {attachment_files} from {message.author.mention}!'
            view = discord.ui.View()
            for (file, url) in urls:
                view.add_item(discord.ui.Button(url=url, label=f'View {file}'))
            await message.channel.send(msg, view=view)

f = open(".secret", "r")
client.run(f.read())