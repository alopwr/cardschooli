# coding=utf-8
"""
generating, updating and saving the card's reverse
"""
import os.path

from PIL import Image, ImageDraw, ImageFont

import cardschooli.fs_interaction


def process_coords(coords, size, psize):
    """
    centers object to be pasted on card
    :param coords: coords of the object to be pasted
    :param size: size of the we are pasting on
    :param psize: size of the object to be pasted
    :return: proper coords of the object to be pasted
    """
    if coords[0] == -1 or coords[1] == -1:
        if coords[0] == -1:
            coords[0] = int((size[0] - psize[0]) / 2)
        if coords[1] == -1:
            coords[1] = int((size[1] - psize[1]) / 2)
    return coords


class CardReverse(object):
    """
    class used to create reverse of card sized 1500x2100px with a dpi of 600
    """

    def __init__(self, project_location):
        self.project_location = project_location
        self.reverse = Image.new("RGB", (1500, 2100))
        self.reverse_draw = ImageDraw.Draw(self.reverse)
        self.save_preview()

    def save_reverse(self):
        """
        saves final reverse and deletes the preview one
        """
        self.reverse.save(cardschooli.fs_interaction.project_location(self.project_location, "reverse.png"),
                          format="PNG", dpi=(600, 600))
        try:
            os.remove(cardschooli.fs_interaction.project_location(self.project_location, "reverse_preview.png"))
        except OSError:
            pass

    def save_preview(self):
        """
        saves card's scaled reverse thubnail at project + reverse_preview.png path
        """
        tn_reverse = self.reverse.copy()
        tn_reverse.thumbnail((380, 520))
        tn_reverse.save(cardschooli.fs_interaction.project_location(self.project_location, "reverse_preview.png"),
                        format="PNG", dpi=(600, 600))

    def change_color(self, color):
        """
        updates color of the card's reverse
        :param color: new color specified in RGB
        """
        self.reverse = Image.new("RGB", (1500, 2100), color)
        self.reverse_draw = ImageDraw.Draw(self.reverse)
        self.save_preview()

    def paste(self, image, coords):
        """
        pastes image to card's reverse
        :param image: path to the image to be pasted
        :param coords: coords of the pasted image on card
        """
        image = Image.open(image).convert("RGBA")
        coords = process_coords(coords, self.reverse.size, image.size)
        self.reverse.paste(image, coords, image)
        self.save_preview()

    def add_text(self, coords, text, size, fill=0, font=os.path.join(os.pardir, "res", "fonts", "font.ttf")):
        """
        adds text to card's reverse
        :param coords: coords of the added text
        :param text: text to be added
        :param size: size of the text to be added
        :param fill: color of the text
        :param font: path to the font's ttf file
        """
        font = ImageFont.truetype(font, size)
        coords = process_coords(coords, self.reverse.size, self.reverse_draw.textsize(text, font))
        if coords[0] < 0 or coords[1] < 0:
            return 1
        self.reverse_draw.text(coords, text, fill, font)
        self.save_preview()
