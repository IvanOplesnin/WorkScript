import json
from pprint import pprint

with open('moysklad_telephony.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
wizard = data.get("wizard")


def get_type_options(id: int):
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

    end_string = f"{str(id)}.value"
    filter = next(item for item in result if item.get("nodeDataSource").endswith(end_string))
    if filter.get("properties").get("type") == "filter":
        return filter.get("properties").get("typeOptions")
    raise ValueError("Нет фильтра с таким id")




def update_filter(type_options: dict = None, load_options: str = "",  settings_id: int = 0):
    result = []

    def get_items(properties):
        if properties["properties"].get("items"):
            for item in properties["properties"]["items"]:
                get_items(item)
        result.append(properties)

    for param in type_options.get("filterParams"):
        param['loadOptionsNode'] = load_options

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

    pprint(dict_type['options'])

    end_string = f"{str(settings_id)}.value"
    opt = next(item for item in result if item.get("nodeDataSource").endswith(end_string))
    if opt:
        opt["properties"]['typeOptions'] = type_options
        pprint(opt)
        return opt
    raise ValueError("Нет фильтра с таким id")



if __name__ == '__main__':
    update_filter()
