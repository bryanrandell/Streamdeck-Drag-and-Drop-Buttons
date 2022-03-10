import sys
import os
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QGridLayout, QGroupBox, QPushButton,
                             QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QImage
from PyQt5.QtCore import QMimeData, Qt, QRunnable, pyqtSlot, QThreadPool, QObject, pyqtSignal
from StreamDeck.DeviceManager import DeviceManager
from Streamdeck_button_configuration_class_key import StreamDeckInit
from Streamdeck_key_class import UserButton, StreamDeckPage, LabelPageList
import Streamdeck_key_class

#todo implement the streamdeck.
#todo handle multiple pages

# dummy function for testing streamdeck implementation
def function_to_implement_streamdeck(deck_key_slot):  #, icon_path, string_function):
    print("button assign to{}".format(deck_key_slot))


# class RespondedToWorkerSignals(QObject):
#     callback_from_worker = pyqtSignal()
#
#todo maybe useless for now or I don't know how to handle it
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
    """
    Label with an icon a name and a function can be dragged to the streamdeck ui
    """
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
    """
    Label representing the streamdeck buttons layout so the user can drag and drop his button and assign them
    to the streamdeck
    """
    def __init__(self, title, index, parent):
        super().__init__(title, parent)
        self.parent = parent
        self.title = title
        self.setAcceptDrops(True)
        self.drop_item_path = "default_icon64.png"
        self.index = index

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
            self.parent.update_streamdeck_keys(self.index)


