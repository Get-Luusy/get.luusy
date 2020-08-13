from instabot import Bot
from config import config

bot = Bot()

bot.login(username=config["insta_name"], password=config["insta_pass"])

post_ids = []
