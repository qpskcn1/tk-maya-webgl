# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Apr 17 15:21:08 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(385, 288)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stack_widget = QtGui.QStackedWidget(Dialog)
        self.stack_widget.setObjectName("stack_widget")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout = QtGui.QVBoxLayout(self.page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.version_name_label = QtGui.QLabel(self.page)
        self.version_name_label.setObjectName("version_name_label")
        self.horizontalLayout.addWidget(self.version_name_label)
        self.version_name = QtGui.QLineEdit(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.version_name.sizePolicy().hasHeightForWidth())
        self.version_name.setSizePolicy(sizePolicy)
        self.version_name.setObjectName("version_name")
        self.horizontalLayout.addWidget(self.version_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.context_widget = ContextWidget(self.page)
        self.context_widget.setObjectName("context_widget")
        self.verticalLayout.addWidget(self.context_widget)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.item_comments = PublishDescriptionEdit(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_comments.sizePolicy().hasHeightForWidth())
        self.item_comments.setSizePolicy(sizePolicy)
        self.item_comments.setMinimumSize(QtCore.QSize(0, 90))
        self.item_comments.setMaximumSize(QtCore.QSize(16777215, 90))
        self.item_comments.setObjectName("item_comments")
        self.gridLayout_2.addWidget(self.item_comments, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.item_thumbnail = Thumbnail(self.page)
        self.item_thumbnail.setMinimumSize(QtCore.QSize(160, 90))
        self.item_thumbnail.setMaximumSize(QtCore.QSize(160, 90))
        self.item_thumbnail.setText("")
        self.item_thumbnail.setScaledContents(False)
        self.item_thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.item_thumbnail.setObjectName("item_thumbnail")
        self.gridLayout_2.addWidget(self.item_thumbnail, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.stack_widget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout = QtGui.QGridLayout(self.page_2)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtGui.QLabel(self.page_2)
        self.label_6.setMinimumSize(QtCore.QSize(100, 100))
        self.label_6.setMaximumSize(QtCore.QSize(100, 100))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/tk_maya_webgl/complete.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.label_8 = QtGui.QLabel(self.page_2)
        self.label_8.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.jump_to_shotgun = QtGui.QPushButton(self.page_2)
        self.jump_to_shotgun.setObjectName("jump_to_shotgun")
        self.verticalLayout_3.addWidget(self.jump_to_shotgun)
        self.jump_to_panel = QtGui.QPushButton(self.page_2)
        self.jump_to_panel.setObjectName("jump_to_panel")
        self.verticalLayout_3.addWidget(self.jump_to_panel)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(31, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 2, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 1, 1, 1)
        self.stack_widget.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.stack_widget)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem6 = QtGui.QSpacerItem(120, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_2.addWidget(self.cancel)
        self.submit = QtGui.QPushButton(Dialog)
        self.submit.setObjectName("submit")
        self.horizontalLayout_2.addWidget(self.submit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.stack_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.version_name, self.submit)
        Dialog.setTabOrder(self.submit, self.cancel)
        Dialog.setTabOrder(self.cancel, self.jump_to_panel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "OFG Model Review", None, QtGui.QApplication.UnicodeUTF8))
        self.version_name_label.setText(QtGui.QApplication.translate("Dialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Screenshot:", None, QtGui.QApplication.UnicodeUTF8))
        self.item_thumbnail.setToolTip(QtGui.QApplication.translate("Dialog", "Click to take a screenshot.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Version Creation Complete!", None, QtGui.QApplication.UnicodeUTF8))
        self.jump_to_shotgun.setText(QtGui.QApplication.translate("Dialog", "Show in Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.jump_to_panel.setText(QtGui.QApplication.translate("Dialog", "Show in Panel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.submit.setText(QtGui.QApplication.translate("Dialog", "Upload to Shotgun", None, QtGui.QApplication.UnicodeUTF8))

from ..qtwidgets import ContextWidget, Thumbnail, PublishDescriptionEdit
from . import resources_rc
