# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'neronetgui.ui'
#
# Created: Fri Apr  1 13:19:54 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1117, 595)
        MainWindow.setMinimumSize(QtCore.QSize(1117, 595))
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.experiment_log = QtGui.QPlainTextEdit(self.centralwidget)
        self.experiment_log.setMaximumSize(QtCore.QSize(352, 286))
        self.experiment_log.setReadOnly(True)
        self.experiment_log.setObjectName(_fromUtf8("experiment_log"))
        self.gridLayout.addWidget(self.experiment_log, 0, 1, 1, 1)
        self.paramTable = QtGui.QTableWidget(self.centralwidget)
        self.paramTable.setMinimumSize(QtCore.QSize(741, 561))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.paramTable.setFont(font)
        self.paramTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.paramTable.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked)
        self.paramTable.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.paramTable.setObjectName(_fromUtf8("paramTable"))
        self.paramTable.setColumnCount(0)
        self.paramTable.setRowCount(0)
        self.paramTable.verticalHeader().setDefaultSectionSize(22)
        self.paramTable.verticalHeader().setMinimumSectionSize(22)
        self.gridLayout.addWidget(self.paramTable, 0, 0, 2, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(352, 285))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.clusters = QtGui.QListWidget(self.tab)
        self.clusters.setGeometry(QtCore.QRect(0, 20, 171, 151))
        self.clusters.setObjectName(_fromUtf8("clusters"))
        self.cluster_name_field = QtGui.QLineEdit(self.tab)
        self.cluster_name_field.setGeometry(QtCore.QRect(230, 20, 113, 27))
        self.cluster_name_field.setObjectName(_fromUtf8("cluster_name_field"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(230, 0, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(230, 50, 101, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.cluster_add_btn = QtGui.QPushButton(self.tab)
        self.cluster_add_btn.setGeometry(QtCore.QRect(230, 100, 111, 27))
        self.cluster_add_btn.setObjectName(_fromUtf8("cluster_add_btn"))
        self.cluster_address_field = QtGui.QLineEdit(self.tab)
        self.cluster_address_field.setGeometry(QtCore.QRect(230, 70, 113, 27))
        self.cluster_address_field.setObjectName(_fromUtf8("cluster_address_field"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 64, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.cluster_type_combo = QtGui.QComboBox(self.tab)
        self.cluster_type_combo.setEnabled(True)
        self.cluster_type_combo.setGeometry(QtCore.QRect(10, 250, 16, 16))
        self.cluster_type_combo.setObjectName(_fromUtf8("cluster_type_combo"))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.cluster_type_combo.addItem(_fromUtf8(""))
        self.submit_btn = QtGui.QPushButton(self.tab)
        self.submit_btn.setGeometry(QtCore.QRect(10, 180, 151, 27))
        self.submit_btn.setObjectName(_fromUtf8("submit_btn"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.PlotParamTable = QtGui.QListWidget(self.tab_2)
        self.PlotParamTable.setGeometry(QtCore.QRect(10, 0, 256, 192))
        self.PlotParamTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.PlotParamTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.PlotParamTable.setObjectName(_fromUtf8("PlotParamTable"))
        self.plot_btn = QtGui.QPushButton(self.tab_2)
        self.plot_btn.setGeometry(QtCore.QRect(10, 200, 93, 29))
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 151, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.run_cmd_field = QtGui.QLineEdit(self.tab_3)
        self.run_cmd_field.setGeometry(QtCore.QRect(10, 30, 251, 31))
        self.run_cmd_field.setObjectName(_fromUtf8("run_cmd_field"))
        self.create_new_btn = QtGui.QPushButton(self.tab_3)
        self.create_new_btn.setGeometry(QtCore.QRect(270, 30, 71, 29))
        self.create_new_btn.setObjectName(_fromUtf8("create_new_btn"))
        self.exp_add_btn = QtGui.QPushButton(self.tab_3)
        self.exp_add_btn.setGeometry(QtCore.QRect(10, 210, 111, 27))
        self.exp_add_btn.setObjectName(_fromUtf8("exp_add_btn"))
        self.refresh_btn = QtGui.QPushButton(self.tab_3)
        self.refresh_btn.setGeometry(QtCore.QRect(120, 210, 111, 27))
        self.refresh_btn.setObjectName(_fromUtf8("refresh_btn"))
        self.terminate_btn = QtGui.QPushButton(self.tab_3)
        self.terminate_btn.setGeometry(QtCore.QRect(230, 210, 111, 27))
        self.terminate_btn.setObjectName(_fromUtf8("terminate_btn"))
        self.dupli_btn = QtGui.QPushButton(self.tab_3)
        self.dupli_btn.setGeometry(QtCore.QRect(10, 170, 111, 29))
        self.dupli_btn.setObjectName(_fromUtf8("dupli_btn"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "NeroGUI", None))
        self.paramTable.setSortingEnabled(True)
        self.label.setText(_translate("MainWindow", "cluster name", None))
        self.label_2.setText(_translate("MainWindow", "cluster address", None))
        self.cluster_add_btn.setText(_translate("MainWindow", "Add cluster", None))
        self.label_3.setText(_translate("MainWindow", "Clusters", None))
        self.cluster_type_combo.setItemText(0, _translate("MainWindow", "unmanaged", None))
        self.cluster_type_combo.setItemText(1, _translate("MainWindow", "slurm", None))
        self.submit_btn.setText(_translate("MainWindow", "Submit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Cluster", None))
        self.plot_btn.setText(_translate("MainWindow", "Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Plot", None))
        self.label_4.setText(_translate("MainWindow", "Insert run command", None))
        self.create_new_btn.setText(_translate("MainWindow", "Create", None))
        self.exp_add_btn.setText(_translate("MainWindow", "Import exp", None))
        self.refresh_btn.setText(_translate("MainWindow", "Fetch exp", None))
        self.terminate_btn.setText(_translate("MainWindow", "Terminate exp", None))
        self.dupli_btn.setText(_translate("MainWindow", "Duplicate exp", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Experiment", None))

