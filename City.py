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

    def add_struct(self):
        print("bạn hãy nhập vị trí của bạn vào vị trí bạn muốn đặt công trình")
        x = input('x = ')
        y = input('y = ')
        z = input('z = ')

        instance = Structure.Structure(mc, vec3.Vec3(int(x), int(y), int(z)))
        self.current = instance

        self.currentNote = input("Hãy nhập vào ghi chú của bạn về công trình này")
        self.structuresInstance.append(instance)
        self.currentIndex = len(self.structuresInstance) - 1
        self.structuresData.append({
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "note": self.currentNote,
            "filename": instance.filename
        })
        pass

    def save_struct(self):
        cIndex = self.currentIndex
        instance = self.structuresInstance[cIndex]
        self.structuresData[cIndex] = {
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "note": self.currentNote,
            "filename": instance.filename
        }
        pass

    def remove_struct(self):
        pass

    def get_struct(self):
        try:
            cIndex = int(input("Nhập vào index của công trình mà bạn muốn sử dụng"))
            return self.structuresInstance[cIndex]
        except:
            print("Không tìm thấy công trình yêu cầu")
        pass

    def run(self):
        pass

    def save(self, name=""):
        if len(name) == 0:
            filename = input("Nhập tên file")
        else:
            filename = name
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
            for st in data['structures']:
                print(st)
                try:
                    temp = Structure.Structure(mc, vec3.Vec3(st['position']['x'],st['position']['y'],st['position']['z']))
                    temp.load(st['filename'])
                    # print(st['note'])
                    # mc.postToChat(st['note'])
                    # mc.postToChat("Vua hoan thien")
                except:
                    print("File dữ liệu bị lỗi")
        pass
