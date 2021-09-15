"""
"""

from asyncio import sleep
from config import Config
from logger import LOGGER
from pyrogram import Client
from pyrogram.errors import MessageNotModified
from plugins.bot.commands import HOME_TEXT, HELP_TEXT
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils import get_admins, get_buttons, get_playlist_str, pause, restart_playout, resume, shuffle_playlist, skip

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await get_admins(Config.CHAT_ID)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "You're Not Allowed! 🤣",
            show_alert=True
            )
        return
    if query.data == "shuffle":
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
            return
        await shuffle_playlist()
        await sleep(1)
        await query.answer("🔁 Shuffling !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(
                    f"{pl}",
                    parse_mode="Markdown",
                    reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if Config.PAUSE:
            await query.answer("⏸ Already Paused !", show_alert=True)
        else:
            await pause()
            await sleep(1)
            await query.answer("⏸ Paused !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass
    
    elif query.data.lower() == "resume":   
        if not Config.PAUSE:
            await query.answer("▶️ Already Resumed !", show_alert=True)
        else:
            await resume()
            await sleep(1)
            await query.answer("▶️ Resumed !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="skip":   
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
        else:
            await skip()
            await sleep(1)
            await query.answer("⏭ Skipped !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="replay":
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
        else:
            await restart_playout()
            await sleep(1)
            await query.answer("🔂 Replaying !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)

        try:
            await query.message.edit(
                HELP_TEXT,
                reply_markup=reply_markup

            )
        except MessageNotModified:
            pass

    elif query.data=="home":
        buttons = [
            [
                InlineKeyboardButton("SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
    await query.answer()

