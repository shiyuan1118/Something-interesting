# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime

start=datetime.datetime.now()
class solution():
    def approximation(c):
        if c<0:
            return 'no solution'
        else:
            c_str=str(c)
            int_part=c_str.split('.')[0]
            dec_part=c_str.split('.')[1]
            if int(dec_part)>=5:
                return int(int_part)+1
            else:
                return int(int_part)
           
print(solution.approximation(3.7))
end=datetime.datetime.now()

print(end-start)

#tips:1.字符串和数值间的变换；2.split函数运用        