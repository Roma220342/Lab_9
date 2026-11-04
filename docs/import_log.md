# Журнал імпорту (2026-11-04 17:16)

## Запуски імпорту
| run | nodes | rels | seconds |
|---|---|---|---|
| 1 | 104 | 319 | 19.01 |
| 2 | 104 | 319 | 2.87 |

Ідемпотентність: **True**

## SHOW CONSTRAINTS
| name | type | labelsOrTypes | properties |
|---|---|---|---|
| action_id | UNIQUENESS | ['Action'] | ['id'] |
| candidate_id | UNIQUENESS | ['Candidate'] | ['id'] |
| competence_id | UNIQUENESS | ['Competence'] | ['id'] |
| course_id | UNIQUENESS | ['Course'] | ['id'] |
| decision_id | UNIQUENESS | ['Decision'] | ['id'] |
| document_id | UNIQUENESS | ['Document'] | ['id'] |
| employee_empid | UNIQUENESS | ['Employee'] | ['employeeId'] |
| employee_id | UNIQUENESS | ['Employee'] | ['id'] |
| event_id | UNIQUENESS | ['Event'] | ['id'] |
| metric_id | UNIQUENESS | ['Metric'] | ['id'] |
| position_id | UNIQUENESS | ['Position'] | ['id'] |
| process_id | UNIQUENESS | ['Process'] | ['id'] |
| reward_id | UNIQUENESS | ['Reward'] | ['id'] |
| rule_id | UNIQUENESS | ['Rule'] | ['id'] |
| sensor_id | UNIQUENESS | ['Sensor'] | ['id'] |
| state_id | UNIQUENESS | ['State'] | ['id'] |
| system_id | UNIQUENESS | ['System'] | ['id'] |
| template_id | UNIQUENESS | ['Template'] | ['id'] |

## SHOW INDEXES
| name | type | labelsOrTypes | properties | state |
|---|---|---|---|---|
| action_id | RANGE | ['Action'] | ['id'] | ONLINE |
| candidate_id | RANGE | ['Candidate'] | ['id'] | ONLINE |
| competence_id | RANGE | ['Competence'] | ['id'] | ONLINE |
| competence_name | RANGE | ['Competence'] | ['name'] | ONLINE |
| course_id | RANGE | ['Course'] | ['id'] | ONLINE |
| decision_id | RANGE | ['Decision'] | ['id'] | ONLINE |
| document_id | RANGE | ['Document'] | ['id'] | ONLINE |
| employee_empid | RANGE | ['Employee'] | ['employeeId'] | ONLINE |
| employee_id | RANGE | ['Employee'] | ['id'] | ONLINE |
| employee_name | RANGE | ['Employee'] | ['name'] | ONLINE |
| employee_score | RANGE | ['Employee'] | ['productivityScore'] | ONLINE |
| event_id | RANGE | ['Event'] | ['id'] | ONLINE |
| metric_id | RANGE | ['Metric'] | ['id'] | ONLINE |
| position_id | RANGE | ['Position'] | ['id'] | ONLINE |
| position_name | RANGE | ['Position'] | ['name'] | ONLINE |
| process_id | RANGE | ['Process'] | ['id'] | ONLINE |
| rel_source | RANGE | ['DIRECT_MANAGER'] | ['source'] | ONLINE |
| reward_id | RANGE | ['Reward'] | ['id'] | ONLINE |
| rule_id | RANGE | ['Rule'] | ['id'] | ONLINE |
| sensor_id | RANGE | ['Sensor'] | ['id'] | ONLINE |
| state_id | RANGE | ['State'] | ['id'] | ONLINE |
| system_id | RANGE | ['System'] | ['id'] | ONLINE |
| template_id | RANGE | ['Template'] | ['id'] | ONLINE |

## Порушення обмежень

```cypher
CREATE (:Employee {id: 'petro', name: 'Дублікат Петра'})
```
`Neo.ClientError.Schema.ConstraintValidationFailed`: Node(48) already exists with label `Employee` and property `id` = 'petro'

```cypher
CREATE (:Employee {id: 'dup_e003', employeeId: 'E-003', name: 'Дублікат E-003'})
```
`Neo.ClientError.Schema.ConstraintValidationFailed`: Node(48) already exists with label `Employee` and property `employeeId` = 'E-003'

## Вузли за мітками
| label | n |
|---|---|
| Action | 6 |
| Candidate | 2 |
| Competence | 4 |
| Course | 2 |
| Decision | 2 |
| Document | 4 |
| Employee | 30 |
| Event | 19 |
| Metric | 3 |
| Position | 4 |
| Process | 8 |
| Reward | 2 |
| Rule | 1 |
| Sensor | 3 |
| State | 6 |
| System | 2 |
| Template | 6 |

## Зв'язки за типами
| type | n |
|---|---|
| HAS_COMPETENCE | 64 |
| STORES_RECORD_OF | 41 |
| IN_STATE | 31 |
| OCCUPIES | 30 |
| DIRECT_MANAGER | 29 |
| CONCERNS_EMPLOYEE | 19 |
| REPORTED_BY | 19 |
| COMPLETED_COURSE | 11 |
| RAISES | 7 |
| REQUIRES_COMPETENCE | 7 |
| HAS_SUB_PROCESS | 7 |
| FROM_STATE | 6 |
| OBSERVED_BY | 6 |
| ON_EVENT | 6 |
| PERFORMS_ACTION | 6 |
| TO_STATE | 6 |
| STORES_DOCUMENT | 4 |
| CANDIDATE_FOR | 2 |
| SUBMITTED_RESUME | 2 |
| DECISION_ABOUT | 2 |
| LOWERS | 2 |
| INCLUDES_COURSE | 2 |
| MAKES_DECISION | 2 |
| EVALUATES_METRIC | 2 |
| EVALUATES | 2 |
| PLAN_FOR | 1 |
| APPLIES_RULE | 1 |
| REQUIRES_DOCUMENT | 1 |
| RULE_LEADS_TO | 1 |
