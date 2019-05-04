from mc import *
from mcpi.minecraft import *
from turtle import *
from mcpi.vec3 import *
from Structure import *
from config import *
from PredefinedStructure import *

dirname = os.path.dirname(__file__)
data_root = os.path.join(dirname, CITY_FOLDER)

startPoint = Vec3(300,3,300)


class City():
    def __init__(self):
        self.structuresInstance = []
        self.structuresData = []
        self.StreetData = []
        self.data = {}
        pass

    def set_data(self, key, value):
        self.data[key] = value

    def add_struct(self, x=False, y=False, z=False, note='', tags=''):
        """Thêm công trình vào thành phố"""
        if not (type(x) is int and type(y) is int and type(z) is int):
            print("bạn hãy nhập vị trí của bạn vào vị trí bạn muốn đặt công trình:")
            x = input('x = ')
            y = input('y = ')
            z = input('z = ')

        instance = Structure(Vec3(int(x), int(y), int(z)))
        self.current = instance
        if not note:
            note = input("Hãy nhập vào ghi chú của bạn về công trình này: ")
        self.structuresInstance.append(instance)
        self.structuresData.append({
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "data" : instance.data,
            "note": note,
            "filename": instance.filename,
            "tags": tags,
        })
        return instance

    def reload_struct(self, index):
        """ Dùng để reload laị công trinh khi chỉ mơí load data"""
        pass

    def show_struct(self):
        length = len(self.structuresInstance)
        for index in range(length):
            st = self.structuresInstance[index]
            stData = self.structuresData[index]
            print("{}.[{},{},{}] {} ".format(index, st.position.x, st.position.y, st.position.z, st.filename))
        pass

    def remove_struct(self, index):
        st = self.structuresInstance[index]
        stData = self.structuresData[index]
        st.clear()
        del self.structuresInstance[index]
        del self.structuresData[index]
        print('delete complete')
        pass

    def save_struct(self, index):
        if index == None:
            index = int(input('Nhập vào số thứ tự công trình muốn lưu:'))
        instance = self.structuresInstance[index]
        self.structuresData[index] = {
            "position": {
                "x": instance.position.x,
                "y": instance.position.y,
                "z": instance.position.z,
            },
            "data": instance.data,
            "note": self.structuresData[index]['note'],
            "filename": instance.filename
        }
        pass

    def save(self, filename=''):
        if len(filename) == 0:
            filename = input("Nhập tên file: ")
        for i in range(len(self.structuresData)):
            self.save_struct(i)
        save_data = {
            "filename": filename,
            "structures": self.structuresData,
            "data": self.data,
            "StreetData": StreetData
        }
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)
        f.close()

    def load(self, filename='', mode=''):
        if len(filename) == 0:
            filename = input("Nhập tên file bạn muốn load: ")
        # try:
        with open(os.path.join(data_root, "{}.json".format(filename))) as f:
            data = json.load(f)
            self.filename = filename
            self.structuresInstance = []
            self.structuresData = []
            if mode == '':
                load_mode = input("""
                1. Chỉ load data
                2. Load công trình và xây dựng
                """)
            for st in data['structures']:
                temp = Structure(Vec3(st['position']['x'], st['position']['y'], st['position']['z']))
                if mode == "2":
                    temp.load(st['filename'])
                self.structuresData.append(st)
                self.data = data['data']
                self.StreetData = data.get('StreetData', [])
                self.structuresInstance.append(temp)

    def monitor(self):
        for st in self.structuresInstance:
            st.draw_region()
        pass

    def statistic(self):
        pass

    def alert(self):
        pass

    def auto_run(self):
        pass

    def city_init_street(self):

        x, y, z = startPoint.x,startPoint.y,startPoint.z
        mc.entity.setPos(mc.getPlayerEntityId('huyhuy171'), x,y,z)

        for i in range(-10, 10):
            street_line_x(Vec3(x + i * 100, y, z), 100)
        for i in range(-10, 10):
            street_line_z(Vec3(x, y, z + i * 100), 100)

        street_intersect(startPoint)

        self.save('QH_CITY')
        pass
