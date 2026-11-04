// CQ C02: Хто безпосередній керівник Петра Бондаря? | шаблон шляху
MATCH (:Employee {name: 'Петро Бондар'})-[:DIRECT_MANAGER]->(m:Employee)
RETURN m.name AS manager
