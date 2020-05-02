import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from Alice import Brain
LOG = logging.getLogger(__name__)


class TimeEstimateTest:
    def test_QtGUI(self):
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
        sys.exit(app.exec_())


class ExceptionCatchTest:
    def test_withRaise(self):
        Brain.ExceptionCatch(handler=LOG.error)
        raise Exception("exception test")

    def test_QtGUI(self):
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
        sys.exit(app.exec_())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # bt = TimeEstimateTest()
    # bt.test_QtGUI()

    bt = ExceptionCatchTest()
    bt.test_QtGUI()
    # bt.test_withRaise()
