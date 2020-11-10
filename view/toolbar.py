from PyQt5.QtWidgets import QMainWindow, QAction


class ToolBar(QMainWindow):
    def __init__(self, parent):
        super(QMainWindow, self).__init__(parent)
        
        openFile = QAction('Open', parent)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(parent.open_file)
        
        saveFile = QAction('Save', parent)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(parent.save_file)
        
        importData = QAction('Import', parent)
        importData.setStatusTip('Import Data')
        importData.triggered.connect(parent.import_data)
        
        menubar = parent.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openFile)
        filemenu.addAction(saveFile)
        filemenu.addAction(importData)


        
        settings= QAction('Settings', parent)
        settings.setStatusTip('Open settings')
        settings.triggered.connect(parent.open_settings)
        

        settingmenu = menubar.addMenu('&Settings')
        settingmenu.addAction(settings)        
        
        helpmenu = menubar.addMenu('&Help')
        
        
