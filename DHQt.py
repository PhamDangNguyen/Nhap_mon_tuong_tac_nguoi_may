#Dung cho Qt5
from PyQt5 import QtWidgets, uic, QtGui, Qt
from PyQt5.QtWidgets import QMessageBox
from math import radians
import re
import numpy as np
import sys
from PyQt5.QtCore import QRect, Qt, QPoint, QTimer
from PyQt5.QtGui import QPainter,QPen,QPixmap
# pip install pyqt5, pip install pyqt5 tools
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QLabel, QHBoxLayout, QMessageBox,QWidget,QFontDialog,QColorDialog,QCheckBox,QMenu, QTableWidgetItem,QDialog
from PyQt5 import QtGui,QtCore
# just change the name

class DH_Input(QDialog):
    def __init__(self):
        super(DH_Input, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('DHPOPUP.ui', self) # Load the .ui file
        self.show() # Show the GUI

class DH_Table(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('DHTABLE.ui', self) # Load the .ui file
# Khoi tao ban dau
        self.data_alpha = -1
        self.data_theta = -1
        self.data_a = -1
        self.data_d = -1

        self.final_data = []
        # self.numJoint = 0
#Start
        self.pushButton_Remove.clicked.connect(self.remove_row)
        self.pushButton_Save.clicked.connect(self.Save)
        self.submit_button.clicked.connect(self.Submit)

        self.pushButton_Alpha.clicked.connect(self.DH_Alpha)
        self.pushButton_Nhapa.clicked.connect(self.DH_A)
        self.pushButton_Nhapd.clicked.connect(self.DH_D)
        self.pushButton_Theta.clicked.connect(self.DH_Theta)

        self.tableWidget.itemDoubleClicked.connect(self.edit)


    def new_popup(self, _suffix):
        self.tempPopup.valueValue.setSuffix(_suffix)
        self.tempPopup.jointMin.setSuffix(_suffix)
        self.tempPopup.jointMax.setSuffix(_suffix)
        self.tempPopup.jointSpeed.setSuffix(_suffix)

        if (_suffix == " m"):
            self.tempPopup.valueValue.setSingleStep(0.1)
            self.tempPopup.jointMin.setSingleStep(0.1)
            self.tempPopup.jointMax.setSingleStep(0.1)
            self.tempPopup.jointSpeed.setSingleStep(0.1)
            self.tempPopup.jointSpeed.setValue(0.1)
        else:
            self.tempPopup.valueValue.setSingleStep(10)
            self.tempPopup.jointMin.setSingleStep(10)
            self.tempPopup.jointMax.setSingleStep(10)
            self.tempPopup.jointSpeed.setSingleStep(10)
            self.tempPopup.jointSpeed.setValue(5)

        # self.tempPopup.jointID.setText(" Q"+str(self.numJoint + 1))

    def edit(self):
        currentSelected = self.tableWidget.selectedItems()
        if not currentSelected: return 
        item = currentSelected[-1]
        current_string = item.text()
        self.edit_row = self.tableWidget.row(item)
        self.edit_column = self.tableWidget.column(item)
        self.tempPopup = DH_Input()
        if (self.edit_column == 0) or (self.edit_column == 3):  self.new_popup(" degree") 
        else: self.new_popup(" m")

        # if (current_string.isdigit()): 
        if (len(current_string) < 10): 
            self.tempPopup.valueButton.setChecked(1)
            self.tempPopup.valueValue.setValue( float(current_string) )
        else:
            minMaxSpeed = current_string[2:-1].split(',')
            self.tempPopup.jointButton.setChecked(1)
            self.tempPopup.jointMin.setValue(float(minMaxSpeed[0]))
            self.tempPopup.jointMax.setValue(float(minMaxSpeed[1]))
            self.tempPopup.jointSpeed.setValue(float(minMaxSpeed[2]))

        self.action = "edit"
        self.tempPopup.actButton.accepted.connect(self.saveDHCOMP)
        self.tempPopup.exec()

    def DH_A(self):
        self.action = "new"
        self.tempPopup = DH_Input()
        self.new_popup(" m")
        self.current_selected = 1
        self.tempPopup.actButton.accepted.connect(self.saveDHCOMP)
        self.tempPopup.exec()

    def DH_D(self):
        self.action = "new"
        self.tempPopup = DH_Input()
        self.new_popup(" m")
        self.current_selected = 2
        self.tempPopup.actButton.accepted.connect(self.saveDHCOMP)
        self.tempPopup.exec()

    def DH_Alpha(self):
        self.action = "new"
        self.tempPopup = DH_Input()
        self.new_popup(" degree")
        self.current_selected = 0
        self.tempPopup.actButton.accepted.connect(self.saveDHCOMP)
        self.tempPopup.exec()

    def DH_Theta(self):
        self.action = "new"
        self.tempPopup = DH_Input()
        self.new_popup(" degree")
        self.current_selected = 3
        self.tempPopup.actButton.accepted.connect(self.saveDHCOMP)
        self.tempPopup.exec()

    def saveDHCOMP(self):
        if (self.action == "new"):
            if   (self.current_selected == 0): l_object = self.lineEdit_1
            elif (self.current_selected == 1): l_object = self.lineEdit_3
            elif (self.current_selected == 2): l_object = self.lineEdit_4
            elif (self.current_selected == 3): l_object = self.lineEdit_2

        get_string = ""
        if (self.tempPopup.valueButton.isChecked()):
            get_string = "{:.4f}".format(self.tempPopup.valueValue.value())
        else:
            if (self.tempPopup.jointMin.value() > self.tempPopup.jointMax.value()): return
            get_string =  "Q({:.4f},{:.4f},{:.4f})".format(self.tempPopup.jointMin.value(), self.tempPopup.jointMax.value(), self.tempPopup.jointSpeed.value())
            # if (len(l_object.getText()) == 0): self.numJoint += 1

        if (self.action == "new"):
            l_object.setText(get_string)
        else:
            item = QTableWidgetItem(get_string)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(self.edit_row, self.edit_column,item)
        self.tempPopup.reject()

    def Submit(self):
        self.final_data = []
        self.numJoint = 0
        self.jointType = []
        self.limit = []
        self.jointSpeeds = []
        for i in range(self.tableWidget.rowCount()):
            singleDH = ""
            for j in range(4):
                cell_string = self.tableWidget.item(i, j).text()
                singleDH = singleDH + cell_string + "  "
                if (len(cell_string) > 10):
                    cell_string = cell_string[2:-1].split(',')
                    self.numJoint += 1
                    if (j == 0) or (j == 3):
                        self.jointType.append('r')
                        self.limit.append( (radians(float(cell_string[0])) , radians(float(cell_string[1]))) )
                        self.jointSpeeds.append(radians(float(cell_string[2])))
                    else:
                        self.jointType.append('l')
                        self.limit.append( (float(cell_string[0]) , float(cell_string[1])) )
                        self.jointSpeeds.append(float(cell_string[2]))

            self.final_data.append(singleDH)
        if (self.numJoint == 0): return
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Confirm Submitting with " + str(self.numJoint) +" Joints ?")
        msgBox.setWindowTitle("Submitting Box")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            # print(self.final_data)
            self.accept()            

    def remove_row(self):
        currentSelected = self.tableWidget.selectedItems()
        if not currentSelected: return        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Confirm Deleting " + str(len(currentSelected)) +" Item ?")
        msgBox.setWindowTitle("Warning Box")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            for item in currentSelected:  
                    self.tableWidget.removeRow(self.tableWidget.row(item))

    # to table 
    def Save(self):
        self.data_alpha = self.lineEdit_1.text()
        self.data_theta= self.lineEdit_2.text()
        self.data_a = self.lineEdit_3.text()
        self.data_d = self.lineEdit_4.text()
        if len(self.data_a)!=0 and len(self.data_d)!=0 and len(self.data_alpha)!=0 and len(self.data_theta)!=0:
            #Qtimer _ progress
            self.process([self.data_alpha, self.data_a, self.data_d, self.data_theta])
        else:
            QMessageBox.information(self,"Notice","Missing Items on DH")

    def process(self, DH_Alpha_A_D_Theta):
        currentSelected = self.tableWidget.selectedItems()
        new_row = 0
        if not currentSelected: new_row =  self.tableWidget.rowCount()
        else: new_row = self.tableWidget.row(currentSelected[-1])

        self.tableWidget.insertRow(new_row)
        #add alpha
        item_alpha = QTableWidgetItem(DH_Alpha_A_D_Theta[0])
        item_alpha.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(new_row,0,item_alpha)
        #add theta
        item_theta = QTableWidgetItem(DH_Alpha_A_D_Theta[3])
        item_theta.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(new_row,3,item_theta)
        #add a
        item_a = QTableWidgetItem(DH_Alpha_A_D_Theta[1])
        item_a.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(new_row,1,item_a)
        #add d
        item_d = QTableWidgetItem(DH_Alpha_A_D_Theta[2])
        item_d.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(new_row,2,item_d)
        #Reset alpha theta a d
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")

    def loadDHTable(self, string_table):
        for i in range(len(string_table)):
            Component = string_table[i].split()
            self.process(Component)



if __name__ == "__main__":
    # run app
    app = QApplication(sys.argv)
    main_win = DH_Table()
    main_win.show()
    sys.exit(app.exec())