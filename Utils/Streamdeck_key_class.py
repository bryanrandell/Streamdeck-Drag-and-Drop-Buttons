import os
import functions_for_streamdeck
# from ui_drag_drop_icons import Application


class StreamDeckPage(dict):
    def __init__(self, number_of_keys, default_icon):
        super().__init__()
        self.number_of_keys = number_of_keys
        self.default_icon = default_icon
        self.icons = self.values()
        self.buttons = self.keys()
        self.page_index = 1

        for i in range(number_of_keys):
            self[i + 1] = self.default_icon

class LabelPageList(dict):
    def __init__(self,number_of_element):
        super().__init__()
        self.element = None
        self.number_of_element = number_of_element
        # self.insert(0,self.number_of_element)
        for i in range(self.number_of_element):
            self[i] = self.element

class StreamdeckKey():
    def __init__(self, key_index):
        self.ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")
        self.default_icon_release = "default_icon64.png"
        self.default_icon_press = "default_icon64_press.png"
        self.default_font = "Roboto-Regular.ttf"
        self.label = "button {}".format(key_index)
        self.name = "button {}".format(key_index)
        self.icon_release = os.path.join(self.ASSETS_PATH, self.default_icon_release)
        self.icon_press = os.path.join(self.ASSETS_PATH, self.default_icon_press)
        self.function = KeyFunction(self.default_icon_release)
        self.font = os.path.join(self.ASSETS_PATH, self.default_font)
        self.state = False

    def change_icons(self, icon_path_release, icon_path_press):
        self.icon_release = os.path.join(self.ASSETS_PATH, icon_path_release)
        self.icon_press = os.path.join(self.ASSETS_PATH, icon_path_press)
        self.function.icon = icon_path_release
        self.name = icon_path_release.split('.')[0]
        self.label = icon_path_release.split('.')[0]

    def change_function(self, function):
        self.function = function

    def change_font(self, font):
        self.font = os.path.join(self.ASSETS_PATH, font)

    def change_state(self, state):
        self.state = state


class KeyFunction():
    def __init__(self, icon_name):
        self.icon = icon_name
        self.key_function = self.function_by_icon_name

    def launch_function(self):
        self.key_function(self.icon)

    # todo dummy function, must be replace with true function use by you device or the software
    def function_by_icon_name(self, icon_name):
        if icon_name == "cam.png":
            functions_for_streamdeck.dummy_os_mkdir_func()
            return print("function cam1")
        elif icon_name == "cam2.png":
            functions_for_streamdeck.dummy_function_testing_davinci()
            return print("function cam2")
        elif icon_name == "cam3.png":
            return print("function cam3")
        elif icon_name == "dest_mon.png":
            return print("function dest_mon")
        elif icon_name == "Exit.png":
            return print("exiting app")
        elif icon_name == "next_page.png":
            return print("function next_page")
        elif icon_name == "prev_page.png":
            return print("function prev_page")
        else:
            return print("function default button")

    def function_next_page(self):
        pass
        # Application().next_page()

class UserButton():
    def __init__(self, name, label, icon):
        self.name = name
        self.label = label
        self.icon = icon
        # self.function = function

    # def function_cam1(self):
    #     print("fucntion cam1")
    #
    # def function_cam2(self):
    #     print("fucntion cam2")
    #
    # def function_cam3(self):
    #     print("fucntion cam3")
    #
    # def function_dest2(self):
    #     print("fucntion dest2")


# user_button_list should be later define by the user in a separate class with specific icons and functions
user_button_list = [
    UserButton("cam", "cam", "cam.png"),
    UserButton("cam2", "cam2", "cam2.png"),
    UserButton("cam3", "cam3", "cam3.png"),
    UserButton("dest_mon", "dest_mon", "dest_mon.png"),
    UserButton("exit", "exit", "Exit.png"),
    UserButton("next_page", "next_page", "next_page.png"),
    UserButton("prev_page", "prev_page", "prev_page.png")
]



