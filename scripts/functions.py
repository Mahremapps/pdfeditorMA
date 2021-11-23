# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
all function needed
"""
import os
import gc
import sys
import json
import time
from typing import Union
import fitz
from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets,
)
from PyQt5.QtWidgets import (
    QInputDialog,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QWidget,
)
from .language import MENU_L, MESSAGE


class Doc(fitz.Document):
    """
    a wrapper to fitz.Document class
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.pass_word = None
        self.rotatedPages = {}


def copy(doc: Doc) -> Doc:
    """
    copy the doc

    :param doc: document to be copied
    :return: copied document
    """
    _doc = Doc(doc.name)
    if not _doc.is_pdf:
        pdf_bites = _doc.convert_to_pdf()
        _doc = Doc('pdf', pdf_bites)
    if doc.pass_word is not None:
        _doc.authenticate(doc.pass_word)
    _doc.name = doc.name
    _doc.rotatedPages = doc.rotatedPages
    if len(_doc.rotatedPages) != 0:
        for page in _doc.rotatedPages:
            _doc[page].set_rotation(_doc.rotatedPages[page])
    return _doc


def open_pdf(file_name: str,
             parent: QWidget) -> (Union[Doc, None], bool):
    """
    open pdf file and return a fitz object if applied

    :param file_name: pdf file name
    :param parent: parent
    :return (doc, bool)
    """
    try:
        doc = Doc(file_name)
    except RuntimeError:
        QMessageBox.critical(
            parent,
            'Oops',
            MESSAGE[parent.language][0],
            QMessageBox.Yes,
        )
        return None, False
    if doc.needs_pass:
        while doc.is_encrypted:
            value, _ = QInputDialog.getText(
                parent,
                '',
                'Password:',
                QLineEdit.Password,
                '',
                QtCore.Qt.Dialog,
            )
            if not _:
                doc.close()
                del doc
                return None, False
            doc.authenticate(value)
            doc.pass_word = value
    if not doc.is_pdf:
        pdf_bites = doc.convert_to_pdf()
        doc = Doc('pdf', pdf_bites)
        doc.name = file_name
    return doc, True


def render_pdf_page(page_data: Doc.load_page) -> QtGui.QPixmap:
    """
    render PDF page

    :param page_data: page data
    :return: a QPixmap
    """
    page_pixmap = fitz.utils.get_pixmap(
        page_data,
        matrix=fitz.Matrix(1.0, 1.0),
        clip=True,
    )
    if page_pixmap.alpha:
        image_format = QtGui.QImage.Format_RGBA8888
    else:
        image_format = QtGui.QImage.Format_RGB888
    page_image = QtGui.QImage(
        page_pixmap.samples,
        page_pixmap.w,
        page_pixmap.h,
        page_pixmap.stride,
        image_format,
    )
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(page_image)
    del page_pixmap
    return pixmap


def pdf_split(doc: Doc) -> list:
    """
    split the selected PDF file into pages;

    :param doc: target PDF file to be split
    :return: book_list
    """
    book_list = []
    for page in range(doc.page_count):
        book_list.append(page)
    return book_list


def add_watermark(doc: any,
                  text: str,
                  rotate: int,
                  colour: tuple,
                  font_size: int,
                  font_file: str,
                  opacity=0.5) -> any:
    """
    add watermark

    :param doc: import file, i.e., fitz.Document or Doc
    :param text: content of watermark
    :param rotate: rotation angle of watermark
    :param colour: colour of watermark; in form of (a, b, c,)
    :param font_size: font size of letter in watermark
    :param font_file: font file location
    :param opacity: opacity of the watermark; range from 0 to 100
    :return: fitz.Document or Doc
    """
    for page in doc:
        r1 = fitz.Rect(
            10,
            10,
            page.rect.width-10,
            page.rect.height-10,
        )
        pos0 = fitz.Point(
            page.rect.width//2,
            page.rect.height//2,
        )
        shape = fitz.utils.Shape(page)
        shape.insert_textbox(
            r1,
            text,
            rotate=0,
            color=colour,
            fontsize=font_size,
            stroke_opacity=0.5,
            fill_opacity=opacity,
            align=1,
            fontfile=font_file,
            fontname=os.path.basename(font_file),
            morph=(
                pos0,
                fitz.Matrix(rotate)
            ),
        )
        shape.commit()
    return doc


