from mcpi import minecraft
mc = False
server_online = "103.237.147.88"
server_local = "localhost"

while True:
    try:
        mc = minecraft.Minecraft.create(server_online)
        break
    except:
        mc = False
        print("Lỗi kết nối")
        server = input("Hãy nhập vào server để kết nối")
        port  = input("Hãy nhập vào server để kết nối")
