// ЛР 9, результат 5: роль лише для читання для text-to-Cypher (Neo4j Enterprise; виконувати в БД system)
:use system
CREATE ROLE t2c_reader IF NOT EXISTS;
GRANT ACCESS ON DATABASE neo4j TO t2c_reader;
GRANT MATCH {*} ON GRAPH neo4j TO t2c_reader;
CREATE USER t2c IF NOT EXISTS SET PASSWORD 't2c-readonly-pass' CHANGE NOT REQUIRED;
GRANT ROLE t2c_reader TO t2c;
SHOW ROLE t2c_reader PRIVILEGES;
