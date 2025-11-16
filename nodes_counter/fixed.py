import json

INPUT_FILE = "flows_nodes_counter_result.json"
OUTPUT_FILE = "flows_nodes_counter_result_fixed.json"

OLD_PREFIX = "https://go.uiscom.ru/flows/"
NEW_PREFIX = "https://go.uiscom.ru/marketplace/flows/"


def fix_links():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for node_type_id, info in data.items():
        links = info.get("links")
        if not links:
            continue

        new_links = []
        for link in links:
            if link.startswith(OLD_PREFIX):
                new_links.append(link.replace(OLD_PREFIX, NEW_PREFIX, 1))
            else:
                new_links.append(link)
        info["links"] = new_links

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Готово. Результат записан в {OUTPUT_FILE}")


if __name__ == "__main__":
    fix_links()