def setting_warning(set_file_name: str,
                    parent: QWidget) -> dict:
    """
    import settings from the JSON file

    :param set_file_name: JSON file name
    :param parent: parent
    :return: a dict loaded from JSON file or default values
    """
    try:
        with open(
                set_file_name,
                'r',
                encoding='utf-8',
        ) as f:
            content = json.load(f)
        if "start dir" not in content:
            content["start dir"] = ""
        if "save dir" not in content:
            content["save dir"] = ""
        if "font dir" not in content:
            content["font dir"] = ""
        if "language" not in content:
            content["language"] = "English"
        else:
            if content["language"] not in ["English", "中文", "日本語"]:
                content["language"] = "English"
            else:
                pass
        if "dir store" not in content:
            content["dir store"] = False
        return content
    except FileNotFoundError:
        reply = QMessageBox.warning(
            parent,
            'Error',
            f'Cannot find {os.path.basename(set_file_name)}\n\n'
            f'Create an empty setting file?',
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.No:
            sys.exit(0)
        if reply == QMessageBox.Yes:
            content = {
                "start dir": "",
                "save dir": "",
                "language": "English",
                "font dir": "",
                "dir store": False
            }
            return content


def shadow(widget,
           colour: QtGui.QColor,
           radius: int) -> None:
    """
    add shadow

    :param widget: widget
    :param colour: colour of shadow, e.g. QColor(10, 10, 10, 100)
    :param radius: radius of the shadow
    :return: None
    """
    _shadow = QtWidgets.QGraphicsDropShadowEffect()
    _shadow.setBlurRadius(radius)
    _shadow.setColor(colour)
    _shadow.setOffset(0, 0)
    widget.setGraphicsEffect(_shadow)


def page_icon(page: fitz.Page,
              width: int,
              w_col: int,
              _scaled: float,
              _scaled_=1) -> QWidget:
    """
    insert image to a QLabel

    :param page: file page
    :param width: width of the table cell
    :param w_col: collum count of the table
    :param _scaled: scaled coefficient of label
    :param _scaled_: scaled coefficient of image in label
    :return: shadowed QWidget()
    """
    _cover = render_pdf_page(page)
    label = QtWidgets.QLabel(None)
    layout = QHBoxLayout(None)
    widget = QWidget(None)
    layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)
    widget.setLayout(layout)
    scaled_width, scaled_height = int(), int()
    if _cover.height() / _cover.width() > 4 / 3:
        scaled_height = width // w_col * 4 / 3 * _scaled
        scaled_width = scaled_height * (_cover.width() / _cover.height())
    if _cover.height() / _cover.width() <= 4 / 3:
        scaled_width = width // w_col * _scaled
        scaled_height = scaled_width * (_cover.height() / _cover.width())
    label.setPixmap(
        QtGui.QPixmap(_cover).scaled(
            scaled_width * _scaled_,
            scaled_height * _scaled_,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation,
        ),
    )
    label.setAlignment(
        QtCore.Qt.AlignCenter,
    )
    label.setFixedSize(scaled_width, scaled_height)
    shadow(label, QtGui.QColor(0, 0, 0, 100), 20)
    del _cover, label, layout
    return widget


def set_icon(widget: QWidget,
             doc: Union[Doc, fitz.Document, None] = None,
             _scaled: float = 0.95,
             _scaled_=1) -> None:
    """
    add image of first page into table element

    :param widget: widget
    :param doc: doc
    :param _scaled: scaled coefficient of label
    :param _scaled_: scaled coefficient of image in label
    :return: None
    """
    x, y = 0, 0
    for i in widget.book_list:
        label = page_icon(
            widget.book[i] if isinstance(
                widget.book_list[0],
                int,
            ) else (i[0] if doc is None else doc[0]),
            widget.table.width(),
            widget.w_col,
            _scaled,
            _scaled_
        )
        widget.table.setCellWidget(x, y, label)
        del label  # delete label (important)
        # do not change the following codes
        # --------------------------------------------------------------
        if ((x + 1) * (y + 1)) // ((x + 1) * widget.w_col) == 0:
            y += 1
        else:
            x += 1
            y -= (widget.w_col - 1)
        # --------------------------------------------------------------


