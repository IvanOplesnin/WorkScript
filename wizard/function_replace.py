import json
from pprint import pprint

with open('flow.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
wizard = data.get("wizard")


def update_options(new_options: list[dict[str, str]] = None, settings_id: int = 0):
    result = []

    def get_items(properties):
        if properties["properties"].get("items"):
            for item in properties["properties"]["items"]:
                get_items(item)
        result.append(properties)

    for data in wizard:
        get_items(data)
    result = [item for item in result if
              item.get("properties").get("items") is None and item.get("source").endswith(".value")]

    dict_type = {}
    for item in result:
        type_ = item.get("properties").get("type")
        if dict_type.get(type_):
            dict_type[type_].append(item)
        else:
            dict_type[type_] = [item]

    pprint(dict_type['filter'])
    k = {'availableOperators': [],
         'id': 'campaign_name',
         'loadOptionsDependsOn': [],
         'loadOptionsMethod': 'get.all_campaigns',
         'loadOptionsNode': '9592ae59-4e91-44d7-926a-9ac0dfa75349',
         'multipleValues': True,
         'name': 'Рекламная кампания',
         'operators': [],
         'options': [],
         'optionsTree': False,
         'type': 'string'}

    for item in dict_type['collection']:
        if values := item['properties'].get("options")[0].get("values"):
            for value in values:
                if value.get('type') == 'filter':
                    pprint(value['typeOptions']['filterParams'])

    end_string = f"{str(settings_id)}.value"
    opt = [item for item in dict_type['options'] if item.get("source").endswith(end_string)]
    if opt:
        opt = opt[0]
        opt["properties"]["options"] = new_options
        return opt
    raise ValueError("Нет выпадашки с таким id")


if __name__ == '__main__':
    update_options()
