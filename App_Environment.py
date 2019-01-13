from app_data import startPoint, endPoint, cityHeight, cityGroundBlock, cityGroundData
from mc import mc
from mcpi import vec3
from mcpi import block
# mc.postToChat("Hello i am clearing environment")
# # Đặt đất nền
# mc.setBlocks(
#     startPoint['x'],
#     startPoint['y'] - 2,
#     startPoint['z'],
#     endPoint['x'],
#     endPoint['y'],
#     endPoint['z'],
#     cityGroundBlock,
#     cityGroundData
# )
# mc.postToChat("We have ground")
#
# # clear không gian
#
# mc.setBlocks(
#     startPoint['x'],
#     startPoint['y'],
#     startPoint['z'],
#     endPoint['x'],
#     endPoint['y'] + cityHeight,
#     endPoint['z'],
#     block.AIR
# )
# mc.postToChat("We have air")

for id in mc.getPlayerEntityIds():
    mc.entity.setPos(id, startPoint['x'],
                     startPoint['y'] +1,
                     startPoint['z'], )
