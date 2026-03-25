import requests
from twilio.rest import Client

import os

YT_API_KEY = os.environ["YT_API_KEY"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
NUMERO_DEST = os.environ["NUMERO_DEST"]
def get_ultimo_video():
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&order=date&maxResults=1&key={YT_API_KEY}"
    r = requests.get(url).json()
    item = r["items"][0]
    return {
        "id": item["id"]["videoId"],
        "titolo": item["snippet"]["title"],
        "link": f"https://youtu.be/{item['id']['videoId']}"
    }

def invia_whatsapp(video):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    messaggio = f"🎬 Nuovo video!\n\n*{video['titolo']}*\n\nGuarda qui: {video['link']}"
    client.messages.create(
        from_=TWILIO_NUMBER,
        to=NUMERO_DEST,
        body=messaggio
    )
    print("✅ Messaggio inviato!")

def main():
    try:
        with open("ultimo_video.txt", "r") as f:
            ultimo_id = f.read().strip()
    except:
        ultimo_id = ""

    video = get_ultimo_video()

    if video["id"] != ultimo_id:
        print(f"🎬 Nuovo video: {video['titolo']}")
        invia_whatsapp(video)
        with open("ultimo_video.txt", "w") as f:
            f.write(video["id"])
    else:
        print("⏳ Nessun nuovo video.")

main()
