from datetime import datetime
def convert_date_to_display_format(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d').strftime('%d.%m.%Y')
    return ""

def convert_date_to_save_format(date_string):
    if date_string:
        return datetime.strptime(date_string, '%d.%m.%Y').strftime('%Y-%m-%d')
    return ""