import time

from mc import mc as mine_connect
import MinecraftStuff
import os
import json
import time
import turtle
import turtle_tool
from turtle import Screen

dirname = os.path.dirname(__file__)
data_folder = "structure-data"
data_root = os.path.join(dirname, data_folder)
mc = mine_connect


class Structure(MinecraftStuff.MinecraftShape):
    def __init__(self, mc, position, shapeBlocks=None, visible=True):
        if mine_connect:
            MinecraftStuff.MinecraftShape.__init__(self, mine_connect, position, shapeBlocks=None, visible=True)
        else:
            MinecraftStuff.MinecraftShape.__init__(self, mc, position, shapeBlocks=None, visible=True)
        self.mc = mc
        self.structData = {
            "Energy consume : ": 0,
            "Storage volume of Energy": 10,
            "Produce * enery/second": 10,
            "Number of Light": 0,
            "====Info====": "",
            "Type": "house",  # Có mấy loại structure như sau  house |vehicle |
            "Description": "ook",

            "====State====": "",
            # "Number of light turn on": "",
            "People in house": "",
            "Light is on": False,

        }
        self.pen = turtle.Turtle()
        self.name = "...."
        self.current_function = ""
        self.filename = ""
        self.auto = False
        self.auto_done = {}
        pass

    def save(self, filename=False):
        data = []
        for dataRow in self.shapeBlocks:
            vec = dataRow.originalPos
            data.append([vec.x, vec.y, vec.z, dataRow.blockType, dataRow.blockData])
        if not filename:
            filename = input("Nhập tên file")

        save_data = {
            "shapeBlocks": data,
            "structData": self.structData,
            "filename": filename
        }
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)
        f.close()
        self.filename = filename
        pass

    def save_full(self):
        data = []
        filename = input("Nhập tên file")
        total = len(self.shapeBlocks)
        self.turn_on_glow()
        count = 0
        for dataRow in self.shapeBlocks:
            vec = dataRow.originalPos
            vec_actual = dataRow.actualPos
            block = mine_connect.getBlockWithData(vec_actual.x, vec_actual.y, vec_actual.z)
            data.append([vec.x, vec.y, vec.z, block.id, block.data])
            count = count + 1
            print("copy {}/{}".format(count, total))
        save_data = {
            "shapeBlocks": data,
            "position": {
                "x": self.position.x, "y": self.position.y, "z": self.position.z
            },
            "structData": self.structData
        }

        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)
        f.close()
        self.filename = filename
        pass

    def save_from_pos(self, x1, y1, z1, x2, y2, z2, filename=False):
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        z_max = max(z1, z2)
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        z_min = min(z1, z2)
        data = []
        if not (filename):
            filename = input("Nhập tên file")
        total = (x_max - x_min + 1) * (z_max - z_min + 1) * (y_max - y_min + 1)
        tempBlocks = list(mine_connect.getBlocks(x_min, y_min, z_min, x_max, y_max, z_max))
        range_y = y_max - y_min
        range_x = x_max - x_min
        range_z = z_max - z_min
        saveBlock = []
        for _y in range(range_y + 1):
            for _x in range(range_x + 1):
                for _z in range(range_z + 1):
                    index = _x * (range_z + 1) + _z + _y * ((range_x + 1) * (range_z + 1))
                    blData = tempBlocks[index]
                    if blData != 0:
                        saveBlock.append([_x, _y, _z, blData])
        count = 0
        total = len(saveBlock)
        for bl in saveBlock:
            block = mine_connect.getBlockWithData(x_min + bl[0], y_min + bl[1], z_min + bl[2])
            print(bl[0], bl[1], bl[2])
            data.append([bl[0], bl[1], bl[2], block.id, block.data])
            count = count + 1
            print("copy {}/{}".format(count, total))

        # for x in range(x_min, x_max +1):
        #     for y in range(y_min, y_max + 1):
        #         for z in range(z_min, z_max + 1):
        #             block = mine_connect.getBlockWithData(x, y, z)
        #             data.append([x -x_min, y-y_min, z - z_min, block.id, block.data])
        #             count = count + 1
        #             print("copy {}/{}".format(count, total))

        save_data = {
            "shapeBlocks": data,
            "position": {
                "x": x_min, "y": y_min, "z": z_min
            },
            "structData": self.structData
        }

        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)
        f.close()
        self.filename = filename
        pass

    def compress_and_save(self, filename):
        data = []
        for dataRow in self.shapeBlocks:
            vec = dataRow.originalPos
            if dataRow.blockType == 0:
                continue
            data.append([vec.x, vec.y, vec.z, dataRow.blockType, dataRow.blockData])
        if not filename:
            filename = input("Nhập tên file")

        save_data = {
            "shapeBlocks": data,
            "structData": self.structData,
            "filename": filename
        }
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)
        f.close()
        self.filename = filename
        pass

        pass

    def load(self, filename=False):
        if not filename:
            filename = input("Nhập tên file bạn muốn load")
        # try:
        with open(os.path.join(data_root, "{}.json".format(filename))) as f:
            data = json.load(f)
            self.filename = filename
            self.shapeBlocks = []
            if type(data) is dict and type(data['shapeBlocks']) is list:
                self.shapeBlocks = []
                # self.clear()
                self.visible = True
                for block in data['shapeBlocks']:
                    x = block[0]
                    y = block[1]
                    z = block[2]
                    blockType = block[3]
                    blockData = block[4]
                    self.shapeBlocks.append(MinecraftStuff.ShapeBlock(x, y, z, blockType, blockData))
                    # self.setBlock(x, y, z, blockType, blockData)
                    self.set_region(x, y, z, blockType, blockData)
                    self.save_glow_pos(x, y, z, blockType, blockData)
                print("Đã load data thành công")
                self.redraw()
                self._move(self.position.x, self.position.y, self.position.z)
            else:
                print("file data không hợp lệ")
                # except:
                #     print('Không tồn tại file này')
                #     input('')
                # pass
            self.draw_region(filename)

    def setIntroduce(self):
        pass

    def set_name(self, text=""):
        self.name = text

    def introduce(self):
        mc.postToChat("Hello. this is a city structure")
        pass

    def save_glow_pos(self, x, y, z, blockType, blockData):
        try:
            self.glow_pos
        except:
            self.glow_pos = []
        if blockType == 89:
            self.glow_pos.append([x, y, z])
        self.structData['Number of Light'] = len(self.glow_pos)
        self.structData['Light is on'] = False
        pass

    def turn_off_glow(self):
        self.pen.color('black')
        self.pen.clear()
        self.draw_region(self.name, )
        try:
            print(self.glow_pos)
        except:
            self.glow_pos = []
        for pos in self.glow_pos:
            self.setBlock(pos[0], pos[1], pos[2], 1)
        self.structData['Light is on'] = False

    def turn_on_glow(self):
        try:
            print(self.glow_pos)
        except:
            self.glow_pos = []
        for pos in self.glow_pos:
            self.setBlock(pos[0], pos[1], pos[2], 89)

        # self.pen.color('yellow')
        self.draw_region(self.name, fill=True)
        self.structData['Light is on'] = True

    def set_region(self, x, y, z, blockType, blockData):
        try:
            if self.x_max and self.y_max and self.z_max and self.x_min and self.y_min and self.z_min:
                pass
        except:
            self.x_max = x
            self.y_max = y
            self.z_max = z
            self.x_min = x
            self.y_min = y
            self.z_min = z
        if self.x_max < x:
            self.x_max = x
        if self.y_max < y:
            self.y_max = y
        if self.z_max < z:
            self.z_max = z
        if self.x_min > x:
            self.x_min = x
        if self.y_min > y:
            self.y_min = y
        if self.z_min > z:
            self.z_min = z

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

    def is_in_turtle_region(self, x_turtle, y_turtle):
        x, y, z = self.position
        return turtle_tool.is_in_region(x_turtle, y_turtle, x + self.x_max, z + self.z_max, x + self.x_min,
                                        z + self.z_min)

    def is_in_structure(self, playerid):
        pos = mc.entity.getTilePos(playerid)
        x_max, x_min = self.x_max + self.position.x, self.x_min + self.position.x
        z_max, z_min = self.z_max + self.position.z, self.z_min + self.position.z
        if x_min <= pos.x <= x_max and z_min <= pos.z <= z_max:
            return True
        else:
            return False

    def is_near_structure(self, playerid):
        pos = mc.entity.getTilePos(playerid)
        x_max, x_min = self.x_max + self.position.x, self.x_min + self.position.x
        z_max, z_min = self.z_max + self.position.z, self.z_min + self.position.z
        if x_min <= pos.x <= x_max and z_min <= pos.z <= z_max:
            mc.postToChat("Co 1 nguoi trong can phong cua toi")
            return True
        else:
            return False

    def check_pos_near_structure(self, x, y, z):
        x_max, x_min = self.x_max + self.position.x + 5, self.x_min + self.position.x - 5
        z_max, z_min = self.z_max + self.position.z + 5, self.z_min + self.position.z - 5
        if x_min <= x <= x_max and z_min <= z <= z_max:
            return True
        else:
            return False

    # Các hàm liên quan đến điện năng thành phố
    def produce_energy(self):
        self.structData["Storage volume of Energy"] = self.structData["Storage volume of Energy"] + self.structData[
            'Produce * enery/second']
        pass


    def auto_light_on(self, plids=[]):
        pass
        # Làm tính năng thông minh
        # Tính năng liên quan đến hệ thống chiếu sáng
        for plid in plids:
            if self.is_in_structure(plid):
                self.turn_on_glow()
                break
            else:
                self.turn_off_glow()

                # KHi người dùng đứng gần căn nhà thì có lời chào
                # Ngoài phần hàm run thì các bạn cần xây 1 một căn nhà đẹp

    def run_per_second(self, data):
        if isinstance(data, dict):
            plids = data.get('plids', [])
            pl_positions = data.get('pl_positions', {})
            if isinstance(data['pl_positions'], dict):
                for plid in pl_positions:
                    plpos = pl_positions[plid]
                    if self.check_pos_near_structure(plpos[0], plpos[1], plpos[2]):
                        self.auto_light_on(plids=plids)
                        pass

        if self.current_function == "1":
            #fly :
            self.move(796,51,660)
            self.rotateBy(-90,0,0)
            self.pen.clear()
            self.draw_region('Start...',True)
            self.current_function = '0'
            pass
        if self.current_function == "2":
            self.structData["Storage volume of Energy"] = 60000
            pass
        if self.current_function == "3":
            self.moveBy(0, 0, 20)
            self.pen.clear()
            self.structData["Storage volume of Energy"] -=60
            if self.position.z > 950:
                self.draw_region('Flying...', True)
                if self.position.z > 1200:
                    self.pen.clear()
                    self.clear()
                    self.current_function = '0'
            else:
                self.draw_region('Moving...', True)
        if self.current_function == "4":
            self.move(870,51,660)
            self.pen.clear()
            self.draw_region('Parking...', True)
            self.current_function = '0'
            pass
        if self.current_function == "5":
            self.move(870, 51, 770)
            self.pen.clear()
            self.draw_region('Parking...', True)
            self.current_function = '0'
            pass
        if self.current_function == "6":
            self.move(870, 51, 880)
            self.pen.clear()
            self.draw_region('Parking...', True)
            self.current_function = '0'
            pass
        if self.current_function == "7":
            self.auto = True
            pass
        if self.current_function == "x":
            self.pen.clear()
            self.clear()
            pass

            pass
        if self.auto == True:
            if not (self.auto_done.get('1', False)):
                self.current_function = '1'
                self.auto_done['1'] = True
                return True
            if self.auto_done.get('1', False) and not (self.auto_done.get('2', False)):
                self.current_function = '2'
                self.auto_done['2'] = True
                return True
            if self.auto_done.get('1', False) and self.auto_done.get('2', False) and not (
            self.auto_done.get('3', False)):
                self.current_function = '3'
                self.auto_done['3'] = True
                return True

    def action_persec(self, function_name):
        self.current_function = function_name
        pass
