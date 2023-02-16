import datetime

def get_input_from_user_str(input_name: str) -> str:
    input_value: str = ""

    while True:
        input_value = input(f"> Enter {input_name}: ")

        if len(input_value) < 1:
            continue

        break

    return input_value

def get_input_from_user_int(input_name: str) -> int:
    input_value: str = ""

    while True:
        input_value = input(f"> Enter {input_name}: ")

        if not input_value.isdigit():
            continue

        break

    return int(input_value)

def get_input_from_user_date(input_name: str, date_format: str) -> datetime.date:
    input_value = None

    while True:
        input_value = input(f"> Enter {input_name}: ")

        if len(input_value) < 1:
            continue

        try:
            input_value = datetime.datetime.strptime(input_value, date_format)
        except ValueError as value_error:
            print(value_error)
            continue

        break

    return input_value.date()