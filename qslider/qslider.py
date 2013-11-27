# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


""" Custom Switch Widget, inspired from some QML desktop components """


# imports
from PyQt4.QtCore import (pyqtSignal, pyqtSignature, QEasingCurve,
                          QPropertyAnimation, Qt)
from PyQt4.QtGui import (QApplication, QColor, QGraphicsDropShadowEffect,
                         QMainWindow, QSlider)


# constants
qss_knob = '''
    QSlider::handle:horizontal {
        border-image: url(knob.png);
        width: 32px; margin: 2px
}'''
qss_off = '''
    QSlider::groove:horizontal {
        border-image: url(off.png);
        height: 35px
}'''
qss_on = '''
    QSlider::groove:horizontal {
        border-image: url(on.png);
        height: 35px
}'''


###############################################################################


class QSwitch(QSlider):
    """ Custom Switch Widget, inspired from some QML desktop components """
    style_knob, style_off, style_on = qss_knob, qss_off, qss_on
    clicked, animationOk = pyqtSignal(), pyqtSignal()

    def __init__(self, parent=None):
        """ Init Custom Switch Widget, set Animation and Glow effects """
        QSlider.__init__(self, parent)
        self.setOrientation(Qt.Horizontal)
        self.animationType = QEasingCurve.OutExpo
        self.animation = QPropertyAnimation(self, "value")
        self.animation.setDuration(1000)
        self.animation.finished.connect(self.animationDone)
        self.clicked.connect(self.changeValue)
        self.setStyleSheet(self.style_knob + self.style_off)
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setOffset(0)
        self.glow.setBlurRadius(99)
        self.glow.setColor(QColor(99, 255, 255))
        self.setGraphicsEffect(self.glow)
        self.glow.setEnabled(False)

    def changeValue(self):
        """ method to change the actual state ON <--> OFF """
        self.animation.setEasingCurve(self.animationType)
        if self.value() == self.maximum():
            self.animation.setStartValue(self.maximum())
            self.animation.setEndValue(self.minimum())
            self.animation.start()
            self.setStyleSheet(self.style_knob + self.style_off)
            self.glow.setEnabled(False)
            return
        else:
            self.animation.setStartValue(self.minimum())
            self.animation.setEndValue(self.maximum())
            self.setStyleSheet(self.style_knob + self.style_on)
            self.glow.setEnabled(True)
        self.animation.start()

    @pyqtSignature("setAtMax()")
    def setAtMax(self):
        """ method to set at Maximum, aka ON """
        if self.value() == self.minimum():
            self.animation.setEasingCurve(self.animationType)
            self.animation.setStartValue(self.minimum())
            self.animation.setEndValue(self.maximum())
            self.animation.start()
            self.setStyleSheet(self.style_knob + self.style_on)

    @pyqtSignature("setAtMin()")
    def setAtMin(self):
        """ method to set at Minimum, aka OFF """
        if self.value() == self.maximum():
            self.animation.setEasingCurve(self.animationType)
            self.animation.setStartValue(self.maximum())
            self.animation.setEndValue(self.minimum())
            self.animation.start()
            self.setStyleSheet(self.style_knob + self.style_off)

    def mousePressEvent(self, event):
        """ method to respond a signal to mouse pointer clicks """
        self.clicked.emit()

    def isChecked(self):
        """ method to return a bool based on actual state """
        return self.value() == self.maximum()

    def wheelEvent(self, event):
        """ dumb method, its not a bug leave it alone """
        return

    def animationDone(self):
        """ method to respond a signal to animation effects """
        self.animationOk.emit()


class MainWindow(QMainWindow):
    """ simplest possible main window to test the slider """
    def __init__(self, parent=None):
        """ just add the slider to window """
        QMainWindow.__init__(self, parent)
        QSwitch(self)


def main():
    """ main function to call main window """
    app, w = QApplication(sys.argv), MainWindow()
    w.show()
    return app.exec_()


###############################################################################


if __name__ == "__main__":
    print(__doc__)
    import sys  # isort:skip
    sys.exit(main())
