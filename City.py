import random

from mc import mc
import os
import json
from mcpi import vec3
from mcpi import block
import time
import Structure
import turtle
import turtle_tool

dirname = os.path.dirname(__file__)
data_folder = "city-data"
data_root = os.path.join(dirname, data_folder)
screen = turtle.Screen()


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
        self.centerPoint = {
            'x': 800,
            'y': 50,
            'z': 800
        }
        self.cityGroundBlock = 155
        self.cityHeight = 50
        self.cityGroundData = 1
        self.data = {
            "energy": 0
        }
        self.pen = turtle.Turtle()

        self.turtlePlayers = [
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
            turtle.Turtle(),
        ]

        for tPlayer in self.turtlePlayers:
            tPlayer.hideturtle()
            tPlayer.penup()
        pass

    def clear(self):
        # Đặt đất nền
        mc.setBlocks(
            self.startPoint['x'],
            self.startPoint['y'] - 3,
            self.startPoint['z'],
            self.endPoint['x'],
            self.endPoint['y'],
            self.endPoint['z'],
            self.cityGroundBlock,
            self.cityGroundData
        )
        mc.postToChat("We have ground")

        # clear không gian
        for i in range(self.cityHeight):
            mc.setBlocks(
                self.startPoint['x'],
                self.startPoint['y']+i,
                self.startPoint['z'],
                self.endPoint['x'],
                self.endPoint['y'] + i,
                self.endPoint['z'],
                block.AIR
            )
            time.sleep(3)
            mc.postToChat("air {} ".format(i))
        mc.postToChat("We have air")

        # for id in mc.getPlayerEntityIds():
        #     mc.entity.setPos(id, self.startPoint['x'],
        #                      self.startPoint['y'] + 1,
        #                      self.startPoint['z'], )

        pass

    def show_struct(self):
        try:
            structures = self.structuresData
            structuresInstance = self.structuresInstance
            for i in range(len(structures)):
                tempst = structures[i]
                print("{}. {} || {}".format(i, tempst.get('filename', ''), tempst.get('note', '')))
                print("Pos", structuresInstance[i].position)

        except:
            print('Có lỗi với dữ liệu thành phố')
        pass

    def add_struct(self, x=False, y=False, z=False, note=False, tags=[]):
        if not (type(x) is int and type(y) is int and type(z) is int):
            print("bạn hãy nhập vị trí của bạn vào vị trí bạn muốn đặt công trình")
            x = input('x = ')
            y = input('y = ')
            z = input('z = ')

        instance = Structure.Structure(mc, vec3.Vec3(int(x), int(y), int(z)))
        self.current = instance
        if not note:
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
            "filename": instance.filename,
            "tags": tags,
        })
        return instance
        pass

    def save_struct(self, cIndex=None):
        if cIndex == None:
            cIndex = int(input('Nhập vào số thứ tự công trình muốn lưu'))
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

    def save_all(self, name):
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
        self.save(name)

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
            "structures": self.structuresData,
            "data": self.data
        }
        f = open(os.path.join(data_root, "{}.json".format(filename)), 'w+', )
        json.dump(save_data, f, ensure_ascii=False)

        f.close()
        pass

    def load(self, filename=False, load_mode=False):
        if not (filename):
            filename = input("Nhập tên file bạn muốn load")
        # try:
        with open(os.path.join(data_root, "{}.json".format(filename))) as f:
            data = json.load(f)
            self.filename = filename
            self.structuresInstance = []
            self.structuresData = []
            if not load_mode:
                load_mode = input("""
                1. Chỉ load data
                2. Load công trình và xây dựng
                """)
            for st in data['structures']:
                print(st)
                # try:
                temp = Structure.Structure(mc,
                                           vec3.Vec3(st['position']['x'], st['position']['y'], st['position']['z']))
                if load_mode == "2":
                    temp.load(st['filename'])
                self.structuresData.append(st)
                self.structuresInstance.append(temp)

                #
                # except:
                #     print("File dữ liệu bị lỗi")
        pass

    def run(self):
        pass

    def teleport_all(self):
        plids = mc.getPlayerEntityIds()
        for id in plids:
            mc.entity.setPos(id, self.startPoint['x'],
                             self.startPoint['y'] + 2,
                             self.startPoint['z'], )

    def increase_energy(self, amount=10):
        self.data['energy'] = self.data['energy'] + amount

    def monitor(self, mainloop=True):
        for i in range(len(self.structuresInstance)):
            st = self.structuresInstance[i]
            st.pen.clear()
            st.set_name("({})".format(i))
            st.draw_region("({})".format(i))
        pen = self.pen
        pen.clear()
        pen.setpos(-500, 400)

        def onclick_structure(x, y):
            pen.clear()
            pen.up()
            for st in self.structuresInstance:
                in_turtle = st.is_in_turtle_region(x, y)
                if in_turtle:
                    pen.write("Cong trinh :{}".format(st.filename))
                    y = pen.ycor()
                    for key in st.structData:
                        pen.sety(pen.ycor() - 30)
                        pen.write("{}:{}".format(key, st.structData[key]))
                    pen.sety(y)
                    break
            pen.pendown()
            pass

        def run_per_second():
            data = {}
            ct.run_per_second()
            # for st in self.structuresInstance:
            #     st.run_per_second(data)
            screen.ontimer(run_per_second, 1000)

        screen.ontimer(run_per_second, 1000)

        screen.onclick(onclick_structure)
        if mainloop:
            screen.mainloop()
        pass

    def run_per_second(self):
        turtlePlayers = self.turtlePlayers
        data = {}
        players = mc.getPlayerEntityIds()

        data['plids'] = players
        data['pl_positions']={}
        for i in range(len(players)):
            tPlayer = turtlePlayers[i]
            tPlayer.showturtle()
            plid = players[i]
            pos = mc.entity.getTilePos(plid)
            data['pl_positions']['plid'] = [pos.x,pos.y,pos.z]
            turtle_tool.move_player(tPlayer, pos.x, pos.z, "{}".format(plid))

        for st in self.structuresInstance:
            st.run_per_second (data)


