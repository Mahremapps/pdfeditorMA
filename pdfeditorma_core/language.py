# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
language related functions
"""
from PyQt5 import QtWidgets

TAB_L = {
    "English": [
        "     Merge PDF    ",
        "    Organise    ",
        "    Security    ",
        "    Metadata    ",
    ],
    "Russian": ["    Объединить документы    ", "    Разделить страницы    ", "    Защита    ", "    Метаданные    "],
    "Turkmen": ["Resminamalary birleşdir", "Sahypalary bölüň", "Resminama goragy", "Metadata"],
}
TIP_L = {
    "English": [
        "Open",
        "Save",
        "Settings",
        "Clean",
        "colours",
        "preview",
        "more",
        "font",
        "update font",
    ],
    "Russian": ["Открыть", "Сохранить", "Настройки", "Очистить", "цвета", "просмотр", "более", "шрифт", "обновить шрифт"],
    "Turkmen": ["Aç", "Saklamak", "Sazlamalar", "Arassala", "reňkler", "プレビュー", "詳細設定", "şrift", "şrift täzele"],
}
LAB_L3 = {
    "English": [
        "PASSWORD",
        "WATERMARK",
        "Font Size:",
        "Open after saving",
        "Opacity:",
        "Rotation:",
        "Preview Mode",
        "Edit Restriction",
    ],
    "Russian": ["ПАРОЛЬ",
        "Водяной знак",
        "Размер шрифта:",
        "Открыть после сохранения",
        "Непрозрачность:",
        "Вращение:",
        "Режим предварительного просмотра",
        "Изменить ограничение",
        ],
    "Turkmen": [
        "パスワード",
        "電子透かし",
        "フォントサイズ：",
        "保存してから開く",
        "不透明度：",
        "回転：",
        "プレビューモード",
        "編集制限",
    ],
}
LAB_L4 = {
    "English": ["Title", "Author", "Subject", "Keywords"],
    "Russian": ["Название", "Автор", "Тема", "Ключевые слова"],
    "Turkmen": ["Ady", "Awtor", "Mowzuk", "Açar sözler"],
}
LAB_LS = {
    "English": ["START DIR", "SAVE DIR", "OPEN AS PREVIOUS"],
    "Russian": ["КАТАЛОГ ДЛЯ НАЧАЛА", "КАТАЛОГ ДЛЯ СОХРАНЕНИЯ", "ОТКРЫТЬ КАК ПРЕДЫДУЩИЙ"],
    "Turkmen": ["開くルーチング", "保存するルーチング", "前使ったルーチングを覚える"],
}
LAB_LP = {
    "English": [
        "Enable Print",
        "Enable Modifying File",
        "Enable Copy",
        "Enable Adding Annotations",
        "Enable Filling in Form",
        "Enable Accessing Adjuvant Contents",
        "Enable Page Editing",
        "Enable HD Print",
    ],
    "Russian": [
        "Включить печать",
        "Включить изменение файла",
        "Включить копирование",
        "Включить добавление аннотаций",
        "Включить заполнение формы",
        "Включить доступ к дополнительному содержимому",
        "Включить редактирование страницы",
        "Включить HD-печать",
    ],
    "Turkmen": [
        "Çap etmegi işjeňleşdir",
        "Faýly üýtgetmegi işjeňleşdiriň",
        "Göçürmäni işjeňleşdir",
        "Annotasiýa goşmagy işjeňleşdiriň",
        "Anketany doldurmaga işjeňleşdir",
        "Ulanyjy mazmuna girmäge işjeňleşdir",
        "Sahypany redaktirlemegi işjeňleşdiriň",
        "HD çap etmegi işjeňleşdiriň",
    ],
}
MENU_L = {
    "English": [
        "delete",
        "view",
        "save as",
        "extract images",
        "rotate 90°",
        "rotate -90°",
        "move to",
        "set watermark position",
    ],
    "Russian": [
        "удалить",
        "просмотр",
        "сохранить как",
        "извлечь изображения",
        "повернуть на 90°",
        "повернуть на -90°",
        "переместить в",
        "установить положение водяного знака",
    ],
    "Turkmen": [
        "削除",
        "ビュー",
        "名前を付けて保存",
        "イメージを出す",
        "90°を旋転する",
        "-90°を旋転する",
        "ページを移動する",
        "透かしの位置を移動する",
    ],
}
LINE_L = {
    "English": [
        "    user password here",
        "    owner password here",
        """
    Catalogue edit here
    e.g.

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
    "Russian": [
        "пароль пользователя",
        "пароль владельца",
        """
    Каталог редактируем здесь
    например：

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
    "Turkmen": [
        "    使用者のパスワード",
        "    所有者のパスワード",
        """
    此処に目録を編集
    例は以下の通り

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
}
MESSAGE = {
    "English": [
        "   Format error:\n cannot open this file",
        "{} image(s) saved to {}",
        "Cannot save! Try a new file name...",
    ],
    "Russian": ["    Ошибка формата: \n невозможно открыть этот файл", "{} изображений сохранено в {}", "Невозможно сохранить! Попробуйте новое имя файла..."],
    "Turkmen": [
        "    格式エラー：\n このファイルが開けません",
        "{}幅のイメージが{}に保存されました",
        "すみません。保存できませんでした。\n 新たな名前を付けてみて下さい。。。",
    ],
}


