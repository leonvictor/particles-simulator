from Environement.environment import *
import time

env = Environment(2)

for i in range(1):
    env.addAgent()

time.sleep(0.01)
for i in range(10000000):
    env.actualize()
    time.sleep(0.01)

