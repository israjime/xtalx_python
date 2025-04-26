# Copyright (c) 2023 by Phase Advanced Sensor Systems, Inc.
# All rights reserved.
import threading
import argparse
import math
import time
import sys
import glotlib
import datetime

import xtalx.p_sensor
from xtalx.tools.math import XYSeries
from OpenGL import GL
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

LINE_WIDTH = 1

class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(900, 825)
        self.setMaximumSize(900,825)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(10, 10)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.args = args
        self.sensor_list = xtalx.p_sensor.find_xti()
        self.standbyWidget = QtWidgets.QWidget(self)
        self.standbyWidget.setStyleSheet("")
        self.standbyWidget.setObjectName("standbyWidget")
        self.connectwidget = QtWidgets.QWidget(self)
        self.connectwidget.setStyleSheet("")
        self.connectwidget.setObjectName("connectwidget")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

    # Uncomment to see each window

        # self.display_standby()
        # self.display_connect()
        self.display_tabs()

        
        # QTimer.singleShot(3000, self.switch_widgets)

    # TODO: Fix issue with display tabs where opengl crashes
    def switch_widgets(self):
        self.sensor_list = xtalx.p_sensor.find_xti()
        if self.sensor_list != []:
            self.connectwidget.hide()
            self.standbyWidget.setParent(None)
            self.standbyWidget.deleteLater()
            self.centralwidget.show()
            self.display_tabs()
        else:
            self.centralwidget.hide()
            self.standbyWidget.setParent(None)
            self.standbyWidget.deleteLater()
            self.connectwidget.show()
            self.display_connect()


    def display_standby(self): 
        self.background = QtWidgets.QLabel(self.standbyWidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 921, 830))
        self.background.setStyleSheet("QLabel {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(209, 103, 65, 154), stop:1 rgba(15, 111, 178, 154))}")
        self.background.setText("")
        self.background.setObjectName("background")
        self.Logo = QtWidgets.QLabel(self.standbyWidget)
        self.Logo.setGeometry(QtCore.QRect(330, 360, 250, 84))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("../../../phase-logo-white.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.setCentralWidget(self.standbyWidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
    
    def display_connect(self):
        self.setStyleSheet("")
        self.connectwidget = QtWidgets.QWidget(self)
        self.connectwidget.setStyleSheet("")
        self.connectwidget.setObjectName("connectwidget")
        self.frame = QtWidgets.QFrame(self.connectwidget)
        self.frame.setGeometry(QtCore.QRect(84, 84, 735, 660))
        self.frame.setStyleSheet("QFrame {\n"
" background-color: rgba(255, 255, 255, 105);\n"
"border-radius: 30px;\n"
"\n"
"\n"
"}\n"
"QLabel { background: transparent; }")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setObjectName("frame")
        self.connect_label = QtWidgets.QLabel(self.frame)
        self.connect_label.setGeometry(QtCore.QRect(159, 380, 440, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(18)
        font.setItalic(False)
        self.connect_label.setFont(font)
        self.connect_label.setStyleSheet("QLabel {\n"
"    color: rgb(255, 255, 255);\n"
"\n"
"    font: 600 18pt \"Open Sans\";\n"
"}")
        self.connect_label.setScaledContents(False)
        self.connect_label.setObjectName("connect_label")
        self.dots = QtWidgets.QLabel(self.frame)
        self.dots.setGeometry(QtCore.QRect(341, 282, 50, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(30)
        self.dots.setFont(font)
        self.dots.setStyleSheet("QLabel {\n"
" color: white;\n"
"}")
        self.dots.setObjectName("dots")
        self.Logo = QtWidgets.QLabel(self.frame)
        self.Logo.setGeometry(QtCore.QRect(216, 136, 300, 124))
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("../../../phase-logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.refresh_button = QtWidgets.QPushButton(self.frame)
        self.refresh_button.setGeometry(QtCore.QRect(285, 457, 171, 41))
        self.refresh_button.setStyleSheet("\n"
"    QPushButton {\n"
"        background-color: rgb(255, 255, 255); \n"
"        color: rgb(143, 158, 177);\n"
"        border-radius: 8px;\n"
"        padding: 10px 20px;\n"
"        font-size: 18px;\n"
"        font-weight: bold;\n"
"\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: rgb(217, 155, 133);\n"
"     color: white;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        color: white;\n"
"        background-color: rgb(116, 159, 192);\n"
"    }")
        self.refresh_button.setObjectName("refresh_button")
        self.connect_failed = QtWidgets.QLabel(self.frame)
        self.connect_failed.setGeometry(QtCore.QRect(305, 530, 132, 16))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        self.connect_failed.setFont(font)
        self.connect_failed.setStyleSheet("QLabel { \n"
"    color: crimson;\n"
"}")
        self.connect_failed.setObjectName("label")
        self.background = QtWidgets.QLabel(self.connectwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 921, 830))
        self.background.setStyleSheet("QLabel {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(209, 103, 65, 154), stop:1 rgba(15, 111, 178, 154))}")
        self.background.setText("")
        self.background.setObjectName("background")
        self.background.raise_()
        self.frame.raise_()
        self.setCentralWidget(self.connectwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_label.setText(_translate("MainWindow", "Please Connect a Phase Sensor Pressure Sensor"))
        self.dots.setText(_translate("MainWindow", "• • •"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.connect_failed.setText(_translate("MainWindow", "No Sensor Found"))
        self.connect_failed.hide()
        self.refresh_button.clicked.connect(lambda: self.refresh())

    def display_tabs(self):
        dev = xtalx.p_sensor.find_one_xti()
        self.x = xtalx.p_sensor.make(dev)
        self.generate_file_name()
        self.draw_elem_tabs()
        self.add_sensor()
        self.generate_file_name()
        self.open_csv()
        self.mt = threading.Thread(target=self.measure_thread)
        self.sensor_connected = True
        self.mt.start()
        self.saveButton.clicked.connect(lambda: self.saved_clicked())

    def draw_elem_tabs(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(900, 825))
        self.setTabShape(QTabWidget.TabShape.Rounded)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.plots = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        self.plots.setFont(font)
        self.plots.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plots.setAcceptDrops(False)
        self.plots.setObjectName("plots")
        self.glotlibWidget = GlotlibContext(self.x.serial_num,self.args.averaging_period_secs,self.args.show_lores_data)
        self.glotlibWidget.setGeometry(QtCore.QRect(0, 35, 900, 700))
        self.glotlibWidget.setParent(self.plots)
        self.glotlibWidget.setObjectName("glotlibWidget")
        self.saveButton = QtWidgets.QPushButton(self.plots)
        self.saveButton.setGeometry(QtCore.QRect(20, 750, 160, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        self.saveButton.setFont(font)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.saveButton.setStyleSheet("")
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.saveButton.setObjectName("saveButton")
        
        self.serialNum = QtWidgets.QLabel(self.plots)
        self.serialNum.setGeometry(QtCore.QRect(10, 6, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.serialNum.setFont(font)
        self.serialNum.setObjectName("serialNum")

        self.recordingText = QtWidgets.QLabel(self.plots)
        self.recordingText.setGeometry(QtCore.QRect(200, 760, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.recordingText.setFont(font)
        self.recordingText.setObjectName("recordingText")
        
        self.filePlaceholder = QtWidgets.QLabel(self.plots)
        self.filePlaceholder.setGeometry(QtCore.QRect(340, 760, 521, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.filePlaceholder.setFont(font)
        self.filePlaceholder.setObjectName("filePlaceholder")
        
        self.serialPlace = QtWidgets.QComboBox(self.plots)
        self.serialPlace.setGeometry(QtCore.QRect(130, 6, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        self.serialPlace.setFont(font)
        self.serialPlace.setObjectName("serialPlace")
        
        self.tabWidget.addTab(self.plots, "")
        
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.tabWidget.addTab(self.settings, "")
    
        self.about = QtWidgets.QWidget()
        self.about.setObjectName("about")
        
        self.label_3 = QtWidgets.QLabel(self.about)
        self.label_3.setGeometry(QtCore.QRect(300, 200, 300, 124))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("xtalx/tools/p_sensor/images/phase-logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        
        self.widget = QtWidgets.QWidget(self.about)
        self.widget.setGeometry(QtCore.QRect(0, 260, 901, 501))
        self.widget.setObjectName("widget")
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setUnderline(True)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        
        self.label_9 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setUnderline(True)
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        
        self.verticalLayout.addWidget(self.label_9)
        
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setUnderline(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        
        self.verticalLayout.addWidget(self.label_10)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.tabWidget.addTab(self.about, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "xtalx"))
        self.saveButton.setText(_translate("MainWindow", "Stop Saving to CSV"))
    
        self.saveButton.setStyleSheet('QPushButton {background-color: crimson; border-radius: 5px; color: white;} QPushButton:hover {background-color: maroon}')
        self.saveButton.setGraphicsEffect(self.shadow)
        self.recordingText.setText(_translate("MainWindow", "Recording Values To:"))
        self.filePlaceholder.setText(self.file_name)
        self.serialNum.setText(_translate("MainWindow", "Select a Sensor:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plots), _translate("MainWindow", "Plots"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Settings"))
        self.label_8.setText(_translate("MainWindow",'<a href="https://www.phasesensors.com/">Website</a>'))
        self.label_9.setText(_translate("MainWindow",'<a href="https://github.com/phasesensors/xtalx_python">GitHub</a>'))
        self.label_10.setText(_translate("MainWindow",'<a href="https://www.phasesensors.com/contact">Contact Us</a>'))
        self.label_8.setOpenExternalLinks(True)
        self.label_9.setOpenExternalLinks(True)
        self.label_10.setOpenExternalLinks(True)
        self.label_2.setText(_translate("MainWindow", "Copyright © 2021 - 2025. Phase Advanced Sensor Systems Corp. All rights reserved."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about), _translate("MainWindow", "About"))
        self.saveButton.setGraphicsEffect(self.shadow)
    
    def add_sensor(self):
        for i in self.sensor_list:
            self.serialPlace.addItem(i.serial_number)
    
    def refresh(self):
        self.sensor_list = xtalx.p_sensor.find_xti()
        if self.sensor_list != []:
            # self.connectwidget.hide()
            self.centralwidget.show()
            self.display_tabs()
        else:
            self.connect_failed.show()

    def saved_clicked(self):
        if self.saveButton.text() == "Stop Saving to CSV":
            self.csv_file.close()
            self.generate_file_name()
            self.open_csv()
            self.saveButton.setText("Start Saving to CSV")
            self.filePlaceholder.setText("")
            self.recordingText.hide()
            self.saveButton.setStyleSheet('QPushButton {background-color: limegreen; border-radius: 5px; color: white;} QPushButton:hover {background-color: mediumseagreen}')
            self.update()
        else:
            self.saveButton.setText("Stop Saving to CSV")
            self.filePlaceholder.setText(self.file_name)
            self.recordingText.show()
            self.recordingText.setText("Recording Values to: ")
            self.saveButton.setStyleSheet('QPushButton {background-color: crimson; border-radius: 5px; color: white;} QPushButton:hover {background-color: maroon}')
            self.update()

    def generate_file_name(self):
        day = datetime.date.today()
        time = datetime.datetime.now().strftime("%H-%M-%S")
        self.file_name = "{}_{}_{}.csv".format(self.x.serial_num,day,time)

    def measure_thread(self):
        try:
            t0 = time.time()
            for m in self.x.yield_measurements(do_reset=False):
                t = time.time()
                m._timestamp = dt = t - t0
                self.glotlibWidget.measurement_callback(m)
                if self.csv_file:
                    temp_c = m.temp_c if m.temp_c is not None else math.nan
                    pressure_psi = (m.pressure_psi if m.pressure_psi is not None
                                    else math.nan)
                    self.csv_file.write('%.6f,%.6f,%.2f,%.5f\n' % (t, dt, temp_c, pressure_psi))
                    self.csv_file.flush()
        except:
            self.sensor_connected = False

    def open_csv(self):
        self.csv_file = open(self.file_name, 'w', encoding='utf8')
        self.csv_file.write('time,dt,temp_c,pressure_psi\n')
        self.csv_file.flush()

class GlotlibContext(QOpenGLWidget):
    def __init__(self, name, period, show_lores_data):
        super().__init__()
        self.width           = 900
        self.height          = 700
        self.msaa            = 2
        self.name            = name
        self.period          = period
        self.show_lores_data = show_lores_data
        self.data_gen        = -1
        self.plot_gen        = -1
        self.data_lock       = threading.Lock()
        self.new_data        = []
        self.p_measurements  = XYSeries([], [])
        self.lp_measurements = XYSeries([], [])
        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(fmt)
        self.setFormat(fmt)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)  

    def initializeGL(self):
        GL.glClearColor(1,1,1,0)
        glotlib.programs.load()
        self.makeCurrent()
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        self.glotlib_context = glotlib.Context(self.width,self.height,self.name,msaa=self.msaa) 
        self.p_plot = self.glotlib_context.add_plot(311, limits=(-0.1, -0.5, 120, 30), max_v_ticks=10)
        self.lp_lines = self.p_plot.add_steps(X=[], Y=[], width=LINE_WIDTH)
        self.p_lines = self.p_plot.add_steps(X=[], Y=[], width=LINE_WIDTH)
        self.lp_lines.color = (0.78, 0.87, 0.93, 1)
        self.p_plot.set_y_label('PSI')
        self.p_slow_plot = self.glotlib_context.add_plot(312, limits=(-0.1, -0.5, 120, 30), max_v_ticks=10, sharex=self.p_plot, sharey=self.p_plot)
        self.lp_slow_lines = self.p_slow_plot.add_lines(X=[], Y=[], width=LINE_WIDTH)
        self.p_slow_lines = self.p_slow_plot.add_lines(X=[], Y=[], width=LINE_WIDTH)
        self.p_slow_plot.set_y_label('PSI (%u-sec Avg)' % self.period)
        self.t_plot = self.glotlib_context.add_plot(313, limits=(-0.1, -0.5, 120, 30), max_v_ticks=10, sharex=self.p_plot)
        self.lt_lines = self.t_plot.add_steps(X=[], Y=[], width=LINE_WIDTH)
        self.t_lines = self.t_plot.add_steps(X=[], Y=[],  width=LINE_WIDTH)
        self.lt_lines.color = (0.78, 0.87, 0.93, 1)
        self.t_plot.set_y_label('Temp (C)')
        self.pos_label = self.glotlib_context.add_label((0.99, 0.01), '', anchor='SE')
        self.mouse_vlines = [self.p_plot.add_vline(0, color='#80C080'), self.p_slow_plot.add_vline(0, color='#80C080'), self.t_plot.add_vline(0, color='#80C080')]
        self.label_font = glotlib.fonts.vera_bold(48, 0)
        self.psi_label = self.glotlib_context.add_label(self.p_plot.bounds[2:4], '', anchor='NE', font=self.label_font)
        self.psi_slow_label = self.glotlib_context.add_label(self.p_slow_plot.bounds[2:4], '', anchor='NE', font=self.label_font)
        self.temp_label = self.glotlib_context.add_label(self.t_plot.bounds[2:4], '', anchor='NE', font=self.label_font)

    def paintGL(self):
        # Mandatory Field 
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.glotlib_context._dirty = True
        self.makeCurrent()
        glotlib.main.draw_contexts(0)
        new_data = None
        with self.data_lock:
            if self.new_data:
                new_data = self.new_data
                self.new_data = []

        if new_data:
            # Low-res temperature measurements.
            X = [m._timestamp for m in new_data if m.lores_temp_c is not None]
            Y = [m.lores_temp_c for m in new_data if m.lores_temp_c is not None]
            if self.show_lores_data:
                self.lt_lines.append_x_y_data(X, Y)

            # Hi-res temperature measurements.
            self.t_lines.append_x_y_data(
                [m._timestamp for m in new_data],
                [m.temp_c for m in new_data])
            self.temp_label.set_text('%.4f \u00B0C' % new_data[-1].temp_c)

            # Low-res pressure (LP) measurements.
            X = [m._timestamp for m in new_data if m.lores_pressure_psi is not None]
            Y = [m.lores_pressure_psi for m in new_data if m.lores_pressure_psi is not None]
            lp_len = len(self.lp_slow_lines.vertices)
            if lp_len: 
                lp_timestamp = self.lp_measurements.X[-1]
            self.lp_measurements.append(X, Y)
            if self.show_lores_data:
                self.lp_lines.append_x_y_data(X, Y)

            # Averaged data from LP measurements.
            if len(X):
                if lp_len:
                    t0    = int(lp_timestamp // self.period) * self.period
                    index = lp_len - 1
                else:
                    t0    = int(X[0] // self.period) * self.period
                    index = 0

                timestamps = []
                pressures  = []
                t          = t0
                while t <= X[-1]:
                    p = self.lp_measurements.get_avg_value(t, t + self.period)
                    if p is not None:
                        timestamps.append(t + self.period / 2)
                        pressures.append(p)
                    t += self.period
                if self.show_lores_data:
                    self.lp_slow_lines.sub_x_y_data(index, timestamps,
                                                    pressures)

            # Hi-res pressure (P) measurements.
            X = [m._timestamp for m in new_data]
            Y = [m.pressure_psi for m in new_data]
            p_len = len(self.p_slow_lines.vertices)
            if p_len:
                self.p_timestamp = self.p_measurements.X[-1]
            self.p_measurements.append(X, Y)
            self.p_lines.append_x_y_data(X, Y)
            self.psi_label.set_text('%.4f PSI' % new_data[-1].pressure_psi)

            # Averaged data from P measurements.
            if p_len:
                t0    = int(self.p_timestamp // self.period) * self.period
                index = p_len - 1
            else:
                t0    = int(X[0] // self.period) * self.period
                index = 0

            timestamps = []
            pressures  = []
            t          = t0
            while t <= X[-1]:
                p = self.p_measurements.get_avg_value(t, t + self.period)
                if p is not None:
                    timestamps.append(t + self.period / 2)
                    pressures.append(p)
                t += self.period
            self.p_slow_lines.sub_x_y_data(index, timestamps, pressures)
            if len(pressures) >= 2:
                self.psi_slow_label.set_text('%.4f PSI' % pressures[-2])

    def resizeGL(self, w, h):
        GL.glViewport(0,0,w,h)
    
    def measurement_callback(self, m):
        with self.data_lock:
            self.new_data.append(m)
            self.update()

def main(args):
    try:    
        app = QtWidgets.QApplication(sys.argv)
        win = MainWindow(args)
        app.setWindowIcon(QIcon("xtalx/tools/p_sensor/images/app-logo.png"))
        win.show()
        sys.exit(app.exec_())
    finally:
        try:
            win.x.halt_yield()
            win.mt.join()
        except:
            pass

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial_number', '-s')
    parser.add_argument('--csv-file')
    parser.add_argument('--averaging-period-secs', type=int, default=3)
    parser.add_argument('--show-lores-data', action='store_true')
    args = parser.parse_args()
    main(args)

if __name__ == '__main__':
    _main()
