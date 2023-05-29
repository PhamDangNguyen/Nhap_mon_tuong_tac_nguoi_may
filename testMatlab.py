from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization! 
from time import sleep
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import robot_class
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class DrawWidget(QtWidgets.QWidget):
    plot_done = pyqtSignal()
    plot_once = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.fig = Figure(dpi = 100)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.canvas.show()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.set_zlim3d(-0.2, 1)                    # viewrange for z-axis should be [-4,4] 
        self.axes.set_ylim3d(-1, 1)                    # viewrange for y-axis should be [-2,2] 
        self.axes.set_xlim3d(-1, 1)
        # self.axes.legend()
        self.current_point = []
        self.history_point = []

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # small_layout = QtWidgets.QHBoxLayout(self)
        # Just some button connected to `plot` method
        # self.button = QtWidgets.QPushButton('Plot')
        # self.button.clicked.connect(self.robot_limit_plot)
    
        # self.pause_button = QtWidgets.QPushButton('Pause')
        # self.pause_button.clicked.connect(self.plot_pause)

        # self.set_pose_button = QtWidgets.QPushButton('Set')
        # self.set_pose_button.clicked.connect(self.set_pose)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(2)

        # small_layout.addWidget(self.button)
        # small_layout.addWidget(self.pause_button)
        # small_layout.addWidget(self.set_pose_button)

        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        # layout.addLayout(small_layout)

        self.setLayout(layout)

        self.jointTrajectory = []

        self.t_counter = 0

        # self.robot = robot_class._Robot()
        self.robot = robot_class.Robot5DOF()

        self.List_Pose = dict()
        self.List_Pose['Home'] = self.robot.QHome

        self.show()
    
    def reset(self):
        self.clear_pose()
        self.jointTrajectory = []
        self.refix(0)
        for line in self.axes.get_lines(): # ax.lines:
            line.remove()
        self.history_point = []
        self.canvas.draw()

    def change_robot(self, new_robot):
        self.robot = new_robot
        self.reset()

    def clear_pose(self):
        self.List_Pose = dict()
        self.List_Pose['Home'] = self.robot.QHome

    def setJointTrajectory(self, jointTrajectory):
        if (jointTrajectory is None): 
            self.jointTrajectory = self.robot.jointSpace
        else: self.jointTrajectory = jointTrajectory

    def robot_limit_plot(self):

        self.t_counter = 0
        if (len(self.jointTrajectory) == 0): self.setJointTrajectory(self.robot.jointSpace)
        self.history_point = []

        try:
            self.timer.timeout.disconnect()
        except:
            pass
        self.timer.timeout.connect(self.all_plot)
        self.timer.start()

    def plot_pause(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except:
            pass
        self.refix(0)
        self.history_point = []

    def all_plot(self):
        if (self.t_counter >= len(self.jointTrajectory)):
            self.drawCurve()
            self.plot_pause()
            # output some signal to host to revert back button
            self.plot_done.emit()
            return

        self.robot.apply_value(self.jointTrajectory[self.t_counter])

        self.plot()
        # self.robot.Q[0] = np.random.random()*(self.robot.limit[0][1] - self.robot.limit[0][0]) + self.robot.limit[0][0]
        self.t_counter += 1

    def drawCurve(self):
        temp_array = np.array(self.history_point).T
        self.axes.plot(temp_array[0], temp_array[1], temp_array[2], color = 'k')
        self.canvas.draw()

    def refix(self, trim_len = 10):
        while (len(self.current_point) > trim_len): 
            last_point = self.current_point.pop(0)
            last_point.remove()

    def plot(self):
 
        for line in self.axes.get_lines(): # ax.lines:
            line.remove()
        self.robot.get_waypoint()
        for i in range(len(self.robot.waypointX) - 1):
            self.axes.plot([self.robot.waypointX[i], self.robot.waypointX[i+1] ] , [self.robot.waypointY[i], self.robot.waypointY[i+1] ],\
                '*--', color = self.robot.linkColour[i], zs= [self.robot.waypointZ[i], self.robot.waypointZ[i+1] ], label=str('Link ' + str(i))) 
        self.current_point.append(self.axes.scatter(self.robot.waypointX[-1], self.robot.waypointY[-1], self.robot.waypointZ[-1], marker = 'x', color='purple') )
        self.history_point.append((self.robot.waypointX[-1], self.robot.waypointY[-1], self.robot.waypointZ[-1]) )

        self.plot_once.emit()

        self.refix()

        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = DrawWidget()
    app.exec()
