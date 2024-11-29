from datetime import datetime


def format_date(date_str):
    if not date_str:
        return "Not available"
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%Y/%m/%d %H:%M:%S")
    except ValueError:
        return "Invalid date"
