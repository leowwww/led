import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from weiwei import leo , save_date

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setWindowTitle('Nixie tube digital identification')
        self.resize(400,300)
        self.setWindowIcon(QIcon('hh.png'))
        self.main()
        self.center()
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        newleft = (screen.width() - size.width())/2
        newtop = (screen.height() - size.height())/2
        self.move(newleft , newtop)
    def main (self):
        layout = QGridLayout()
        #添加控件
        self.label1 = QPushButton("加载视频文件")
        self.label2 = QLineEdit()
        self.label3 = QPushButton('开始')
        self.label6 = QLineEdit()
        self.label4 = QLineEdit('地址')
        self.label5 = QPushButton('保存')
        
        #信号槽函数
        self.label1.clicked.connect(self.loadfile)
        self.label5.clicked.connect(self.savefile)
        self.label3.clicked.connect(self.star)
        layout.addWidget(self.label1,1,0)
        layout.addWidget(self.label2,1,1)
        layout.addWidget(self.label5,2,0)
        layout.addWidget(self.label4,2,1)
        layout.addWidget(self.label3,3,0)
        layout.addWidget(self.label6,3,1)
        self.setLayout(layout)

    def loadfile(self):
        filename,_ = QFileDialog.getOpenFileName(self,"打开文件")
        self.label2.setText(filename)

    def savefile(self):
        filename,_ = QFileDialog.getOpenFileName(self,"打开文件")
        self.label4.setText(filename)
    def star(self):
        filename = self.label2.text()
        up , lower = leo(filename)
        QMessageBox.information(self,"状态","执行完毕!",QMessageBox.Yes|QMessageBox.No , QMessageBox.Yes)
        print(up , lower)
        savename = self.label4.text()
        print(savename)
        if self.label4.text == '':
            QMessageBox.warning(self,"警告","未设置保存路径,默认存在c盘",QMessageBox.Yes|QMessageBox.No ,QMessageBox.yes)
            save_date(up,lower)
        else:
            save_date(up , lower , self.label4.text)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())