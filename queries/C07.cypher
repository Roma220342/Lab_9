// CQ C07: Хто з співробітників завершив курс, а хто — ні? | OPTIONAL MATCH + WITH
MATCH (e:Employee)
OPTIONAL MATCH (e)-[:COMPLETED_COURSE]->(c:Course)
WITH e, count(c) AS courses
RETURN CASE WHEN courses > 0 THEN 'завершив курс' ELSE 'без курсу' END AS status, count(e) AS employees
ORDER BY status
