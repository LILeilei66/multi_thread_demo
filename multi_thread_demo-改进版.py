
import sys
import time
from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QLabel,
                             QPushButton, QApplication, QLineEdit,
                             QTextBrowser, QVBoxLayout, QWidget)
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
        self.show()

    def init_thread_and_connect(self):
        sub_thread = QThread()
        self.sub_thread_object = SubThreadObject()

        # moveToThread函数要放在信号槽绑定之前，感觉可能是pyQt5的问题。
        # 我测试C++版Qt和pyQt4都没这个问题。
        self.sub_thread_object.moveToThread(sub_thread)

        self.calc_btn.clicked.connect(self.start_calc)
        self.startCalcSignal.connect(self.sub_thread_object.classification)
        self.sub_thread_object.infoSignal.connect(self.process_info)
        self.sub_thread_object.classificationResultSignal.connect(self.process_result)

        sub_thread.start()

    def start_calc(self):
        data = self.input_data_edit.text()
        self.startCalcSignal.emit(data)

    def process_info(self, info):
        self.info_text.append(info)

    def process_result(self, result):
        self.result_edit.setText(str(result))


class SubThreadObject(QObject):
    classificationResultSignal = pyqtSignal(int)
    infoSignal = pyqtSignal(str)

    def classification(self, data):
        self.infoSignal.emit("开始计算")

        try:
            time.sleep(2)
            result = int(data) * 2
        except Exception as e:
            self.infoSignal.emit("参数错误")
            return

        self.classificationResultSignal.emit(result)
        self.infoSignal.emit("计算完成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

