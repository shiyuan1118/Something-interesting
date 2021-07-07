# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Solution():
    def reverse(c):
        c_str=list(str(c))
        if len(c_str)==1:
            return c
        else:
            
            if c_str[0]!='-': 
                result=[]
                for i in range(len(c_str)):
                    result.append(c_str[-i-1])
                return int("".join(result))
                    
            if c_str[0]=='-':  
                result=[]
                for i in range(1,len(c_str)):
                    result.append(c_str[-i])                   
                return -1*int("".join(result))

print(Solution.reverse(1534236469))
        
               
                
                
                
            
           

