# Аналіз графа (Neo4j GDS)

## Проєкція
| graphName | nodeCount | relationshipCount |
|---|---|---|
| kg | 104 | 638 |

## PageRank — топ-10
| id | label | name | pagerank |
|---|---|---|---|
| stateActive | State | stateActive | 4.6632 |
| hris1 | System | hris1 | 4.2394 |
| pythonDeveloperPost | Position | Python-розробник | 3.1176 |
| negotiation | Competence | negotiation | 2.7222 |
| teamCommunication | Competence | teamCommunication | 2.508 |
| ivan | Employee | Іван Шевчук | 2.4881 |
| olena | Employee | Олена Коваль | 2.1851 |
| pythonProgramming | Competence | pythonProgramming | 2.1684 |
| sensorLMS | Sensor | sensorLMS | 2.1258 |
| productivityQ3 | Metric | productivityQ3 | 1.9816 |

## Louvain
| communityCount | modularity | nodePropertiesWritten |
|---|---|---|
| 8 | 0.33553129391417147 | 104 |

### Спільноти
| community | size | composition |
|---|---|---|
| 45 | 24 | ['Employee: 17', 'Course: 2', 'System: 2', 'Document: 1', 'Position: 1', 'State: 1'] |
| 98 | 17 | ['Event: 7', 'Action: 3', 'Template: 3', 'State: 2', 'Employee: 1', 'Sensor: 1'] |
| 72 | 14 | ['Employee: 6', 'Competence: 2', 'Position: 2', 'Candidate: 1', 'Decision: 1', 'Document: 1', 'Rule: 1'] |
| 101 | 13 | ['Event: 10', 'Action: 1', 'Sensor: 1', 'Template: 1'] |
| 81 | 12 | ['Process: 7', 'Metric: 2', 'Decision: 1', 'Document: 1', 'Reward: 1'] |
| 87 | 12 | ['State: 3', 'Action: 2', 'Event: 2', 'Template: 2', 'Candidate: 1', 'Document: 1', 'Sensor: 1'] |
| 77 | 11 | ['Employee: 6', 'Competence: 2', 'Metric: 1', 'Position: 1', 'Process: 1'] |
| 85 | 1 | ['Reward: 1'] |

## Збереження у графі
| withPagerank | communities |
|---|---|
| 104 | 8 |

## PROFILE до/після
| запит | dbHits | мс | рядки | оператори |
|---|---|---|---|---|
| P1_before | 6093 | 431.9 | [{'e.id': 'bench1999'}] | ProduceResults@neo4j → Projection@neo4j → Filter@neo4j → NodeByLabelScan@neo4j |
| P2_before | 19094 | 1267.0 | [{'pairs': 81771}] | ProduceResults@neo4j → EagerAggregation@neo4j → ValueHashJoin@neo4j → Apply@neo4j → CartesianProduct@neo4j → Filter@neo4j → NodeByLabelScan@neo4j → NodeByLabelScan@neo4j → Limit@neo4j → Expand(Into)@neo4j → Argument@neo4j → Apply@neo4j → CartesianProduct@neo4j → Filter@neo4j → NodeByLabelScan@neo4j → NodeByLabelScan@neo4j → Limit@neo4j → Expand(Into)@neo4j → Argument@neo4j |
| P1_after | 4 | 138.0 | [{'e.id': 'bench1999'}] | ProduceResults@neo4j → Projection@neo4j → NodeIndexSeek@neo4j |
| P2_after | 4540 | 427.7 | [{'pairs': 81771}] | ProduceResults@neo4j → EagerAggregation@neo4j → Filter@neo4j → NodeHashJoin@neo4j → Filter@neo4j → Expand(All)@neo4j → NodeIndexSeekByRange@neo4j → Expand(All)@neo4j → NodeIndexSeekByRange@neo4j |
