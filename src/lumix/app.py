import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from PIL import Image, ImageEnhance, ImageFilter
import io


class ImageEditorApp(toga.App):
    def startup(self):
        self.original_image = None
        self.edited_image = None

        # === Controls Section (Left panel) ===
        self.control_box = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))

        # Load, Reset, Export Buttons
        button_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        load_button = toga.Button("📂 Load", on_press=self.load_image, style=Pack(padding_right=5, flex=1))
        reset_button = toga.Button("🔄 Reset", on_press=self.reset_image, style=Pack(padding_right=5, flex=1))
        export_button = toga.Button("💾 Export", on_press=self.export_image, style=Pack(flex=1))
        button_box.add(load_button)
        button_box.add(reset_button)
        button_box.add(export_button)

        self.control_box.add(button_box)

        # Sliders with Labels
        def add_slider(label, slider):
            self.control_box.add(toga.Label(label, style=Pack(padding_top=5)))
            self.control_box.add(slider)

        self.brightness_slider = toga.Slider(min=0.1, max=2.0, value=1.0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.contrast_slider = toga.Slider(min=0.1, max=2.0, value=1.0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.red_slider = toga.Slider(min=0.0, max=2.0, value=1.0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.green_slider = toga.Slider(min=0.0, max=2.0, value=1.0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.blue_slider = toga.Slider(min=0.0, max=2.0, value=1.0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.blur_slider = toga.Slider(min=0.0, max=10.0, value=0.0, on_change=self.update_image, style=Pack(padding_bottom=5))

        add_slider("🌞 Brightness", self.brightness_slider)
        add_slider("🌓 Contrast", self.contrast_slider)
        add_slider("🔴 Red", self.red_slider)
        add_slider("🟢 Green", self.green_slider)
        add_slider("🔵 Blue", self.blue_slider)
        add_slider("🌫️ Gaussian Blur", self.blur_slider)

        # Cropping sliders (percent based)
        self.crop_left = toga.Slider(min=0, max=50, value=0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.crop_right = toga.Slider(min=0, max=50, value=0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.crop_top = toga.Slider(min=0, max=50, value=0, on_change=self.update_image, style=Pack(padding_bottom=5))
        self.crop_bottom = toga.Slider(min=0, max=50, value=0, on_change=self.update_image, style=Pack(padding_bottom=5))

        add_slider("⬅️ Crop Left (%)", self.crop_left)
        add_slider("➡️ Crop Right (%)", self.crop_right)
        add_slider("⬆️ Crop Top (%)", self.crop_top)
        add_slider("⬇️ Crop Bottom (%)", self.crop_bottom)

        # === Image Display (Right panel) ===
        self.image_view = toga.ImageView(style=Pack(height=500, flex=3, padding=10))

        # === Main layout ===
        main_content = toga.Box(style=Pack(direction=ROW))
        main_content.add(self.control_box)
        main_content.add(self.image_view)

        self.main_window = toga.MainWindow(title="🖼️ Lumix Image Editor")
        self.main_window.content = main_content
        self.main_window.show()

    async def load_image(self, widget):
        dialog = toga.OpenFileDialog("Choose an image", multiple_select=False)
        path = await self.main_window.dialog(dialog)

        if path:
            self.original_image = Image.open(path).convert("RGB")
            self.reset_sliders()
            self.update_image()

    def update_image(self, widget=None):
        if not self.original_image:
            return

        image = self.original_image.copy()

        # Cropping
        width, height = image.size
        left_crop = int((self.crop_left.value / 100) * width)
        right_crop = int((self.crop_right.value / 100) * width)
        top_crop = int((self.crop_top.value / 100) * height)
        bottom_crop = int((self.crop_bottom.value / 100) * height)

        new_left = left_crop
        new_upper = top_crop
        new_right = width - right_crop
        new_lower = height - bottom_crop

        if new_right > new_left and new_lower > new_upper:
            image = image.crop((new_left, new_upper, new_right, new_lower))

        # Enhancements
        image = ImageEnhance.Brightness(image).enhance(self.brightness_slider.value)
        image = ImageEnhance.Contrast(image).enhance(self.contrast_slider.value)

        # RGB adjustment
        r, g, b = image.split()
        r = r.point(lambda i: max(0, min(255, int(i * self.red_slider.value))))
        g = g.point(lambda i: max(0, min(255, int(i * self.green_slider.value))))
        b = b.point(lambda i: max(0, min(255, int(i * self.blue_slider.value))))
        image = Image.merge("RGB", (r, g, b))

        # Blur
        if self.blur_slider.value > 0:
            image = image.filter(ImageFilter.GaussianBlur(radius=self.blur_slider.value))

        # Show in ImageView
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            self.image_view.image = toga.Image(data=output.getvalue())

        self.edited_image = image

    def reset_sliders(self):
        self.brightness_slider.value = 1.0
        self.contrast_slider.value = 1.0
        self.red_slider.value = 1.0
        self.green_slider.value = 1.0
        self.blue_slider.value = 1.0
        self.blur_slider.value = 0.0
        self.crop_left.value = 0
        self.crop_right.value = 0
        self.crop_top.value = 0
        self.crop_bottom.value = 0

    def reset_image(self, widget=None):
        if self.original_image:
            self.reset_sliders()
            self.update_image()

    async def export_image(self, widget):
        if not self.edited_image:
            return

        dialog = toga.SaveFileDialog("Save Edited Image", suggested_filename="edited_image.png")
        path = await self.main_window.dialog(dialog)

        if path:
            self.edited_image.save(path, format="PNG")


def main():
    return ImageEditorApp("Lumix", "org.example.lumix")
