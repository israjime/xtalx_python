# Copyright (c) 2023 by Phase Advanced Sensor Systems, Inc.
# All rights reserved.
import threading
import argparse
import math
import time
import sys
import glotlib

import xtalx.p_sensor
from xtalx.tools.math import XYSeries
from OpenGL import GL
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self, serial_num, averaging_period_secs,
                        show_lores_data):
        super().__init__()
        self.setObjectName("MainWindow")

        self.setMaximumSize(900,825)
        self.setMinimumSize(900, 825)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 900, 825))
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
        self.glotlibWidget = glotlibglotlib_context(serial_num, averaging_period_secs,show_lores_data)
        self.glotlibWidget.setGeometry(QtCore.QRect(0, 35, 900, 700))
        self.glotlibWidget.setParent(self.plots)
        self.glotlibWidget.setObjectName("glotlibWidget")
        self.saveButton = QtWidgets.QPushButton(self.plots)
        self.saveButton.setGeometry(QtCore.QRect(725, 748, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        self.saveButton.setFont(font)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.saveButton.setStyleSheet("")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::DocumentSave")
        self.saveButton.setIcon(icon)
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.saveButton.setObjectName("saveButton")
        self.serialNum = QtWidgets.QLabel(self.plots)
        self.serialNum.setGeometry(QtCore.QRect(10, 6, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.serialNum.setFont(font)
        self.serialNum.setObjectName("serialNum")
        self.serialPlace = QtWidgets.QLabel(self.plots)
        self.serialPlace.setGeometry(QtCore.QRect(120, 6, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        self.serialPlace.setFont(font)
        self.serialPlace.setObjectName("serialPlace")
        self.tabWidget.addTab(self.plots, "")
        self.about = QtWidgets.QWidget()
        self.about.setObjectName("about")
        self.tabWidget.addTab(self.about, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.tabWidget.addTab(self.settings, "")
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "xtalx"))
        self.saveButton.setText(_translate("MainWindow", "Save as CSV File"))
        self.serialNum.setText(_translate("MainWindow", "Serial Number:"))
        self.serialPlace.setText(_translate("MainWindow", "Place Holder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plots), _translate("MainWindow", "Plots"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about), _translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "About"))

LINE_WIDTH = 1

class glotlibglotlib_context(QOpenGLWidget):
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

        # Manually sets OpenGl version to 3.3
        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(fmt)
        self.setFormat(fmt)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)  # Update approximately every 16ms (~60 FPS)

    def initializeGL(self):
        
        GL.glClearColor(1,1,1,0)
        glotlib.programs.load()
        self.makeCurrent()
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        
        self.glotlib_context = glotlib.Context(self.width,self.height,self.name,msaa=self.msaa) 

        self.p_plot = self.glotlib_context.add_plot(311, limits=(-0.1, -0.5, 120, 300), max_v_ticks=10)
        self.lp_lines = self.p_plot.add_steps(X=[], Y=[], width=LINE_WIDTH)
        self.p_lines = self.p_plot.add_steps(X=[], Y=[], width=LINE_WIDTH)
        self.lp_lines.color = (0.78, 0.87, 0.93, 1)
        self.p_plot.set_y_label('PSI')
        self.p_slow_plot = self.glotlib_context.add_plot(312, limits=(-0.1, -0.5, 120, 300), max_v_ticks=10, sharex=self.p_plot, sharey=self.p_plot)
        self.lp_slow_lines = self.p_slow_plot.add_lines(X=[], Y=[], width=LINE_WIDTH)
        self.p_slow_lines = self.p_slow_plot.add_lines(X=[], Y=[], width=LINE_WIDTH)
        self.p_slow_plot.set_y_label('PSI (%u-sec Avg)' % self.period)
        self.t_plot = self.glotlib_context.add_plot(313, limits=(-0.1, -0.5, 120, 50), max_v_ticks=10, sharex=self.p_plot)
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
        print("hello")
        self._dirty = True
        self.makeCurrent()
        print("drawing")
        glotlib.main.draw_contexts(0)
        updated = False

        new_data = None
        with self.data_lock:
            if self.new_data:
                new_data = self.new_data
                self.new_data = []

        if new_data:
            updated = True
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

def measure_thread(x, tw, csv_file):
    t0 = time.time()
    for m in x.yield_measurements(do_reset=False):
        t = time.time()
        m._timestamp = dt = t - t0

        tw.glotlibWidget.measurement_callback(m)

        if csv_file:
            temp_c = m.temp_c if m.temp_c is not None else math.nan
            pressure_psi = (m.pressure_psi if m.pressure_psi is not None
                            else math.nan)
            csv_file.write('%.6f,%.6f,%.2f,%.5f\n' % (t, dt, temp_c, pressure_psi))
            csv_file.flush()


def main(args):
    if not args.intf:
        dev = xtalx.p_sensor.find_one_xti(serial_number=args.serial_number)
        x   = xtalx.p_sensor.make(dev)
    else:
        x = xtalx.p_sensor.XHTISM(args.intf, args.baud_rate, int(args.modbus_addr, 0))

    if args.csv_file:
        csv_file = open(  # pylint: disable=R1732
            args.csv_file, 'a+', encoding='utf8')

        pos = csv_file.tell()
        if pos != 0:
            csv_file.seek(0)
            if csv_file.read(28) != 'time,dt,temp_c,pressure_psi\n':
                print('%s does not appear to be a pressure sensor log file.' %
                        args.csv_file)
                return
            csv_file.seek(pos)
        else:
            csv_file.write('time,dt,temp_c,pressure_psi\n')
            csv_file.flush()
    else:
        csv_file = None

    try:
        app = QtWidgets.QApplication(sys.argv)
        win = MainWindow(x.serial_num, args.averaging_period_secs, args.show_lores_data)
        mt = threading.Thread(target=measure_thread, args=(x, win, csv_file))
        mt.start()
        win.show()
        sys.exit(app.exec_())
    finally:
        x.halt_yield()
        mt.join()


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--intf', '-i')
    parser.add_argument('--baud-rate', type=int, default=115200)
    parser.add_argument('--modbus-addr', '-m', default='0x80')
    parser.add_argument('--serial_number', '-s')
    parser.add_argument('--csv-file')
    parser.add_argument('--averaging-period-secs', type=int, default=3)
    parser.add_argument('--show-lores-data', action='store_true')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    _main()
