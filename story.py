# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


def add_story(a,b,c):
    f= open('C:/Users/User/Desktop/stories.md','a')
    f.write("\n## " + a + " path\n")
    f.write("* " + b +"\n")
    f.write("  - " + c + "\n")
    f.close()
    print('got')

add_story("hi" ,"Hello" ,"How are you")

f= open('C:/Users/User/Desktop/stories.md','r')
print(f.read())       