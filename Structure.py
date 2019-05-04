import turtle_tool
from MinecraftStuff import *
from mcpi.vec3 import Vec3
from turtle import *
from mc import mc
import os
from config import *
import json

dirname = os.path.dirname(__file__)
data_root = os.path.join(dirname, STRUCTURE_FOLDER)


class Structure(MinecraftShape):
    def __init__(self, position=Vec3(0, 0, 0)):
        MinecraftShape.__init__(self, mc, position)
        self.data = {}
        self.pen = Turtle()
        self.name = "No name"
        self.filename = ""
        self.x_min = 0
        self.y_min = 0
        self.z_min = 0
        self.x_max = 0
        self.y_max = 0
        self.z_max = 0

    def set_data(self, data):
        self.data = data

    def setMinMaxPos(self, x, y, z):
        self.x_max = max(self.x_max, x)
        self.y_max = max(self.y_max, y)
        self.z_max = max(self.z_max, z)
        self.x_min = min(self.x_min, x)
        self.y_min = min(self.y_min, y)
        self.z_min = min(self.z_min, z)

    def setBlocks(self, x1, y1, z1, x2, y2, z2, blockType, blockData=0, tag=""):
        super().setBlocks(x1, y1, z1, x2, y2, z2, blockType, blockData, tag="")
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        z_max = max(z1, z2)
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        z_min = min(z1, z2)
        self.x_max = max(self.x_max, x_max)
        self.y_max = max(self.y_max, y_max)
        self.z_max = max(self.z_max, z_max)
        self.x_min = min(self.x_min, x_min)
        self.y_min = min(self.y_min, y_min)
        self.z_min = min(self.z_min, z_min)

    def setBlock(self, x, y, z, blockType, blockData=0, tag=""):
        super().setBlock(x, y, z, blockType, blockData, tag)
        self.x_max = max(self.x_max, x)
        self.y_max = max(self.y_max, y)
        self.z_max = max(self.z_max, z)
        self.x_min = min(self.x_min, x)
        self.y_min = min(self.y_min, y)
        self.z_min = min(self.z_min, z)

    def _save(self, filename="", mode='normal', x1=0, y1=0, z1=0, x2=0, y2=0, z2=0,
              replace_func=lambda blockid, blockdata: [blockid, blockdata]):
        if len(filename) == 0:
            filename = input('Nhập vào tên file')
        self.filename = filename
        for block in self.shapeBlocks:
            pass
        self.data['region_border'] = [self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max, ]
        saveData = {
            "data": self.data,
            "filename": self.filename,
            "shapeBlocks": [],
        }
        print('Save in mode :', mode)
        if mode == 'normal':
            actual_pos = self.position
            x, y, z = actual_pos.x, actual_pos.y, actual_pos.z
            saveData['shapeBlocks'] = self._get_block_pos(
                x + self.x_min, y + self.y_min, z + self.z_min,
                x + self.x_max, y + self.y_max, z + self.z_max, )
        elif mode == 'quick':
            for dataRow in self.shapeBlocks:
                vec = dataRow.originalPos
                saveData['shapeBlocks'].append([vec.x, vec.y, vec.z, dataRow.blockType, dataRow.blockData])
        elif mode == 'pos':
            saveData['shapeBlocks'] = self._get_block_pos(x1, y1, z1, x2, y2, z2)
        elif mode == 'replace':
            for dataRow in self.shapeBlocks:
                vec = dataRow.originalPos
                newBlock = replace_func(dataRow.blockType, dataRow.blockData)
                saveData['shapeBlocks'].append([vec.x, vec.y, vec.z, newBlock[0], newBlock[1]])
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(saveData, f, ensure_ascii=False)
        f.close()
        print('Save ', filename, ' !ok')

    def save(self, filename=""):
        self._save(filename, 'normal')

    def save_quick(self, filename=""):
        self._save(filename, 'quick')

    def save_custom_pos(self, filename, x1, y1, z1, x2, y2, z2):
        self._save(filename, 'pos', x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2)

    def _get_block_pos(self, x1, y1, z1, x2, y2, z2):
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        z_max = max(z1, z2)
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        z_min = min(z1, z2)
        data = []
        tempBlocks = list(mc.getBlocks(x_min, y_min, z_min, x_max, y_max, z_max))
        range_y = y_max - y_min
        range_x = x_max - x_min
        range_z = z_max - z_min
        saveBlock = []
        print('Actual size: ', len(tempBlocks))
        for _y in range(range_y + 1):
            for _x in range(range_x + 1):
                for _z in range(range_z + 1):
                    index = _x * (range_z + 1) + _z + _y * ((range_x + 1) * (range_z + 1))
                    blData = tempBlocks[index]
                    if blData != 0:
                        saveBlock.append([_x, _y, _z, blData])
        count = 0
        total = len(saveBlock)
        print('Compress size:', total)
        for bl in saveBlock:
            block = mc.getBlockWithData(x_min + bl[0], y_min + bl[1], z_min + bl[2])
            data.append([bl[0], bl[1], bl[2], block.id, block.data])
            count = count + 1
            if count % 100 == 0:
                print("copy {}/{}".format(count, total))
        return data

    def load(self, filename=""):
        if len(filename) == 0:
            filename = input("Nhập tên file bạn muốn load")
        # try:
        with open(os.path.join(data_root, "{}.json".format(filename))) as f:
            data = json.load(f)
            self.filename = filename

            self.data = data.get('data', False)
            if not (self.data):
                self.data = data.get('structData', {})
            self.shapeBlocks = []
            if type(data) is dict and type(data['shapeBlocks']) is list:
                self.shapeBlocks = []
                self.visible = True
                for block in data['shapeBlocks']:
                    x = block[0]
                    y = block[1]
                    z = block[2]
                    blockType = block[3]
                    blockData = block[4]
                    self.shapeBlocks.append(ShapeBlock(x, y, z, blockType, blockData))
                    self.setMinMaxPos(x, y, z)
                print("Đã load data thành công")
                self.redraw()
                self._move(self.position.x, self.position.y, self.position.z)
            else:
                print("file data không hợp lệ")

    def replace_blocks(self, filename, replace_func):
        self._save(filename, 'replace', replace_func=replace_func)

    def draw_region(self, text="", fill=True, fill_color='yellow'):
        pen = self.pen
        if len(text) == 0:
            text = self.name
        pen.speed(0)
        x, y, z = self.position
        try:
            if fill:
                turtle_tool.draw_square_fill_two_point(pen, x + self.x_max, z + self.z_max, x + self.x_min,
                                                       z + self.z_min,
                                                       text, fill_color)
            else:
                turtle_tool.draw_square_two_point(pen, x + self.x_max, z + self.z_max, x + self.x_min, z + self.z_min,
                                                  text)

        except:
            print("ok")


