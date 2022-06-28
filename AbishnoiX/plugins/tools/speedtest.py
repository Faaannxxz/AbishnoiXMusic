
import asyncio
import os

import speedtest
import wget
from pyrogram import filters

from strings import get_command
from AbishnoiX import app
from AbishnoiX.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("`ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴘᴇᴇᴅᴛᴇsᴛ`")
        test.download()
        m = m.edit("`ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅᴛᴇsᴛ`")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("Sharing SpeedTest Results")
        path = wget.download(result["share"])
    except Exception as e:
        return m.edit(e)
    return result, path


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("`ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅ ᴛᴇsᴛ`")
    loop = asyncio.get_event_loop()
    result, path = await loop.run_in_executor(None, testspeed, m)
    output = f"""**sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs**
    
<u>**Client:**</u>
 **ʙᴏᴛ ɪs ᴏɴʟɪɴᴇ ʙᴀʙʏ**
**__𝖨𝖲𝖯:__** {result['client']['isp']}
**__𝙲𝚘𝚞𝚗𝚝𝚛𝚢:__** {result['client']['country']}
  
<u>**𝐒𝐞𝐫𝐯𝐞𝐫:**</u>
**__𝑵𝒂𝒎𝒆:__** {result['server']['name']}
**__𝐶𝑜𝑢𝑛𝑡𝑟𝑦:__** {result['server']['country']}, {result['server']['cc']}
**__sᴘᴏɴsᴏʀ:__** {result['server']['sponsor']}
**__𝑳𝒂𝒕𝒆𝒏𝒄𝒚:__** {result['server']['latency']}  
**__ℙ𝕀ℕ𝔾:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
