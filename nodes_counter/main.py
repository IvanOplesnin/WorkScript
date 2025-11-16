import aiohttp
import json
import asyncio



import asyncio
import aiohttp

BASE_URL = "https://uis-prod-msk-mrkt-marketplace-api.uiscom.ru"

# ⚠️ Не клади это в git
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
    "access_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImpQWmozdjdaLVVXUUZobE5PelVSZFNIUFFUVUxtWUUxdHJoQ0F5VnJqNkUiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI5ZDgwYWVlMi04Y2FjLTRhZDQtODVkZS03ZDY2YWUxYWJmOTQiLCJzaWQiOiI0YzBlMDAxMi1iYTZiLTQwOTAtYmIxOS1lZTNiNDdiNDk0NzciLCJpc3MiOiJodHRwczovL3Vpcy1wcm9kLW1zay11Yy1zc28tYXBpLnVpc2NvbS5ydSIsImF1ZCI6WyJodHRwczovL3Vpcy1wcm9kLW1zay1tcmt0LW1hcmtldHBsYWNlLWFwaS51aXNjb20ucnUiXSwic3ViIjoiQ29tYWdpY0RCfHVpczJ8NTg4NjZ8MTE0MTU2Iiwic3ViZCI6eyJhcHBfaWQiOjU4ODY2LCJjdXN0b21lcl9pZCI6NTU1MjIwLCJ1c2VyX2lkIjoxMTQxNTYsImxvZ2luIjoiYS5maWxjaGVua292QGNvbWFnaWMuZGV2IiwiaXNfc3lzdGVtIjpmYWxzZSwic3lzdGVtX3VzZXJfaWQiOjgxNDEwOX0sImNsaWVudF9pZCI6Imh0dHBzOi8vdWlzLXByb2QtbXNrLW1ya3QtbWFya2V0cGxhY2UtYXBpLnVpc2NvbS5ydSIsImlhdCI6MTc2MzA2ODIxOH0.lywA50YtkPjZceE09f_nXPFcSi7cBJW5etNkrntYQGFDAKkQGWGCXvQ2y3ULcX3I-awXTPphvImU2DuowN0O33NjC0a6OkqyMxUVkN55qlfCH_ov2ZRLaSWHxI1vlUejapz-pwAISQdlqCTD30hDjpEX8P6sq7-6oMQeWvvbp4zbB6W_kMdfl7VuS5uSkATrJJUOXL_G5-tpsFZeAeLt1lDWtguF5u7Mf00M26H3AcN0oegrmYeGAIvkaF8FsMvvsj0owYVZyygj1bMkUO1f0cw1K6QpoumbzA0NPlE3RsVyfnTT6aCgF0gB6gc8IQ7beChnG2rDX3z9OpiSXlieRF7NNYyO9-pDSnXskCPi4RZ8iHys8oLFA3wWuLDJ3FOGXg3qUp65mRwc6ltCZdEY3FNssWbGWFCnGfMSwRNmvmCcyjXxShA77-3-Yd-FvDmwGseN0nF0GlqBhNcLiJHgFDVF_mOMpkROxCVqH2TOWNPRCjzgC_pijyO8XvHpB0o61Nk4Xg4dQG5Agv6aQ_aLV18HyNw_4cMhb_WCBfvO1n7tkm4SrY03TP_Yjebsgt44aqpW8ZVnV6fovXP8iF9s3zhiyXoM3ISPvVj8bTwOeMeWVF7p4iHXqRP7ZSnRcuEBpMF7vhLkL-rM8aKHg3ZEzzYVCeleusTpasBBVv4EUWk; "
    "_ym_isad=1; "
    "mindboxDeviceUUID=ff6781bb-c364-46fc-ae99-f755a3b8ad51; "
    "directCrm-session=%7B%22deviceGuid%22%3A%22ff6781bb-c364-46fc-ae99-f755a3b8ad51%22%7D"
)

COMMON_HEADERS = {
    "Accept": "application/json",
    "Referer": "https://uis-prod-msk-mrkt-marketplace-api.uiscom.ru/doc",
    "Cookie": COOKIE_HEADER,
}


async def marketplace_request(
    session: aiohttp.ClientSession,
    method: str,
    path: str,
    *,
    params: dict | None = None,
    json: dict | None = None,
) -> dict:
    url = BASE_URL + path
    async with session.request(method.upper(), url, params=params, json=json) as resp:
        resp.raise_for_status()
        return await resp.json()


async def main():
    # Пример: твой запрос к /node_types/detailed
    with open("all_id_flows.json", "r") as f:
        list_ids = json.load(f)

    with open("nodes_counter.json", "r") as f:
        nodes_type_ids = json.load(f)

    counter: dict[str, dict] = {
        node_type["id"]: {
            "count": 0,
            "name": node_type["displayName"],
            "flows_ids": set(),
        }
        for node_type in nodes_type_ids
    }

    async with aiohttp.ClientSession(headers=COMMON_HEADERS) as session:
        n = 0
        for flow_id in list_ids:
            n += 1
            print(f"Выполняется: {n}/{len(list_ids)}")
            path = f"/flows/{flow_id}"
            print(path)
            try:
                data = await marketplace_request(session, "GET", path)
            except aiohttp.ClientResponseError as e:
                print(f"[ERROR] flow {flow_id}: {e.status} {e.message}")
                continue
            except Exception as e:
                print(f"[ERROR] flow {flow_id}: {e}")
                continue

            graph = data.get("graph") or {}
            nodes = graph.get("nodes") or {}

            seen_node_types: set[str] = set()

            for node in nodes.values():
                node_data = node.get("data") or {}
                node_type_id = node_data.get("nodeTypeId")
                if not node_type_id:
                    continue

                if node_type_id in counter:
                    seen_node_types.add(node_type_id)

            for node_type_id in seen_node_types:
                counter[node_type_id]["count"] += 1
                counter[node_type_id]["flows_ids"].add(flow_id)

    result: dict[str, dict] = {}
    for node_type_id, info in counter.items():
        flows_ids = sorted(info["flows_ids"])
        links = [f"https://go.uiscom.ru/marketplace/flows/{fid}" for fid in flows_ids]

        result[node_type_id] = {
            "count": info["count"],  # число сценариев, где встречается nodeType
            "name": info['name'],
            "flows_ids": flows_ids,  # список id таких сценариев
            "links": links,  # удобные ссылки
        }

    with open("flows_nodes_counter_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Готово, результат сохранен в flows_nodes_counter_result.json")

if __name__ == "__main__":
    asyncio.run(main())
