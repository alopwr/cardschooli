# coding=utf-8
"""
generating, updating and saving the card's obverse
"""
import os.path

from PIL import Image, ImageDraw, ImageFont

import fs_interaction


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


def add_command(command, path):
    """
    addes command to the command's file
    :param command: command to be added
    :param path: path at which command file is located
    """
    with open(path, "a") as cf:
        cf.write(command)


def generate(name, data_path, config_path):
    """ proceeds with creating obverses from config file """
    obverses = [CardObverse(name, data_path, i) for i in range(fs_interaction.get_file_lenght(data_path) - 1)]
    cmds = fs_interaction.read_config(config_path)
    for i in cmds:
        print(i)
        for j in obverses:
            if i[0] == "col":
                j.change_color(i[1], False)
            elif i[0] == "img":
                j.paste(i[1], (i[2], i[3]), False)
            elif i[0] == "imgf":
                j.add_image_folder(i[1], i[2], (i[3], i[4]), False)
            elif i[0] == "txt":
                j.add_text((i[1], i[2]), i[3], i[5], i[6], i[4], False)
            elif i[0] == "chrt":
                j.add_series_of_charts(i[1], (i[2], i[3]), i[4], False)
    for i, obv in enumerate(obverses):
        obv.obverse.save(fs_interaction.project_location(name, "obverse{}.png".format(i)))


def get_numb_rows(name, filename):
    obverses = [CardObverse(name, filename, i) for i in range(fs_interaction.get_file_lenght(filename) - 1)]

    return len(obverses)


class CardObverse(object):
    """
    class used to create obverse of card sized 1500x2100px with a dpi of 600
    """

    def __init__(self, project_name, data_path, number=1):
        self.project_name = project_name
        self.config_path = fs_interaction.project_location(self.project_name, "obverse.cardconfig")
        self.data_path = data_path
        self.number = number
        self.obverse = Image.new("RGB", (1500, 2100), 0)
        self.obverse_draw = ImageDraw.Draw(self.obverse)

    def save_preview(self):
        """ saves scaled preview of obverse (the first one) """
        tn_obverse = self.obverse.copy()
        tn_obverse.thumbnail((380, 520))
        tn_obverse.save(fs_interaction.project_location(self.project_name, "obverse_preview.png"),
                        format="PNG", dpi=(600, 600))

    def change_color(self, color, gen_cnfg=True):
        """
        updates color of the card's obverse
        :param color: new color specified in RGB
        :param gen_cnfg: if True will save a command
        """
        self.obverse = Image.new("RGB", (1500, 2100), color)
        self.obverse_draw = ImageDraw.Draw(self.obverse)
        if gen_cnfg:
            add_command("col^^{}\n".format(color), self.config_path)

    def paste(self, image, coords, gen_cnfg=True):
        """
        pastes image to card's obverse
        :param image: image to be pasted
        :param coords: coords of the pasted image on card
        :param gen_cnfg: if True will save a command
        """
        pimage = Image.open(image).convert("RGBA")
        coords = process_coords(coords, self.obverse.size, pimage.size)
        self.obverse.paste(pimage, coords, pimage)
        if gen_cnfg:
            add_command("img^^{}^^{}^^{}\n".format(image, coords[0], coords[1]), self.config_path)

    def add_series_of_charts(self, column_nr, coords, project, gen_cnfg=True):
        row = fs_interaction.read_csv_line(self.data_path, self.number)
        name = row[column_nr].strip() + "_wykres.png"
        self.paste(os.path.join(os.pardir, "cards", project, name), coords, False)
        if gen_cnfg:
            add_command("chrt^^{}^^{}^^{}^^{}\n".format(column_nr, coords[0], coords[1], project), self.config_path)

    def add_image_folder(self, folder_path, column, coords, gen_cnfg=True):
        row = fs_interaction.read_csv_line(self.data_path, self.number)
        self.paste(os.path.join(folder_path, row[column] + ".png"), coords, False)
        if gen_cnfg:
            add_command("imgf^^{}^^{}^^{}^^{}".format(folder_path, column, coords[0], coords[1]), self.config_path)

    def adding_chart(self, name, coords, project):
        imported = fs_interaction.project_location(project, name)
        self.paste(imported, coords)
    def add_text(self, coords, text, size, fill=0, font=os.path.join(os.pardir, "res", "fonts", "font.ttf"),
                 gen_cnfg=True):
        """
        adds text to card's obverse
        :param coords: coords of the added text
        :param text: text to be added
        :param size: size of the text to be added
        :param fill: color of the text
        :param font: path to the font's ttf file
        :param gen_cnfg: if True will save a command
        """
        if gen_cnfg:
            add_command("txt^^{}^^{}^^{}^^{}^^{}^^{}\n".format(coords[0], coords[1], text, font, size, fill),
                        self.config_path)
        font = ImageFont.truetype(font, size)
        coords = process_coords(coords, self.obverse.size, self.obverse_draw.textsize(text, font))
        if coords[0] < 0 or coords[1] < 0:
            return 1
        self.obverse_draw.text(coords, text, fill, font)