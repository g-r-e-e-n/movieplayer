
import os
import sys
from config import Config
from logger import LOGGER
from utils import update, is_admin
from pyrogram import Client, filters
from plugins.bot.controls import is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**, \n\nI'm **Video Player Bot**. \n\n** By green👑**"
HELP_TEXT = """
🏷️ --**Setting Up**-- :

\u2022 Add the bot and user account in your group with admin rights.
\u2022 Start a voice chat in your group & restart the bot if not joined to vc.
\u2022 Use /play [video name] or use /play as a reply to an video file or youtube link.

🏷️ --**Common Commands**-- :

\u2022 `/start` - start the bot
\u2022 `/help` - shows the help
\u2022 `/playlist` - shows the playlist

🏷️ --**Admins Only Commands**-- :

\u2022 `/skip` - skip current video
\u2022 `/stream` - start live stream
\u2022 `/pause` - pause playing video
\u2022 `/resume` - resume playing video
\u2022 `/leave` - leave the voice chat
\u2022 `/shuffle` - shuffle the playlist
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clrlist` - clear the playlist queue
\u2022 `/getlogs` - get the ffmpeg bot logs
\u2022 `/restart` - update & restart the bot

© **Powered By** : 
**green👑**
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    buttons = [
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        HELP_TEXT,
        reply_markup=reply_markup
        )

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    k=await message.reply_text("🔄 **Restarting ...**")
    await update()
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin @AsmSafone For More!**")
    except:
        pass

@Client.on_message(filters.command(['getlogs', f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="green👑 Bot Logs"))
    if logs:
        await message.reply_media_group(logs)
        logs.clear()
    else:
        await message.reply_text("❌ **No Log Files Found !**")
