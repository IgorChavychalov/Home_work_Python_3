#!/usr/bin/python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton



class OpenImage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.btn_save = QPushButton('добавить в базу')
        self.btn_dell = QPushButton('удалить из базы')
        self.btn_show = QPushButton('показать базу')
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.le_input = QtWidgets.QLineEdit()
        self.le_output = QtWidgets.QLabel('')
        self.lbl_name = QtWidgets.QLabel('Name')
        self.hbox.addWidget(self.lbl_name)
        self.hbox.addWidget(self.le_input)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.le_output)
        self.vbox.addWidget(self.btn_show)
        self.vbox.addWidget(self.btn_save)
        self.vbox.addWidget(self.btn_dell)
        self.setLayout(self.vbox)

        self.initUT()

    def save_into_db(self):
        item = {}
        try:
            value = self.le_input.text()
            item['name'] = value
            self.collection.insert_one(item)
            self.le_output.setText('Сохранено')
            self.load_into_db()
        except Exception as e:
            print(e)

    def load_into_db(self):
        m = ''
        i = 0
        for collection in self.collection.find():
            t = str(collection.__repr__())
            i += 1
            m = f'{m}\n{i}.{t}'
        self.le_output.setText(m)

    def dell_into_db(self):
        item = {}
        value = self.le_input.text()
        item['name'] = value
        self.collection.remove(item)
        self.load_into_db()

    def initUT(self):
        client = MongoClient()
        db = client.db
        self.collection = db.new_collection
        try:
            self.btn_save.clicked.connect(self.save_into_db)
            self.btn_dell.clicked.connect(self.dell_into_db)
            self.btn_show.clicked.connect(self.load_into_db)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = OpenImage()
    w.setWindowTitle('Работа с Монго')
    w.resize(400, 370)
    w.show()
    sys.exit(app.exec_())
