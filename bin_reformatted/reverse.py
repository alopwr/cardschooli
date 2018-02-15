# coding=utf-8
"""
generating, updating and saving the card's reverse
"""
from PIL import Image, ImageDraw

import fs_interaction
import os.path


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
    class used to create reverse of card sized 180x252px
    """

    def __init__(self, project_location):
        self.project_location = project_location
        self.reverse = Image.new("RGB", (180, 252))
        self.reverse_draw = ImageDraw.Draw(self.reverse)
        self.save_preview()

    def save_preview(self):
        """
        saves card's reverse at project + reverse.png path
        """
        self.reverse.save(fs_interaction.project_location(self.project_location, "reverse.png"))

    def change_color(self, color):
        """
        updates color of the card's reverse
        :param color: new color specified in RGB
        """
        self.reverse = Image.new("RGB", (180, 252), color)
        self.save_preview()

    def paste(self, image, coords):
        """
        pastes image to card's reverse
        :param image: image to be pasted
        :param coords: coords of the pasted image on card
        """
        coords = process_coords(coords, image.size, self.reverse.size)
        self.reverse.paste(image, coords, image)
        self.save_preview()

    def add_text(self, coords, text, fill=0, font=os.path.join(os.pardir, 'fonts', 'font.ttf')):
        """
        adds text to card's reverse
        :param coords: coords of the added text
        :param text: text to be added
        :param fill: color of the text
        :param font: path to the font's ttf file
        """
        coords = process_coords(coords, self.reverse.size, self.reverse_draw.textsize(text, font))
        self.reverse.text(coords, text, fill, font)
        self.save_preview()
