import sys
from GUI.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from dev.config import Config

d = Config()
print(d.language)
app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())

