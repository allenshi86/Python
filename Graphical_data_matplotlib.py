#!/usr/bin/env python3

import os
import sys
import matplotlib.pyplot as plt

resultfile = sys.argv[1]

x = []
y = []

def get_garph():
    fp = open(resultfile,'r')
    data = fp.readlines()

    for i in data:
        tempx = (i.split())[0]
        tempy = (i.split())[1]
        x.append(tempx)
        y.append(int(tempy))

    fp.close()
    plt.ylim(1, 100)
    plt.title("Exam Score-2020", fontsize=24)
    plt.xlabel("Name", fontsize=14)
    plt.ylabel("Score", fontsize=14)
    plt.plot(x, y)
    plt.show()
    return

if __name__ == '__main__':
    get_garph()
