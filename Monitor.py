import json
from turtle import *
from mc import *
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os

dirname = os.path.dirname(__file__)
data_root = os.path.join(dirname, CITY_FOLDER)
sc = Screen()
sc.setup(width=1200, height=800)
sc.bgcolor('#d7ddc3')
sc._root.option_add('*font', 'Inconsolata 10')
root = sc._root
panel = tk.Frame(sc._root).pack()


def showList():
    title = "Đây là danh sách công dân đang trực tuyến"
    text = """
    Danh sách công dân đang hoạt động:                                                   
    """
    players = list(playerData.keys())
    for index in range(len(players)):
        name = players[index]
        try:
            pl = mc.getPlayerEntityId(name)
            pos = mc.entity.getTilePos(pl)
            text += "\n{: <15}<{: <5}>-online-x={},y={},z={}".format(name, pl, pos.x, pos.y, pos.z)

        except:
            text += "\n" + name + ": offline"
            "player không tồn tại"
    messagebox.showinfo(title, text, parent=root)
    pass


btnShowList = tk.Button(panel, text="Danh sách công dân", command=showList).pack(side=tk.LEFT)

playersOnMap = [Turtle(), Turtle(), Turtle(), Turtle(), Turtle(), Turtle()]
for player in playersOnMap:
    player.shape('triangle')
    player.penup()
    player.shapesize(0.5, 0.5)
    player.speed(0)
    player.ht()
playerData = {
    "huyhuy17": {
        "name": "huyhuy17",
        'id': 0
    },
    "SeriousGuy": {
        "name": "SeriousGuy",
        'id': 0
    },
    "Free": {
        "name": "Free",
        'id': 0
    },
}


def getRelativePos(x, y):
    return x + 0, y - 0


count = 0


def make_map():
    with open(os.path.join(data_root, "{}.json".format("HACK2"))) as f:
        data = json.load(f)
        structures = data['structures']
        for st in structures:
            pen = Turtle()
            pen.penup()
            pos = st['position']
            pen.setpos(pos['x'], pos['z'])
            pen.write(st['filename'])
        pass


make_map()


def player_onclick(playerpen, index, plid):
    print('onlick work ', index)

    def onclick(x, y):
        title = "Xem thông tin nhân vật"

        text = """
            Tại đây bạn có thể xem thông chi tiết và tương tác với nhân vật
            ===
            1. Xem thông tin 
            2. Dịch chuyển - đưa công dân tới vị trí mong muốn
            3. Gửi thông báo tới công dân
            4. Đăng ký dịch vụ  - Cho phép công dân sử dụng dịch vụ của thành phố
            """
        yc = sc.textinput(title, text)
        if yc == '1':
            sc.textinput("Người chơi id = ", plid)
            pass
        elif yc == '2':
            pos = sc.textinput("Nhập nội toạ độ di chuyển", "x,y,z:")
            pos = pos.split(',')
            try:
                mc.entity.setPos(plid, int(pos[0]), int(pos[1]), int(pos[2]))
            except:
                print("lỗi")
        elif yc == '3':
            text = sc.textinput("Nhập nội dung thông báo", "Thông báo:")
            mc.postToChat(text)
        elif yc == '2':
            pass

    playerpen.onclick(onclick)


def main():
    playerids = mc.getPlayerEntityIds()
    global count
    for index in range(len(playerids)):
        plid = playerids[index]
        x, y, z = mc.entity.getTilePos(plid)
        pen = playersOnMap[index]
        pen.showturtle()
        pen.clear()
        pen.write(plid)
        pen.shape('circle')
        pen.color('red')
        pen.setpos(getRelativePos(x, z))
        if count == 1:
            player_onclick(pen, index, plid)
            count = 1
    count += 1

    sc.ontimer(main, 100)


main()

sc.mainloop()
