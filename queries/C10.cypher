// CQ C10 (аналіз впливу, глибина 4): Кого зачепить зміна вимог до компетенції «negotiation»
// (компетенція <- посада <- співробітник -> керівник ланцюжком до 2 рівнів)?
MATCH (c:Competence {id: 'negotiation'})<-[:REQUIRES_COMPETENCE]-(p:Position)<-[:OCCUPIES]-(e:Employee)
OPTIONAL MATCH (e)-[:DIRECT_MANAGER*1..2]->(m:Employee)
RETURN p.name AS position, count(DISTINCT e) AS affectedEmployees, collect(DISTINCT m.name) AS managersToNotify
ORDER BY affectedEmployees DESC
