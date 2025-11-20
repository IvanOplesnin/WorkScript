import asyncio
import json

import aiohttp

"""
Cisco Secure Client 5.1.4.1158  
(Wed Jun 18 20:25:06 2025)

Информация об адресе
    Клиент (IPv4):  10.81.120.171
"""
# Cisco Secure Client 5.1.4.1158
# (Fri Nov 14 16:29:02 2025)
#
# Информация об адресе
# 	Клиент (IPv4):	10.81.121.128

user_ip = "http://10.81.121.128:82" # Введите IP адрес вашего vpn сервера

with open("secrets.json", "r") as f:
    secrets = json.loads(f.read())
    token_ip = secrets["token_ip"]

async def main():
    async with aiohttp.ClientSession() as session:
        body = {
            "user_name": "i_vanya0956",
            "user_ip": user_ip,
            "user_token": token_ip
        }

        async with session.get('https://custom.comagic.ru/congrok/change', json=body) as response:
            print(await response.text())


asyncio.run(main())
