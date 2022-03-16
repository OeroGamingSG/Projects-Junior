# This is the code I use for my import_folder command

from os import walk
from csv import reader
import pygame

def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for images in img_files:
            full_path = path + '/' + images
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        return surface_list

def import_set(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for images in img_files:
            full_path = path + '/' + images
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        return surface_list
