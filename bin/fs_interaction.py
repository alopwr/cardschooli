# coding=utf-8
import csv
import os.path


def read_csv_line(path, num):
    """
    reads num line of csv file
    :param path: path to the csv file
    :param num: number of the line to be read
    :return: num line of the path csv
    """
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for i in range(num + 1):
            line = next(reader)
    return line


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