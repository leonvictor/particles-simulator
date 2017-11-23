from Environement.environment import *
import time
import threading
import _thread
from GUI.Gui import *

lock = threading.Lock()
env = Environment(2, lock)

a = Gui(env.quadTree, lock)

for i in range(10):
    env.addAgent()

continuer = True

def runMAS():
    time.sleep(0.01)
    while a:
        env.actualize()
        time.sleep(0.01)


_thread.start_new_thread(runMAS, ())
a.run()
del a





