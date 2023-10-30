# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 15:27:40 2022

@author: erika
"""

#%%

V_in = 5
V_led = 1.35
I = 50e-3
N = 9

R = (V_in - V_led)/(N*I)
P_r = I**2*R

print(R)
print(P_r)