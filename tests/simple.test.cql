CREATE KEYSPACE ks WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
USE ks
CREATE TABLE t (id int, v int, PRIMARY KEY(id, v)) WITH read_repair_chance = 0.0 ;
INSERT INTO t (id, v) VALUES (0, 1) ;
INSERT INTO t (id, v) VALUES (0, 2) ;
SELECT * FROM t;
