# PasteBot
Simple Discord bot to automatically creating pastes from uploaded files

# How to install

To run this app you need to pass in following environmental variables.

| ENV    | Description |
| -------- | ------- |
| BOT_TOKEN | The token of your bot |
| SERVER_ID | ID of your discord server that has the bot |
| CHANNEL | Optionally a channel category to listen to. If not specified listens to all channels in the server |

Then Simply run `pip install -r requirements.txt`.  
After that run `python ./paste.py`.

An easier way of doing this is create an `.env` file and simply run the docker compose.