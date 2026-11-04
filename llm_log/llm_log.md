# Журнал LLM (ЛР 9)

- Дата: 2026-11-04
- Модель: claude-opus-5-5 (сесія Claude Code, підказка v1)
- Параметри: temperature=за замовчуванням (чат); seed не підтримується
- Версія підказки: v1
- Сирий вихід: tests/t2c_results.jsonl
- Рішення людини: підтверджено 10 із 13

## Підказка
```
Роль: консультант з графового моделювання. Перетвори питання українською на ОДИН запит Cypher для Neo4j 5.
Мітки вузлів: Action, Candidate, Competence, Course, Decision, Document, Employee, Event, Metric, Position, Process, Reward, Rule, Sensor, State, System, Template.
Дозволені шаблони зв'язків:
(:Employee)-[:APPLIES_RULE]->(:Rule)
(:Candidate)-[:CANDIDATE_FOR]->(:Position)
(:Employee)-[:COMPLETED_COURSE]->(:Course)
(:Event)-[:CONCERNS_EMPLOYEE]->(:Employee)
(:Decision)-[:DECISION_ABOUT]->(:Employee)
(:Employee)-[:DIRECT_MANAGER]->(:Employee)
(:Process)-[:EVALUATES]->(:Competence)
(:Process)-[:EVALUATES_METRIC]->(:Metric)
(:Template)-[:FROM_STATE]->(:State)
(:Employee)-[:HAS_COMPETENCE]->(:Competence)
(:Process)-[:HAS_SUB_PROCESS]->(:Process)
(:Document)-[:INCLUDES_COURSE]->(:Course)
(:Candidate)-[:IN_STATE]->(:State)
(:Employee)-[:IN_STATE]->(:State)
(:Decision)-[:LOWERS]->(:Metric)
(:Process)-[:LOWERS]->(:Metric)
(:Employee)-[:MAKES_DECISION]->(:Decision)
(:Template)-[:OBSERVED_BY]->(:Sensor)
(:Employee)-[:OCCUPIES]->(:Position)
(:Template)-[:ON_EVENT]->(:Event)
(:Template)-[:PERFORMS_ACTION]->(:Action)
(:Document)-[:PLAN_FOR]->(:Employee)
(:Course)-[:RAISES]->(:Metric)
(:Decision)-[:RAISES]->(:Metric)
(:Process)-[:RAISES]->(:Metric)
(:Reward)-[:RAISES]->(:Metric)
(:Event)-[:REPORTED_BY]->(:Sensor)
(:Position)-[:REQUIRES_COMPETENCE]->(:Competence)
(:Process)-[:REQUIRES_DOCUMENT]->(:Document)
(:Rule)-[:RULE_LEADS_TO]->(:Decision)
(:System)-[:STORES_DOCUMENT]->(:Document)
(:System)-[:STORES_RECORD_OF]->(:Employee)
(:Candidate)-[:SUBMITTED_RESUME]->(:Document)
(:Template)-[:TO_STATE]->(:State)
Ідентифікатор вузла — властивість id, людська назва — name. Поверни лише запит, без пояснень.
```
