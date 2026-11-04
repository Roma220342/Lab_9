// CQ C09 (аналіз впливу, глибина 3): Які процеси зачепить зміна кореневого процесу «Управління персоналом»?
MATCH path = (root:Process {id: 'personnelManagement'})-[:HAS_SUB_PROCESS*1..3]->(p:Process)
RETURN p.id AS process, p.kind AS kind, length(path) AS depth ORDER BY depth, process
