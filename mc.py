from mcpi import minecraft
mc = False
server = "localhost"
while True:
    try:
        mc = minecraft.Minecraft.create()
        break
    except:
        mc = False
        print("Lỗi kết nối")
        server = input("Hãy nhập vào server để kết nối")
        port  = input("Hãy nhập vào server để kết nối")
