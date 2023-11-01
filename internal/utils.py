from typing import Optional
from rich import print
from functools import cache

import json
import os
import string
import shutil
import codecs
import time

from discord import Guild, Member # type: ignore


header = """[bold white]
                            █████   █████                        █████                      
                           ░░███   ░░███                        ░░███                       
       ████████  █████ ████ ░███    ░███  █████ ████ ████████   ███████    ██████  ████████ 
      ░░███░░███░░███ ░███  ░███████████ ░░███ ░███ ░░███░░███ ░░░███░    ███░░███░░███░░███
       ░███ ░███ ░███ ░███  ░███░░░░░███  ░███ ░███  ░███ ░███   ░███    ░███████  ░███ ░░░ 
       ░███ ░███ ░███ ░███  ░███    ░███  ░███ ░███  ░███ ░███   ░███ ███░███░░░   ░███     
       ░███████  ░░███████  █████   █████ ░░████████ ████ █████  ░░█████ ░░██████  █████    
       ░███░░░    ░░░░░███ ░░░░░   ░░░░░   ░░░░░░░░ ░░░░ ░░░░░    ░░░░░   ░░░░░░  ░░░░░     
       ░███       ███ ░███                                                                  
       █████     ░░██████                                                                   
      ░░░░░       ░░░░░░                                                                                                                                                                         
[/]"""
header2 = """[bold white]
 ██████████     █████████     █████   █████                     ███     ███████████            █████              
░░███░░░░███   ███░░░░░███   ░░███   ░░███                     ░░░     ░░███░░░░░███          ░░███               
 ░███   ░░███ ███     ░░░     ░███    ░███   ██████  ████████  ████     ░███    ░███  ██████  ███████   █████ ████
 ░███    ░███░███             ░███    ░███  ███░░███░░███░░███░░███     ░██████████  ███░░███░░░███░   ░░███ ░███ 
 ░███    ░███░███             ░░███   ███  ░███████  ░███ ░░░  ░███     ░███░░░░░███░███ ░███  ░███     ░███ ░███ 
 ░███    ███ ░░███     ███     ░░░█████░   ░███░░░   ░███      ░███     ░███    ░███░███ ░███  ░███ ███ ░███ ░███ 
 ██████████   ░░█████████        ░░███     ░░██████  █████     █████    ███████████ ░░██████   ░░█████  ░░████████
░░░░░░░░░░     ░░░░░░░░░          ░░░       ░░░░░░  ░░░░░     ░░░░░    ░░░░░░░░░░░   ░░░░░░     ░░░░░    ░░░░░░░░ 
                                                                                                                  
                                                                                                                  
                                                                                                                                                                                                                                                                                        
[/]"""
info = """[bold black]
🏴Bu program pyHunter tarafından yapılmıştır.
[bold yellow]🚀Instagram:  https://www.instagram.com/pyhunter_/
[bold green]✅ Bionluk: https://bionluk.com/pyhunter
[bold green]✅ Discord: pyHunter#0698
[/]"""

default_data = {
  "token": "",
  "guild_id": 0,
  "pfp_format": "png",
  "purge_old_data": True,
  "download_pfp": True,
  "channel_id": 0
}


@cache
def show_header():
  print(f"{header}")
  time.sleep(1)
  print(f"{header2}")
  time.sleep(1)
  print(f"{info}")

@cache
def check_config_file():

  if not os.path.isfile("config.json"): 
    json.dump(default_data, open("config.json", "w"), indent=2)
    return


  with open("config.json", "r") as file:
    file_data = json.loads(file.read())
  
  required_data = {}


  for key, value in file_data.items():
    if key in default_data.keys():
      required_data[key] = value

  for default_key, default_value in default_data.items():
    if default_key not in required_data.keys():
      required_data[default_key] = default_value

  json.dump(required_data, open("config.json", "w"), indent=2)


class Logger():
  def __init__(self) -> None:
    ...

  def scraper(self, text: str) -> None:
    print(f"[bold white][Scraper] {text} [/]")

  def success(self, text: str) -> None:
    print(f"[bold green][Success] {text} [/]")

  def error(self, text: str) -> None:
    print(f"[bold red][Error] {text} [/]")

  def custom(self, text: str, header: Optional[str] = None, color: str = "white") -> None:
    print(f"[bold {color}][{header}] {text} [/]")

@cache
def get_account_settings():
  return json.load(open("config.json"))

@cache
def create_guild_directory(guild: Guild):
  if get_account_settings()["purge_old_data"]:
    shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
  os.makedirs(f"DataScraped/{guild.name}", exist_ok=True)


@cache
def clean_string(string_to_clean: str) -> str:
  return "".join([char for char in string_to_clean if char in string.printable])

@cache
async def create_member_file(member: Member):
  if member.bot:
    return

  try:
    username = clean_string(member.display_name)
    profile = await member.guild.fetch_member_profile(member.id)
    file = codecs.open(f"DataScraped/{member.guild.name}/uye_verileri.txt","a","utf-8")
    file.write(member.display_name+"#"+member.discriminator+"\n")

  except Exception as e: 
    print(f"[bold red][Error] Üye verilerini dosyaya yazarken hata yaşandı. \"{member}\": {e} [/]")
