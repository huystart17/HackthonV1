from City import *


def _make_street():
    x = 809
    y = 50
    z = 600
    housewidth = 26
    numOfHouseInRow = 4
    distance = 10
    numOfRows = 10
    mc.setBlocks(x, y - 1, z, x + (housewidth + distance) * numOfHouseInRow, y - 1,
                 z + (housewidth + distance) * numOfRows,
                 35, 7)

    for i in range(numOfRows):
        for j in range(numOfHouseInRow):
            mc.setBlocks(x, y, z, x + housewidth, y, z + housewidth, 44, 0)
            mc.setBlocks(x + 2, y, z + 2, x + housewidth - 2, y, z + housewidth - 2, 0, 1)
            mc.setBlocks(x + 2, y - 1, z + 2, x + housewidth - 2, y - 1, z + housewidth - 2, 155, 1)
            x = x + housewidth + distance
        z = z + housewidth + distance
        x = 809
    z = 600
    x = 809
    for i in range(numOfRows):
        mc.setBlocks(x, y, z + 2, x + 2, z + housewidth - 2)
        z = z + housewidth + distance

def _make_street_2():
    x = 787
    y = 50
    z = 600
    housewidth = -26
    numOfHouseInRow = -4
    distance = 10
    numOfRows = 10
    mc.setBlocks(x, y - 1, z, x + (housewidth + distance) * numOfHouseInRow, y - 1,
                 z + (housewidth + distance) * numOfRows,
                 35, 7)

    for i in range(numOfRows):
        for j in range(numOfHouseInRow):
            mc.setBlocks(x, y, z, x + housewidth, y, z + housewidth, 44, 0)
            mc.setBlocks(x + 2, y, z + 2, x + housewidth - 2, y, z + housewidth - 2, 0, 1)
            mc.setBlocks(x + 2, y - 1, z + 2, x + housewidth - 2, y - 1, z + housewidth - 2, 155, 1)
            x = x + housewidth + distance
        z = z + housewidth + distance
        x = 809
    z = 600
    x = 809
    for i in range(numOfRows):
        mc.setBlocks(x, y, z + 2, x + 2, z + housewidth - 2)
        z = z + housewidth + distance
# ct.clear()
# _make_street()
# ct.load("hackv9")



