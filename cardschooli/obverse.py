# coding=utf-8
"""
generating, updating and saving the card"s obverse
"""
import os.path

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

import cardschooli.fs_interaction


def calculate_enters(xy_size, text, coords, font):
    text_data = text.split()

    free_x_place = xy_size[0] - coords[0]

    new_text = ""
    dlugosc_calosci = 0
    for word in text_data:
        word_leght = font.getsize(word)[0]
        if dlugosc_calosci + word_leght < free_x_place:
            new_text += word
            dlugosc_calosci += word_leght

        elif word_leght > free_x_place:
            for letter in word:
                literka_dlugosc = font.getsize(letter)[0]
                if dlugosc_calosci + literka_dlugosc < free_x_place:
                    new_text += letter
                    dlugosc_calosci += literka_dlugosc
                else:
                    new_text += "\n"
                    new_text += letter
                    dlugosc_calosci = literka_dlugosc
        else:
            new_text += "\n"
            new_text += word
            dlugosc_calosci = word_leght
        new_text += " "
        dlugosc_calosci += font.getsize(" ")[0]
    return new_text


def process_coords(coords, size, psize):
    """
    centers object to be pasted on card
    :param coords: coords of the object to be pasted
    :param size: size of the object we are pasting on
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
    addes command to the command"s file
    :param command: command to be added
    :param path: path at which command file is located
    """
    with open(path, "a") as cf:
        cf.write(command)


def generate(name, data_path, config_path):
    """ proceeds with creating obverses from config file """
    pdf = FPDF()
    obverses = [CardObverse(name, data_path, i) for i in
                range(cardschooli.fs_interaction.get_file_lenght(data_path) - 1)]
    try:
        cmds = cardschooli.fs_interaction.read_config(config_path)
    except FileNotFoundError:
        return 1
    for i in cmds:
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
            elif i[0] == "txtS":
                j.add_text_series(i[1], (i[2], i[3]), i[4], i[5], i[6], False)
    locations = [(x, y) for y in range(3) for x in range(3)]
    grid = Image.new("RGB", (4500, 6300), (255, 255, 255))
    for i, obv in enumerate(obverses):
        path = cardschooli.fs_interaction.project_location(name, "obverse{}.png".format(i))
        obv.obverse.save(path)
        img = Image.open(path)
        if i % 9 == 0 and i != 0:
            grid.save(cardschooli.fs_interaction.project_location(name, "grid{}.png".format(i)), dpi=(600, 600))
            add_grid(pdf, cardschooli.fs_interaction.project_location(name, "grid{}.png".format(i)),
                     cardschooli.fs_interaction.project_location(name, "reverse.png"))
            grid = Image.new("RGB", (4500, 6300), (255, 255, 255))
        x, y = locations[i % 9][0] * 1500, locations[i % 9][1] * 2100
        grid.paste(img, (x, y))
    if len(obverses) % 9 != 0:
        grid.save(cardschooli.fs_interaction.project_location(name, "grid{}.png".format(i)), dpi=(600, 600))
        add_grid(pdf, cardschooli.fs_interaction.project_location(name, "grid{}.png".format(i)),
                 cardschooli.fs_interaction.project_location(name, "reverse.png"))
    pdf.output(cardschooli.fs_interaction.project_location(name, "cards.pdf"))


def add_grid(pdf, grid, rev):
    pdf.add_page()
    pdf.image(grid, w=190.5, h=266.7)
    pdf.add_page()
    pdf.image(rev, w=190.5, h=266.7)


