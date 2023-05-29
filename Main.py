#Dung cho Qt5
from PyQt5 import QtWidgets, uic, QtGui, Qt
from PyQt5.QtWidgets import QMessageBox

import numpy as np
import sys
from PyQt5.QtCore import QRect, Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter,QPen,QPixmap
# pip install pyqt5, pip install pyqt5 tools
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QLabel, QHBoxLayout, QMessageBox,QWidget,QFontDialog,QColorDialog,QCheckBox,QMenu, QTableWidgetItem,QDialog
from PyQt5 import QtGui,QtCore
# just change the name

class second_screen(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('DHTABLE.ui', self) # Load the .ui file
# Khoi tao ban dau
        self.data_alpha = -1
        self.data_theta = -1
        self.data_a = -1
        self.data_d = -1
#Start
        self.pushButton_Remove.clicked.connect(self.remove_row)
        self.pushButton_Save.clicked.connect(self.Save)  

        self.pushButton_Alpha.clicked.connect(self.DH_Alpha)
        self.pushButton_Nhapa.clicked.connect(self.DH_A)
        self.pushButton_Nhapd.clicked.connect(self.DH_D)
        self.pushButton_Theta.clicked.connect(self.DH_Theta)

#     def remove_row(self):
#         current_row = self.tableWidget.currentRow()
#         if (current_row!=0):
#             self.tableWidget.removeRow(current_row)

#     #Doc o bat ky, ung dung lay thong so trong bang
#     def read_cell(self):
#         try:
#             a = self.uic.tableWidget.item(0,0).text()
#             print(a)
#         except:
#             print("empty")
# #Tao Save
#     def Save(self):
#         self.data_alpha = self.lineEdit_1.text()
#         self.data_theta= self.lineEdit_2.text()
#         self.data_a = self.lineEdit_3.text()
#         self.data_d = self.lineEdit_4.text()
#         if self.data_a!='' and self.data_d!='' and self.data_alpha[0]!='' and self.data_theta[0]!='':
#             #Qtimer _ progress
#             timer = QTimer(self)
#             self.a = 0
#             timer.timeout.connect(self.process)
#             timer.start(5)    
#         else:
#             QMessageBox.information(self,"Notice","Nhap thieu du lieu roi")

#     def process(self):
#         self.a +=1
#         self.progressBar.setValue(self.a)
#         if (self.progressBar.value()==100):
#             row_bottom = self.tableWidget.rowCount()
#             self.tableWidget.insertRow(row_bottom)
#             self.tableWidget.setVerticalHeaderLabels(['Note','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39'])
#             #add alpha
#             item_alpha = QTableWidgetItem(self.data_alpha)
#             item_alpha.setTextAlignment(Qt.AlignCenter)
#             self.tableWidget.setItem(row_bottom,0,item_alpha)
#             #add theta
#             item_theta = QTableWidgetItem(self.data_theta)
#             item_theta.setTextAlignment(Qt.AlignCenter)
#             self.tableWidget.setItem(row_bottom,1,item_theta)
#             #add a
#             item_a = QTableWidgetItem(self.data_a)
#             item_a.setTextAlignment(Qt.AlignCenter)
#             self.tableWidget.setItem(row_bottom,2,item_a)
#             #add d
#             item_d = QTableWidgetItem(self.data_d)
#             item_d.setTextAlignment(Qt.AlignCenter)
#             self.tableWidget.setItem(row_bottom,3,item_d)
#             #Reset alpha theta a d
#             self.lineEdit_1.setText("")
#             self.lineEdit_2.setText("")
#             self.lineEdit_3.setText("")
#             self.lineEdit_4.setText("")
#             self.progressBar.setValue(0)

if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    main_win = second_screen()
    main_win.show()
    sys.exit(app.exec())