// ЛР 9, результат 4: PageRank і Louvain (Neo4j Graph Data Science 2.x)
// 1) Проєкція всього графа (неорієнтовано — для Louvain; PageRank рахуємо на тій самій проєкції)
CALL gds.graph.drop('kg', false) YIELD graphName;
CALL gds.graph.project('kg', '*', {ALL: {type: '*', orientation: 'UNDIRECTED'}})
YIELD graphName, nodeCount, relationshipCount;

// 2) PageRank: топ-10 (stream) і запис у властивість pagerank
CALL gds.pageRank.stream('kg', {dampingFactor: 0.85, maxIterations: 50})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, labels(gds.util.asNode(nodeId))[0] AS label,
       gds.util.asNode(nodeId).name AS name, round(score, 4) AS pagerank
ORDER BY pagerank DESC LIMIT 10;

CALL gds.pageRank.write('kg', {dampingFactor: 0.85, maxIterations: 50, writeProperty: 'pagerank'})
YIELD nodePropertiesWritten, ranIterations;

// 3) Louvain: спільноти та запис у властивість community
CALL gds.louvain.write('kg', {writeProperty: 'community', concurrency: 1})
YIELD communityCount, modularity, nodePropertiesWritten;

// 4) Склад спільнот
MATCH (n) WHERE n.community IS NOT NULL
WITH n.community AS community, labels(n)[0] AS label, count(*) AS c
ORDER BY c DESC
WITH community, collect(label + ': ' + c) AS composition, sum(c) AS size
RETURN community, size, composition ORDER BY size DESC;

// 5) Перевірка збереження
MATCH (n) RETURN count(n.pagerank) AS withPagerank, count(DISTINCT n.community) AS communities;
