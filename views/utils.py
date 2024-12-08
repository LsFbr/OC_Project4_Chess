from datetime import datetime


def format_date(date_obj):
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj)
        except ValueError:
            return "Invalid date"
    elif not isinstance(date_obj, datetime):
        return "Not available"

    return date_obj.strftime("%Y/%m/%d %H:%M:%S")
