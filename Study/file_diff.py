#!/usr/bin/env python3

import os

person1 = open("1.txt","r").readlines()
person2 = open("2.txt","r").readlines()
for i in person1:
    if i not in person2:
        print(i)
