#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

class SendMessageWindow(QMainWindow):
    # связь с дизайном
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('send_message.ui', self)
        self.initUT()

    def set_smile(self, smile_src, smile_name, toolbar):
        """ дабовление смайликов в панель и создание связи с действием"""
        smile = QAction(QIcon(smile_src), smile_name, self)
        # создание связи кнопки с действие (лямда для передачи аргмента)
        smile.triggered.connect(lambda: self.insert_smile(smile_src))
        toolbar.addAction(smile)

    def insert_smile(self, src):
        """ вставить элемент в текст """
        self.textEdit.textCursor().insertHtml('<img src="%s" />' % src)

    def set_format(self, font_src, font_name, toolbar):
        """ дабовление эффектов шрифта в панель и создание связи с действием """
        font = QAction(QIcon(font_src), font_name, self)
        # создание связи кнопки с действие
        tag = font_name[:1] # используем название файлов до точки ([i].jpg)
        font.triggered.connect(lambda: self.change_font(tag))
        toolbar.addAction(font)

    def change_font(self, tag):
        """ вставить элемент в текст """
        selected_text = self.textEdit.textCursor().selectedText()
        self.textEdit.textCursor().insertHtml(
            '<{tag}>{val}</{tag}>'.format(val=selected_text, tag=tag))

    def conn_menu(self, menubar):
        menubar.triggered.connect(self.open_file)

    def open_file(self):
        """ запуск вкладки открытие файла """
        try:
            self.fname = QFileDialog.getOpenFileName(self)
            pixmap = QPixmap(self.fname[0])
            t = pixmap.scaled(180, 180, QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(t)
            self.show_button()
        except Exception as e:
            print(e)

    def show_button(self):
        self.black_white.setEnabled(1)
        self.black_white.clicked.connect(self.black)

    def black(self):
        # чё-то её раздуваеть =))
        try:
            p = self.fname[0]
            image = Image.open(p)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()

            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    S = (a + b + c) // 3
                    draw.point((i, j), (S, S, S))
            img_tmp = ImageQt(image.convert('RGBA'))
            pmap = QPixmap.fromImage(img_tmp)
            self.label.setPixmap(pmap)

        except Exception as e:
            print(e)


    def initUT(self):
        # ссылки на иконки
        SMILE_SRC = r'picture_button\smile.jpg'
        MELANCHOLY_SRC = r'picture_button\melancholy.jpg'
        BOLT_SRC = r'picture_button\b.jpg'
        ITALIC_SRC = r'picture_button\i.jpg'

        # подключаемся к toolbar
        toolbar = self.toolBar
        # добавляем кнопок в toolbar
        self.set_smile(SMILE_SRC, 'Smile', toolbar)
        self.set_smile(MELANCHOLY_SRC, 'Melancholy', toolbar)
        self.set_format(BOLT_SRC, 'Bolt', toolbar)
        self.set_format(ITALIC_SRC, 'italic', toolbar)

        # подключаемся к menubar
        menubar = self.menuBar()
        # подключаемся к menubar
        self.conn_menu(menubar)
        # отображени окна
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SendMessageWindow()
    sys.exit(app.exec_())