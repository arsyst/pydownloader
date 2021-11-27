from PyQt5 import QtCore, QtGui, QtWidgets


class PushButtonDelegate(QtWidgets.QStyledItemDelegate):
    clicked = QtCore.pyqtSignal(QtCore.QModelIndex)

    def paint(self, painter, option, index):
        if (
            isinstance(self.parent(), QtWidgets.QAbstractItemView)
            and self.parent().model() is index.model()
        ):
            self.parent().openPersistentEditor(index)

    def createEditor(self, parent, option, index):
        button = QtWidgets.QPushButton(parent)
        button.clicked.connect(lambda *args, ix=index: self.clicked.emit(ix))
        return button

    def setEditorData(self, editor, index):
        editor.setText(index.data(QtCore.Qt.DisplayRole))

    def setModelData(self, editor, model, index):
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QTableView()
    model = QtGui.QStandardItemModel(0, 2)
    for i in range(10):
        it1 = QtGui.QStandardItem()
        it1.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
        # noinspection PyTypeChecker
        it1.setFlags(it1.flags() | QtCore.Qt.ItemIsUserCheckable)
        it2 = QtGui.QStandardItem()
        it2.setData("text-{}".format(i), QtCore.Qt.DisplayRole)
        model.appendRow([it1, it2])

    # pass the view as parent
    delegate = PushButtonDelegate(w)
    w.setItemDelegateForColumn(1, delegate)

    def on_clicked(index):
        print(index.data())

    delegate.clicked.connect(on_clicked)

    w.setModel(model)
    w.show()
    sys.exit(app.exec_())
