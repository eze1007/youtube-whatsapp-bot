import requests
from twilio.rest import Client

# --- CREDENZIALI ---
YT_API_KEY = "AIzaSyCdiP8wjd-QCjP7zLr3ev6U6c8OqSJ7Ciw"
CHANNEL_ID = "UCwSlaSn1zyQDKBRij3qZbOA"
TWILIO_SID = "AC03c8f0302659ad355d599baf3d5e4d13"
TWILIO_TOKEN = "1187c15282b835aff2d66979173ae689"
TWILIO_NUMBER = "whatsapp:+14155238886"
NUMERO_DEST = "whatsapp:+393517273999"

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
