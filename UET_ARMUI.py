from PyQt5 import QtWidgets, uic, QtGui, QtCore,Qt
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox, QDialog, QCompleter,QLineEdit
from DHQt import DH_Table
from Help import Ui_Dialog
from Search import Ui_Dialog_2

import random, string
# import matplotlib.pyplot as plt

import numpy as np

import sys
from math import radians

import robot_class
import arm_matplot

class second_screen(QDialog,Ui_Dialog):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # define button change page
        self.menu = 0
        self.pushButton.clicked.connect(self.show_menu)
        self.pushButton_Overview.clicked.connect(self.screen_page)
        self.pushButton_PipeLine_2.clicked.connect(self.screen_page)
        self.pushButton_PipeLine.clicked.connect(self.screen_page)
        self.pushButton_SearchFeature.clicked.connect(self.screen_page)
        self.pushButton_AdHTable.clicked.connect(self.screen_page)
        self.pushButton_AddAction.clicked.connect(self.screen_page)
        self.pushButton_ThreeBut.clicked.connect(self.screen_page)
        self.pushButton_Interact1.clicked.connect(self.screen_page)
        self.pushButton_Interact2.clicked.connect(self.screen_page)

    def show_menu(self):
        if self.menu == 0:
            self.frame_6.setMaximumSize(QtCore.QSize(273,16777215))
            self.menu = 1
        elif self.menu == 1:
            self.frame_6.setMaximumSize(QtCore.QSize(70,16777215))
            self.menu = 0

    def screen_page(self):
        click_signal = self.sender()
        button_name = click_signal.objectName()
        if button_name == "pushButton_Overview":
            self.stackedWidget.setCurrentWidget(self.page_1)
        elif button_name == "pushButton_PipeLine_2":
            self.stackedWidget.setCurrentWidget(self.page_2)
        elif button_name == "pushButton_PipeLine":
            self.stackedWidget.setCurrentWidget(self.page_3)
        elif button_name == "pushButton_SearchFeature":
            self.stackedWidget.setCurrentWidget(self.page_4)
        elif button_name == "pushButton_AdHTable":
            self.stackedWidget.setCurrentWidget(self.page_5)
        elif button_name == "pushButton_AddAction":
            self.stackedWidget.setCurrentWidget(self.page_6)
        elif button_name == "pushButton_ThreeBut":
            self.stackedWidget.setCurrentWidget(self.page_7)
        elif button_name == "pushButton_Interact1":
            self.stackedWidget.setCurrentWidget(self.page_8)
        elif button_name == "pushButton_Interact2":
            self.stackedWidget.setCurrentWidget(self.page_9)

