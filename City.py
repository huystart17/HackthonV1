from mc import mc
import os
import json
from mcpi import vec3
from mcpi import block
import time
import Structure

dirname = os.path.dirname(__file__)
data_folder = "city-data"
data_root = os.path.join(dirname, data_folder)


class City:
    """
    Đây là class giúp lưu lại các thông tin của thành phố qua đó sử dụng các công trình và làm việc
    """

    def __init__(self):
        self.structuresData = []
        self.structuresInstance = []
        self.currentIndex = None
        self.current = None
        self.startPoint = {
            'x': 600,
            'y': 50,
            'z': 600
        }
        self.endPoint = {
            'x': 1000,
            'y': 50,
            'z': 1000
        }
        self.cityGroundBlock = 1
        self.cityHeight = 50
        self.cityGroundData = 1

        pass

    def clear(self):
        # Đặt đất nền
        mc.setBlocks(
            self.startPoint['x'],
            self.startPoint['y'] - 2,
            self.startPoint['z'],
            self.endPoint['x'],
            self.endPoint['y'],
            self.endPoint['z'],
            self.cityGroundBlock,
            self.cityGroundData
        )
        mc.postToChat("We have ground")

        # clear không gian

        mc.setBlocks(
            self.startPoint['x'],
            self.startPoint['y'],
            self.startPoint['z'],
            self.endPoint['x'],
            self.endPoint['y'] + self.cityHeight,
            self.endPoint['z'],
            block.AIR
        )
        mc.postToChat("We have air")

        for id in mc.getPlayerEntityIds():
            mc.entity.setPos(id, self.startPoint['x'],
                             self.startPoint['y'] + 1,
                             self.startPoint['z'], )

        pass

    def show_struct(self):
        try:
            structures = self.structuresData
            for i in range(len(structures)):
                tempst = structures[i]
                print("{}. {} || {}".format(i, tempst.get('filename', ''), tempst.get('note', '')))
        except:
            print('Có lỗi với dữ liệu thành phố')
        pass

    def add_struct(self, x=False, y=False, z=False):
        if not (type(x) is int and type(y) is int and type(z) is int):
            print("bạn hãy nhập vị trí của bạn vào vị trí bạn muốn đặt công trình")
            x = input('x = ')
            y = input('y = ')
            z = input('z = ')

        instance = Structure.Structure(mc, vec3.Vec3(int(x), int(y), int(z)))
        self.current = instance

        note = input("Hãy nhập vào ghi chú của bạn về công trình này")
        self.structuresInstance.append(instance)
        self.currentIndex = len(self.structuresInstance) - 1
        self.structuresData.append({
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "note": note,
            "filename": instance.filename
        })
        return instance
        pass

    def save_struct(self, cIndex=None):
        if cIndex == None:
            cIndex = int(input('Nhập vào số thứ tự công trình muốn lưu'))
        cIndex = self.currentIndex
        instance = self.structuresInstance[cIndex]
        self.structuresData[cIndex] = {
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "note": self.structuresData[cIndex]['note'],
            "filename": instance.filename
        }
        pass

    def save_all(self):
        for cIndex in range(len(self.structuresData)):
            instance = self.structuresInstance[cIndex]
            self.structuresData[cIndex] = {
                "position": {
                    "x": instance.position.x,
                    "y": instance.position.y,
                    "z": instance.position.z,
                },
                "note": self.structuresData[cIndex]['note'],
                "filename": instance.filename
            }
        self.save()

    def remove_struct(self, cIndex=None):
        if cIndex == None:
            cIndex = int(input('Nhập vào số thứ tự công trình muốn xoá'))
        self.structuresInstance[cIndex].clear()
        del self.structuresInstance[cIndex]
        del self.structuresData[cIndex]
        pass

    def get_struct(self, cIndex=None):
        try:
            if cIndex == None:
                cIndex = int(input('Nhập vào số thứ tự công trình muốn sử dụng'))
                return self.structuresInstance[cIndex]
        except:
            print("Không tìm thấy công trình yêu cầu")
        pass
        return self.structuresInstance[cIndex]

    def save(self, name=""):
        if len(name) == 0:
            filename = input("Nhập tên file")
        else:
            filename = name
        for i in range(len(self.structuresData)):
            self.save_struct(i)
        save_data = {
            "filename": filename,
            "structures": self.structuresData
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
            self.structuresInstance = []
            self.structuresData = []
            for st in data['structures']:
                print(st)
                try:
                    temp = Structure.Structure(mc,
                                               vec3.Vec3(st['position']['x'], st['position']['y'], st['position']['z']))
                    temp.load(st['filename'])
                    self.structuresData.append(st)
                    self.structuresInstance.append(temp)


                except:
                    print("File dữ liệu bị lỗi")
        pass

    def run(self):
        pass

    def teleport_all(self):
        plids = mc.getPlayerEntityIds()
        for id in plids:
            mc.entity.setPos(id, self.startPoint['x'],
                             self.startPoint['y'] + 2,
                             self.startPoint['z'], )


ct = City()



def make_house_line ():
    for i in range(5):
        st = ct.add_struct(615,50,637 + i * 20)
        st.load('mh2_1')


