def translate_emp_columns(columns):
    translation_dict = {
        "ID_EMPLOYER": "ID\n\n",
        "SMALL_DATA": "ФИО",
        "SURNAME": "Фамилия",
        "NAME_EMP": "Имя",
        "SURNAME_FATHER": "Отчество",
        "POL": "Пол",
        "INN": "ИНН",
        "SNILS": "СНИЛС",
        "DATA_BIRTH": "Дата рождения",
        "DATE_CITY": "Место рождения",
        "TYPE_DOC": "Тип документа",
        "DOC_NUM": "Номер документа",
        "DOC_DATE": "Дата выдачи \n документа",
        "DOC_WERE": "Кем выдан документ",
        "ADRESS_REGIST": "Адрес регистрации",
        "ADRESS_PROPISKA": "Адрес прописки",
        "MILITARY_NUM": "Номер  \n военного билета",
        "MILITARY_DATE": "Дата \n военного билета",
        "EDUCATION": "Образование"
    }
    return [translation_dict.get(col, col) for col in columns]
def translate_emp_list_columns(columns):
    translation_dict = {
        "ID": "ID",
        "EMPLOYER_NAME": "Сотрудник",
        "DEPARTMENT_NAME": "Отдел",
        "PROFESION_NAME": "Профессия",
        "SOVM_NAME": "Совмещение",
        "BENEFITS_NAME": "Льгота",
        "OKLAD": "Оклад",
        "DATE_ADD": "Дата добавления",
        "DATE_FIRED": "Дата увольнения"
    }
    return [translation_dict.get(col, col) for col in columns]
def translate_bef_columns(columns):
    translation_dict = {
        "ID": "ID",
        "CATEGORY": "Категория",
        "SUM_WITHOUT": "Сумма без НДС"
    }
    return [translation_dict.get(col, col) for col in columns]

def translate_dep_columns(columns):
    translation_dict = {
        "ID": "ID",
        "TAG": "Отдел"
    }
    return [translation_dict.get(col, col) for col in columns]

def translate_fact_columns(columns):
    translation_dict = {
        "SMALL_NAME": "Краткое наименование",
        "FULL_NAME": "Полное наименование",
        "INN": "ИНН",
        "KPP": "КПП",
        "OKPO": "ОКПО",
        "KOD_GNI": "Код ГНИ",
        "KOD_SNIILS": "Код СНИИЛС",
        "ADRES": "Адрес",
        "RUK_DOLG": "Должность руководителя",
        "RUK_FIO": "ФИО руководителя",
        "GL_BUX": "Главный бухгалтер"
    }
    return [translation_dict.get(col, col) for col in columns]
def translate_post_columns(columns):
    translation_dict = {
        "TITLE": "Заголовок",
        "DESCRIPTION": "Описание",
        "AUTHOR": "Автор",
        "DATE_POSTS": "Дата публикации"
    }
    return [translation_dict.get(col, col) for col in columns]
def translate_prof_columns(columns):
    translation_dict = {
        "ID": "ID",
        "TAG": "Профессия"
    }
    return [translation_dict.get(col, col) for col in columns]

def translate_sovm_columns(columns):
    translation_dict = {
        "ID": "ID",
        "TAG": "Категория Совместительства"
    }
    return [translation_dict.get(col, col) for col in columns]

def translate_doc_columns(columns):
    translation_dict = {
        "ID": "ID",
        "TAG": "Тег",
        "DOCUMENT_TYPE": "Тип документа",
        "FILE_DATA": "Данные файла",
        "INNER_DATE": "Дата"
    }
    return [translation_dict.get(col, col) for col in columns]
