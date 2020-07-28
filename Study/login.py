#!/usr/bin/env python3

count = 0
while count < 4:
    user = input("请输入用户名:")
    pwd = input("请输入密码:")

    if user == 'root'  and pwd == 'root':
        print("登陆成功!")
    else:
        print("用户名或密码错误，请重新输入!")
        count += 1

print("超过重试次数限制，登陆失败!")
