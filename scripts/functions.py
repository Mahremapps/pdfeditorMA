# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import fitz
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget


def render_pdf_page(page_data):
    """
    render PDF page

    :param page_data: page data
    :return: a QPixmap
    """
    page_pixmap = page_data.get_pixmap(
        matrix=fitz.Matrix(0.7, 0.7),
        clip=True,
    )
    if page_pixmap.alpha:
        image_format = QtGui.QImage.Format_RGBA8888
    else:
        image_format = QtGui.QImage.Format_RGB888
    page_image = QtGui.QImage(
        page_pixmap.samples,
        page_pixmap.width,
        page_pixmap.height,
        page_pixmap.stride,
        image_format,
    )
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(page_image)
    del page_pixmap
    return pixmap


def pdf_split(input_pdf: str):
    """
    split the selected PDF file into pages;

    :param input_pdf: target PDF file to be split
    :return: book_list
    """
    book_list = list()
    doc0 = fitz.open(input_pdf)
    if doc0.needsPass:
        QMessageBox.critical(None, 'Error',
                             'Cannot open an encrypted file.',
                             QMessageBox.Yes | QMessageBox.No)
        doc0.close()
        del doc0
        return book_list
    else:
        for page in range(doc0.pageCount):
            book_list.append(page)
        doc0.close()
        del doc0
        return book_list


def security(input_pdf: str,
             output_pdf: str,
             text: str,
             rotate: int,
             colour: tuple,
             font_size: int,
             font_file: str,
             opacity=0.5,
             owner_pass='',
             user_pass=''):
    """
    add password and/or watermark

    :param input_pdf: import file name
    :param output_pdf: export file name
    :param text: content of watermark
    :param rotate: rotation angle of watermark; must be 0, 90, 180, 270, 360
    :param colour: colour of watermark; in form of (a, b, c,)
    :param font_size: font size of little in watermark
    :param font_file: font file location
    :param opacity: opacity of the watermark; range from 0 to 100
    :param owner_pass: owner password
    :param user_pass: user password
    :return: None
    """
    perm = int(
        fitz.PDF_PERM_ACCESSIBILITY  # always use this
        | fitz.PDF_PERM_PRINT  # permit printing
        | fitz.PDF_PERM_COPY  # permit copying
        | fitz.PDF_PERM_ANNOTATE  # permit annotations
    )
    encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm
    doc = fitz.open(input_pdf)
    for page in doc:
        r1 = fitz.Rect(10, 10, page.rect.width-10, page.rect.height-10)
        shape = page.newShape()
        shape.insertTextbox(
                        r1,
                        text,
                        rotate=rotate,
                        color=colour,
                        fontsize=font_size,
                        stroke_opacity=0.5,
                        fill_opacity=opacity,
                        align=1,
                        fontfile=font_file,
                        fontname="EXT_0"
                        )
        shape.commit()
    doc.save(output_pdf,
             encryption=encrypt_meth,  # set the encryption method
             owner_pw=owner_pass,  # set the owner password
             user_pw=user_pass,  # set the user password
             permissions=perm,  # set permissions
             )
    doc.close()
    del doc


def setting_warning(set_file_name: str):
    """
    import settings in JSON file

    :param set_file_name: JSON file name
    :return: a dist loaded from JSON file
    """
    try:
        with open(set_file_name, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        QMessageBox.warning(
            None,
            'Error',
            'Cannot find '+set_file_name.split('\\')[-1],
            QMessageBox.Yes | QMessageBox.No,
        )
        exit()


def set_icon(f_name, widget, _page=0):
    """
    add image of first page into table element

    :param f_name: import file name
    :param widget: widget
    :param _page: page index
    :return: bool
    """
    doc = fitz.open(f_name)
    if doc.needsPass:
        QMessageBox.critical(None, 'Error',
                             'Cannot open an encrypted file.',
                             QMessageBox.Yes | QMessageBox.No)
        doc.close()
        del doc
        return False
    else:
        page = doc.loadPage(_page)
        _cover = render_pdf_page(page)
        label = QtWidgets.QLabel(None)
        scaled_width, scaled_height = None, None
        if _cover.height()/_cover.width() > 4/3:
            scaled_height = (widget.table.width()-15)//widget.w_col*4/3-5
            scaled_width = scaled_height*(_cover.width()/_cover.height())
        if _cover.height()/_cover.width() <= 4/3:
            scaled_width = (widget.table.width()-15)//widget.w_col-5
            scaled_height = scaled_width*(_cover.height()/_cover.width())
        label.setPixmap(
            QtGui.QPixmap(_cover).scaled(scaled_width,
                                         scaled_height,
                                         QtCore.Qt.IgnoreAspectRatio,
                                         QtCore.Qt.SmoothTransformation),
            )
        label.setAlignment(QtCore.Qt.AlignCenter)
        widget.table.setCellWidget(widget.x, widget.y, label)
        del label  # delete label (important)
        del _cover, scaled_width, scaled_height
        widget.crow, widget.col = widget.x, widget.y
        try:
            if (not widget.y % (widget.w_col-1)) and widget.y:
                # 每（self.w_col）个元素换行
                widget.x += 1
                widget.y = 0
            else:
                widget.y += 1
        except ZeroDivisionError:
            pass
        doc.close()
        del doc
        return True


def add(main: QWidget, widget: QWidget):
    """
    add a file

    :param main: main widget
    :param widget: widget
    :return: None
    """
    f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                            main.s_dir, '(*.pdf)')
    if _ and (f_name not in widget.book_list):
        if set_icon(f_name, widget):
            widget.book_list.append(f_name)
        else:
            pass
    else:
        pass


