# coding=utf-8
import csv
import os.path


def read_csv(path, *line_num):
    """
    reads num line of csv file
    :param path: path to the csv file
    :param line_num: number of the line to be read, if empty, returns full file
    :return: num line of the path csv
    """
    with open(path, newline="") as f:
        reader = csv.reader(f)
        if line_num:
            for i in range(line_num[0] + 1):
                line = next(reader)
            return line
        else:
            return list(reader)


def get_file_lenght(path):
    """ gets lenght of a file """
    with open(path) as f:
        return len(f.readlines())


def project_location(name, fname=None):
    """
    generates path to the cards project folder
    :param name: name of the card project
    :param fname: file to append to the path
    :return: path of the card project
    """
    if not os.path.isdir(os.path.join(os.pardir, "cards", name)):
        os.makedirs(os.path.join(os.pardir, "cards", name))
    if fname:
        return os.path.join(os.pardir, "cards", name, fname) if name.isalnum() else None
    return os.path.join(os.pardir, "cards", name) if name.isalnum() else None


def read_config(path):
    """
    reads config
    :param path: path to the config
    :return: config converted to list
    """
    commands = []
    with open(path) as f:
        for i in f.readlines():
            i = i[:-1].split("^^")
            for j in range(len(i)):
                try:
                    i[j] = int(i[j])
                except ValueError:
                    pass
            commands.append(i)
    return commands


def clean_files(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            if name.endswith("wykres.png") or name.endswith(
                    "wykresOLD.png") or name == "obverse_preview.png" or name.endswith(".cardconfig"):
                os.remove(os.path.join(root, name))
