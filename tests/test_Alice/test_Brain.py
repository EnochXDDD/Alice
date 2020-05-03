import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from Alice import Brain
LOG = logging.getLogger(__name__)


class TimeEstimateTest:
    def test_QtGUI(self, exec_on=False):
        @Brain.TimeEstimate(handler=LOG.debug)
        def multiArgs(a, b, c):
            LOG.debug("Ans: {}".format(a + b + c))

        @Brain.TimeEstimate(without_any_args=True, handler=LOG.debug)
        def on_OK_clicked():
            with Brain.TimeEstimate(block_name="print OK", handler=LOG.debug):
                LOG.debug("btn_OK is clicked")
            multiArgs(1, 2, 3)

        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setFixedSize(640, 480)

        widget = QWidget(parent=window)
        layout = QVBoxLayout()
        btn_OK = QPushButton("OK", parent=widget)
        btn_OK.clicked.connect(on_OK_clicked)
        layout.addWidget(btn_OK)
        widget.setLayout(layout)

        window.setCentralWidget(widget)
        window.show()
        if exec_on:
            app.exec_()
        else:
            btn_OK.click()


class ExceptionCatchTest:
    def test_QtGUI(self, exec_on=False):
        Brain.ExceptionCatch(handler=LOG.error)

        def on_OK_clicked():
            raise Exception("btn_OK is clicked")

        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setFixedSize(640, 480)

        widget = QWidget(parent=window)
        layout = QVBoxLayout()
        btn_OK = QPushButton("OK", parent=widget)
        btn_OK.clicked.connect(on_OK_clicked)
        layout.addWidget(btn_OK)
        widget.setLayout(layout)

        window.setCentralWidget(widget)
        window.show()
        if exec_on:
            app.exec_()
        else:
            btn_OK.click()


def test_TimeEstimate(exec_on=False):
    bt = TimeEstimateTest()
    bt.test_QtGUI(exec_on=exec_on)


def test_ExceptionCatch(exec_on=False):
    bt = ExceptionCatchTest()
    bt.test_QtGUI(exec_on=exec_on)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_TimeEstimate(exec_on=True)
    test_ExceptionCatch(exec_on=True)
