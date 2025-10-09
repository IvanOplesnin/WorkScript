from typing import Optional, Dict, Any, List


def create_customfields(**kwargs) -> dict:
    """
    Сформировать блок дополнительных полей для тела запроса.

    Обязательные параметры (kwargs):
        hook (dict): Источник данных, из которого берутся значения по ключам (параметрам CoMagic).
        ext_fields (list[dict]): Описание сопоставлений полей.
            Каждый элемент списка — словарь вида:
              - extra_field_name (str) — ИД (или имя) кастомного поля получателя (куда пишем значение).
              - comagic_parameter (str) — ключ для чтения значения из `hook`.
              - update_always (bool, необяз.) — флаг «обновлять всегда» (если используется вместе с update=True).

    Необязательные параметры (kwargs):
        update (bool): Глобальный переключатель режима обновления. По умолчанию False.
            Логика: если передан update=False, то для каждого ext_field флаг update_always принудительно считается True.

    Возвращает:
        dict: Словарь вида:
            {
                "customFieldData": [
                    {
                        "field": {"id": <extra_field_name>},
                        "value": <значение из hook по comagic_parameter>
                    },
                    ...
                ]
            }
            Пустой список, если подходящих значений не нашлось.
    """
    hook = kwargs['hook']
    ext_fields = kwargs['ext_fields']
    update = kwargs.get('update', False)

    body = {
        "customFieldData": []
    }
    list_customfields = []
    if ext_fields:
        for ext_field in ext_fields:
            try:
                # Параметры для создания атрибутов
                extra_field_name = ext_field['extra_field_name']
                comagic_parameter = ext_field['comagic_parameter'].strip(' ')
                update_always = ext_field['update_always'] if update else True

                if update_always:
                    value = hook.get(comagic_parameter)
                    if value:
                        customfield = {
                            "field": {
                                "id": extra_field_name
                            },
                            "value": value
                        }
                        list_customfields.append(customfield)

            except KeyError:
                pass

        if list_customfields:
            body['customFieldData'] = list_customfields
    return body


def add_messages(**kwargs):
    """
    Сконструировать текст комментария из списка сообщений.

    Обязательные параметры (kwargs):
        data_messagees (list[dict]): Список сообщений.
            Каждый элемент — словарь вида:
              - date_time (str): Дата/время в формате "%Y-%m-%d %H:%M:%S.%f".
              - text (str): Текст сообщения (может содержать переносы строк).
              - source (str): Источник/отправитель.

    Необязательные параметры (kwargs):
        (нет)

    Возвращает:
        dict: Словарь вида {"description": "<сформированный HTML-текст c <br>>"}.
             Формат времени в выводе — "дд.мм.гггг чч:мм".
    """
    from datetime import datetime

    data_messagees = kwargs['data_messagees']

    text = ""
    split = "<br>"
    for mes in data_messagees:
        s = mes['date_time']
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
        text_time = dt.strftime("%d.%m.%Y %H:%M")
        m_text = mes['text'].replace('\n', split)
        text += f"{text_time}{split}От: {mes['source']}{split}Сообщение: {m_text}{split}{split}"
    return {
        "description": text
    }


def replace_template(**kwargs):
    """
    Заменить плейсхолдеры в шаблоне значениями из hook.

    Обязательные параметры (kwargs):
        template (str): Текст шаблона. Плейсхолдеры могут быть в виде {{key}} или просто key.
                        Функция сперва удаляет '{{' и '}}', затем подставляет значения.
        hook (dict): Источник значений. Для каждого key из hook все вхождения 'key' в шаблоне будут заменены.

    Необязательные параметры (kwargs):
        (нет)

    Возвращает:
        str: Текст с подстановками.
             Для пустых/None значений в hook подставляется пустая строка.
    """
    template = kwargs['template']
    hook = kwargs['hook']

    template = template.replace("{{", "").replace("}}", "")
    text = template
    for key, value in hook.items():
        if not value:
            value = ''
        template = template.replace(key, str(value))
        text = template

    return text


