import json


with open("all_flows.json", "r") as f:
    result = []
    flows = json.load(f)
    for flow in flows:
        result.append(flow['id'])

print(len(result))

with open("all_id_flows.json", "w") as f:
    json.dump(result, f)

