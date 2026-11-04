// CQ C05: Скільки співробітників і яка середня оцінка на кожній посаді? | агрегація
MATCH (e:Employee)-[:OCCUPIES]->(p:Position)
RETURN p.name AS position, count(e) AS employees, round(avg(e.productivityScore), 2) AS avgScore
ORDER BY employees DESC
