__authour__ = 'Harry Burge'
__date_created__ = '21/05/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '21/05/2020'

# Imports
import sys

from PyQt5.QtWidgets import QApplication
from UI.screen_manager import ScreenManager


def Visuals():
    app = QApplication(sys.argv)

    sm = ScreenManager()
    sm.show_screen('CDR')
    sys.exit(app.exec_())


if __name__ == '__main__':
    Visuals()