class CardObverse(object):
    """
    class used to create obverse of card sized 1500x2100px with a dpi of 600
    """

    def __init__(self, project_name, data_path, number=1):
        self.project_name = project_name
        self.config_path = cardschooli.fs_interaction.project_location(self.project_name, "obverse.cardconfig")
        self.data_path = data_path
        self.number = number

        x_size = 1500
        y_size = 2100
        self.xy_size = (x_size, y_size)

        self.obverse = Image.new("RGB", (x_size, y_size), 0)
        self.obverse_draw = ImageDraw.Draw(self.obverse)

    def save_preview(self):
        """ saves scaled preview of obverse (the first one) """
        tn_obverse = self.obverse.copy()
        tn_obverse.thumbnail((380, 520))
        tn_obverse.save(cardschooli.fs_interaction.project_location(self.project_name, "obverse_preview.png"),
                        format="PNG", dpi=(600, 600))

    def change_color(self, color, gen_cnfg=True):
        """
        updates color of the card"s obverse
        :param color: new color specified in RGB
        :param gen_cnfg: if True will save a command
        """
        self.obverse = Image.new("RGB", (1500, 2100), color)
        self.obverse_draw = ImageDraw.Draw(self.obverse)
        if gen_cnfg:
            add_command("col^^{}\n".format(color), self.config_path)

    def paste(self, image, coords, gen_cnfg=True):
        """
        pastes image to card"s obverse
        :param image: image to be pasted
        :param coords: coords of the pasted image on card
        :param gen_cnfg: if True will save a command
        """
        pimage = Image.open(image).convert("RGBA")
        coords = process_coords(coords, self.obverse.size, pimage.size)
        self.obverse.paste(pimage, coords, pimage)
        if gen_cnfg:
            add_command("img^^{}^^{}^^{}\n".format(image, coords[0], coords[1]), self.config_path)

    def add_series_of_charts(self, column_nr, coords, project, gen_cnfg=True, first=False):
        if first:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number)
        else:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number + 1)
        name = row[column_nr].strip() + "_wykres.png"
        self.paste(cardschooli.fs_interaction.project_location(project, name), coords, False)
        if gen_cnfg:
            add_command("chrt^^{}^^{}^^{}^^{}\n".format(column_nr, coords[0], coords[1], project), self.config_path)

    def add_image_folder(self, folder_path, column, coords, gen_cnfg=True, first=False):
        if first:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number)
        else:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number + 1)
        print(row)
        print(row[column])
        self.paste(os.path.join(folder_path, row[column].strip() + ".png"), coords, False)
        if gen_cnfg:
            add_command("imgf^^{}^^{}^^{}^^{}\n".format(folder_path, column, coords[0], coords[1]), self.config_path)

    def adding_chart(self, name, coords, project):
        imported = cardschooli.fs_interaction.project_location(project, name)
        self.paste(imported, coords)

    def add_text_series(self, column_nr, coords, size, fill=0,
                        font=os.path.join(os.pardir, "res", "fonts", "font.ttf"), gen_cnfg=True, first=False):
        if first:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number)
        else:
            row = cardschooli.fs_interaction.read_csv(self.data_path, self.number + 1)

        text = str(row[column_nr])

        self.add_text(coords, text, size, fill, font, False, series=True)
        if gen_cnfg:
            add_command("txtS^^{}^^{}^^{}^^{}^^{}^^{}\n".format(column_nr, coords[0], coords[1], size, fill, font),
                        self.config_path)

    def add_text(self, coords, text, size, fill=0, font=os.path.join(os.pardir, "res", "fonts", "font.ttf"),
                 gen_cnfg=True, series=False):

        """
        adds text to card"s obverse
        :param coords: coords of the added text
        :param text: text to be added
        :param size: size of the text to be added
        :param fill: color of the text
        :param font: path to the font"s ttf file
        :param gen_cnfg: if True will save a command
        """
        if gen_cnfg:
            add_command("txt^^{}^^{}^^{}^^{}^^{}^^{}\n".format(coords[0], coords[1], text, font, size, fill),
                        self.config_path)

        font = ImageFont.truetype(font, size)

        if series:
            text = calculate_enters(self.xy_size, text, coords, font)

        coords = process_coords(coords, self.obverse.size, self.obverse_draw.textsize(text, font))
        if coords[0] < 0 or coords[1] < 0:
            return 1
        self.obverse_draw.text(coords, text, fill, font)