# st = Structure(Vec3(-62, 142, -341))
# # st.save_custom_pos('QH_HOTEL',97,100,-19,135,66,-47)
# # st.load('QH_HOUSE')
# # st.clear()
# st.load('QH_HOTEL')
#
#
# # st.clear()
def convert(id, data):
    if id == 160 or id == 102:
        return [95, data]
    else:
        return [id, data]


#
#
# st.replace_blocks('QH_HOTEL_2', replace_func=convert)
# st.clear()
# st.load('QH_HOTEL_2')


# st = Structure(Vec3(-1862,140,117))
# # st.save_custom_pos('QH_FACTORY', 54,66,131,148,100,22)
# st.replace_blocks('QH_HOTEL_3', replace_func=convert)



# external code tool
def save_villa():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_VILLA_2', -1584, 68, 42, -1623, 80, 81)
    stx.replace_blocks('QH_VILLA_2', replace_func=convert)


def save_villa_negative_X():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_VILLA_FACE_X_NEG', -1664, 67, 81, -1623, 80, 42)
    # stx.replace_blocks('QH_VILLA_2', replace_func=convert)


def save_hotel_4():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_HOTEL_4', -697, 67, -947, -688, 97, -968)


def save_hotel_3():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_HOTEL_3', -1768, 68, 377, -1818, 122, 437)


def save_hotel_5():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_HOTEL_5', -664, 67, -111, -121, 100, -88)

def save_villa():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('QH_VILLA', 317, 0, 317, 356, 16, 356)
def mc_donan():
    stx = Structure(Vec3(0, 0, 140))
    stx.save_custom_pos('DH_MCDONAN',208, 3, 389, 183, 19, 410)

# mc_donan()