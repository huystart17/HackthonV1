import time

from mc import mc as mine_connect
import MinecraftStuff
import os
import json
import time

dirname = os.path.dirname(__file__)
data_folder = "structure-data"
data_root = os.path.join(dirname, data_folder)
mc = mine_connect
eneryPerSecond = 0.05


class Structure(MinecraftStuff.MinecraftShape):
    def __init__(self, mc, position, shapeBlocks=None, visible=True):
        if mine_connect:
            MinecraftStuff.MinecraftShape.__init__(self, mine_connect, position, shapeBlocks=None, visible=True)
        else:
            MinecraftStuff.MinecraftShape.__init__(self, mc, position, shapeBlocks=None, visible=True)
        self.mc = mc
        self.structData = {
            "eneryMoney": 0,
            "eneryDuration": 0,
            "lightStartTime": time.time(),
            "lightEndTime": False
        }
        self.filename = ""
        pass

    def save(self):
        data = []
        for dataRow in self.shapeBlocks:
            vec = dataRow.originalPos
            data.append([vec.x, vec.y, vec.z, dataRow.blockType, dataRow.blockData])
        filename = input("Nhập tên file")

        save_data = {
            "shapeBlocks": data,
            "structData": self.structData,
            "filename": filename
        }
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)

        f.close()
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
        pass

    def load(self, filename=False):
        if not (filename):
            filename = input("Nhập tên file bạn muốn load")
        # try:
        with open(os.path.join(data_root, "{}.json".format(filename))) as f:
            data = json.load(f)
            self.filename = filename
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
                    self.setBlock(x, y, z, blockType, blockData)
                    self.set_region(x, y, z, blockType, blockData)
                    self.save_glow_pos(x, y, z, blockType, blockData)
            else:
                print("file data không hợp lệ")
                # except:
                #     print('Không tồn tại file này')
                #     input('')
                # pass

    def introduce(self):
        pass

    def save_glow_pos(self, x, y, z, blockType, blockData):
        try:
            self.glow_pos
        except:
            self.glow_pos = []
        if blockType == 89:
            self.glow_pos.append([x, y, z])
        pass

    def turn_off_glow(self):
        try:
            print(self.glow_pos)
        except:
            self.glow_pos = []
        for pos in self.glow_pos:
            self.setBlock(pos[0], pos[1], pos[2], 1)

    def turn_on_glow(self):
        try:
            print(self.glow_pos)
        except:
            self.glow_pos = []
        for pos in self.glow_pos:
            self.setBlock(pos[0], pos[1], pos[2], 89)

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

    def is_in_structure(self, playerid):
        pos = mc.entity.getTilePos(playerid)
        x_max, x_min = self.x_max + self.position.x, self.x_min + self.position.x
        z_max, z_min = self.z_max + self.position.z, self.z_min + self.position.z
        if x_min <= pos.x <= x_max and z_min <= pos.z <= z_max:
            mc.postToChat("Co 1 nguoi trong can phong cua toi")
            return True
        else:
            return False

    def is_near_house(self):
        if self.position:
            self.introduce()

    def handle_answer(self):
        pass

    def run(self):
        pass
        # Làm tính năng thông minh
        plids = mc.getPlayerEntityIds()
        # Tính năng liên quan đến hệ thống chiếu sáng
        for plid in plids:
            if self.is_in_structure(plid):
                self.turn_on_glow()
                break
            else:
                self.turn_off_glow()

                # KHi người dùng đứng gần căn nhà thì có lời chào
                # Ngoài phần hàm run thì các bạn cần xây 1 một căn nhà đẹp

