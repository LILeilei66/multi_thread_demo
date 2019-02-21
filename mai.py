import sys
from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QLabel,       QPushButton, QApplication, QLineEdit,QTextBrowser, QVBoxLayout, QWidget)
from PyQt5.QtCore import QThread, QObject, pyqtSignal


class MainWindow(QMainWindow):
    startCalcSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_thread_and_connect()

    def init_ui(self):
        self.input_data_edit = QLineEdit()
        self.calc_btn = QPushButton('计算')
        calc_layout = QHBoxLayout()
        calc_layout.addWidget(self.input_data_edit)
        calc_layout.addWidget(self.calc_btn)

        info_label = QLabel('进度：')
        info_label_layout = QHBoxLayout()
        info_label_layout.addWidget(info_label)
        info_label_layout.addStretch(1)
        self.info_text = QTextBrowser()

        result_label = QLabel('结果：')
        result_label_layout = QHBoxLayout()
        result_label_layout.addWidget(result_label)
        result_label_layout.addStretch(1)
        self.result_edit = QLineEdit()

        main_layout = QVBoxLayout()
        main_layout.addLayout(calc_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(info_label_layout)
        main_layout.addWidget(self.info_text)
        main_layout.addSpacing(20)
        main_layout.addLayout(result_label_layout)
        main_layout.addWidget(self.result_edit)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        

    def init_thread_and_connect(self):
        self.myWorkerThread = WorkerThread()
        self.myClearThread = ClearThread()

        self.calc_btn.clicked.connect(self.myClearThread,self.myWorkerThread)
        self.myWorkerThread.infoSignal.connect(self.process_info)
        
        self.sub_thread_object.classificationResultSignal.connect(self.process_result)

        self.sub_thread.start()
        self.sub_thread_object.moveToThread(self.sub_thread)   

    
 

class ClearThread(QThread,MainWindow):
    textclearedSignal=pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def clearText(self):
        self.info_text.append('10086')

class WorkerThread(QThread,MainWindow):
    classificationResultSignal = pyqtSignal(int)
    infoSignal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def classification(self, data):
        self.infoSignal.emit("开始计算")
    
        try:
            time.sleep(5)
            result = int(data) * 2
        except Exception as e:
            self.infoSignal.emit("参数错误")
            return
    
        self.classificationResultSignal.emit(result)
        self.infoSignal.emit("计算完成")   
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())