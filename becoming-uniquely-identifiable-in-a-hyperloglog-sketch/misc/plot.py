#!/usr/bin/env python3

import argparse
import math
import sqlite3

from matplotlib import pyplot as plt

get_data_stmt = """
SELECT B, psim, pcalc FROM Data WHERE B=?;
"""

b_vec = range(3, 12)

class StreamStdev:
    def __init__(self):
        self.xbar = 0.0
        self.n = 0
        self.xbar_sq = 0.0

    def add(self, x: float):
        old_xbar = self.xbar

        self.n += 1
        self.xbar += (x-self.xbar)/self.n
        self.xbar_sq += (x-old_xbar)*(x-self.xbar)

    def get_xbar(self) -> float:
        return self.xbar

    def get_stdev(self) -> float:
        return math.sqrt(self.xbar_sq/(self.n-1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Uniquely Identifiable in HyperLogLog (BATCH)'
    )

    parser.add_argument("dbname", type=str)
    args = parser.parse_args()
    con = sqlite3.connect(args.dbname)
    cur = con.cursor()

    curves = []
    for b in b_vec:
        sd = StreamStdev()
        pcalc = 0
        for row in cur.execute(get_data_stmt, (b,)):
            sd.add(row[1])
            if not pcalc:
                pcalc = row[2]
        curves += [[b, pcalc, sd.get_xbar(), sd.get_xbar()+sd.get_stdev(), sd.get_xbar()-sd.get_stdev()]]
    con.close()

    fig, ax = plt.subplots()
    ax.semilogy([c[0] for c in curves], [c[1] for c in curves], label="Simulated")
    ax.semilogy([c[0] for c in curves], [c[2] for c in curves], 'k--', label="Calculated")
    ax.fill_between([c[0] for c in curves], [c[4] for c in curves], [c[3] for c in curves], alpha=0.3)
    ax.set_title("Probability of meing uniquely discernible in a HyperLogLog")
    ax.set_xlabel("Bucket address width (bits)")
    ax.set_ylabel("p(Uniquely Discernible)")
    ax.legend()

    plt.savefig("/tmp/ud.png")
