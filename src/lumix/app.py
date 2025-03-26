import toga
from toga.style.pack import COLUMN, ROW, Pack
from toga.colors import color
from travertino.constants import CENTER

from lumix.custom_colors import *

class lumix(toga.App):
    def startup(self):

        ## TOTAL LAYOUT ####################################################################################       
        main_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    )
                )

        ## Creating Menu Bar 
        menu_bar = toga.Box(
                style=Pack(
                    direction=ROW,
                    flex=1,
                    background_color=color(crust),
                    vertical_align_items=CENTER
                    )
                )
        main_box.add(menu_bar)
        
        ## Creating Horizontal Box for layout
        hbox = toga.Box(
                style=Pack(
                    direction=ROW,
                    flex=19
                    )
                )
        main_box.add(hbox)

        ## Creating Option Box
        option_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    flex = 1,
                    background_color=color(mantle),
                    vertical_align_items=CENTER,
                    horizontal_align_content=CENTER
                    )
                )
        hbox.add(option_box)
        
        ## Creating Vertical Box for layout
        vbox = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    flex = 19
                    )
                )
        hbox.add(vbox)

        ## Creating Image Preview 
        image_preview_box = toga.Box(
                style=Pack(
                    flex=15,
                    background_color=surface,
                    vertical_align_items=CENTER
                    )
                )
        vbox.add(image_preview_box)

        ## Creating Control Box
        control_box = toga.Box(
                style=Pack(
                    flex=4,
                    background_color=base,
                    vertical_align_items=CENTER
                    )
                )
        vbox.add(control_box)
        ####################################################################################################
        
        ## MENU SECTION ####################################################################################
        menu_label = toga.Label(
                "MENU HERE",
                style=Pack(
                    flex=1,
                    text_align=CENTER,
                    color=color(text)
                    )
                )
        menu_bar.add(menu_label)
        ####################################################################################################

        ## OPTION SECTION ##################################################################################
        option_label = toga.Label(
                "O\nP\nT\nI\nO\nN\n\nH\nE\nR\nE\n",
                style=Pack(
                    text_align=CENTER,
                    color=color(text),
                    )
                )
        option_box.add(option_label)
        ####################################################################################################

        ## IMAGE PREVIEW ###################################################################################
        image_preview_label = toga.Label(
                "IMAGE PREVIEW",
                style=Pack(
                    flex=1,
                    text_align=CENTER,
                    color=color(text)
                    )
                )
        image_preview_box.add(image_preview_label)
        ####################################################################################################

        ## CONTROL PANEL ###################################################################################
        control_label = toga.Label(
                "CONTROL HERE",
                style=Pack(
                    flex=1,
                    text_align=CENTER,
                    color=color(text)
                    )
                )
        control_box.add(control_label)
        ####################################################################################################

        self.main_window = toga.Window(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return lumix("Lumix", icon="./resources/lumix.png")
