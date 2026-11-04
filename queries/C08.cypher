// CQ C08: Які керівники мають щонайменше 5 безпосередніх підлеглих і яка середня оцінка команди? | WITH + агрегація
MATCH (e:Employee)-[:DIRECT_MANAGER]->(m:Employee)
WITH m, count(e) AS team, avg(e.productivityScore) AS avgScore
WHERE team >= 5
RETURN m.name AS manager, team, round(avgScore, 2) AS avgScore ORDER BY team DESC
