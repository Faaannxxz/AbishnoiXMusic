
import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from strings import get_command
from AbishnoiX import app
from AbishnoiX.core.call import Alisha
from AbishnoiX.misc import db
from AbishnoiX.utils.database import get_authuser_names, get_cmode
from AbishnoiX.utils.decorators import (ActualAdminCB, AdminActual,
                                         language)
from AbishnoiX.utils.formatters import alpha_to_int

### Multi-Lang Commands
RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(
            chat_id, filter="administrators"
        )
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴᴄᴀᴄʜᴇ. ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ."
        )


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.. ʀᴇsᴛᴀʀᴛɪɴɢ {MUSIC_BOT_NAME} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Alisha.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await Alisha.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(
        "`sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴛᴀʀᴛᴇᴅ. ᴛʀʏ ᴘʟᴀʏɪɴɢ ɴᴏᴡ...`"
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(
    filters.regex("stop_downloading") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴏʀ ᴄᴀɴᴄᴇʟʟᴇᴅ.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer(
                "ғᴀɪʟᴇᴅ ᴛᴏ sᴛᴏᴘ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ.", show_alert=True
            )
    await CallbackQuery.answer(
        "ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇ ʀᴜɴɴɪɴɢ ᴛᴀsᴋ", show_alert=True
    )
