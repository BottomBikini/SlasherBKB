import os
import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QApplication, QFrame, QGridLayout, QPushButton, QCheckBox, \
    QComboBox, QProgressBar, QFileDialog
from PyQt5.QtGui import QIcon, QPalette, QColor, QDesktopServices
from PyQt5.QtCore import QUrl, QTimer
from time import time
import SlasherBKBCore as sbc


class SlasherBKB(QWidget):
    def __init__(self):
        super().__init__()
        self.custom_enforce_width = None
        self.progress_value = None
        self.status = None
        self.width_enforce_types = None
        self.width_enforce_type = None
        self.scan_line_step = None
        self.ignorable_edges_pixels = None
        self.slicing_senstivity = None
        self.show_advanced_settings = None
        self.output_files_type = None
        self.num_split = None
        self.num_pixel = None
        self.pixels_mode = None
        self.split_mode = None
        self.batch_mode = None
        self.output_path = None
        self.input_path = None
        self.initUI()

    def variables(self):
        self.input_path = QLineEdit('')
        self.output_path = QLineEdit('')
        self.batch_mode = False
        # Базовые настройки
        self.split_mode = False
        self.pixels_mode = True
        self.num_pixel = QLineEdit("10000")
        self.num_split = QLineEdit("10")
        self.output_files_type = ".png"
        # Расширенные настройки
        self.show_advanced_settings = False
        self.slicing_senstivity = QLineEdit("90")
        self.ignorable_edges_pixels = QLineEdit("10")
        self.scan_line_step = QLineEdit("5")
        self.width_enforce_type = "Без соблюдения ширины"
        self.width_enforce_types = ['Без соблюдения ширины', 'Автоматическая равномерная ширина',
                                    'Пользовательская ширина']
        self.custom_enforce_width = "720"
        # Статусы
        self.status = QLabel("Простой")
        self.progress_value = 0
        ####
        self.show_subprocess_settings = False
        self.enable_subprocess_execution = False
        self.subprocess_path = ''
        self.subprocess_arguments = ''

    def initUI(self):
        self.variables()
        # GUI
        self.set_dark_background()
        self.setGeometry(0, 0, 400, 300)  # Set your window size here

        screen = QApplication.instance().desktop().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        self.setWindowTitle('SlasherBKB')
        self.setWindowIcon(QIcon('res/SlasherBKBLogo.ico'))

        # Первый блок параметров
        paths_frame = QFrame(self)
        paths_frame.setFrameShape(QFrame.Box)
        paths_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        paths_layout = QGridLayout(paths_frame)
        self.setup_paths_frame(paths_layout)

        # Второй блок параметров
        basic_frame = QFrame(self)
        basic_frame.setFrameShape(QFrame.Box)
        basic_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        basic_layout = QGridLayout(basic_frame)
        self.setup_basic_frame(basic_layout)

        # Третий блок параметров
        advanced_frame = QFrame(self)
        advanced_frame.setFrameShape(QFrame.Box)
        advanced_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        advanced_layout = QGridLayout(advanced_frame)
        self.setup_advanced_frame(advanced_layout)

        # Четвёртый блок параметров
        subprocess_frame = QFrame(self)
        subprocess_frame.setFrameShape(QFrame.Box)
        subprocess_frame.setStyleSheet("QFrame { border: 1px solid white;}")
        subprocess_layout = QGridLayout(subprocess_frame)
        self.setup_subprocess_frame(subprocess_layout)

        # Размещаем блоки
        main_layout = QGridLayout(self)
        main_layout.setColumnStretch(0, 0)
        main_layout.setRowStretch(0, 0)
        main_layout.setRowStretch(1, 0)
        main_layout.setRowStretch(2, 0)
        main_layout.setRowStretch(3, 0)
        main_layout.addWidget(paths_frame, 0, 0)
        main_layout.addWidget(basic_frame, 1, 0)
        main_layout.addWidget(advanced_frame, 2, 0)
        main_layout.addWidget(subprocess_frame, 3, 0)

    def setup_paths_frame(self, layout):
        # фрейм для путей
        self.input_path = QLineEdit()
        layout.addWidget(self.input_path, 1, 0)
        choose_folder_button = QPushButton("Выбрать папку")
        choose_folder_button.clicked.connect(self.show_folder_dialog)
        layout.addWidget(choose_folder_button, 1, 1)
        self.output_path = QLineEdit()
        layout.addWidget(self.output_path, 2, 0, 1, 2)

        self.checkbox = QCheckBox('Пакетный режим [Входная папка содержит несколько папок с главами]')
        self.checkbox.stateChanged.connect(self.toggle_batch_mode)
        layout.addWidget(self.checkbox, 3, 0, 1, 2)

    def setup_basic_frame(self, layout):
        # Фрейм с базовыми настройками
        self.pixel_checkbox = QCheckBox("Высота скана(в пикселях):")
        self.pixel_checkbox.setChecked(self.pixels_mode)
        self.pixel_checkbox.stateChanged.connect(self.toggle_pixel_mode)
        layout.addWidget(self.pixel_checkbox, 0, 0)
        layout.addWidget(self.num_pixel, 1, 0)
        self.split_checkbox = QCheckBox('Кол-во сканов на выходе:')
        self.split_checkbox.setChecked(self.split_mode)
        self.split_checkbox.stateChanged.connect(self.toggle_split_mode)
        layout.addWidget(self.split_checkbox, 0, 1)
        layout.addWidget(self.num_split, 1, 1)
        self.type_image_box = QComboBox(self)
        self.type_image_box.addItems([".png", ".jpg"])
        self.type_image_box.currentIndexChanged.connect(self.type_image_box_change)
        layout.addWidget(self.type_image_box, 2, 0)
        self.open_link_button = QPushButton("VK:Bikini Bottom", self)
        self.open_link_button.clicked.connect(self.open_link)
        layout.addWidget(self.open_link_button, 2, 1)

    def setup_advanced_frame(self, layout):
        # Фрейм для расширенных настроек
        self.advanced_settings_checkbox = QCheckBox('Показать расширенные настройки')
        self.advanced_settings_checkbox.setChecked(self.show_advanced_settings)
        self.advanced_settings_checkbox.stateChanged.connect(self.toggle_advanced_settings)
        layout.addWidget(self.advanced_settings_checkbox, 0, 0)
        self.tmplayot = layout

    def setup_subprocess_frame(self, layout):
        # Прогресс фрейм
        layout.addWidget(self.status, 0, 0)
        yes_button = QPushButton('ПОПЛЫЛИ', self)
        yes_button.clicked.connect(self.launch_slash)
        layout.addWidget(yes_button, 0, 1)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 1, 0, 2, 2)
        self.progress_timer = QTimer(self)

    def launch_slash(self):
        if not self.pre_process_check():
            pass
        else:
            self.progress_timer.start(100)

            starting_time = time()
            try:
                process_status = self.stitch_process()
            except Exception as e:
                process_status = "Краш"
            ending_time = time()
            delta = ending_time - starting_time
            if (process_status == "Краш"):
                self.status.setText(process_status)
            elif (process_status == "complete"):
                self.status.setText("Фаил успешно разрезан за " + str(format(delta, '.2f')) + "сек!")
            else:
                self.status.setText(process_status)

    def pre_process_check(self):
        # проверяем введённые данные
        if str(self.input_path.text()) == "":
            self.status.setText("Не указан путь к входной папке!")
            return False
        if (str(self.output_path.text()) == ""):
            self.status.setText("Не задан путь к выходной папке!")
            return False
        if (not os.path.exists(str(self.input_path.text()))):
            self.status.setText("Путь к входной папке не существует.")
            return False
        if (str(self.num_pixel.text()) == "" or str(self.num_pixel.text()) == "0"):
            self.status.setText("Значение 'Высоты сканов' не было установлено")
            return False
        if (str(self.num_split.text()) == "" or str(self.num_split.text()) == "0"):
            self.status.setText("Значение 'Кол-во сканов' не было установлено!")
            return False
        if (str(self.slicing_senstivity.text()) == ""):
            self.status.setText("Значение чувствительности обнаружения не было установлено!")
            return False
        if (str(self.ignorable_edges_pixels.text()) == ""):
            self.status.setText("Не установлено значение игнорирвания пикселей")
            return False
        if (str(self.scan_line_step.text()) == ""):
            self.status.setText("Не установлено значение шага линии сканирования!")
            return False
        return True

    def add_advanced_layout(self):
        self.unadvanced_layout = QGridLayout()
        self.tmplayot.addLayout(self.unadvanced_layout, 1, 0)

        self.senstivity_label = QLabel('Чувствительность при обнаружении пустоты(%):')
        self.unadvanced_layout.addWidget(self.senstivity_label, 0, 0)
        self.scan_line_step_label = QLabel('Отступ от конца скана:')
        self.unadvanced_layout.addWidget(self.scan_line_step_label, 2, 0)
        self.ignorable_pixels_label = QLabel('Игнорируемые пиксели границ:')
        self.unadvanced_layout.addWidget(self.ignorable_pixels_label, 0, 1)

        self.slicing_senstivity_la = QLineEdit(self.slicing_senstivity.text())
        self.unadvanced_layout.addWidget(self.slicing_senstivity_la, 1, 0)
        self.ignorable_edges_pixels_la = QLineEdit(self.ignorable_edges_pixels.text())
        self.unadvanced_layout.addWidget(self.ignorable_edges_pixels_la, 1, 1)
        self.scan_line_step_la = QLineEdit(self.scan_line_step.text())
        self.unadvanced_layout.addWidget(self.scan_line_step_la, 3, 0)

        self.width_enforce_type_label = QLabel('Настройка ширины:')
        self.unadvanced_layout.addWidget(self.width_enforce_type_label, 2, 1)
        self.width_enforce_type_input = QLineEdit()
        self.width_enforce_type_input.setText("Временно не работает")
        self.width_enforce_type_input.setReadOnly(True)
        self.unadvanced_layout.addWidget(self.width_enforce_type_input, 3, 1)

    def remove_advanced_layout(self):
        # Скрывание расширенных настроек
        while self.unadvanced_layout.count():
            item = self.unadvanced_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.resize(200, 300)

    def toggle_advanced_settings(self, state):
        if state == 2:
            self.show_advanced_settings = True
            self.add_advanced_layout()
        else:
            self.show_advanced_settings = False
            self.remove_advanced_layout()

    def toggle_batch_mode(self, state):
        if state == 2:
            self.batch_mode = True
        else:
            self.batch_mode = False

    def toggle_pixel_mode(self, state):
        if state == 2:
            self.pixels_mode = True
            self.split_mode = False
            self.split_checkbox.setChecked(False)
        else:
            self.pixels_mode = False
            self.split_mode = True

    def toggle_split_mode(self, state):
        if state == 2:
            self.pixels_mode = False
            self.split_mode = True
            self.pixel_checkbox.setChecked(False)
        else:
            self.pixels_mode = True
            self.split_mode = False

    def open_link(self):
        QDesktopServices.openUrl(QUrl("https://vk.com/bkbmanga"))

    def type_image_box_change(self, index):
        output_files_type = self.type_image_box.itemText(index)
        self.output_files_type = output_files_type

    def set_dark_background(self):
        # Устанавливаем темный фон
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

    def show_folder_dialog(self):
        # Открываем диалоговое окно выбора папки
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", "")
        # Обновляем строку ввода пути и метку с выбранной папкой
        if folder_path:
            self.input_path.setText(folder_path)
            self.output_path.setText(folder_path + "[Разрезано]")

    def stitch_process(self):
        """Основная функция запуска разрезки и отображения в поле статуса процесса"""
        self.status.setText("Выполнение - Загрузка файлов изображений!")
        self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)
        # потом
        # self.subprocess_console['text'] = ""
        folder_paths = sbc.get_folder_paths(self.batch_mode, self.input_path.text(), self.output_path.text())
        # Устанавливает количество папок в качестве глобальной переменной использования в других функциях.
        self.num_of_inputs = len(folder_paths)
        if (self.num_of_inputs == 0):
            return "Пакетный режим(Но внутри нет папок)"
        for path in folder_paths:
            images = sbc.load_images(path[0])
            if len(images) == 0 and self.num_of_inputs == 1:
                return "Изображения не найдены"
            elif len(images) == 0:
                continue

            # The reason index is used here is because the core functions use intgers to switch between enforcement modes/types

            width_type_index = self.width_enforce_types.index(self.width_enforce_type)
            if width_type_index == 0:
                self.update_gui_progress(" Работа - Склеивание файлов изображений", (10 / self.num_of_inputs))
            else:
                self.update_gui_progress("Работа - Изменение размеров и склеивания файлов Изображений!",
                                         (10 / self.num_of_inputs))
            resized_images = sbc.resize_images(images, width_type_index, self.custom_enforce_width)
            combined_image = sbc.combine_images(resized_images)

            # Проверяем какой мод стоит, по пикселям или по кол-ву
            if self.pixels_mode:
                self.update_gui_progress("Работа - Нарезка склееного изображения на итоговые изображения!",
                                         (10 / self.num_of_inputs))
                final_images = sbc.split_image(combined_image, self.num_pixel.text(), self.slicing_senstivity.text(),
                                               self.ignorable_edges_pixels.text(), self.scan_line_step.text())
            if not self.pixels_mode:
                self.update_gui_progress("Работа - Нарезка склееного изображения на итоговые изображения!",
                                         (10 / self.num_of_inputs))
                final_images = sbc.split_image(combined_image,
                                               sbc.new_count_heights(resized_images, self.num_split.text()),
                                               self.slicing_senstivity.text(),
                                               self.ignorable_edges_pixels.text(), self.scan_line_step.text())
            self.update_gui_progress("Работа - Сохранение Итоговых Изображений!", (20 / self.num_of_inputs))
            # Сохранение изображений, самый длительный этап
            sbc.save_data(final_images, path[1], self.output_files_type, self.update_saving_progress)
        return "complete"

    def update_gui_progress(self, status_message, progress_increase):
        """Обновляет статус и увеличивает прогресс на заданное значение"""
        self.status.setText(status_message)
        self.progress_value += progress_increase
        self.progress_bar.setValue(int(self.progress_value))

    def update_saving_progress(self, num_of_data):
        """Обновляет значение прогресса в соответствии с количеством сохраняемых файлов."""
        self.progress_value += ((60 * 1 / num_of_data) / self.num_of_inputs)
        self.progress_bar.setValue(int(self.progress_value))


if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = SlasherBKB()
        window.show()
        sys.exit(app.exec_())
