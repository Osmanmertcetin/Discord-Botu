import random

from rich.progress import track
from discord import Client, Guild
from internal.utils import get_account_settings, create_guild_directory, create_member_file, Logger

client = Client(chunk_guilds_at_startup = False)
logger = Logger()


async def scrape(conf, guild: Guild):
  logger.scraper("Başlanıyor...")
  members = await guild.fetch_members([random.choice(guild.channels)] if conf["channel_id"] != 0 else conf["channel_id"])
  members = [member for member in members if not member.bot]
  logger.success("Üyelere başarıyla erişildi.")
  return members


@client.event
async def on_ready():
  logger.scraper(f"{client.user} olarak giriş yapıldı.")

  config = get_account_settings()
  guild_id = config["guild_id"]

  guild = client.get_guild(int(guild_id))
  members = await scrape(config, guild)

  create_guild_directory(guild)

  for member in track(members, description="[bold white][Scraper] Üyeler çekiliyor...[/]", refresh_per_second=100000):
    await create_member_file(member)


  logger.success("Üyelerin kullanıcı adları başarıyla çekildi.\n")
  print("!!! Uyarı: Tekrar veri çekimi yapabilmek için programı kapatıp tekrar açmanız gerekir.")


