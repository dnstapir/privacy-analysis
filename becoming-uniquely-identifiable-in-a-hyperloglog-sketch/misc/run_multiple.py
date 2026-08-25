#!/usr/bin/env python3

import argparse
import sqlite3

from uniquely_discernible import System

schema = """
CREATE TABLE IF NOT EXISTS Data (
    subnet TEXT,
    Q      INTEGER,
    B      INTEGER,
    hashl  INTEGER,
    psim   REAL,
    pcalc  REAL,
    UNIQUE(subnet, Q, B, hashl)
);
"""

insert_data = """
INSERT INTO Data VALUES(?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Uniquely Identifiable in HyperLogLog (BATCH)'
    )

    parser.add_argument("n_subnets", type=int)
    parser.add_argument("dbname", type=str)

    args = parser.parse_args()

    hash_size = 64
    b_vec = range(3, 12)
    slash = 16

    con = sqlite3.connect(args.dbname)
    cur = con.cursor()
    cur.execute("PRAGMA synchronous = OFF;")
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute(schema)

    for b in b_vec:
        C = hash_size-b
        Q = 2 ** (32-slash)
        s = System(Q, b, C)
        print(f"Simulating a System({Q}, {b}, {C})...")
        pcalc = s.p_most_leading()
        print(f"Done simulating a System({Q}, {b}, {C})!")
        subnets = []
        for i in range(0, args.n_subnets):
            subnet = f"10.{i}.0.0/{slash}"
            psim = s.simulate_subnet(subnet)
            subnets += [(subnet, Q, b, hash_size, psim, pcalc)]
        cur.executemany(insert_data, subnets)
    con.commit()
    con.close()
