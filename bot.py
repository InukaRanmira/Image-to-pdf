import os
from PIL import Image
from pyrogram import Client,filters 
from pyrogram.types import InlineKeyboardButton,  InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied


TOKEN = os.environ.get("TOKEN", "")

API_ID = int(os.environ.get("API_ID", 12345))

API_HASH = os.environ.get("API_HASH", "")

app = Client(
        "pdf",
        bot_token=TOKEN,
        api_hash=API_HASH,
        api_id=API_ID
    )


LIST = {}

JOIN_ASAP = " **You can't use me untill subscribe our updates channel** ☹️\n\n So Please join our updates channel by the following button and hit on the ` /start ` button again 😊"

FSUBB = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="Join our update Channel 🗣", url=f"https://t.me/szteambots") 
        ]]      
    )

@app.on_message(filters.command(['start']))
async def start(client, message):
    try:
        await message._client.get_chat_member(int("-1001325914694"), message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
        text=JOIN_ASAP, disable_web_page_preview=True, reply_markup=FSUBB
    )
        return 
    await message.reply_text(text =f"""Hello {message.from_user.first_name }\n I'm image to pdf bot. 
i can convert image to pdf\n\n Just send a image

This bot created by @InukaRanmira""",reply_to_message_id = message.message_id ,  reply_markup=InlineKeyboardMarkup(
            [
                
                    [InlineKeyboardButton("Support " ,url="https://t.me/slbotzone") ],
                    [InlineKeyboardButton("Channel", url="https://t.me/szteambots") ]
                    ],[
                    [InlineKeyboardButton("Deverloper", url="https://t.me/InukaRanmira") ],  
            ]))


@app.on_message(filters.private & filters.photo)
async def pdf(client,message):
 
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.photo.file_id)
 ms = await message.reply_text("Converting to PDF ......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} image   Successful created PDF if you want add more image Send me One by one\n\n **if done click here 👉 /convert** ")
 

@app.on_message(filters.command(['convert']))
async def done(client,message):
 images = LIST.get(message.from_user.id)

 if isinstance(images, list):
  del LIST[message.from_user.id]
 if not images:
  await message.reply_text( "No image !!")
  return

 path = f"{message.from_user.id}" + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 
 await client.send_document(message.from_user.id, open(path, "rb"), caption = "Here your pdf !!")
 os.remove(path)
  
app.run()