def delete(index, widget: QWidget):
    """
    delete select file/page

    :param index: position index
    :param widget: widget
    :return: None
    """
    if index >= 0:
        widget.book_list.pop(index)
    widget.table.clearContents()
    widget.x, widget.y = 0, 0
    if not widget.book_list:
        widget.crow = -1
        widget.col = -1
    if len(widget.book_list) != 0:
        reset_table(len(widget.book_list), widget)
        for f_name in widget.book_list:
            # reset images
            if type(f_name) is str:
                set_icon(f_name, widget)
            if type(f_name) is int:
                set_icon(widget.book_name, widget, f_name)


def generate_menu(pos, widget: QWidget, select=0, main=None):
    """
    generate menu

    :param pos: position
    :param select: select=0 => only delete;
                   select=1 => with save as
    :param widget: widget
    :param main: main
    :return: None
    """
    row_num = col_num = -1
    for i in widget.table.selectionModel().selection().indexes():
        row_num = i.row()
        col_num = i.column()
    index = row_num * widget.w_col + col_num  # get position
    if 0 <= index < len(widget.book_list):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction('delete')
        item2, item3 = None, None
        if select == 0:
            item3 = menu.addAction('view')
        if select == 1:
            item2 = menu.addAction('save as')
        action = menu.exec_(widget.table.mapToGlobal(pos))
        if action == item1:
            try:
                delete(index, widget)
            except IndexError:
                pass
        if action == item2 and select == 1:
            try:
                save_as(index, widget, main)
            except IndexError:
                pass
        if action == item3 and select == 0 and main is not None:
            main.view(index, widget)


def reset_table(book_len, widget: QWidget):
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
    widget.table.setRowCount(widget.w_row)
    for i in range(widget.w_col):
        widget.table.setColumnWidth(
            i,
            (widget.table.width()-15)//widget.w_col,
        )
    for i in range(widget.w_row):
        widget.table.setRowHeight(
            i,
            ((widget.table.width()-15)//widget.w_col)*4//3,
        )


def save_as(index, widget: QWidget, main: QWidget):
    """
    save the selected page as PDF file

    :param index: position index
    :param widget: widget
    :param main: main
    :return: None
    """
    doc = fitz.open(widget.book_name)
    f_name = os.path.splitext(os.path.basename(widget.book_name))[0]+'{}{}{}'.\
        format('-', widget.book_list[index]+1, '.pdf')
    file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                main.o_dir + f_name,
                                                ".pdf")
    if ok:
        doc.select([widget.book_list[index]])
        doc.save(file_name.replace('/', '\\'))
    doc.close()


def clean(widget: QWidget):
    """

    :param widget: widget
    :return: None
    """
    widget.book_list = list()
    widget.x, widget.y = 0, 0
    widget.col, widget.crow = -1, -1
    widget.table.clearContents()
    reset_table(book_len=1, widget=widget)


def choose(widget, c_dir):
    """

    :param widget: widget
    :param c_dir: from where to choose
    """
    root = QFileDialog.getExistingDirectory(
        None,
        "choose",
        c_dir,
    )
    if len(root) != 0:
        widget.setText(root.replace('/', '\\'))
