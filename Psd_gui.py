import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QFrame, QGridLayout, QLineEdit, QPushButton, QCheckBox, QFileDialog, QLabel, \
    QProgressBar
from time import time
import Psd_core as psc
import BaseFunc as bd


class PsdGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.after_slash_mode = False
        self.original_save_mode = True
        self.psd_to_png_mode = True
        self.png_to_gif_mode = False
        self.status = QLabel("Простой")
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

        # Четвёртый блок параметров
        self.subprocess_frame = QFrame(self)
        self.subprocess_frame.setFrameShape(QFrame.Box)
        self.subprocess_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        self.subprocess_layout = QGridLayout(self.subprocess_frame)
        self.setup_subprocess_frame(self.subprocess_layout)

        self.unload_resent()
        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(self.paths_frame, 0, 0)
        self.main_layout.addWidget(self.base_frame, 1, 0)
        self.main_layout.addWidget(self.subprocess_frame, 3, 0)

    def setup_paths_frame(self, layout):
        # фрейм для путей
        self.input_path = QLineEdit()
        layout.addWidget(self.input_path, 1, 0)
        choose_folder_button = QPushButton("Выбрать папку")
        choose_folder_button.clicked.connect(self.show_folder_dialog)
        layout.addWidget(choose_folder_button, 1, 1)
        self.output_path = QLineEdit()
        layout.addWidget(self.output_path, 2, 0, 1, 2)

    def setup_base_frame(self, layout):
        self.after_slash = QCheckBox('После разрезки(НЕАРАБ)')
        self.after_slash.setChecked(self.after_slash_mode)
        self.after_slash.stateChanged.connect(self.toggle_after_slash)
        layout.addWidget(self.after_slash, 3, 0, 1, 2)

        self.original_save = QCheckBox('Сохранять исходные файлы')
        self.original_save.setChecked(self.original_save_mode)
        self.original_save.stateChanged.connect(self.toggle_original_save)
        layout.addWidget(self.original_save, 3, 1, 1, 2)

        self.textPSD_PNG_GIF = QLabel('Если выбраны оба варианта значит (PSD -> GIF):')
        layout.addWidget(self.textPSD_PNG_GIF, 4, 0, 1, 0)

        self.psd_to_png_box = QCheckBox('PSD -> PNG')
        self.psd_to_png_box.setChecked(self.psd_to_png_mode)
        self.psd_to_png_box.stateChanged.connect(self.toggle_psd_to_png)
        layout.addWidget(self.psd_to_png_box, 5, 0, 1, 2)

        self.png_to_gif_box = QCheckBox('PNG -> GIF')
        self.png_to_gif_box.setChecked(self.png_to_gif_mode)
        self.png_to_gif_box.stateChanged.connect(self.toggle_png_to_gif)
        layout.addWidget(self.png_to_gif_box, 5, 1, 1, 2)

    def setup_subprocess_frame(self, layout):
        # Прогресс фрейм
        layout.addWidget(self.status, 0, 0)
        yes_button = QPushButton('ПОПЛЫЛИ', self)
        yes_button.clicked.connect(self.launch_convert)
        layout.addWidget(yes_button, 0, 1)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 1, 0, 2, 2)
        self.progress_timer = QTimer(self)

    def launch_convert(self):
        if not self.pre_process_check():
            pass
        else:
            self.progress_timer.start(100)

            starting_time = time()
            try:
                process_status = self.convert_process()
            except Exception as e:
                process_status = "Краш"
            ending_time = time()
            delta = ending_time - starting_time
            if (process_status == "Краш"):
                self.status.setText(process_status)
            elif (process_status == "complete"):
                self.status.setText("Фаилы успешно обработаны за " + str(format(delta, '.2f')) + "сек!")
            else:
                self.status.setText(process_status)

    def convert_process(self):
        self.load_resent()
        """Основная функция запуска конвертации и отображения в поле статуса процесса"""
        self.status.setText("Выполнение - Загрузка файлов изображений!")
        self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)
        folder_paths = psc.get_folder_paths(False, self.input_path.text(), self.output_path.text())
        self.num_of_inputs = len(folder_paths)
        if (self.num_of_inputs == 0):
            return "Пакетный режим(Но внутри нет папок)"
        # Проверяем выбрана ли конвертация PSD в PNG
        self.update_gui_progress("Работа - конвертируем PSD в PNG", 10)
        if self.psd_to_png_mode == True:
            list_to_work = psc.convert_all_psd_to_png(folder_paths[0][0], folder_paths[0][1], self.original_save_mode)
            for i in range(len(list_to_work[0])):
                self.status.setText(
                    self.update_gui_progress(f"Работа - обрабатываем {i + 1} изображение", (10 / self.num_of_inputs)))
                psc.convert_psd_to_png(list_to_work[0][i], list_to_work[1][i])
            if self.png_to_gif_mode == True:
                self.status.setText(self.update_gui_progress(f"Работа - обрабатываем GIF", (10 / self.num_of_inputs)))
                psc.convert_png_to_gif(folder_paths[0][1], folder_paths[0][1])
                return "complete"
        elif self.png_to_gif_mode == True:
            self.status.setText(self.update_gui_progress(f"Работа - обрабатываем GIF", 40))
            psc.convert_png_to_gif(folder_paths[0][0], folder_paths[0][0])
            self.progress_value = 100
        else:
            return "Всё пошло не так"
        return "complete"

    def update_gui_progress(self, status_message, progress_increase):
        """Обновляет статус и увеличивает прогресс на заданное значение"""
        self.status.setText(status_message)
        self.progress_value += progress_increase
        self.progress_bar.setValue(int(self.progress_value))

    def pre_process_check(self):
        # проверяем введённые данные
        if self.psd_to_png_mode == False and self.png_to_gif_mode == False:
            self.status.setText("Что делаем то?")
            return False
        if str(self.input_path.text()) == "":
            self.status.setText("Не указан путь к входной папке!")
            return False
        if (str(self.output_path.text()) == ""):
            self.status.setText("Не задан путь к выходной папке!")
            return False
        if (not os.path.exists(str(self.input_path.text()))):
            self.status.setText("Путь к входной папке не существует.")
            return False
        return True

    def toggle_original_save(self, state):
        if state == 2:
            self.original_save_mode = True
        else:
            self.original_save_mode = False
        self.load_resent()

    def toggle_after_slash(self, state):
        if state == 2:
            self.after_slash_mode = True
        else:
            self.after_slash_mode = False
        self.load_resent()

    def toggle_psd_to_png(self, state):
        if state == 2:
            self.psd_to_png_mode = True
        else:
            self.psd_to_png_mode = False
        self.load_resent()

    def toggle_png_to_gif(self, state):
        if state == 2:
            self.png_to_gif_mode = True
        else:
            self.png_to_gif_mode = False
        self.load_resent()

    def show_folder_dialog(self):
        # Открываем диалоговое окно выбора папки
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", "")
        # Обновляем строку ввода пути и метку с выбранной папкой
        if folder_path:
            self.input_path.setText(folder_path)
            self.output_path.setText(folder_path + "[PNG]")

    def load_resent(self):
        load_var = {
            "after_slash_mode": str(self.after_slash_mode),
            "original_save_mode": str(self.original_save_mode),
            "psd_to_png_mode": str(self.psd_to_png_mode),
            "png_to_gif_mode": str(self.png_to_gif_mode),
        }
        bd.update_recent_set(load_var)

    def unload_resent(self):
        unload_var = bd.get_recent_set()
        if unload_var.get("original_save_mode") is not None:
            self.after_slash_mode = unload_var.get("after_slash_mode").lower() == "true"
            self.original_save_mode = unload_var.get("original_save_mode").lower() == "true"
            self.psd_to_png_mode = unload_var.get("psd_to_png_mode").lower() == "true"
            self.png_to_gif_mode = unload_var.get("png_to_gif_mode").lower() == "true"
            self.after_slash.setChecked(self.after_slash_mode)
            self.original_save.setChecked(self.original_save_mode)
            self.psd_to_png_box.setChecked(self.psd_to_png_mode)
            self.png_to_gif_box.setChecked(self.png_to_gif_mode)
        else:
            self.load_resent()
