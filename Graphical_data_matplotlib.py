#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt

x = []
y = []

fp = open("score.txt",'r')
data = fp.readlines()

for i in data:
    tempx = (i.split())[0]
    tempy = (i.split())[1]
    x.append(tempx)
    y.append(int(tempy))

fp.close()
plt.ylim(1, 100)
plt.title("Exam Score", fontsize=24)
plt.xlabel("Name", fontsize=14)
plt.ylabel("Score", fontsize=14)
plt.plot(x, y)
plt.show()