ct = City()


def hieu_minh_load():
    st = ct.add_struct(735, 50, 764, 'Super market Hiếu Minh')
    st.load('HM_SP_MARKET')
    ct.save_all('HACKTHON_CITY')


def wind_mill():
    st = ct.add_struct(670, 50, 757)
    st.setBlocks(-4, -4, 0, 4, 4, 0, 1)
    st.save('coi_xoay_gio')
    ct.save_all("city_x")
    for i in range(10):
        time.sleep(1)
        st.rotateBy(0, 0, 36)
        ct.increase_energy(10)
    ct.save_all('city_x')
    print("data", ct.data)


def make_sky_hotel():
    st = ct.add_struct(735, 50, 800, 'SKY HOTEL Hiếu Minh')
    y = 0
    st.setBlocks(-5, y, -5, 15, y, 15, 184, 0)
    st.setBlocks(-4, y, -4, 14, y, 14, 0, 0)
    for j in range(5):
        y = j * 6
        st.setBlocks(0, y, 0, 10, y, 10, 0)
        st.setBlocks(1, y + 5, 1, 9, y + 5, 9, 24, 4)
        for i in range(10):
            if (i % 2 == 0):
                st.setBlocks(0 + i, y, 0, 0 + i, y + 5, 0, 1)
                st.setBlocks(0, y, 0 + i, 0, y + 5, 0 + i, 1)
                st.setBlocks(10, y, 0 + i, 10, y + 5, 0 + i, 1)
                st.setBlocks(0 + i, y, 10, 0 + i, y + 5, 10, 1)
            else:
                st.setBlocks(0 + i, y, 0, 0 + i, y + 5, 0, 95, 4)
                st.setBlocks(0, y, 0 + i, 0, y + 5, 0 + i, 95, 4)
                st.setBlocks(10, y, 0 + i, 10, y + 5, 0 + i, 95, 4)
                st.setBlocks(0 + i, y, 10, 0 + i, y + 5, 10, 95, 4)
        st.setBlocks(1, 0, 1, 9, 0, 9, 24, 4)


def set_roads():
    x, y, z = 716, 50, 757

    for _z in range(10):
        st = ct.add_struct(x, y, z + _z * 21, 'đoạn đường')
        st.load("DH_BIG_ROAD")
    ct.save_all('city')
