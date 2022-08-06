import os.path
import subprocess
import sys
from typing import Optional

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QProgressBar, QVBoxLayout, QPushButton, QFileDialog, QApplication, QCheckBox, QSpinBox, \
    QMessageBox

from src import AzarArchive, CaesarCipher, CaesarDecoder, ARCHIVE_EXTENSION

PACK_ICON: Optional[QIcon] = None
UNPACK_ICON: Optional[QIcon] = None


class ShannonWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ShannonWidget, self).__init__()

        #
        # Window initialization
        #
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)
        self.setWindowTitle('Shannon | by ZavaruKitsu')

        #
        # Shared variables
        #
        self.out_path = ''
        self.progress_callback = self.on_progress

        btn_style = 'font-size: 24px'

        #
        # UI elements
        #
        self.encode_btn = QPushButton('Encode')
        self.encode_btn.setToolTip('Encode specified file using Shannon code & encrypt using Caesar cipher.')
        self.decode_btn = QPushButton('Decode')
        self.decode_btn.setToolTip('Decode specified file using Shannon code & decrypt using Caesar cipher.')

        # add icons
        self.encode_btn.setIcon(PACK_ICON)
        self.decode_btn.setIcon(UNPACK_ICON)
        self.encode_btn.setIconSize(QSize(28, 28))
        self.decode_btn.setIconSize(QSize(28, 28))

        # place icons at right
        self.encode_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.decode_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        # add event handlers
        self.encode_btn.clicked.connect(self.encode)
        self.decode_btn.clicked.connect(self.decode)

        self.draw_progress_bar_checkbox = QCheckBox('Draw progress bar')
        self.draw_progress_bar_checkbox.setToolTip('Turning this off can improve encryption & decryption speed')
        self.draw_progress_bar_checkbox.setChecked(True)
        self.draw_progress_bar_checkbox.stateChanged.connect(self.draw_progress_bar_checked)

        self.encryption_key = QSpinBox()
        self.encryption_key.setToolTip('The encryption key. Set 0 to disable.')
        self.encryption_key.setMinimum(0)
        self.encryption_key.setMaximum(999999)

        self.encode_btn.setStyleSheet(btn_style)
        self.decode_btn.setStyleSheet(btn_style)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(QtCore.Qt.AlignHCenter)

        self.layout = QVBoxLayout(self)

        self.layout.addStretch()
        self.layout.addWidget(self.encode_btn)
        self.layout.addWidget(self.decode_btn)
        self.layout.addWidget(self.draw_progress_bar_checkbox)
        self.layout.addWidget(self.encryption_key)
        self.layout.addWidget(self.progress_bar)
        self.layout.addStretch()

    def encode(self):
        dialog = QFileDialog(self)
        path = dialog.getOpenFileName(self, 'Select a file to pack', filter='Text files (*.txt)')[0]

        if not path:
            return

        filename = os.path.basename(path) + '.' + ARCHIVE_EXTENSION

        self.out_path = dialog.getSaveFileName(self, 'Select where to save a file', os.path.join('./out', filename))[0]

        if not self.out_path:
            return

        self.setDisabled(True)

        with AzarArchive(path, self.out_path, CaesarCipher, self.progress_callback, self.on_finish) as azar:
            azar.encoder.key = self.encryption_key.value()
            azar.write()

    def decode(self):
        dialog = QFileDialog(self)
        path = dialog.getOpenFileName(self, 'Select a file to unpack', './out',
                                      filter=f'ZavaruKitsu ARchive (*.{ARCHIVE_EXTENSION})')[0]

        if not path:
            return

        filename = os.path.basename(path).replace('.' + ARCHIVE_EXTENSION, '')

        self.out_path = dialog.getSaveFileName(self, 'Select where to save a file', os.path.join('./out', filename))[0]

        if not self.out_path:
            return

        self.setDisabled(True)

        with AzarArchive(path, self.out_path, CaesarDecoder, self.progress_callback, self.on_finish) as azar:
            azar.decoder.key = self.encryption_key.value()

            try:
                azar.read()
            except ValueError:
                self.on_finish('Invalid encryption key')


    def setDisabled(self, state: bool):
        self.encode_btn.setDisabled(state)
        self.decode_btn.setDisabled(state)
        self.draw_progress_bar_checkbox.setDisabled(state)
        self.encryption_key.setDisabled(state)

    def on_progress(self, total, processed):
        if self.progress_bar.maximum() != total:
            self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(processed)

        if processed % 100:
            QApplication.processEvents()

    def on_finish(self, msg: str):
        self.setDisabled(False)

        if msg != 'OK':
            msg_box = QMessageBox(QMessageBox.Warning, 'Error while reading\\writing', msg)
            msg_box.exec()
            return
        else:
            self.out_path = self.out_path.replace('/', '\\')
            subprocess.Popen(f'explorer /select,"{self.out_path}"')

        self.progress_bar.setValue(0)

    def draw_progress_bar_checked(self, event):
        self.progress_callback = self.on_progress if self.draw_progress_bar_checkbox.isChecked() else None


if __name__ == "__main__":
    if not os.path.exists('out'):
        os.makedirs('out')

    app = QtWidgets.QApplication([])

    PACK_ICON = QIcon(QPixmap('./assets/pack.png'))
    UNPACK_ICON = QIcon(QPixmap('./assets/unpack.png'))

    app.setWindowIcon(QIcon('./assets/app.ico'))

    widget = ShannonWidget()
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec())