class Application(QWidget):
    """
    A UI to assign multiple pages and personnalized button (both icon and function) to a streamdeck
    Work in paralell with the streamdeck and has to be open so the streamdeck can work with
    """
    valueChanged = pyqtSignal(int)

    def __init__(self, streamdecks, user_button_list):
        super().__init__()

        #todo declare these varibles in a more pythonic way in the streamdeck_key_class.py file
        # self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_7,self.label_6, self.label_8, \
        # self.label_9, self.label_10, self.label_11, self.label_12,self.label_13, self.label_14, \
        # self.label_15 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        #
        # self.all_labels = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6,
        #                    self.label_7, self.label_8, self.label_9, self.label_10, self.label_11, self.label_12,
        #                    self.label_13, self.label_14, self.label_15]
        # self.all_labels_page = [self.all_labels]


        self.setWindowTitle("drag and drop streamdeck")
        # initialize the streamdeck
        self.streamdeck_instance = StreamDeckInit(streamdecks)
        # get the streamdeck infos for creating the UI
        self.streamdeck_button_count_vertically = self.streamdeck_instance.deck.KEY_COLS
        self.streamdeck_button_count_horizontally = self.streamdeck_instance.deck.KEY_ROWS
        self.streamdeck_button_count_total = self.streamdeck_instance.deck.KEY_COUNT
        # initialize the second thread so the streamdeck can work in paralell with PyQt5
        self.threadpool = QThreadPool()
        self.worker = Worker(self.streamdeck_instance)
        self.threadpool.start(self.worker)

        # create the grid layouts
        left_grid_layout = QGridLayout()
        self.right_grid_layout_list = QGridLayout()

        #todo put these on the steamdeck_key_class.py
        self.assets_path = "assets/"
        self.default_icon = "default_icon64.png"
        icon_height = 50
        icon_width = 50

        # create the pages list for both streamdeck and grid layout
        self._streamdeck_page_index = 0
        self.streamdeck_page_list = [StreamDeckPage(self.streamdeck_button_count_total,
                                                    os.path.join(self.assets_path, self.default_icon))]
        self.all_labels_page = [LabelPageList(self.streamdeck_button_count_total)]

        # user_button_list is for the user to create specific buttons
        self.user_button_list = user_button_list

        # create the grid layout with user button
        left_grid_loop_count = 0
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                if left_grid_loop_count >= len(self.user_button_list): break
                label_drag = DraggableLabel(self,
                                            os.path.join(self.assets_path, self.user_button_list[left_grid_loop_count].icon),
                                            self.user_button_list[left_grid_loop_count].icon)
                left_grid_layout.addWidget(label_drag, x, y)
                left_grid_loop_count += 1

        # create the default grid representing the streamdeck layout
        button_count = 1
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                # button_list_label.append(my_label("Button {}".format(x+y),self))
                self.all_labels_page[self.streamdeck_page_index][button_count - 1] = \
                    StreamDeckLabel("Button {}".format(button_count), button_count, self)
                self.all_labels_page[self.streamdeck_page_index][button_count- 1].setPixmap(QPixmap.fromImage(
                    QImage(os.path.join(self.assets_path,"default_icon64.png"))))
                # button_list_label[x+y].resize(50,50)
                #todo try make an event for instantly uploading streamdeck buttons

                self.right_grid_layout_list.addWidget(self.all_labels_page[self.streamdeck_page_index][button_count - 1], x, y)
                self.streamdeck_page_list[self.streamdeck_page_index][button_count] = \
                    self.all_labels_page[self.streamdeck_page_index][button_count - 1].drop_item_path
                button_count += 1

        self.main_layout = QHBoxLayout(self)

        vertical_layout = QVBoxLayout()

        button_next_page = QPushButton("next page", self)
        button_next_page.clicked.connect(self.next_page)
        vertical_layout.addWidget(button_next_page)

        button_previous_page = QPushButton("previous page", self)
        button_previous_page.clicked.connect(self.previous_page)
        vertical_layout.addWidget(button_previous_page)

        self.label_page = QLabel("Page {}".format(self.streamdeck_page_index + 1))
        vertical_layout.addWidget(self.label_page)


        self.main_layout.addLayout(vertical_layout)
        self.main_layout.addLayout(self.right_grid_layout_list)
        self.main_layout.addLayout(left_grid_layout)

        self.valueChanged.connect(self.change_page_streamdeck)


    # ------- function with event ---------
    # trigger the value change of the page index
    @property
    def streamdeck_page_index(self):
        return self._streamdeck_page_index

    @streamdeck_page_index.setter
    def streamdeck_page_index(self, value):
        self._streamdeck_page_index = value
        self.valueChanged.emit(value)
        print('page changed')

    # def change_page_streamdeck(self):
    #     print('page changed 3')

    def keyPressEvent(self, event):
        """
        a simple key press event to quit the app
        :param e:
        :return:
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """
        a close event handle to quit both the UI and the streamdeck instance who work in paralell
        :param event:
        :return:
        """
        message_box = QMessageBox.question(self,
                                           'Window and StreamDeck Close',
                                           'Are you sure you want to close the window and the streamdeck?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message_box == QMessageBox.Yes:
            if self.streamdeck_instance.deck.is_open():
                print("deck up")
                self.streamdeck_instance.deck.reset()
                self.streamdeck_instance.deck.close()
            event.accept()
            # self.threadpool.terminate()
            print('Window closed')
        else:
            event.ignore()

    # ------- function for streamdeck ---------
    def next_page(self):
        self.streamdeck_page_index += 1
        if len(self.streamdeck_page_list) <= self.streamdeck_page_index:
            self.streamdeck_page_list.append(StreamDeckPage(self.streamdeck_button_count_total, self.default_icon))
            self.all_labels_page.append(LabelPageList(self.streamdeck_button_count_total))
            # self.right_grid_layout_list.append(QGridLayout())
            # self.new_page()
        self.delete_widgets_grid()
        self.refresh_streamdeck_page()
        print(self.streamdeck_page_list[self.streamdeck_page_index])
        self.label_page.setText("Page {}".format(self.streamdeck_page_index + 1))

    def previous_page(self):
        if self.streamdeck_page_index > 0:
            self.delete_widgets_grid()
            self.streamdeck_page_index -= 1
            self.refresh_streamdeck_page()
            print(self.streamdeck_page_list[self.streamdeck_page_index])
            self.label_page.setText("Page {}".format(self.streamdeck_page_index + 1))

    def delete_widgets_grid(self):
        """
        trying to refresh the streamdeck grid layout
        :return:
        """
        button_count = 1
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                self.right_grid_layout_list.removeWidget(
                    self.all_labels_page[self.streamdeck_page_index - 1][button_count - 1])

    def refresh_streamdeck_page(self):
        """
        function used when the user change the page
        :return:
        """
        button_count = 1
        for x in range(self.streamdeck_button_count_horizontally):
            for y in range(self.streamdeck_button_count_vertically):
                # button_list_label.append(my_label("Button {}".format(x+y),self))
                self.all_labels_page[self.streamdeck_page_index][button_count - 1] = StreamDeckLabel("Button {}".format(button_count), button_count,self)
                icon = self.streamdeck_page_list[self.streamdeck_page_index][button_count]
                icon_press_path = self.streamdeck_page_list[self.streamdeck_page_index][button_count].split(".")[0] + "_press." + \
                                  self.streamdeck_page_list[self.streamdeck_page_index][button_count].split(".")[1]
                self.streamdeck_instance.key_list[button_count - 1].change_icons(icon, icon_press_path)
                # self.streamdeck_instance.key_list[button].change_function()
                self.streamdeck_instance.update_key_image(self.streamdeck_instance.deck, button_count - 1, False)
                self.all_labels_page[self.streamdeck_page_index][button_count - 1].setPixmap(QPixmap.fromImage(QImage(os.path.join(self.assets_path,
                                                                                                  icon))))
                # button_list_label[x+y].resize(50,50)
                # todo try make an event for instantly uploading streamdeck buttons
                self.right_grid_layout_list.addWidget(self.all_labels_page[self.streamdeck_page_index][button_count - 1], x, y)
                button_count += 1

    def update_streamdeck_keys(self, index):
        """
        this function is triggered when a user button is dragged to the streamdeck layout and refresh the streamdeck
        :param index:
        :return:
        """
        self.streamdeck_page_list[self.streamdeck_page_index][index] = self.all_labels_page[self.streamdeck_page_index][index - 1].drop_item_path
        icon = self.streamdeck_page_list[self.streamdeck_page_index][index]
        icon_press_path = self.streamdeck_page_list[self.streamdeck_page_index][index].split(".")[0] + "_press." + self.streamdeck_page_list[self.streamdeck_page_index][index].split(".")[1]
        self.streamdeck_instance.key_list[index - 1].change_icons(icon, icon_press_path)
        # self.streamdeck_instance.key_list[button].change_function()
        self.streamdeck_instance.update_key_image(self.streamdeck_instance.deck, index - 1, False)
        print(self.streamdeck_page_list[self.streamdeck_page_index])

    # # function used when the user change the page
    # def refresh_streamdeck_page(self):
    #     button_count = 1
    #     for x in range(self.streamdeck_button_count_horizontally):
    #         for y in range(self.streamdeck_button_count_vertically):
    #             # button_list_label.append(my_label("Button {}".format(x+y),self))
    #             self.all_labels_page[self.streamdeck_page_index][button_count - 1] = StreamDeckLabel("Button {}".format(button_count), button_count,self)
    #             icon = self.streamdeck_page_list[self.streamdeck_page_index][button_count]
    #             self.all_labels_page[self.streamdeck_page_index][button_count - 1].setPixmap(QPixmap.fromImage(QImage(os.path.join(self.assets_path,
    #                                                                                               icon))))
    #             # button_list_label[x+y].resize(50,50)
    #             # todo try make an event for instantly uploading streamdeck buttons
    #             self.right_grid_layout_list.addWidget(self.all_labels_page[self.streamdeck_page_index][button_count - 1], x, y)
    #             button_count += 1


    # # may be useless
    # def new_page(self):
    #     button_count = 1
    #     for x in range(self.streamdeck_button_count_horizontally):
    #         for y in range(self.streamdeck_button_count_vertically):
    #             # button_list_label.append(my_label("Button {}".format(x+y),self))
    #             self.all_labels_page[self.streamdeck_page_index][button_count - 1] = StreamDeckLabel("Button {}".format(button_count), button_count, self)
    #             self.all_labels_page[self.streamdeck_page_index][button_count- 1].setPixmap(QPixmap.fromImage(QImage(os.path.join(self.assets_path,
    #                                                                                              "default_icon64.png"))))
    #             # button_list_label[x+y].resize(50,50)
    #             #todo try make an event for instantly uploading streamdeck buttons
    #
    #             self.right_grid_layout_list.addWidget(self.all_labels_page[self.streamdeck_page_index][button_count - 1], x, y)
    #             self.streamdeck_page_list[self.streamdeck_page_index][button_count] = self.all_labels_page[self.streamdeck_page_index][button_count - 1].drop_item_path
    #             button_count += 1

    #
    # @pyqtSlot()
    # def push_button_update_streamdeck(self):
    #     for button in range(len(self.streamdeck_page_list[self.streamdeck_page_index])):
    #         self.streamdeck_page_list[self.streamdeck_page_index][button + 1] = self.all_labels_page[self.streamdeck_page_index][button].drop_item_path
    #         icon_press_path = self.all_labels_page[self.streamdeck_page_index][button].drop_item_path.split(".")[0] + "_press." + self.all_labels_page[self.streamdeck_page_index][button].drop_item_path.split(".")[1]
    #         self.streamdeck_instance.key_list[button].change_icons(self.all_labels_page[self.streamdeck_page_index][button].drop_item_path, icon_press_path)
    #         # self.streamdeck_instance.key_list[button].change_function()
    #         self.streamdeck_instance.update_key_image(self.streamdeck_instance.deck, button, False)
    #
    #     print(self.streamdeck_page_list[self.streamdeck_page_index])

if __name__ == "__main__":
    user_button_list = Streamdeck_key_class.user_button_list
    streamdecks = DeviceManager().enumerate()
    app = QApplication(sys.argv)
    fenetre = Application(streamdecks, user_button_list)
    fenetre.show()

    sys.exit(app.exec_())


