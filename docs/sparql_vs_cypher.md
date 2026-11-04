# SPARQL (rdflib, kb.ttl) vs Cypher (Neo4j)

| id | question | rows_sparql | rows_cypher | equal_values | ms_sparql | ms_cypher | len_sparql | len_cypher |
|---|---|---|---|---|---|---|---|---|
| T05 | Хто є безпосереднім керівником Петра Бондаря? | 1 | 1 | True | 229.6 | 7.8 | 118 | 84 |
| T08 | Хто транзитивно підпорядкований Івану? | 13 | 13 | True | 5.6 | 9.1 | 57 | 93 |
| T13 | Який керівник має найбільше безпосередніх підлеглих? | 1 | 1 | True | 44.6 | 12.1 | 98 | 88 |
| T16 | Для кожної посади: скільки співробітників мають оцінку ≥ 7? | 4 | 4 | True | 64.2 | 12.5 | 134 | 109 |
| T19 | Хто пропрацював в організації понад 60 місяців? | 13 | 13 | True | 42.1 | 14.6 | 121 | 61 |

### T05
```sparql
SELECT ?name WHERE { ?e hr:fullName ?n ; hr:directManager ?m . FILTER(STR(?n) = "Петро Бондар") ?m hr:fullName ?name }
```
```cypher
MATCH (:Employee {name:'Петро Бондар'})-[:DIRECT_MANAGER]->(m) RETURN m.name AS name
```

### T08
```sparql
SELECT DISTINCT ?e WHERE { ?e hr:directManager+ hr:ivan }
```
```cypher
MATCH (e:Employee)-[:DIRECT_MANAGER*1..10]->(:Employee {id:'ivan'}) RETURN DISTINCT e.id AS e
```

### T13
```sparql
SELECT ?m (COUNT(?e) AS ?n) WHERE { ?e hr:directManager ?m } GROUP BY ?m ORDER BY DESC(?n) LIMIT 1
```
```cypher
MATCH (e)-[:DIRECT_MANAGER]->(m) RETURN m.id AS m, count(e) AS n ORDER BY n DESC LIMIT 1
```

### T16
```sparql
SELECT ?t (COUNT(?e) AS ?n) WHERE { ?e hr:occupies ?p ; hr:productivityScore ?s . ?p hr:positionTitle ?t FILTER(?s >= 7) } GROUP BY ?t
```
```cypher
MATCH (e:Employee)-[:OCCUPIES]->(p:Position) WHERE e.productivityScore >= 7 RETURN p.name AS t, count(e) AS n
```

### T19
```sparql
SELECT ?e WHERE { VALUES ?cls { hr:Employee hr:Manager hr:Recruiter } ?e a ?cls . ?e hr:tenureMonths ?t FILTER(?t > 60) }
```
```cypher
MATCH (e:Employee) WHERE e.tenureMonths > 60 RETURN e.id AS e
```
