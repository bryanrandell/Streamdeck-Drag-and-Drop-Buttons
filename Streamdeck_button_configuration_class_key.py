#!/usr/bin/env python3
#                 FROM
#         Python Stream Deck Library
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Example script showing basic library usage - updating key images with new
# tiles generated at runtime, and responding to button state change events.

import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from AJA_Kumo_HTTP_GET_REQUEST import kumo_config_main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Streamdeck_key_class import StreamdeckKey

# Used for controlling the AJA KUMO with selenium webdriver and HTTP GET request
# options = Options()
# options.headless = True
# driver = webdriver.Chrome()
# driver.get("http://169.254.78.35/")
#
# web_dest_1_label, web_dest_2_label = 17, 18
#
# button_dest_1 = driver.find_element_by_id("eParamID_Button_Settings_{}".format(web_dest_1_label))
# button_dest_2 = driver.find_element_by_id("eParamID_Button_Settings_{}".format(web_dest_2_label))



# Folder location of image assets used by this example.
def dummy_function_for_testing_button_function_cam_press():
    print("dummy_function_for_testing_button_function_cam_press")

def dummy_function_for_testing_button_function_dest_press():
    print("dummy_function_for_testing_button_function_dest_press")


class StreamDeckInit():
    """
    I transformed the initial fuction from
    """
    def __init__(self, streamdecks):
        self.ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
        self.streamdecks = streamdecks
        print("Found {} Stream Deck(s).\n".format(len(self.streamdecks)))
        for index, deck in enumerate(self.streamdecks):
            self.deck = deck
    def main_run(self):
        self.deck.open()
        self.deck.reset()
        print("Opened '{}' device (serial number: '{}')".format(self.deck.deck_type(), self.deck.get_serial_number()))
        # Set initial screen brightness to 30%.
        self.deck.set_brightness(30)
        # Set initial key images.
        self.key_list = []
        for key_index in range(self.deck.key_count()):
            self.key_list.append(StreamdeckKey(key_index))
            self.update_key_image(self.deck, key_index, False)
        # Register callback function for when a key state changes.
        self.deck.set_key_callback(self.key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        # for t in threading.enumerate():
        #     try:
        #         t.join()
        #     except RuntimeError:
        #         pass


    # Generates a custom tile with run-time generated text and custom image via the
    # PIL module.
    def render_key_image(self, deck, icon_filename, font_filename, label_text):
        """
        Resize the source image asset to best-fit the dimensions of a single key,
        leaving a margin at the bottom so that we can draw the key title
        afterwards.
        :param deck:
        :param icon_filename:
        :param font_filename:
        :param label_text:
        :return:
        """
        icon = Image.open(icon_filename)
        image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_filename, 14)
        draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")
        return PILHelper.to_native_format(deck, image)

    def get_key_style(self, deck, key, state):

        name = self.key_list[key].name
        if not state:
            icon = self.key_list[key].icon_release
        else:
            icon = self.key_list[key].icon_press
        font = self.key_list[key].font
        label = self.key_list[key].label
        function = self.key_list[key].function

        return {
            "name": name,
            "icon": icon,
            "font": font,
            "label": label,
            "function" : function
        }

    # Returns styling information for a key based on its position and state.
    def old_get_key_style(self, deck, key, icon_filename, state):
        # Last button in the example application is the exit button.
        exit_key_index = deck.key_count() - 1

        if key == exit_key_index:
            # name = "exit"
            # icon = "{}.png".format("Exit")
            font = "Roboto-Regular.ttf"
            label = "Bye" if state else "Exit"
            function = "function"

        elif key == 3:
            # name = "dest_{}".format(key - 2)
            # icon = "{}.png".format("dest_mon_press" if state else "dest_mon")
            font = "Roboto-Regular.ttf"
            label = "Pressed!" if state else "Dest {}".format(key - 2)
            function = "function"
        elif key == 4:
            # name = "dest_{}".format(key - 2)
            # icon = "{}.png".format("dest2_mon2_press" if state else "dest2_mon2")
            font = "Roboto-Regular.ttf"
            label = "Pressed!" if state else "Dest {}".format(key - 2)
            function = "function"
        else:
            if key == 0:
                # name = "cam_{}".format(key + 1)
                # icon = "{}.png".format("cam_press" if state else "cam")
                font = "Roboto-Regular.ttf"
                label = "Pressed!" if state else "Cam {}".format(key + 1)
                function = "function"
            elif key == 1:
                # name = "cam_{}".format(key + 1)
                # icon = "{}.png".format("cam2_press" if state else "cam2")
                font = "Roboto-Regular.ttf"
                label = "Pressed!" if state else "Cam {}".format(key + 1)
                function = "function"
            elif key == 2:
                name = "cam_{}".format(key + 1)
                # icon = "{}.png".format("cam3_press" if state else "cam3")
                font = "Roboto-Regular.ttf"
                label = "Pressed!" if state else "Cam {}".format(key + 1)
                function = "function"
            else:
                name = "exit"
                # icon = "{}.png".format("Exit")
                font = "Roboto-Regular.ttf"
                label = "Bye" if state else "Exit"
                function = "function"

        return {
            "name": name,
            "icon": os.path.join(self.ASSETS_PATH, icon_filename),
            "font": os.path.join(self.ASSETS_PATH, font),
            "label": label,
            "function" : function
        }



    def update_key_image(self, deck, key, state):
        """
        Creates a new key image based on the key index, style and current key state
        and updates the image on the StreamDeck.
        :param deck:
        :param key:
        :param state:
        :return:
        """
        # Determine what icon and label to use on the generated key.
        key_style = self.get_key_style(deck, key, state)

        # Generate the custom key with the requested image and label.
        image = self.render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

        # Use a scoped-with on the deck to ensure we're the only thread using it
        # right now.
        with deck:
            # Update requested key with the generated image.
            deck.set_key_image(key, image)



    def update_key_image_from_state_change(self, deck, key, state):
        """
        Determine what icon and label to use on the generated key.
        :param deck:
        :param key:
        :param state:
        :return:
        """
        key_style = self.get_key_style(deck, key, state)
        key_style["icon"] = os.path.join(self.ASSETS_PATH, key_style["icon"].split(".")[0] + "_press" + key_style["icon"].split(".")[1])
        # Generate the custom key with the requested image and label.
        image = self.render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

        # Use a scoped-with on the deck to ensure we're the only thread using it
        # right now.
        with deck:
            # Update requested key with the generated image.
            deck.set_key_image(key, image)


    def key_change_callback(self, deck, key, state):
        """
        Prints key state change information, updates rhe key image and performs any
        associated actions when a key is pressed.
        :param deck:
        :param key:
        :param state:
        :return:
        """

        #todo put a function inside the callback function to trigger function in AJA_Kumo_HTTP_GET_REQUEST.py
        global destination

        # Print new key state
        print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

        # Update the key image based on the new key state.
        self.update_key_image(deck, key, state)

        # Check if the key is changing to the pressed state.
        if state:
            key_style = self.get_key_style(deck, key, state)

            if key_style["function"]:
                key_style["function"].launch_function()

            if key_style["name"] == "cam":
                try:
                    kumo_config_main("169.254.78.35", 1, destination)
                except NameError:
                    print("destination is not defined")
                    # kumo_config_main("169.254.78.35", 1, 1)

            elif key_style["name"] == "cam2":
                try:
                    kumo_config_main("169.254.78.35", 2, destination)
                except NameError:
                    print("destination is not defined")
                    # kumo_config_main("169.254.78.35", 2, 1)
            elif key_style["name"] == "cam3":
                try:
                    kumo_config_main("169.254.78.35", 3, destination)
                except NameError:
                    print("destination is not defined")
                    # kumo_config_main("169.254.78.35", 3, 1)
            elif key_style["name"] == "dest_mon":
                # button_dest_1.click()
                destination = 1
                print(key_style["function"])
                # print(kumo_config_main("169.254.78.35", destination))
            elif key_style["name"] == "dest_2":
                # button_dest_2.click()
                destination = 2
                # print(kumo_config_main("169.254.78.35", destination))

            # When an exit button is pressed, close the application.
            if key_style["name"] == "Exit":
                # Use a scoped-with on the deck to ensure we're the only thread
                # using it right now.
                with deck:
                    # Reset deck, clearing all button images.
                    deck.reset()

                    # Close deck handle, terminating internal worker threads.
                    deck.close()
                    # driver.close()


