from MinecraftStuff import *
from mcpi.vec3 import Vec3
from turtle import *
from mc import mc
import os
from config import *
import json

StreetData = []


def street_line_x(position, length):
    street = MinecraftShape(mc, position)
    street.setBlocks(0, 0, 0, length, 0, 16, 35, 15)
    street.setBlocks(0, 1, 0, length, 1, 16, 44)
    street.setBlocks(0, 1, 4, length, 1, 12, 0)

    StreetData.append({
        'func': 'street_line_x',
        'position': [position.x, position.y, position.z],
        'length': length
    })


def street_line_z(position, length):
    street = MinecraftShape(mc, position)
    street.setBlocks(0, 0, 0, 16, 0, length, 35, 15)
    street.setBlocks(0, 1, 0, 16, 1, length, 44)
    street.setBlocks(4, 1, 4, 12, 1, length, 0)
    StreetData.append({
        'func': 'street_line_z',
        'position': [position.x, position.y, position.z],
        'length': length
    })


def street_intersect(position):
    street = MinecraftShape(mc, position)
    # xây đường
    street.setBlocks(0, 0, 0, 16, 0, 16, 35, 15)
    # xây hè phố
    street.setBlocks(0, 1, 0, 16, 1, 16, 0, )
    street.setBlocks(0, 1, 0, 3, 1, 3, 44)
    street.setBlocks(13, 1, 0, 16, 1, 3, 44)
    street.setBlocks(0, 1, 13, 3, 1, 16, 44)
    street.setBlocks(13, 1, 13, 16, 1, 16, 44)
    # street.setBlocks(16, 1, 16, 12, 1, 12, 44)
    # street.setBlocks(16, 1, 16, 12, 1, 12, 35, 14)

    StreetData.append({
        'func': 'street_intersect',
        'position': [position.x, position.y, position.z],

    })
