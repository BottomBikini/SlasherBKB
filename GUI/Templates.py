from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from MAIN.Core import BaseFunc as bd


class Templates(QWidget):
    def __init__(self):
        super(Templates, self).__init__()
        self.all_words = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.textlab = QLabel('Выставите нужные настройки и создайте/выберите шаблон:')
        self.textlab.setStyleSheet("color: red; font-size: 18px;")

        self.line_edit = QLineEdit(self)
        self.add_button = QPushButton("+", self)
        self.add_button.clicked.connect(self.add_button_clicked)

        self.line_layout = QHBoxLayout()
        self.line_layout.addWidget(self.line_edit)
        self.line_layout.addWidget(self.add_button)

        self.layout.addWidget(self.textlab)
        self.layout.addLayout(self.line_layout)
        self.layout.setAlignment(self.textlab, QtCore.Qt.AlignTop)
        self.layout.setAlignment(self.line_layout, QtCore.Qt.AlignTop)  # выравнивание по верху

        # Один QVBoxLayout для всех кнопок
        self.button_layout = QVBoxLayout()

        bd.create_table_presets()
        old_pres = bd.get_all_presets()
        self.list_name = []
        for i in range(len(old_pres)):
            preset = old_pres[i]['name']
            self.list_name.append(preset)
            self.add_button_clicked(wordes=preset)

    def add_button_clicked(self, wordes):
        if wordes:
            word = wordes
        else:
            word = self.line_edit.text()
        if len(self.all_words) < 10 and word not in self.all_words:
            if word:
                self.all_words.append(word)

                button_Hlayout = QHBoxLayout()

                word_button = QPushButton(word, self)
                word_button.clicked.connect(lambda _, btn=word_button: self.word_button_clicked(btn))
                button_Hlayout.addWidget(word_button)

                remove_button = QPushButton("-", self)
                remove_button.clicked.connect(lambda _, btn=word_button: self.remove_button_clicked(btn))
                button_Hlayout.addWidget(remove_button)

                if word not in self.list_name:
                    preset = bd.get_recent_set()
                    preset["name"] = word
                    bd.create_new_preset(data=preset)

                self.button_layout.addLayout(button_Hlayout)
                self.layout.addLayout(self.button_layout)
                self.layout.setAlignment(self.button_layout, QtCore.Qt.AlignTop)
                self.line_edit.clear()

    def word_button_clicked(self, button):
        pres_to_load = bd.get_one_preset(button.text())
        del pres_to_load['name']
        bd.update_recent_set(pres_to_load)

    def remove_button_clicked(self, button):
        for i in reversed(range(self.button_layout.count())):
            layout_item = self.button_layout.itemAt(i)
            if layout_item and layout_item.layout():
                h_layout = layout_item.layout()
                if h_layout.itemAt(0).widget() == button:
                    h_layout.itemAt(0).widget().deleteLater()
                    h_layout.itemAt(1).widget().deleteLater()
                    h_layout.deleteLater()
                    bd.delete_preset(button.text())
                    self.all_words.remove(button.text())
                    break
