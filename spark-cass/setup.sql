CREATE KEYSPACE IF NOT EXISTS testkeyspace
  WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1'};

CREATE TABLE IF NOT EXISTS trigram (
  first text,
  second text,
  third text,
  PRIMARY KEY (first,second,third)
);

copy trigram from '/tmp/out';
