// ЛР 9, результат 2: імпорт LOAD CSV + MERGE (згенеровано scripts/build_data.py)
// Ідемпотентний: MERGE за id вузла та за парою кінців зв'язку; повторний запуск не створює дублікатів.

LOAD CSV WITH HEADERS FROM 'file:///nodes_Action.csv' AS row
MERGE (n:Action {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Candidate.csv' AS row
MERGE (n:Candidate {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Competence.csv' AS row
MERGE (n:Competence {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Course.csv' AS row
MERGE (n:Course {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.courseHours = toInteger(row.courseHours);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Decision.csv' AS row
MERGE (n:Decision {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Document.csv' AS row
MERGE (n:Document {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Employee.csv' AS row
MERGE (n:Employee {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.employeeId = row.employeeId, n.hireDate = datetime(row.hireDate), n.productivityScore = toFloat(row.productivityScore), n.tenureMonths = toInteger(row.tenureMonths);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Event.csv' AS row
MERGE (n:Event {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.occurredOn = datetime(row.occurredOn);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Metric.csv' AS row
MERGE (n:Metric {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.kpiTarget = toFloat(row.kpiTarget), n.turnoverRate = toFloat(row.turnoverRate);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Position.csv' AS row
MERGE (n:Position {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.salaryGrade = toInteger(row.salaryGrade);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Process.csv' AS row
MERGE (n:Process {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Reward.csv' AS row
MERGE (n:Reward {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.salaryAmount = toFloat(row.salaryAmount);

LOAD CSV WITH HEADERS FROM 'file:///nodes_Rule.csv' AS row
MERGE (n:Rule {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Sensor.csv' AS row
MERGE (n:Sensor {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_State.csv' AS row
MERGE (n:State {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_System.csv' AS row
MERGE (n:System {id: row.id})
SET n.name = row.name, n.kind = row.kind;

LOAD CSV WITH HEADERS FROM 'file:///nodes_Template.csv' AS row
MERGE (n:Template {id: row.id})
SET n.name = row.name, n.kind = row.kind, n.guard = row.guard;

LOAD CSV WITH HEADERS FROM 'file:///rels_APPLIES_RULE__Employee__Rule.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Rule {id: row.to})
MERGE (a)-[r:APPLIES_RULE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_CANDIDATE_FOR__Candidate__Position.csv' AS row
MATCH (a:Candidate {id: row.from}), (b:Position {id: row.to})
MERGE (a)-[r:CANDIDATE_FOR]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_COMPLETED_COURSE__Employee__Course.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Course {id: row.to})
MERGE (a)-[r:COMPLETED_COURSE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_CONCERNS_EMPLOYEE__Event__Employee.csv' AS row
MATCH (a:Event {id: row.from}), (b:Employee {id: row.to})
MERGE (a)-[r:CONCERNS_EMPLOYEE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_DECISION_ABOUT__Decision__Employee.csv' AS row
MATCH (a:Decision {id: row.from}), (b:Employee {id: row.to})
MERGE (a)-[r:DECISION_ABOUT]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_DIRECT_MANAGER__Employee__Employee.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Employee {id: row.to})
MERGE (a)-[r:DIRECT_MANAGER]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_EVALUATES__Process__Competence.csv' AS row
MATCH (a:Process {id: row.from}), (b:Competence {id: row.to})
MERGE (a)-[r:EVALUATES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_EVALUATES_METRIC__Process__Metric.csv' AS row
MATCH (a:Process {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:EVALUATES_METRIC]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_FROM_STATE__Template__State.csv' AS row
MATCH (a:Template {id: row.from}), (b:State {id: row.to})
MERGE (a)-[r:FROM_STATE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_HAS_COMPETENCE__Employee__Competence.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Competence {id: row.to})
MERGE (a)-[r:HAS_COMPETENCE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_HAS_SUB_PROCESS__Process__Process.csv' AS row
MATCH (a:Process {id: row.from}), (b:Process {id: row.to})
MERGE (a)-[r:HAS_SUB_PROCESS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_INCLUDES_COURSE__Document__Course.csv' AS row
MATCH (a:Document {id: row.from}), (b:Course {id: row.to})
MERGE (a)-[r:INCLUDES_COURSE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_IN_STATE__Candidate__State.csv' AS row
MATCH (a:Candidate {id: row.from}), (b:State {id: row.to})
MERGE (a)-[r:IN_STATE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_IN_STATE__Employee__State.csv' AS row
MATCH (a:Employee {id: row.from}), (b:State {id: row.to})
MERGE (a)-[r:IN_STATE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_LOWERS__Decision__Metric.csv' AS row
MATCH (a:Decision {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:LOWERS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_LOWERS__Process__Metric.csv' AS row
MATCH (a:Process {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:LOWERS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_MAKES_DECISION__Employee__Decision.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Decision {id: row.to})
MERGE (a)-[r:MAKES_DECISION]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_OBSERVED_BY__Template__Sensor.csv' AS row
MATCH (a:Template {id: row.from}), (b:Sensor {id: row.to})
MERGE (a)-[r:OBSERVED_BY]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_OCCUPIES__Employee__Position.csv' AS row
MATCH (a:Employee {id: row.from}), (b:Position {id: row.to})
MERGE (a)-[r:OCCUPIES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_ON_EVENT__Template__Event.csv' AS row
MATCH (a:Template {id: row.from}), (b:Event {id: row.to})
MERGE (a)-[r:ON_EVENT]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_PERFORMS_ACTION__Template__Action.csv' AS row
MATCH (a:Template {id: row.from}), (b:Action {id: row.to})
MERGE (a)-[r:PERFORMS_ACTION]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_PLAN_FOR__Document__Employee.csv' AS row
MATCH (a:Document {id: row.from}), (b:Employee {id: row.to})
MERGE (a)-[r:PLAN_FOR]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_RAISES__Course__Metric.csv' AS row
MATCH (a:Course {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:RAISES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_RAISES__Decision__Metric.csv' AS row
MATCH (a:Decision {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:RAISES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_RAISES__Process__Metric.csv' AS row
MATCH (a:Process {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:RAISES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_RAISES__Reward__Metric.csv' AS row
MATCH (a:Reward {id: row.from}), (b:Metric {id: row.to})
MERGE (a)-[r:RAISES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_REPORTED_BY__Event__Sensor.csv' AS row
MATCH (a:Event {id: row.from}), (b:Sensor {id: row.to})
MERGE (a)-[r:REPORTED_BY]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_REQUIRES_COMPETENCE__Position__Competence.csv' AS row
MATCH (a:Position {id: row.from}), (b:Competence {id: row.to})
MERGE (a)-[r:REQUIRES_COMPETENCE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_REQUIRES_DOCUMENT__Process__Document.csv' AS row
MATCH (a:Process {id: row.from}), (b:Document {id: row.to})
MERGE (a)-[r:REQUIRES_DOCUMENT]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_RULE_LEADS_TO__Rule__Decision.csv' AS row
MATCH (a:Rule {id: row.from}), (b:Decision {id: row.to})
MERGE (a)-[r:RULE_LEADS_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_STORES_DOCUMENT__System__Document.csv' AS row
MATCH (a:System {id: row.from}), (b:Document {id: row.to})
MERGE (a)-[r:STORES_DOCUMENT]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_STORES_RECORD_OF__System__Employee.csv' AS row
MATCH (a:System {id: row.from}), (b:Employee {id: row.to})
MERGE (a)-[r:STORES_RECORD_OF]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_SUBMITTED_RESUME__Candidate__Document.csv' AS row
MATCH (a:Candidate {id: row.from}), (b:Document {id: row.to})
MERGE (a)-[r:SUBMITTED_RESUME]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels_TO_STATE__Template__State.csv' AS row
MATCH (a:Template {id: row.from}), (b:State {id: row.to})
MERGE (a)-[r:TO_STATE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);