def create_task(**kwargs):
    """
    Сформировать тело задачи (task) с опциональным назначением ответственного и кастомными полями.

    Обязательные параметры (kwargs):
        responsible (str | int): ИД пользователя-исполнителя по умолчанию.
        template (str): Шаблон для генерации имени/описания задачи (передается в replace_template).
        hook (dict): Данные для шаблона (replace_template) и для кастомных полей (create_customfields).

    Необязательные параметры (kwargs):
        contact (dict | None): Карточка контакта. Если передан, добавляется:
            {
                "counterparty": {"id": contact['id']}
            }
            Дополнительно, если option_responsible="from_card", пытается назначить первого руководителя:
            contact['supervisors']['users'][0]['id'].
        option_responsible (str): Способ выбора ответственного. Значения:
            - "from_card" — попытаться взять из contact['supervisors'] (если не получилось — упасть на responsible).
            - любое другое значение — использовать `responsible`. По умолчанию "from_settings".
        ext_fields (list[dict]): Описание кастомных полей (см. create_customfields).

    Зависимости:
        - Для генерации названия/описания: использует replace_template(**kwargs) и, следовательно, ожидает ключи `template` и `hook`.
        - Для кастомных полей: вызывает create_customfields(update=False, **kwargs). Если нужны поля — ожидается ключ `ext_fields`.

    Возвращает:
        dict: Тело задачи вида:
            {
                "name": <str>,
                "description": <str>,
                "counterparty": {"id": <contact.id>}?,            # если contact передан
                "customFieldData": [...],                          # если ext_fields заданы и найдены значения
                "assignees": {"users": [{"id": "user:<id>"}]}?     # если назначен ответственный
            }
    """
    contact = kwargs.get('contact')
    responsible = kwargs['responsible']
    option_responsible = kwargs.get('option_responsible', "from_settings")

    body = {}
    # Создание названия задача
    name = replace_template(**kwargs)
    body['name'] = name
    body['description'] = name
    if contact:
        body['counterparty'] = {
            "id": contact['id']
        }
    custom_fields = create_customfields(update=False, **kwargs)
    if custom_fields:
        body['customFieldData'] = custom_fields['customFieldData']

    if option_responsible == "from_card":
        if option_responsible == "from_card":
            try:
                resp = contact['supervisors']['users'][0]['id']
                if "user" in resp:
                    body['assignees'] = {
                        "users": [
                            {
                                "id": resp
                            }
                        ]
                    }
                else:
                    raise
            except:
                body['assignees'] = {
                    "users": [
                        {
                            "id": f"user:{responsible}"
                        }
                    ]
                }
        else:
            body['assignees'] = {
                "users": [
                    {
                        "id": f"user:{responsible}"
                    }
                ]
            }

    return body


def _take(d: Dict[str, Any], key: str) -> Optional[str]:
    v = d.get(key)
    return v if v not in (None, "", "None") else None


def create_contact(**kwargs) -> dict:
    """
    Сформировать тело контакта.

    Обязательные:
        hook (dict): источник значений (в т.ч. телефон/почта и плейсхолдеры для шаблона имени).
        template (str): шаблон имени контакта (поддерживаются {{key}} и key).
        responsible (str|int): ИД ответственного (будет записан как "user:<id>").

    Необязательные:
        template_number (str|int|None): ИД шаблона карточки. *Игнорируется при update=True*.
        ext_fields (list[dict]): описание кастомных полей (см. create_customfields).
        update (bool): если True — обновлять ТОЛЬКО телефон, email и доп. поля; не изменять template и name.
                       По умолчанию False.
        phone_key (str): ключ телефона в hook. По умолчанию "visitor_phone_number".
        email_key (str): ключ email в hook. По умолчанию "visitor_email".
        phone_type (int): тип телефона. По умолчанию 1.
        data (dict): альтернативный источник телефона/почты (fallback), по умолчанию {}.

    Возвращает:
        dict: тело контакта для API. Состав полей зависит от флага update:
              - update=False: template, phones/email, name, supervisors, customFieldData (если есть).
              - update=True : ТОЛЬКО phones/email и customFieldData (если есть).
    """
    hook: Dict[str, Any] = kwargs['hook']
    template: str = kwargs['template']
    responsible = kwargs['responsible']

    template_number = kwargs.get('template_number')
    ext_fields: List[Dict[str, Any]] = kwargs.get('ext_fields') or []
    update: bool = kwargs.get('update', False)

    phone_key: str = kwargs.get('phone_key', 'visitor_phone_number')
    email_key: str = kwargs.get('email_key', 'visitor_email')
    phone_type: int = kwargs.get('phone_type', 1)

    data: Dict[str, Any] = kwargs.get('data', {}) or {}

    result: Dict[str, Any] = {}

    # Всегда: телефон/почта (из hook, затем fallback data)
    phone = _take(hook, phone_key) or _take(data, phone_key)
    if phone:
        result['phones'] = [{"number": phone, "type": phone_type}]

    email = _take(hook, email_key) or _take(data, email_key)
    if email:
        result['email'] = email

    # Кастомные поля — всегда можно обновлять (если описаны)
    if ext_fields:
        customfields = create_customfields(hook=hook, ext_fields=ext_fields, update=update)
        if customfields.get('customFieldData'):
            result['customFieldData'] = customfields['customFieldData']

    # Если это не режим update — можно задавать остальные поля (template, name, supervisors)
    if not update:
        if template_number:
            result['template'] = {"id": template_number}

        name = replace_template(template=template, hook=hook)
        result['name'] = name

        resp_str = str(responsible)
        result['supervisors'] = {
            "users": [
                {"id": "user:{resp_str}"}
            ]
        }

    return result


func_dict = {
    "create_customfields": create_customfields,
    "add_messages": add_messages,
    "replace_template": replace_template,
    "create_task": create_task,
    "create_contact": create_contact
}


def main(**kwargs):
    func_name = kwargs['f']
    return func_dict[func_name](**kwargs)

if __name__ == '__main__':
    pass


