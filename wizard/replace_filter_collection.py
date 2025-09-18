import json
from pprint import pprint

with open('moysklad_telephony.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
wizard = data.get("wizard")


def get_filter(id: int):
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
    collection = next(item for item in result if item.get("nodeDataSource").endswith(end_string))
    if collection.get("properties").get("type") == "collection":
        return collection.get("properties").get("options")[0].get("values")[1]
    raise ValueError("Нет фильтра с таким id")




def update_collection_filter(new_filter: dict = None,  settings_id: int = 0, load_options_node: str = ""):
    result = []

    for param in new_filter.get("typeOptions").get("filterParams"):
        param['loadOptionsNode'] = load_options_node

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

    end_string = f"{str(settings_id)}.value"
    opt = next(item for item in result if item.get("nodeDataSource").endswith(end_string))
    if opt:
        # collection.get("properties").get("options")[0].get("values")[1]
        opt["properties"]['options'][0]['values'][1] = new_filter
        return opt
    raise ValueError("Нет фильтра с таким id")



if __name__ == '__main__':
    pprint(get_filter(41))
    # update_filter()
