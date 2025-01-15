from pathlib import Path
from fontTools.ttLib import TTFont
from tkinter import font as tkFont

def load_custom_font(font_path, font_name):
    try:
        font_obj = TTFont(font_path)
        font_obj.save(font_path)
        tkFont.Font(font=font_name, family=font_path)
    except FileNotFoundError:
        pass  
    except Exception as e:
        print(f"Ошибка при загрузке шрифта: {e}")

def custom_font():
    current_dir = Path(__file__).resolve().parent
    app_dir = current_dir.parents[4] / 'App'
    font_path_header = app_dir / 'font' / 'gothampro_bold.ttf'
    font_path_text = app_dir / 'font' / 'TT Travels Next Trial Bold.ttf'

    if font_path_header.exists():
        load_custom_font(font_path_header, 'CustomHeaderFont')

    if font_path_text.exists():
        load_custom_font(font_path_text, 'CustomTextFont')
