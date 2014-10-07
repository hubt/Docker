#!/usr/bin/env python

# Copyright 2013-2014 DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "testkeyspace"

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    log.info("creating keyspace...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    log.info("creating table...")
    session.execute("""
        CREATE TABLE IF NOT EXISTS trigram (
            first text,
            second text,
            third text,
            PRIMARY KEY (first,second,third)
        )
        """)

    query = SimpleStatement("""
        INSERT INTO trigram (first, second, third)
        VALUES (%(first)s, %(second)s, %(third)s)
        """, consistency_level=ConsistencyLevel.ONE)

    prepared = session.prepare("""
        INSERT INTO trigram (first, second, third)
        VALUES (?,?,?)
        """)

    wordlist = [ x.rstrip() for x in open("/etc/dictionaries-common/words").readlines() ]
    wordcount = len(wordlist)
    import random
    out = open("/tmp/out","w+")
    for i in range(100*1000):
        first = wordlist[random.randint(0,wordcount-1)]
        second = wordlist[random.randint(0,wordcount-1)]
        third = wordlist[random.randint(0,wordcount-1)]
        out.write("%s,%s,%s\n" %(first,second,third))
        #session.execute(prepared, words)
        #for i in range(3000):
            #first = wordlist[random.randint(0,wordcount)]
            #second = wordlist[random.randint(0,wordcount)]
            #third = wordlist[random.randint(0,wordcount)]
            #log.info("inserting row %d" % i)
            #session.execute(query, dict(first=first, second=second, third=third))
            #session.execute(prepared, (first,second,third))

    #future = session.execute_async("SELECT * FROM trigram limit 10")
    log.info("key\tcol1\tcol2")
    log.info("---\t----\t----")

    try:
        rows = future.result()
    except Exception:
        log.exeception()

    for row in rows:
        log.info('\t'.join(row))

    #session.execute("DROP KEYSPACE " + KEYSPACE)

if __name__ == "__main__":
    main()
