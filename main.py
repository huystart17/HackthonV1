from City import *
from threading import Thread
import _main
_main._make_street()
ct.clear()
ct.load('hackv13', '2')

ct.monitor()
mc.entity.getTilePos()