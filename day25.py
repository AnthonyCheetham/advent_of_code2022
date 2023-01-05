# Day 25 of Advent of Code 2022
import math
from functools import cache

with open("datasets/day25_input.dat","r") as myf:
    data = myf.read().splitlines()

s2d = {"2":2,"1":1,"0":0,"-":-1,"=":-2}
d2s = {2:"2",1:"1",0:"0",-1:"-",-2:"="}

def snafu_to_decimal(snafu_num):
    snafu_num = snafu_num[::-1]
    num = 0
    for ix in range(len(snafu_num)):
        num += s2d[snafu_num[ix]]*(5**ix)
    return num

@cache
def get_extra_val(n):
    return sum([2*5**a for a in range(n)])

def decimal_to_snafu(decimal_num):
    n_digits = int(2+math.log(decimal_num+1,5))
    remainder = decimal_num
    snafu_num = ""
    for ix in range(n_digits-1,-1,-1):
        coeff = 5**ix
        extra = get_extra_val(ix)
        digit = ((remainder + extra)//coeff)
        remainder -= digit*coeff
        snafu_num = snafu_num+d2s[digit]

    return snafu_num.lstrip("0")

tally = 0
for line in data:
    tally += snafu_to_decimal(line)

print("Part 1:",decimal_to_snafu(tally))
    