import discord
from discord.ext import tasks
import datetime
import pytz
import os

TOKEN      = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = 852170678291267684

PARIS_TZ     = pytz.timezone("Europe/Paris")
RETOUR_ELONE = datetime.date(2026, 6, 8)

intents = discord.Intents.default()
client  = discord.Client(intents=intents)

def jours_restants() -> int:
    aujourd_hui = datetime.datetime.now(PARIS_TZ).date()
    delta = RETOUR_ELONE - aujourd_hui
    return max(delta.days, 0)

def message_decompte() -> str:
    jours = jours_restants()
    if jours == 0:
        return "🎉🎉🎉 **C'est le grand jour !** 🎉🎉🎉\nElone rentre du Canada **AUJOURD'HUI** ! Bienvenue à la maison cousin ! 🍁❤️"
    elif jours == 1:
        return "⏳ Plus que **1 jour** avant le retour d'Elone !\nDemain c'est le grand retour ! 🍁🎊"
    else:
        return f"⏳ Plus que **{jours} jours** avant le retour d'Elone !\nRetour prévu le **lundi 8 juin 2026** 🍁"

@tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=PARIS_TZ))
async def decompte_quotidien():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[ERREUR] Salon introuvable (ID: {CHANNEL_ID})")
        return
    await channel.send(message_decompte())
    print(f"[OK] Message envoyé — {jours_restants()} jours restants")

@client.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {client.user}")
    print(f"📅 Retour d'Elone : {RETOUR_ELONE}  —  {jours_restants()} jours restants")
    decompte_quotidien.start()

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.strip().lower() == "!elone":
        await message.channel.send(message_decompte())

client.run(TOKEN)