def set_language(widget: QtWidgets.QWidget) -> None:
    """
    set language

    :param widget: QWidget -> self
    :return: None
    """
    widget.setTabToolTip(1, TAB_L[widget.language][0])
    widget.setTabToolTip(2, TAB_L[widget.language][1])
    widget.setTabToolTip(3, TAB_L[widget.language][2])
    widget.setTabToolTip(4, TAB_L[widget.language][3])
    widget.tab1.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab1.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab1.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab1.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab2.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab2.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab2.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab2.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab3.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab3.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab3.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab3.button4.setToolTip(TIP_L[widget.language][4])
    widget.tab3.button5.setToolTip(TIP_L[widget.language][5])
    widget.tab3.button6.setToolTip(TIP_L[widget.language][6])
    widget.tab3.button7.setToolTip(TIP_L[widget.language][7])
    widget.tab3.button8.setToolTip(TIP_L[widget.language][3])
    widget.tab3.button9.setToolTip(TIP_L[widget.language][8])
    widget.tab4.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab4.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab4.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab4.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab3.label1.setText(". " * 9 + LAB_L3[widget.language][0] + " ." * 9)
    widget.tab3.label2.setText(". " * 8 + LAB_L3[widget.language][1] + " ." * 8)
    widget.tab3.label4.setText(LAB_L3[widget.language][2])
    widget.tab3.label5.setText(LAB_L3[widget.language][3])
    widget.tab3.label7.setText(LAB_L3[widget.language][4])
    widget.tab3.label9.setText(LAB_L3[widget.language][5])
    widget.tab3.label11.setText(LAB_L3[widget.language][6])
    widget.tab3.label12.setText(LAB_L3[widget.language][7])
    widget.tab4.label2.setText("." * 10 + LAB_L4[widget.language][0] + "." * 10)
    widget.tab4.label3.setText("." * 10 + LAB_L4[widget.language][1] + "." * 10)
    widget.tab4.label4.setText("." * 10 + LAB_L4[widget.language][2] + "." * 10)
    widget.tab4.label5.setText("." * 10 + LAB_L4[widget.language][3] + "." * 10)
    widget.tab3.line1.setPlaceholderText(LINE_L[widget.language][0])
    widget.tab3.line2.setPlaceholderText(LINE_L[widget.language][1])
    widget.tab4.text.setPlaceholderText(LINE_L[widget.language][2])


def lag_s(parent: QtWidgets.QWidget, language: str) -> None:
    """
    set language
    """
    parent.label1.setText(LAB_LS[language][0])
    parent.label2.setText(LAB_LS[language][1])
    parent.label3.setText(LAB_LS[language][2])


def lag_p(parent: QtWidgets.QWidget, language: str) -> None:
    """
    set language
    """
    parent.label1.setText(LAB_LP[language][0])
    parent.label2.setText(LAB_LP[language][1])
    parent.label3.setText(LAB_LP[language][2])
    parent.label4.setText(LAB_LP[language][3])
    parent.label5.setText(LAB_LP[language][4])
    parent.label6.setText(LAB_LP[language][5])
    parent.label7.setText(LAB_LP[language][6])
    parent.label8.setText(LAB_LP[language][7])
