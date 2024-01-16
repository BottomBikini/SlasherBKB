import sys

from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QTabWidget, QGridLayout
import SlasherBKB as firstapp
import Templates as tepl


class Centres(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.set_dark_background()
        self.setWindowTitle('SlasherBKB')
        self.setWindowIcon(QIcon('res/SlasherBKBLogo.ico'))

        self.tab_widget = QTabWidget(self)  # Таб виджет

        slasher_wid = QWidget()
        self.slash_window = firstapp.SlasherBKB()
        slasher_layout = QGridLayout(slasher_wid)
        slasher_layout.addWidget(self.slash_window)

        self.tab_widget.addTab(slasher_wid, "Слэшер")  # В который мы кладём QWidget tab_a
        self.tab_widget.tabBar().setTabTextColor(self.tab_widget.indexOf(slasher_wid), QColor("black"))

        tempalate_wid = QWidget()
        tepl_window = tepl.Templates()
        tepl_layout = QGridLayout(tempalate_wid)
        tepl_layout.addWidget(tepl_window)

        self.tab_widget.addTab(tempalate_wid, "Шаблоны")  # В который мы кладём QWidget tab_a
        self.tab_widget.tabBar().setTabTextColor(self.tab_widget.indexOf(tempalate_wid), QColor("black"))


        self.tab_widget.currentChanged.connect(self.tab_changed)

        # Заглушка ПИЗДЕЦ
        tempalate_wid.setFixedSize(480, 425)
        slasher_wid.setFixedSize(480, 425)
        self.tab_widget.setFixedSize(480, 425)

    def tab_changed(self, index):
        if index == 0:
            self.slash_window.unload_resent()
        if index == 1:
            self.slash_window.load_resent()

    def set_dark_background(self):
        # Устанавливаем темный фон
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)


if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Centres()
        window.show()
        sys.exit(app.exec_())
