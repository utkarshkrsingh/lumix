import toga
from toga.style.pack import COLUMN, ROW, Pack
from travertino.constants import CENTER

from lumix.custom_colors import *

class lumix(toga.App):
    def startup(self):

        ## TOTAL LAYOUT ####################################################################################       
        main_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    background_color=crust
                    )
                )

        ## Creating Menu Bar 
        menu_bar = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    flex=1,
                    background_color=crust,
                    horizontal_align_items=CENTER,
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
                    background_color=mantle,
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
        self.open_button = toga.Button(
                "Open File",
                on_press = self.open_file,
                style=Pack(
                    background_color=surface,
                    flex=1,
                    color=text
                    )
                )
        menu_bar.add(self.open_button)
        ####################################################################################################

        ## OPTION SECTION ##################################################################################
        option_label = toga.Label(
                "O\nP\nT\nI\nO\nN\n\nH\nE\nR\nE\n",
                style=Pack(
                    text_align=CENTER,
                    color=text,
                    )
                )
        option_box.add(option_label)
        ####################################################################################################

        ## IMAGE PREVIEW ###################################################################################
        my_Image = toga.Image("./resources/lumix.png")
        self.image_preview = toga.ImageView(
                my_Image,
                style=Pack(
                    flex=1
                    )
                )
        image_preview_box.add(self.image_preview)
        ####################################################################################################

        ## CONTROL PANEL ###################################################################################
        control_label = toga.Label(
                "CONTROL HERE",
                style=Pack(
                    flex=1,
                    text_align=CENTER,
                    color=text
                    )
                )
        control_box.add(control_label)
        ####################################################################################################

        self.main_window = toga.Window(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def open_file(self, widget):
        file_path = await self.main_window.open_file_dialog(
                title="Select Image File"
                )
        if file_path:
            print(file_path)
            my_image = toga.Image(file_path)
            self.image_preview.image = my_image


def main():
    return lumix("Lumix", icon="./resources/lumix.png")
