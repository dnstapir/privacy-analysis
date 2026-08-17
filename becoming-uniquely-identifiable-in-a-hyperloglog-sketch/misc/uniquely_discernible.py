#!/usr/bin/env python3

import argparse
import math
import ipaddress

import mmh3


class System:
    def __init__(self, Q, B, C):
        assert B >= 0
        assert Q >= 1
        assert C >= 1
        self.Q = Q
        self.B = B
        self.C = C


    def p_N(self, n):
        if self.B == 0: # only one bucket
            if n != Q:
                return 0
            else:
                return 1

        res = math.exp(self.log_p_N(n))
        assert res >= 0
        assert res <= 1

        return res

    def log_p_N(self, n):
        assert n >= 0
        res = math.lgamma(self.Q) - math.lgamma(n) - math.lgamma(self.Q-n+1)

        p = 2 ** (-self.B)
        res += (n-1)*math.log(p)
        res += (self.Q-n)*math.log(1-p)

        return res


    def p_L(self, l):
        assert l >= 1
        if l == self.C+1:
            return 1/math.pow(2, self.C)
        return 1/math.pow(2, l)


    def p_most_leading_given_L_N(self, l, n):
        assert n <= self.Q
        assert l >= 1
        assert l <= self.C+1

        s = 0
        for i in range(1, l):
            s += self.p_L(i)
        assert s <= 1

        p1 = math.pow(s, n-1)
        assert p1 <= 1

        return p1


    def p_most_leading_given_L(self, l):
        assert l >= 1
        assert l <= self.C+1

        s = 0
        for j in range(1, self.Q+1):
            s += self.p_N(j)*self.p_most_leading_given_L_N(l, j)
        # assert s <= 1 # TODO trips for large hash sizes, still close to 1.0. FP error?

        return s


    def p_most_leading(self):
        s = 0
        for k in range(1, self.C+1):
            s += self.p_L(k)*self.p_most_leading_given_L(k)
        assert s <= 1

        return s

    def simulate_subnet(self, subnet):
        buckets = {}
        u_count = 0
        net = ipaddress.ip_network(subnet)
        for ip in net.hosts():
            hash = mmh3.hash(ip.packed, seed=0, signed=False)
            hash_bin = format(hash, 'b').zfill(32)
            #print(f"{ip}: {hash_bin}")

            head = hash_bin[0:self.B]
            tail = hash_bin[self.B:]
            leadingzeros = len(tail) - len(tail.lstrip('0'))

            if head not in buckets.keys():
                buckets[head] = []
            buckets[head] += [leadingzeros]

        for b in sorted(buckets.keys()):
            if len(buckets[b]) == 1:
                #print(f"warning, unique ID found, alone in bucket: {b}-{buckets[b][0]}")
                u_count += 1
                continue

            maxcount = max(buckets[b])
            if buckets[b].count(maxcount) == 1:
                #print(f"warning, unique ID found, unique maximum: {b}-{maxcount}")
                u_count += 1

        return u_count/net.num_addresses




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Uniquely Identifiable in HyperLogLog'
    )

    parser.add_argument("hashsize", type=int)
    parser.add_argument("bucket_addr_width", type=int)
    parser.add_argument("subnet", type=str)

    args = parser.parse_args()

    net = ipaddress.ip_network(args.subnet)
    Q = net.num_addresses
    hash_length = args.hashsize
    B = args.bucket_addr_width
    C = hash_length - B

    s = System(Q, B, C)

    if s.C <= 20:
        for i in range(1, C+1+1):
            print(f"p(L={i}) = {s.p_L(i)}")

    if s.Q <= 20:
        for j in range(1, Q+1):
            print(f"p(N={j}) = {s.p_N(j)}")

    sample_prob = s.simulate_subnet(args.subnet)
    print(f"Sample prob for {args.subnet}: {sample_prob}")
    print(f"p(Uniquely discernible) = {s.p_most_leading()}")
