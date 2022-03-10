import sys
import os
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QGridLayout, QGroupBox, QPushButton,
                             QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QImage
from PyQt5.QtCore import QMimeData, Qt, QRunnable, pyqtSlot, QThreadPool, QObject, pyqtSignal
# from StreamDeck.DeviceManager import DeviceManager
from streamdeck_dummy import DeviceManager
from Streamdeck_button_configuration_class_key import StreamDeckInit
from Streamdeck_key_class import UserButton

#todo implement the streamdeck.

# dummy function for testing streamdeck implementation
def function_to_implement_streamdeck(deck_key_slot):  #, icon_path, string_function):
    print("button assign to{}".format(deck_key_slot))




# class RespondedToWorkerSignals(QObject):
#     callback_from_worker = pyqtSignal()
#
# #todo maybe useless for now or I don't know how to handle it
class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, streamdecks_instance):
        super(Worker, self).__init__()
        self.streamdecks_thread_instance = streamdecks_instance

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print('starting streamdeck')
        # basic_usage.run()
        # streamdeck_button_configuration.main(self.args[0])
        # self.instance(streamdecks)
        self.streamdecks_thread_instance.main_run()


class DraggableLabel(QLabel):
    def __init__(self, parent, image,text):
        super(QLabel,self).__init__(parent)
        self.setText(text)
        self._text = text
        self.setPixmap(QPixmap(image))
        self.show()

    def text(self):
        if self._text:
            return self._text
        return super().text()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        mimedata.setImageData(self.pixmap().toImage())
        # mimedata.setUrls(["test"])

        drag.setMimeData(mimedata)
        # pixmap = QPixmap(self.size())
        pixmap = QPixmap(self.size())

        # pixmap.scaledToWidth(50)
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class StreamDeckLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.title = title
        self.setAcceptDrops(True)
        self.drop_item_path = "default_icon64.png"

        # put the default item in the streamdeck button
        function_to_implement_streamdeck(self.title)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            print("event accepted")
            event.accept()
        else:
            print("event rejected")
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            self.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
            self.drop_item_path = event.mimeData().text()
            # replace the default button by the new item dropped
            function_to_implement_streamdeck(self.drop_item_path)
            # basic_usage.set_button()
            # streamdeck_button_configuration.update_key_image(streamdecks[0], , True)
            print("{} assign to {}".format(self.title, self.drop_item_path))


class Application(QWidget):
    def __init__(self, streamdecks, user_button_list):
        super().__init__()
        # self.initUI()
        self.dict_label_streamdeck = {}
        self.user_button_list = user_button_list
        #todo declare these varibles in a more pythonic way in the streamdeck_key_class.py file
        self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_7,self.label_6, self.label_8, \
        self.label_9, self.label_10, self.label_11, self.label_12,self.label_13, self.label_14, \
        self.label_15 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None

        self.all_labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6,
                           self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12,
                           self.label_13, self.label_14, self.label_15]

        self.setWindowTitle("drag and drop streamdeck")

        self.streamdeck_instance = StreamDeckInit(streamdecks)

        self.streamdeck_button_count_vertically = self.streamdeck_instance.deck.KEY_COLS
        self.streamdeck_button_count_horizontally = self.streamdeck_instance.deck.KEY_ROWS
        print(self.streamdeck_button_count_vertically, self.streamdeck_button_count_horizontally)
        self.threadpool = QThreadPool()
        self.worker = Worker(self.streamdeck_instance)
        self.threadpool.start(self.worker)

        left_grid_layout = QGridLayout()
        right_grid_layout = QGridLayout()

        #todo put these on the steamdeck_key_class.py

        icon_height = 50
        icon_width = 50
        assets_path = "assets/"
        # for icon in os.listdir(assets_path):
        #     if icon.endswith(".png"):
        left_grid_loop_count = 0
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                if left_grid_loop_count >= len(self.user_button_list): break
                label_drag = DraggableLabel(self,
                                            os.path.join(assets_path, self.user_button_list[left_grid_loop_count].icon),
                                            self.user_button_list[left_grid_loop_count].icon)
                left_grid_layout.addWidget(label_drag, x, y)
                left_grid_loop_count += 1


        # groupBox = QGroupBox("Steamdeck")

        button_list_label = []
        button_count = 1
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                # button_list_label.append(my_label("Button {}".format(x+y),self))
                self.all_labels[button_count - 1] = StreamDeckLabel("Button {}".format(button_count), self)
                self.all_labels[button_count- 1].setPixmap(QPixmap.fromImage(QImage(os.path.join(assets_path,
                                                                                                 "default_icon64.png"))))
                # button_list_label[x+y].resize(50,50)
                #todo try make an event for instantly uploading streamdeck buttons
                # self.all_labels[button_count - 1].dropEvent()
                right_grid_layout.addWidget(self.all_labels[button_count - 1], x, y)
                self.dict_label_streamdeck[button_count] = self.all_labels[button_count - 1].drop_item_path
                button_count += 1

        # groupBox.setLayout(right_grid_layout)
        main_layout = QHBoxLayout(self)

        vertical_layout = QVBoxLayout()
        button_update = QPushButton("update", self)
        button_update.clicked.connect(self.push_button_update_streamdeck)
        vertical_layout.addWidget(button_update)

        main_layout.addLayout(vertical_layout)
        main_layout.addLayout(right_grid_layout)
        main_layout.addLayout(left_grid_layout)
        # main_layout.addLayout(groupBox)

    def drop_event(self, label):
        print('ok'.format(label))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window and StreamDeck Close',
                                     'Are you sure you want to close the window and the streamdeck?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.streamdeck_instance.deck.is_open():
                print("deck up")
                self.streamdeck_instance.deck.reset()
                self.streamdeck_instance.deck.close()
            event.accept()
            # self.threadpool.terminate()
            print('Window closed')
        else:
            event.ignore()

    @pyqtSlot()
    def push_button_update_streamdeck(self):
        for button in range(len(self.dict_label_streamdeck)):
            self.dict_label_streamdeck[button + 1] = self.all_labels[button].drop_item_path
            icon_press_path = self.all_labels[button].drop_item_path.split(".")[0] + "_press." + self.all_labels[button].drop_item_path.split(".")[1]
            self.streamdeck_instance.key_list[button].change_icons(self.all_labels[button].drop_item_path, icon_press_path)
            # self.streamdeck_instance.key_list[button].change_function()

            self.streamdeck_instance.update_key_image(self.streamdeck_instance.deck, button, False)

        print(self.dict_label_streamdeck)


if __name__ == "__main__":
    user_button_list = [
        UserButton("cam", "cam", "cam.png"),
        UserButton("cam2", "cam2", "cam2.png"),
        UserButton("cam3", "cam3", "cam3.png"),
        UserButton("dest_mon", "dest_mon", "dest_mon.png"),
        UserButton("exit", "exit", "Exit.png"),
        UserButton("next_page", "next_page", "next_page.png"),
        UserButton("prev_page", "prev_page", "prev_page.png")
    ]
    streamdecks = DeviceManager().enumerate()
    app = QApplication(sys.argv)
    fenetre = Application(streamdecks, user_button_list)
    fenetre.show()

    sys.exit(app.exec_())


