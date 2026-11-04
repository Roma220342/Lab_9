// CQ C01: Які компетенції вимагає посада «Python-розробник»? | фільтр за властивістю
MATCH (p:Position {name: 'Python-розробник'})-[:REQUIRES_COMPETENCE]->(c:Competence)
RETURN c.id AS competence, c.kind AS kind ORDER BY competence
