from PyQt5 import QtWidgets, QtCore

import sys
import logging

from window import MainAppWindow
import settings.settings as s

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    if s.DEBUG:
        logging.basicConfig(
            filename=s.LOGGING_FILE_PATH,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )
    else:
        logging.basicConfig(
            filename=s.LOGGING_FILE_PATH,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )

    logger.error('Starting app')

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    main_window = MainAppWindow()
    main_window.show()

    sys.exit(app.exec_())
