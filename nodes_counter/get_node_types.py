import asyncio
import json

import aiohttp

BASE_URL = "https://uis-prod-msk-mrkt-uc-flow-api.uiscom.ru"

# ⚠️ Не клади это в git/репозиторий
COOKIE_HEADER = (
    "__ddg9_=213.111.128.212; "
    "__ddg1_=utgFAQVtKq7qvGnykOoX; "
    "_ym_uid=1762987949666387098; "
    "_ym_d=1762987949; "
    "__ddg10_=1762987949; "
    "BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A12%2C%22EXPIRE%22%3A1763067540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; "
    "__ddg8_=7FN9Qwq6WW8rTjUk; "
    "popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; "
    "_cmg_csstEDW1C=1762987951; "
    "_comagic_idEDW1C=48840481.125738262.1762987950; "
    "access_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImpQWmozdjdaLVVXUUZobE5PelVSZFNIUFFUVUxtWUUxdHJoQ0F5VnJqNkUiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI3NWRiMzYzYy1hOGZhLTQ4NzctOGMwNC1hM2Q1NGJmY2E4M2MiLCJzaWQiOiI0YzBlMDAxMi1iYTZiLTQwOTAtYmIxOS1lZTNiNDdiNDk0NzciLCJpc3MiOiJodHRwczovL3Vpcy1wcm9kLW1zay11Yy1zc28tYXBpLnVpc2NvbS5ydSIsImF1ZCI6WyJodHRwOi8vdWlzLXByb2QtbXNrLW1ya3QtdWMtZmxvdy1hcGkudWlzLXByb2QtbXNrLW1ya3QtdWMtZmxvdyIsImh0dHBzOi8vdWlzLXByb2QtbXNrLW1ya3QtdWMtZmxvdy1hcGkudWlzY29tLnJ1Il0sInN1YiI6IkNvbWFnaWNEQnx1aXMyfDU4ODY2fDExNDE1NiIsInN1YmQiOnsiYXBwX2lkIjo1ODg2NiwiY3VzdG9tZXJfaWQiOjU1NTIyMCwidXNlcl9pZCI6MTE0MTU2LCJsb2dpbiI6ImEuZmlsY2hlbmtvdkBjb21hZ2ljLmRldiIsImlzX3N5c3RlbSI6ZmFsc2UsInN5c3RlbV91c2VyX2lkIjo4MTQxMDl9LCJjbGllbnRfaWQiOiJodHRwczovL3Vpcy1wcm9kLW1zay1tcmt0LXVjLWZsb3ctYXBpLnVpc2NvbS5ydSIsImlhdCI6MTc2MzA2ODI2OX0.EtLOTFYcrPWT9tp6ZDh0vw0X5ep7Odbd6j4bygSErAkVxS1X1TzdGtK5-jzqWp5bSmNLynhhpjzU00Pzk5jJ0PbMvqMgBu1sMPtvuKNTvXfjvHJgP257y4xd1xcgO-AqNRuipMvPkRsBRRZyTiq9UQ0gI-BGbYZ_64KKCX-EEmsmNnhOKn7tHLOgW6c-C9xqdamAHdAo7qGtxeLrXOSk8iy3-fXl5LJoilOfU1UW6uBMmr4WcTsZKQNLzAAuBAQXYRY5G5Y8C76j8n1qpNrTpCgeTwLplEyRDPweT1e_3SLLBeY3uTjhLOyIqVv5qr2Z9l0tlt59uqj3aLhgbyG60py97U3EX7_-dCGud4TDH0yZM7fowAzvzGEY3Pk-dRI7sLHkHKsMnC0FJpIVgz7drIGhz7dZH1vuIc95Sy-koiJiYnxnnk_EtneGHlmhKipznYVJ47ia8Fg6R8UlmZzNyPgc3y9a5tch_QgI9HbS5Qbja0g-q4mo1a6o032yW3WZwupQyqqQcc_tCwFUPWUnDPbbFs0NOJn4WjjeJCeKSiV9UErthkgc1YQ38QnSWDF6P8tubnTa_Jqs_xmJCEtQcW5Q05wtdsmXLnwo9ksIXgcHUsi6mzH8R1jjG-qwVBKR6xS2ICD5D66RquUGVPTODKqkOgYgobgMukO9WUo5Syg; "
    "_ym_isad=1; "
    "mindboxDeviceUUID=ff6781bb-c364-46fc-ae99-f755a3b8ad51; "
    "directCrm-session=%7B%22deviceGuid%22%3A%22ff6781bb-c364-46fc-ae99-f755a3b8ad51%22%7D"
)

COMMON_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://go.uiscom.ru",
    "Referer": "https://go.uiscom.ru/",
    "Cookie": COOKIE_HEADER,
}


async def request_api(
    method: str,
    path: str,
    *,
    params: dict | None = None,
    json: dict | None = None,
) -> dict:
    """
    Универсальная функция запроса к uc-flow-api.
    path — строка вида "/node_types/detailed" или "/flows/..."
    """
    url = BASE_URL + path
    async with aiohttp.ClientSession(headers=COMMON_HEADERS) as session:
        async with session.request(method.upper(), url, params=params, json=json) as resp:
            resp.raise_for_status()
            return await resp.json()


async def main():
    # Пример: твой запрос к /node_types/detailed
    result = []
    for i in range(3):
        data = await request_api(
            "GET",
            "/node_types/detailed",
            params={
                "_end": 50*(i+1),
                "_order": "asc",
                "_sort": "displayName",
                "_start": i*50,
            },
        )
        for node_type in data:
            result.append(
                {
                    "id": node_type["id"],
                    "displayName": node_type["displayName"],
                    "type": node_type["type"],
                }
            )

    with open("nodes_counter.json", "w") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)




if __name__ == "__main__":
    asyncio.run(main())


