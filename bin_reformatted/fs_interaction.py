# coding=utf-8
import os.path


def read_csv(path):
    """
    opens csv file at specified path, reads it and return its contents
    :param path: path to the .csv file
    :return: contents of the file
    """
    pass


def read_csv_line(path, num):
    pass


def project_location(name, file=None):
    """
    generates path to the cards project folder
    :param name: name of the card project
    :param file: file to append to the path
    :return: path of the card project
    """
    return os.path.join(os.pardir, 'cards', name, file) if name.isalnum() and file.isalnum() else None
