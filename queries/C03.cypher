// CQ C03: Скільки всього (транзитивно) підлеглих має Олена Коваль? | шлях змінної довжини
MATCH (e:Employee)-[:DIRECT_MANAGER*1..5]->(:Employee {name: 'Олена Коваль'})
RETURN count(DISTINCT e) AS subordinates
