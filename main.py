from Environement.environement import *
import time

env = Environement(2)

for i in range(1):
    env.addAgent()

time.sleep(0.01)
for i in range(10000000):
    env.actualize()
    time.sleep(0.01)

