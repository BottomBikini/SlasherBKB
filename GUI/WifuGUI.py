from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QLineEdit, QPushButton, QFileDialog, QCheckBox, QLabel, \
    QComboBox
from MAIN.Core import BaseFunc as bd, Wifu_core as wfc


class WifuGui(QWidget):
    def __init__(self):
        super().__init__()
        self.before_slash_wif_mode = False
        self.noise_mode = False
        self.increase_mode = False
        self.increase_strength = '0.0'
        self.strength_noise = "1 lvl"
        self.type_increase = "По величине"
        self.output_files_type_wifu = "png"
        self.path_to_wif_state = ""
        self.initUI()

    def initUI(self):
        # Первый блок параметров
        self.paths_frame = QFrame(self)
        self.paths_frame.setFrameShape(QFrame.Box)
        self.paths_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        self.paths_layout = QGridLayout(self.paths_frame)
        self.setup_paths_frame(self.paths_layout)

        # Третий блок параметров
        self.base_frame = QFrame(self)
        self.base_frame.setFrameShape(QFrame.Box)
        self.base_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        self.base_layout = QGridLayout(self.base_frame)
        self.setup_base_frame(self.base_layout)

        self.main_layout = QGridLayout(self)
        self.unload_resent()
        self.main_layout.addWidget(self.paths_frame, 0, 0)
        self.main_layout.addWidget(self.base_frame, 1, 0)

    def setup_paths_frame(self, layout):
        # фрейм для путей
        self.input_path = QLineEdit()
        layout.addWidget(self.input_path, 1, 0)
        choose_folder_button = QPushButton("Выбрать папку с изображениями")
        choose_folder_button.clicked.connect(self.show_folder_dialog)
        layout.addWidget(choose_folder_button, 1, 1)
        self.output_path = QLineEdit()
        layout.addWidget(self.output_path, 2, 0, 1, 2)

        self.path_to_wif_line = QLineEdit()
        layout.addWidget(self.path_to_wif_line, 3, 0)
        choose_path_to_wif_button = QPushButton("Выбрать ФАЙЛ вайфу")
        choose_path_to_wif_button.clicked.connect(self.show_path_to_wif_dialog)
        layout.addWidget(choose_path_to_wif_button, 3, 1)

    def setup_base_frame(self, layout):
        self.before_slash = QCheckBox('Выполнить перед разрезкой')
        self.before_slash.setChecked(self.before_slash_wif_mode)
        self.before_slash.stateChanged.connect(self.toggle_before_slash)
        layout.addWidget(self.before_slash, 0, 0, 1, 2)

        self.noise_box = QCheckBox('Шум')
        self.noise_box.setChecked(self.noise_mode)
        self.noise_box.stateChanged.connect(self.toggle_noise_mode)
        layout.addWidget(self.noise_box, 1, 0, 1, 2)

        self.increase_box = QCheckBox('Увеличить')
        self.increase_box.setChecked(self.increase_mode)
        self.increase_box.stateChanged.connect(self.toggle_increase_mode)
        layout.addWidget(self.increase_box, 1, 1, 1, 2)

        self.type_image_box = QComboBox(self)
        self.type_image_box.addItems(["png", "png"])
        self.type_image_box.currentIndexChanged.connect(self.type_image_box_change)
        layout.addWidget(self.type_image_box, 1, 2, 1, 1)

        self.strength_noise_box = QComboBox(self)
        self.strength_noise_box.addItems(["1 lvl", "2 lvl", "3 lvl"])
        self.strength_noise_box.currentIndexChanged.connect(self.strength_noise_change)
        layout.addWidget(self.strength_noise_box, 2, 0, 1, 1)

        self.type_increase_box = QComboBox(self)
        self.type_increase_box.addItems(["По величине:", "По высоте:", "По ширине:"])
        self.type_increase_box.currentIndexChanged.connect(self.type_increase_change)
        layout.addWidget(self.type_increase_box, 2, 1, 1, 1)

        self.increase_num = QLineEdit(self.increase_strength)
        layout.addWidget(self.increase_num, 2, 2, 1, 1)

        self.status = QLabel('ЗАВИСАЕТ ОКНО, А РАБОТА - НЕТ')
        layout.addWidget(self.status, 3, 0, 1, 0)

        yes_button = QPushButton('ПОПЛЫЛИ', self)
        yes_button.clicked.connect(self.launch_wifu)
        layout.addWidget(yes_button, 3, 2, 1, 1)

    def launch_wifu(self):
        self.load_resent()
        if not self.pre_process_check():
            pass
        else:
            self.status.setText(
                wfc.run_wifu(self.input_path.text(), self.path_to_wif_state, self.noise_mode, self.increase_mode,
                             self.increase_strength, self.strength_noise, self.type_increase))

    def pre_process_check(self):
        # проверяем введённые данные
        if (str(self.path_to_wif_state) == ""):
            self.status.setText("Не задан путь к вайфу!")
            return False
        if self.noise_mode == False and self.increase_mode == False:
            self.status.setText("Не указано что делаем!")
            return False
        if self.increase_mode:
            if self.increase_strength:
                try:
                    g = int(self.increase_strength)
                except ValueError:
                    self.status.setText("Укажите целое число в увел!")
                    return False
        if self.before_slash_wif_mode:
            self.status.setText("Запустите Слэшер")
            return False
        else:
            if str(self.input_path.text()) == "":
                self.status.setText("Не указан путь к входной папке!")
                return False
            if (str(self.output_path.text()) == ""):
                self.status.setText("Не задан путь к выходной папке!")
                return False
        return True

    def type_image_box_change(self, index):
        output_files_type = self.type_image_box.itemText(index)
        self.output_files_type_wifu = output_files_type
        self.load_resent()

    def type_increase_change(self, index):
        type_increase = self.type_increase_box.itemText(index)
        self.type_increase = type_increase
        self.load_resent()

    def strength_noise_change(self, index):
        strength_noise = self.strength_noise_box.itemText(index)
        self.strength_noise = strength_noise
        self.load_resent()

    def toggle_increase_mode(self, state):
        if state == 2:
            self.increase_mode = True
        else:
            self.increase_mode = False
        self.load_resent()

    def toggle_noise_mode(self, state):
        if state == 2:
            self.noise_mode = True
        else:
            self.noise_mode = False
        self.load_resent()

    def toggle_before_slash(self, state):
        if state == 2:
            self.before_slash_wif_mode = True
        else:
            self.before_slash_wif_mode = False
        self.load_resent()

    def show_path_to_wif_dialog(self):
        path_to_wifu = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Исполняемые файлы (*.exe);;Все файлы (*)')
        if path_to_wifu:
            self.path_to_wif_line.setText(path_to_wifu[0])
            self.path_to_wif_state = str(path_to_wifu[0])
        self.load_resent()

    def show_folder_dialog(self):
        # Открываем диалоговое окно выбора папки
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", "")
        # Обновляем строку ввода пути и метку с выбранной папкой
        if folder_path:
            self.input_path.setText(folder_path)
            self.output_path.setText(folder_path + "[WIF]")

    def load_resent(self):
        pass
        load_var = {
            "before_slash_wif_mode": str(self.before_slash_wif_mode),
            "noise_mode": str(self.noise_mode),
            "increase_mode": str(self.increase_mode),
            "increase_strength": str(self.increase_num.text()),
            "strength_noise": str(self.strength_noise),
            "type_increase": str(self.type_increase),
            "output_files_type_wifu": str(self.output_files_type_wifu),
            "path_to_wif_state": str(self.path_to_wif_state),
        }
        bd.update_recent_set(load_var)

    def unload_resent(self):
        pass
        unload_var = bd.get_recent_set()
        if unload_var.get("strength_noise") is not None:
            self.before_slash_wif_mode = unload_var.get("before_slash_wif_mode").lower() == "true"
            self.noise_mode = unload_var.get("noise_mode").lower() == "true"
            self.increase_mode = unload_var.get("increase_mode").lower() == "true"
            self.increase_strength = unload_var.get("increase_strength")
            self.strength_noise = unload_var.get("strength_noise")
            self.type_increase = unload_var.get("type_increase")
            self.output_files_type_wifu = unload_var.get("output_files_type_wifu")
            self.path_to_wif_state = unload_var.get("path_to_wif_state")

            self.path_to_wif_line.setText(self.path_to_wif_state)
            self.before_slash.setChecked(self.before_slash_wif_mode)
            self.noise_box.setChecked(self.noise_mode)
            self.increase_box.setChecked(self.increase_mode)
            self.strength_noise_box.setCurrentText(self.strength_noise)
            self.type_increase_box.setCurrentText(self.type_increase)
            self.increase_num.setText(self.increase_strength)
        else:
            self.load_resent()
