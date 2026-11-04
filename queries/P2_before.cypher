// PROFILE 2 (до): пари «низька/висока оцінка на одній посаді» — декартів добуток і фільтр за id
PROFILE MATCH (a:Employee), (b:Employee), (pa:Position), (pb:Position)
WHERE (a)-[:OCCUPIES]->(pa) AND (b)-[:OCCUPIES]->(pb) AND pa.id = pb.id
  AND a.productivityScore < 5.0 AND b.productivityScore >= 8.0
RETURN count(*) AS pairs
