import asyncio
import json
import re
import subprocess
from pathlib import Path

import aiohttp


def get_vpn_ip(interface: str = "vpn0") -> str:
    """
    Возвращает IPv4-адрес интерфейса VPN (например, 10.81.120.171 для vpn0).

    Использует команду:
      ip -4 addr show dev <interface>
    и парсит строку вида:
      inet 10.81.120.171/23 ...
    """
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show", "dev", interface],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Не удалось выполнить команду ip: {e}") from e

    match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/", result.stdout)
    if not match:
        raise RuntimeError(
            f"Не удалось найти IPv4-адрес для интерфейса {interface}. "
            f"Вывод команды ip:\n{result.stdout}"
        )

    return match.group(1)


async def main():
    # 1. Получаем IP vpn0
    vpn_ip = get_vpn_ip("vpn0")
    user_ip = f"http://{vpn_ip}:82"

    # 2. Читаем токен из secrets.json
    base_dir = Path(__file__).resolve().parent
    secrets_path = base_dir / "secrets.json"
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = json.load(f)
        token_ip = secrets["token_ip"]

    body = {
        "user_name": "i_vanya0956",
        "user_ip": user_ip,
        "user_token": token_ip,
    }

    # 3. Отправляем запрос в рабочую систему
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://custom.comagic.ru/congrok/change",
            json=body,
        ) as response:
            text = await response.text()
            print("Статус:", response.status)
            print("Ответ:", text)


if __name__ == "__main__":
    asyncio.run(main())
