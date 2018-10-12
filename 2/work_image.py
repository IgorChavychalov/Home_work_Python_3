#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from alchemy import Connect, Images
from PyQt5.QtCore import QBuffer, QByteArray
import io
conn = Connect().get_session()


class OpenImage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.btn_open = QPushButton('открыть')
        self.btn_scrop = QPushButton('обрезка')
        self.btn_save = QPushButton('сохранить')
        self.btn_load = QPushButton('загрузить')
        self.vbox = QtWidgets.QVBoxLayout()
        self.lbl = QtWidgets.QLabel('')
        self.vbox.addWidget(self.btn_open)
        self.vbox.addWidget(self.btn_scrop)
        self.vbox.addWidget(self.btn_save)
        self.vbox.addWidget(self.btn_load)
        self.vbox.addWidget(self.lbl)
        self.setLayout(self.vbox)
        self.initUT()

    def open_img(self):
        fname = QFileDialog.getOpenFileName(self)
        # открываем в байтах
        with open(fname[0], "rb") as f:
            r = f.read()
        # конвертируем байты -> QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(r)
        # вставляем в лайбол
        self.past_img(pixmap)

    def past_img(self, pix: QPixmap):
        t = pix.scaled(270, 270, QtCore.Qt.KeepAspectRatio)
        self.lbl.setPixmap(t)

    def scrop_img(self):
        try:
            # получение QPixmap из лайбла
            img = self.lbl.pixmap()
            # конвертируем QPixmap -> PIL Image
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            img.save(buffer, "PNG")
            # img = Image.open(io.BytesIO(r)) # конвертируем байты в изображение
            pil_im = Image.open(io.BytesIO(buffer.data()))
            # Обрезка
            image = pil_im.crop((50, 150, 200, 250))
            # конвертируем PIL Image -> QPixmap
            img_tmp = ImageQt(image.convert('RGBA'))
            pixmap = QPixmap.fromImage(img_tmp)
            # вставляем в лайбол
            self.past_img(pixmap)

        except Exception as e:
            print(e)

    def save_img(self):
        # получение QPixmap изображения из лайбла
        pic = self.lbl.pixmap()
        # конвертируем QPixmap -> байты
        bytes = QByteArray()
        buffer = QBuffer(bytes)
        buffer.open(QtCore.QIODevice.WriteOnly)
        pic.save(buffer, "PNG")
        p = buffer.data()
        # сохраняем в базу
        conn.add(Images(images=p))
        conn.commit()
        self.lbl.setText('сохраненно с изменениями')

    def load_img(self):
        result = []
        # загружаем байты
        result = conn.query(Images).all()
        # находим последний элемент
        img = result[-1].images
        # конвертируем байты -> QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(img)
        # вставляем в лайбол
        self.past_img(pixmap)

    def initUT(self):
        self.btn_open.clicked.connect(self.open_img)
        self.btn_scrop.clicked.connect(self.scrop_img)
        self.btn_save.clicked.connect(self.save_img)
        self.btn_load.clicked.connect(self.load_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = OpenImage()
    w.setWindowTitle('Работа с изображением')
    w.resize(300, 370)
    w.show()
    sys.exit(app.exec_())