def add(main: QWidget,
        _format: str) -> (str, bool):
    """
    add a file

    :param main: main widget
    :param _format: file format filter, e.g., '(*.pdf)'
    :return: [f_name, state]
    """
    f_name, state = QFileDialog.getOpenFileName(
        main,
        'Open files',
        main.s_dir,
        _format,
    )
    if state and main.dir_store_state:
        main.s_dir = os.path.dirname(f_name.replace('/', '\\'))
    return f_name.replace('/', '\\'), state


def save(main: QWidget,
         _format: str) -> (str, bool):
    """
    save a file

    :param main: main widget
    :param _format: file format filter, e.g., '.pdf'
    :return: [f_name, state]
    """
    f_name, state = QFileDialog.getSaveFileName(
        main,
        "save",
        main.o_dir + "new.pdf",
        _format,
    )
    if state and main.dir_store_state:
        main.o_dir = os.path.dirname(f_name.replace('/', '\\'))
    return f_name.replace('/', '\\'), state


def delete(index: int,
           widget: QWidget) -> None:
    """
    delete select file/page

    :param index: position index
    :param widget: widget
    :return: None
    """
    if index >= 0:
        widget.book_list.pop(index)
    widget.table.clearContents()
    if len(widget.book_list) != 0:
        reset_table(
            book_len=len(widget.book_list),
            widget=widget,
        )
        # reset images
        set_icon(widget)


def generate_menu(pos,
                  widget: QWidget,
                  main: QWidget,
                  select: int = 0) -> None:
    """
    generate menu

    :param pos: position
    :param select: select=0 => only delete;
                   select=1 => with other functions
    :param widget: widget
    :param main: main
    :return: None
    """
    row_num = col_num = int()
    for i in widget.table.selectionModel().selection().indexes():
        row_num = i.row()
        col_num = i.column()
    index = row_num * widget.w_col + col_num  # get position
    if 0 <= index < len(widget.book_list):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction(
            QtGui.QIcon('ico\\delete.svg'),
            MENU_L[main.language][0],
        )
        item2, item3, item4, item5, item6, item7 = None, None, None, None, None, None
        if select == 0:
            item3 = menu.addAction(
                QtGui.QIcon('ico\\view.svg'),
                MENU_L[main.language][1],
            )
        if select == 1:
            item2 = menu.addAction(
                QtGui.QIcon('ico\\down.svg'),
                MENU_L[main.language][2],
            )
            item4 = menu.addAction(
                QtGui.QIcon('ico\\Photo.svg'),
                MENU_L[main.language][3],
            )
            item5 = menu.addAction(
                QtGui.QIcon('ico\\rotate_clockwise.svg'),
                MENU_L[main.language][4],
            )
            item6 = menu.addAction(
                QtGui.QIcon('ico\\rotate_anticlockwise.svg'),
                MENU_L[main.language][5],
            )
            item7 = menu.addAction(
                QtGui.QIcon('ico\\move_page.svg'),
                MENU_L[main.language][6],
            )
        action = menu.exec_(
            widget.table.mapToGlobal(pos),
        )
        if action == item1:
            delete(
                index=index,
                widget=widget,
             )
        if action == item2 and select == 1:
            save_as(
                index=index,
                widget=widget,
                main=main,
            )
        if action == item3 and select == 0:
            main.view(index, widget)
        if action == item4 and select == 1:
            extract_img(
                index=index,
                widget=widget,
                main=main,
            )
        if action == item5 and select == 1:
            rotate_page(
                index=index,
                degree=90,
                widget=widget,
            )
        if action == item6 and select == 1:
            rotate_page(
                index=index,
                degree=-90,
                widget=widget,
            )
        if action == item7 and select == 1:
            rearrange_page(
                index=index,
                widget=widget,
                parent=main,
            )