class ActionPopup(QtWidgets.QDialog):
    def __init__(self):
        super(ActionPopup, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('JointPopup.ui', self) # Load the .ui file
        self.show() # Show the GUI

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UET_ARMUI.ui', self) # Load the .ui file

        # define function button of options 
        self.actionSearch.triggered.connect(self.add_Search)
        self.actionHelp.triggered.connect(self.Help)
        # define signal and slot
        self.AddActionButton.clicked.connect(self.openAddPopup)
        self.DeleteActionButton.clicked.connect(self.openDelPopup)
        self.EditActionButton.clicked.connect(self.editJointPopup)
        # self.PoseActionButton.clicked.connect(self.openPoseTab)
        self.ExecuteActionButton.clicked.connect(self.pre_execute)
        # define initial flag and value
        self.listActionName = set()
        self.listAction = dict()

        self.ListActionView.itemDoubleClicked.connect(self._editJointPopup)
        self.ListActionView.itemSelectionChanged.connect(self._countAction)
        self.push_edit_but.clicked.connect(self.openDHPopup)
        
        #define view tab
        self.tabViewInitial()

        self.currentAction = 'Init'

        self.editName = None

        #define table view
        # self.endpoint.setColumnCount(3)
        self.endpoint.setHorizontalHeaderLabels(["X", "Y", "Z"])
        
        #define change robot
        self.ur_change.toggled.connect(self.change_robot)
        self.dof_change.toggled.connect(self.change_robot)
        self.cus_change.toggled.connect(self.change_robot)

        self.show() # Show the GUI

#Add
    def Help(self):
        self.second_s=second_screen()
        self.second_s.exec()
    
    def add_Search(self):
        item, ok = QtWidgets.QInputDialog.getText(self, 'Search', 'Service', QLineEdit.Normal, QDir().home().dirName())
        if ok and item:
            if item == "Add" or item == "add":
                self.openAddPopup()
            elif item == "delete" or item == "Delete":
                self.openDelPopup()
            elif item == "Edit" or item == "edit":
                self.editJointPopup()
            elif item == "Execute" or item == "execute": 
                self.pre_execute()
            elif item == "pause" or item == "Pause":
                self.canvas.plot_pause()
                self.ExecuteActionButton.setText("Execute")
            elif item == "Help" or item =="help":
                self.Help()
#end add

    def openDHPopup(self):
        if not(self.cus_change.isChecked()): return
        self.new_DH = DH_Table()
        self.new_DH.loadDHTable(self.canvas.robot.DHTABLE)
        if (self.new_DH.exec() == QtWidgets.QDialog.Accepted):
            self.reset_all()
            self.canvas.robot = robot_class.Robot_Custom(self.new_DH.numJoint, self.new_DH.jointType, self.new_DH.limit, self.new_DH.jointSpeeds, self.new_DH.final_data)
            

    def reset_all(self):
        self.endpoint.clearContents()
        self.endpoint.setRowCount(0)

        if (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

        self.listActionName = set()
        self.listAction = dict()

        self.currentAction = 'Init'
        self.editName = None

        self.ListActionView.clear()
        self.CurrentNumSelectValue.setText( "Actions: " )
        self.CurrentTotalTimeValue.setText( "Time: TBA" )

        self.canvas.reset()

    def change_robot(self):
        #reset all first
        self.reset_all()
        if (self.dof_change.isChecked()): self.canvas.change_robot(robot_class.Robot5DOF())
        if (self.ur_change.isChecked()): self.canvas.change_robot(robot_class.RobotUR5())
        if (self.cus_change.isChecked()):
            self.canvas.change_robot(robot_class.Robot_Custom(2, ['r', 'r'], [(0, radians(120)), (radians(-90), radians(90))], [radians(15), radians(15)], \
            ['0.0  1.0  0.0  Q(0.0,120.0,15.0)  ', '0.0  0.5  0.0  Q(-90.0,90.0,15.0)  ']))



    def tabViewInitial(self):
        self.canvas = arm_matplot.DrawWidget()

        self.canvas.plot_done.connect(self.matlab_plot_done)
        self.canvas.plot_once.connect(self.update_endpointView)

        self.MatplotLayout.addWidget(self.canvas)

    def _countAction(self):
        currentSelected = self.ListActionView.selectedItems()
        self.CurrentNumSelectValue.setText( "Actions: "+str(len(currentSelected)) )
        self.CurrentTotalTimeValue.setText( "Time: TBA" )

    def update_endpointView(self):
        self.endpoint.insertRow(self.endpoint.rowCount())
        self.endpoint.setItem(self.endpoint.rowCount()-1, 0, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointX[-1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 1, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointY[-1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 2, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointZ[-1] )))

        self.endpoint.scrollToBottom()

    def addPosePopup(self):
        item, ok = QtWidgets.QInputDialog.getItem(self, 'Pose Dialog', 'Select pose', list(self.canvas.List_Pose.keys()), 0, False)
        if ok and item:
            newItem = QtWidgets.QListWidgetItem(item, type = 808)
            newItem.setIcon(QtGui.QIcon("pose.jpg"))
            self.ListActionView.addItem(newItem)
        self.tempPopup.reject()

    def setPose(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Pose Name Input Dialog', 'Enter pose name:')
        if (ok):
            if (text == 'Home'):
                self.canvas.robot.QHome = robot_class.Pose(text, self.canvas.robot.Q.copy(), self.canvas.robot.poseJointSpeeds)
            self.canvas.List_Pose[text] = robot_class.Pose(text, self.canvas.robot.Q.copy(), self.canvas.robot.poseJointSpeeds)
        self.tempPopup.reject()


    def openAddPopup(self):
        self.tempPopup = ActionPopup()
        self.tempPopup.ActionthLabel.setText(str("Action: "+str(self.ListActionView.count())))
        self.tempPopup.ActionNameLabel.setText( ''.join(random.choices(string.ascii_uppercase + string.digits, k=1 + self.ListActionView.count())) )
        self.tempPopup.SpeedValue.setValue( self.canvas.robot.jointSpeeds[0] )
        self.tempPopup.JointhValue.setMaximum ( self.canvas.robot.numJoint - 1 )
        self.adaptJointID()
        self.tempPopup.JointhValue.valueChanged.connect( self.adaptJointID )
        self.currentAction = 'Add'

        self.tempPopup.ActionButton.clicked.connect(self.saveAction)
        # print(tempPopup.ActionButton.standardButtons)

        self.tempPopup.AddPoseButton.clicked.connect(self.addPosePopup)
        self.tempPopup.NewPoseButton.clicked.connect(self.setPose)
        self.tempPopup.exec()
    
    def adaptJointID(self):
        jID =  self.tempPopup.JointhValue.value()
        if (self.currentAction == 'Add'): self.tempPopup.SpeedValue.setValue(  self.canvas.robot.jointSpeeds[ jID ] )
        self.tempPopup.JointhTargetValue.setMaximum(self.canvas.robot.limit[jID][1] - 0.0001)
        self.tempPopup.JointhTargetValue.setMinimum(self.canvas.robot.limit[jID][0] + 0.0001)

        if ( self.canvas.robot.jointType[ jID ] == 'r' ):
            self.tempPopup.RevoluteRadioButton.setChecked(1)
            self.tempPopup.SpeedValue.setSuffix(" rad")
            self.tempPopup.JointhTargetValue.setSuffix(" rad")
        else:
            self.tempPopup.PrismaticRadioButton.setChecked(1)
            self.tempPopup.SpeedValue.setSuffix(" m")
            self.tempPopup.JointhTargetValue.setSuffix(" m")

    def coverPopup(self, jointAction):
        self.tempPopup.ActionNameLabel.setText( jointAction.name )
        self.tempPopup.JointhValue.setValue(jointAction.jointID)
        self.adaptJointID()
        self.tempPopup.SpeedValue.setValue( jointAction.speed )
        self.tempPopup.JointhTargetValue.setValue( jointAction.targetValue )

        if (jointAction.lockType == 'union'):
            self.tempPopup.UnionRadioButton.setChecked(1)
        else:
            self.tempPopup.LockRadioButton.setChecked(1)

    def editJointPopup(self):
        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: return 
        self._editJointPopup(currentSelected[-1])

    def _editJointPopup(self, last_item):
        last_item_id = self.ListActionView.row(last_item)
        self.editName = None
        if (self.listAction.get(last_item.text()) is None): return
        self.editName = last_item.text()

        self.tempPopup = ActionPopup()
        self.tempPopup.ActionthLabel.setText(str("Action: "+str(last_item_id)))
        self.tempPopup.JointhValue.setMaximum ( self.canvas.robot.numJoint - 1 )
        self.tempPopup.JointhValue.valueChanged.connect( self.adaptJointID )
    
        self.coverPopup(self.listAction[self.editName])
        self.currentAction = 'Edit'
        self.tempPopup.ActionNameLabel.setReadOnly(True)
        self.tempPopup.ActionButton.clicked.connect(self.saveAction)
        self.tempPopup.exec()

    def checkAction(self, _name, _jointId, _jointValue, _jointType, _moveType):
        if (self.currentAction == 'Add') and (_name in self.listActionName): raise Exception("Duplicate Name")
        if not(self.canvas.robot.check_limitId(_jointId, _jointValue)): raise Exception("Joint Value wrong")
        if (_jointType) and (self.canvas.robot.jointType[_jointId] == 'l'): raise Exception("Joint Type wrong")
        if not(_jointType) and (self.canvas.robot.jointType[_jointId] == 'r'): raise Exception("Joint Type wrong")
        return True

    def saveAction(self, clickedButton):
        if clickedButton == \
                    self.tempPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Reset):
            print("Reset Now")
            if (self.currentAction == 'Edit'):
                self.coverPopup(self.listAction[self.editName])
        elif clickedButton == \
                    self.tempPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Cancel):
            print("Cancel Successful")
            self.tempPopup.reject()
            if (self.currentAction == 'Edit'): self.editId = -1
        elif clickedButton == \
                    self.tempPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Save):

            # Check for correctness
            try:
                currentName = self.tempPopup.ActionNameLabel.text()
                self.checkAction( currentName, self.tempPopup.JointhValue.value(), self.tempPopup.JointhTargetValue.value(),\
                            self.tempPopup.RevoluteRadioButton.isChecked(), self.tempPopup.UnionRadioButton.isChecked())
                self.listAction[currentName] = robot_class.JointAction(currentName, self.tempPopup.JointhValue.value(),\
                                                            'union' if self.tempPopup.UnionRadioButton.isChecked() else 'lock' , self.tempPopup.JointhTargetValue.value(), self.tempPopup.SpeedValue.value() )
                
                if (self.currentAction == 'Add'):

                    newItem = QtWidgets.QListWidgetItem(currentName, type = 404)
                    if (self.tempPopup.UnionRadioButton.isChecked()):
                        newItem.setIcon(QtGui.QIcon("chain.png"))
                    else:
                        newItem.setIcon(QtGui.QIcon("lock.png"))

                    self.ListActionView.addItem(newItem)
                    self.listActionName.add(currentName)
                elif (self.currentAction == 'Edit'):
                    assert(self.editName == currentName)
                    item = self.ListActionView.findItems(currentName,Qt.Qt.MatchExactly)[0]

                    if (self.tempPopup.UnionRadioButton.isChecked()):
                        item.setIcon(QtGui.QIcon("chain.png"))
                    else:
                        item.setIcon(QtGui.QIcon("lock.png"))

                self.tempPopup.reject()
            except Exception as eMessage:
                self.tempPopup.ErrorLabel.setText(str(eMessage))

            # self.tempPopup.reject()

    def openDelPopup(self):
        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: return        

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Confirm Deleting " + str(len(currentSelected)) +" Item ?")
        msgBox.setWindowTitle("Warning Box")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            for item in currentSelected:
                del_item = self.ListActionView.takeItem(self.ListActionView.row(item))
                q_action_name = del_item.text()
                try:
                    self.listAction.pop(q_action_name)
                    self.listActionName.remove(q_action_name)
                except:
                    pass

    def matlab_plot_done(self):
        if (self.ExecuteActionButton.text() == "Pause"):
            self.ExecuteActionButton.setText("Execute")

            # print(self.canvas.robot.waypointX)
            # print(self.canvas.robot.waypointY)
            # print(self.canvas.robot.waypointZ)

    def pre_execute(self):
        if (self.ExecuteActionButton.text() == "Execute"):

            self.endpoint.clearContents()
            self.endpoint.setRowCount(0)

            self.execute()
            self.CurrentTotalTimeValue.setText(str( len(self.canvas.jointTrajectory) ))
            self.canvas.robot_limit_plot()
            self.ExecuteActionButton.setText("Pause")
        elif (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

    def execute(self):
        POSE_TYPE = 808
        JOINT_TYPE = 404

        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: 
            self.canvas.setJointTrajectory(None)
            return

        tempDict = {}
        for item in currentSelected:
            tempDict[self.ListActionView.row(item)] = item
        tempIndexes = sorted(tempDict)

        # define a list to contain the resultant items i.e sorted items
        tempGroup = []
        for index in tempIndexes:
            if tempDict[index].type() == POSE_TYPE:
                tempGroup.append(self.canvas.List_Pose[tempDict[index].text() ])
            else:
                tempGroup.append(self.listAction[ tempDict[index].text() ])
        timeTable = robot_class.TimeTable(self.canvas.robot.numJoint, self.canvas.robot.QHome)
        timeTable.prepare(tempGroup)
        self.canvas.setJointTrajectory(timeTable.gen_jointList())
        # print(timeTable.gen_jointList())


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
