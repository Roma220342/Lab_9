// CQ C04: Який ланцюжок підпорядкування від Петра Бондаря до Олени Коваль? | shortestPath
MATCH (a:Employee {name: 'Петро Бондар'}), (b:Employee {name: 'Олена Коваль'}),
      p = shortestPath((a)-[:DIRECT_MANAGER*..6]->(b))
RETURN length(p) AS hops, [n IN nodes(p) | n.name] AS chain
