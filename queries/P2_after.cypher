// PROFILE 2 (після): переписано на зв'язаний шаблон, фільтр за індексованою оцінкою першим
PROFILE MATCH (a:Employee) WHERE a.productivityScore < 5.0
MATCH (a)-[:OCCUPIES]->(p:Position)<-[:OCCUPIES]-(b:Employee)
WHERE b.productivityScore >= 8.0
RETURN count(*) AS pairs
