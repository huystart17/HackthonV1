from mcpi import minecraft
mc = False
server_online = "103.237.147.88"
server_local = "localhost"

port_lvl5 = 4712
port_luyen_thi = 4713
port_may_bay = 4714
while True:
    try:
        mc = minecraft.Minecraft.create(server_local, port_may_bay)
        break
    except:
        mc = False
        print("Lỗi kết nối")
        server = input("Hãy nhập vào server để kết nối")
        port  = input("Hãy nhập vào server để kết nối")