def reset_table(book_len: int,
                widget: QWidget) -> None:
    """
    reset the table element

    :param book_len: length of book_list
    :param widget: widget
    :return: None
    """
    if book_len % widget.w_col == 0:
        w_row = book_len//widget.w_col
    else:
        w_row = book_len//widget.w_col + 1
    widget.w_row = w_row
    widget.table.setColumnCount(widget.w_col)
    widget.table.setRowCount(widget.w_row)
    for i in range(widget.w_col):
        widget.table.setColumnWidth(
            i,
            widget.table.width()//widget.w_col,
        )
    for i in range(widget.w_row):
        widget.table.setRowHeight(
            i,
            (widget.table.width()//widget.w_col)*4//3,
        )


def save_as(index: int,
            widget: QWidget,
            main: QWidget) -> None:
    """
    save the selected page as PDF file

    :param index: position index
    :param widget: widget
    :param main: main
    :return: None
    """
    doc = fitz.Document()
    doc.insert_pdf(widget.book, widget.book_list[index], widget.book_list[index])
    f_name = os.path.splitext(
        os.path.basename(widget.book.name),
    )[0]+f'-{widget.book_list[index]+1}.pdf'
    file_name, ok = QFileDialog.getSaveFileName(
        main,
        "save",
        main.o_dir + f_name,
        "PDF file (*.pdf);;images (*.png *.jpg)",
    )
    if ok:
        if file_name.endswith('.pdf'):
            doc.save(file_name.replace('/', '\\'))
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            pix = fitz.utils.get_pixmap(
                doc[0],
                matrix=fitz.Matrix(1.0, 1.0),
                alpha=True,
            )
            pix.save(file_name.replace('/', '\\'))
    doc.close()
    del doc


def clean(widget: QWidget) -> None:
    """
    clear the table contents

    :param widget: widget
    :return: None
    """
    if len(widget.book_list) != 0:
        if isinstance(widget.book_list[0], (Doc, fitz.Document,)):
            for item in widget.book_list:
                item.close()
        else:
            widget.book.close()
            widget.book = None
        widget.book_list = []
        widget.table.clearContents()
        reset_table(
            book_len=1,
            widget=widget,
        )
    gc.collect(2)


def extract_img(index: int,
                widget: QWidget,
                main: QWidget) -> None:
    """
    extract images from pdf page.

    :param index: page index
    :param widget: widget
    :param main: main
    :return: None
    """
    doc = widget.book
    img_inf = doc[widget.book_list[index]].get_images()
    for key, inf in enumerate(img_inf):
        f_name = os.path.splitext(
            os.path.basename(widget.book.name),
        )[0] + f'-{widget.book_list[index]+1}-image-{key+1}.png'
        img_name = main.s_dir+'\\'+f_name
        # xref is inf[0]
        img = fitz.Pixmap(
            doc,
            inf[0],
        )
        img.save(img_name)
    QMessageBox.information(
        main,
        'Saved',
        MESSAGE[main.language][1].format(
            len(img_inf),
            main.s_dir,
        ),
        QMessageBox.Yes,
    )


def rotate_page(index: int,
                degree: int,
                widget: QWidget) -> None:
    """
    rotate page

    :param index: index of the page
    :param degree: rotate degrees
    :param widget: widget
    :return: None
    """
    page_index = widget.book_list[index]
    if page_index in widget.book.rotatedPages:
        degree += widget.book.rotatedPages[page_index]
        widget.book[page_index].set_rotation(degree)
    else:
        widget.book[page_index].set_rotation(degree)
    widget.book.rotatedPages[page_index] = degree
    widget.table.clearContents()
    reset_table(
        book_len=len(widget.book_list),
        widget=widget,
    )
    set_icon(widget)


def rearrange_page(index: int,
                   widget: QWidget,
                   parent: QWidget) -> None:
    """
    rearrange pages

    :param index: position index of the selected page
    :param widget: widget
    :param parent: parent widget
    :return: None
    """
    book_length = len(widget.book_list)
    value, _ = QInputDialog.getInt(
        parent,
        '',
        f'Move to page: (from 1 to {book_length})',
        value=index+1,
        min=1,
        max=book_length,
        step=1,
        flags=QtCore.Qt.Dialog,
    )
    if not _:
        return None
    page_index = widget.book_list[index]
    widget.book_list[index] = None
    if value <= index:
        widget.book_list.insert(value-1, page_index)
    else:
        widget.book_list.insert(value, page_index)
    widget.book_list.remove(None)
    widget.table.clearContents()
    reset_table(
        book_len=len(widget.book_list),
        widget=widget,
    )
    set_icon(widget)
    return None


def choose(widget: QtWidgets.QLineEdit,
           c_dir: str) -> None:
    """
    choose folder

    :param widget: widget
    :param c_dir: from where to choose
    :return: None
    """
    root = QFileDialog.getExistingDirectory(
        None,
        "choose",
        c_dir,
    )
    if len(root) != 0:
        widget.setText(
            root.replace('/', '\\'),
        )


def set_metadata0(doc: fitz.fitz,
                  author: Union[str, None]) -> None:
    """
    set defeat metadata

    :param doc: fitz Document
    :param author: str or None
    :return: None
    """
    _time = time.localtime(time.time())
    metadata = doc.metadata
    metadata["producer"] = "pyPDFEditor-GUI"
    metadata["modDate"] = "D:" + "".join((
        str(_time[0]),
        str(_time[1]).zfill(2),
        str(_time[2]).zfill(2),
        str(_time[3]).zfill(2),
        str(_time[4]).zfill(2),
        str(_time[5]).zfill(2),
        time.strftime('%z'),
        '\'' + time.strftime('%z')[3:] + '\'',
    ))
    metadata["author"] = author
    doc.set_metadata(metadata)


def set_metadata1(metadata: dict,
                  title: str,
                  author: str,
                  subject: str,
                  keywords: str) -> dict:
    """
    set metadata to pdf document

    :param metadata: the metadata table from pdf file
    :param title: title
    :param author: author
    :param subject: subject
    :param keywords: keywords
    :return: a dict -> metadata
    """
    _time = time.localtime(time.time())
    metadata["producer"] = "pyPDFEditor-GUI"
    metadata["modDate"] = "D:" + "".join((
        str(_time[0]),
        str(_time[1]).zfill(2),
        str(_time[2]).zfill(2),
        str(_time[3]).zfill(2),
        str(_time[4]).zfill(2),
        str(_time[5]).zfill(2),
        time.strftime('%z')[:3],
        '\''+time.strftime('%z')[3:]+'\'',
    ))
    metadata["title"] = title
    metadata["author"] = author
    metadata["subject"] = subject
    metadata["keywords"] = keywords
    return metadata


def toc2plaintext(toc: list) -> str:
    """
    :param toc: table of content <- DOCUMENT.get_toc()
    :return: plaintext
    """
    plaintext = []
    for content in toc:
        head = f'{int(content[0])*"*"}-->{content[1]}-->{content[2]}'
        plaintext.append(head)
    plaintext = '\n'.join(plaintext)
    return plaintext


def plaintext2toc(plaintext: str) -> list:
    """
    :param plaintext: plaintext
    :return: table of content -> DOCUMENT.get_toc()
    """
    toc = []
    contents = plaintext.split('\n')
    for content in contents:
        if len(content) != 0:
            c = content.split('-->')
            t = [len(c[0]), c[1], int(c[2])]
            toc.append(t)
    return toc


def find_font(font_dirs: list) -> (dict, dict):
    """
    find all TrueType font files (.ttf): all their font name and file addresses
    then write their directories to a json file

    :param font_dirs: the directions where font files locate
    :return: two dictionaries => {font name: font file address} &
                                 {font file address: font name}
    """
    name_dict = {}
    dir_dict = {}
    for font_dir in font_dirs:
        for file_name in os.listdir(font_dir):
            full_name = os.path.join(
                font_dir.replace('/', '\\'),
                file_name,
            )
            try:
                font_name = fitz.Font(fontfile=full_name).name
                name_dict[font_name] = full_name
                dir_dict[full_name] = font_name
            except RuntimeError:
                pass
    with open(
        file='settings\\font_dir_cache.json',
        mode='w',
        encoding='utf-8',
    ) as f:
        json.dump(
            name_dict,
            f,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )
    return name_dict, dir_dict


def read_from_font_cache(cache_file_name: str) -> (dict, dict):
    """
    read font directories from json file

    :param cache_file_name: json cache file name
    :return: two dictionaries => {font name: font file address} &
                                 {font file address: font name}
    """
    dir_dict = {}
    with open(
        file=cache_file_name,
        mode='r',
        encoding='utf-8',
    ) as f:
        name_dict = json.load(f)
    for font_name in name_dict:
        dir_dict[name_dict[font_name]] = font_name
    return name_dict, dir_dict


def _warning(parent) -> None:
    """
    :param parent: parent
    :return: None
    """
    QMessageBox.warning(
        parent,
        'Oops',
        MESSAGE[parent.language][2],
        QMessageBox.Yes,
    )
