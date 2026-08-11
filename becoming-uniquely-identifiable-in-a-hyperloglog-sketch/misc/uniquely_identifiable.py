#!/usr/bin/env python3

import argparse
import math

parser = argparse.ArgumentParser(
                  prog='Uniquely Identifiable in HyperLogLog')

parser.add_argument("hashsize", type=int)
parser.add_argument("B", type=int)
parser.add_argument("hosts", type=int)

args = parser.parse_args()

Q = args.hosts
hash_length = args.hashsize
B = args.B
C = hash_length - B
halfQ = Q // 2
halfC = C // 2

assert B >= 0
assert Q >= 1
assert C >= 1

def p_alone():
    return p_N(1)

def p_N(n):
    assert n >= 0
    p1 = math.pow(1/math.pow(2, B), n-1)
    p2 = math.pow(1-1/math.pow(2, B), Q-n)
    return p1*p2

def p_L(l):
    assert l >= 0
    if l == C:
        return 1/math.pow(2, C)
    return 1/math.pow(2, l+1)

def p_most_leading_given_L_N(l, n):
    if n == 1:
        return 1
    assert n >= 2
    assert n <= Q
    assert l >= 0
    assert l <= C

    s = 0
    for i in range(0, l):
        s += p_L(i)
    assert s <= 1

    p1 = math.pow(s, n-1)
    assert p1 <= 1

    if l == 0:
        assert p1 == 0

    return p_L(l)*p1

def p_most_leading_given_L(l):
    assert l >= 0
    assert l <= C

    s = 0
    for j in range(2, Q+1):
        s += p_N(j)*p_most_leading_given_L_N(l, j)
    assert s <= 1

    return s

def p_most_leading():
    s = 0
    for k in range(0, C+1):
        s += p_L(k)*p_most_leading_given_L(k)
    assert s <= 1

    return s

print(f"Q = {Q}, C = {C}, B = {B}")

print(f"p(L=1 most leading | N=Q) = {p_most_leading_given_L_N(1, Q)}")
print(f"p(L=0 most leading | N=Q) = {p_most_leading_given_L_N(0, Q)}")
print(f"p(L=1 most leading | N=Q/2) = {p_most_leading_given_L_N(1, halfQ)}")
print(f"p(L=0 most leading | N=Q/2) = {p_most_leading_given_L_N(0, halfQ)}")
print(f"p(L=C/2 most leading | N=Q/2) = {p_most_leading_given_L_N(halfC, halfQ)}")
print(f"p(L=C most leading | N=Q/2) = {p_most_leading_given_L_N(C, halfQ)}")
print(f"p(L=C most leading | N=Q) = {p_most_leading_given_L_N(C, Q)}")

print(f"p(L=C/2 most leading) = {p_most_leading_given_L(halfC)}")
print(f"p(L=C most leading) = {p_most_leading_given_L(C)}")
print(f"p(L=1 most leading) = {p_most_leading_given_L(1)}")
print(f"p(L=0 most leading) = {p_most_leading_given_L(0)}")

most_leading = p_most_leading()
print(f"p(Alone in bucket) = {p_alone()}")
print(f"p(Most leading) = {most_leading}")
print(f"p(Uniquely discernible) = {most_leading + p_alone()}")

# TODO why does two hosts, 0 bucket, 1-bit hash give 0.125?
