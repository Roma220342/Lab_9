# Результати запитів Cypher (Neo4j)

## C01
CQ C01: Які компетенції вимагає посада «Python-розробник»? | фільтр за властивістю

```cypher
MATCH (p:Position {name: 'Python-розробник'})-[:REQUIRES_COMPETENCE]->(c:Competence)
RETURN c.id AS competence, c.kind AS kind ORDER BY competence
```
Час (медіана 5 запусків): 15.2 мс

| competence | kind |
|---|---|
| pythonProgramming | HardSkill |
| teamCommunication | SoftSkill |

## C02
CQ C02: Хто безпосередній керівник Петра Бондаря? | шаблон шляху

```cypher
MATCH (:Employee {name: 'Петро Бондар'})-[:DIRECT_MANAGER]->(m:Employee)
RETURN m.name AS manager
```
Час (медіана 5 запусків): 19.1 мс

| manager |
|---|
| Іван Шевчук |

## C03
CQ C03: Скільки всього (транзитивно) підлеглих має Олена Коваль? | шлях змінної довжини

```cypher
MATCH (e:Employee)-[:DIRECT_MANAGER*1..5]->(:Employee {name: 'Олена Коваль'})
RETURN count(DISTINCT e) AS subordinates
```
Час (медіана 5 запусків): 14.1 мс

| subordinates |
|---|
| 29 |

## C04
CQ C04: Який ланцюжок підпорядкування від Петра Бондаря до Олени Коваль? | shortestPath

```cypher
MATCH (a:Employee {name: 'Петро Бондар'}), (b:Employee {name: 'Олена Коваль'}),
      p = shortestPath((a)-[:DIRECT_MANAGER*..6]->(b))
RETURN length(p) AS hops, [n IN nodes(p) | n.name] AS chain
```
Час (медіана 5 запусків): 8.3 мс

| hops | chain |
|---|---|
| 2 | ['Петро Бондар', 'Іван Шевчук', 'Олена Коваль'] |

## C05
CQ C05: Скільки співробітників і яка середня оцінка на кожній посаді? | агрегація

```cypher
MATCH (e:Employee)-[:OCCUPIES]->(p:Position)
RETURN p.name AS position, count(e) AS employees, round(avg(e.productivityScore), 2) AS avgScore
ORDER BY employees DESC
```
Час (медіана 5 запусків): 9.7 мс

| position | employees | avgScore |
|---|---|---|
| Python-розробник | 22 | 6.8 |
| Рекрутер | 3 | 5.43 |
| Керівник команди | 3 | 7.1 |
| HR-менеджер | 2 | 7.85 |

## C06
CQ C06: Хто має оцінку нижче 5 при стажі понад 12 місяців (кандидати на навчання)? | фільтри

```cypher
MATCH (e:Employee)
WHERE e.productivityScore < 5.0 AND e.tenureMonths > 12
RETURN e.name AS employee, e.productivityScore AS score, e.tenureMonths AS tenure
ORDER BY score
```
Час (медіана 5 запусків): 9.3 мс

| employee | score | tenure |
|---|---|---|
| Уляна Литвин | 3.5 | 95 |
| Оксана Яремчук | 4.1 | 15 |
| Петро Бондар | 4.2 | 44 |
| Олег Павлюк | 4.5 | 70 |
| Ярослав Вовк | 4.8 | 19 |

## C07
CQ C07: Хто з співробітників завершив курс, а хто — ні? | OPTIONAL MATCH + WITH

```cypher
MATCH (e:Employee)
OPTIONAL MATCH (e)-[:COMPLETED_COURSE]->(c:Course)
WITH e, count(c) AS courses
RETURN CASE WHEN courses > 0 THEN 'завершив курс' ELSE 'без курсу' END AS status, count(e) AS employees
ORDER BY status
```
Час (медіана 5 запусків): 14.7 мс

| status | employees |
|---|---|
| без курсу | 19 |
| завершив курс | 11 |

## C08
CQ C08: Які керівники мають щонайменше 5 безпосередніх підлеглих і яка середня оцінка команди? | WITH + агрегація

```cypher
MATCH (e:Employee)-[:DIRECT_MANAGER]->(m:Employee)
WITH m, count(e) AS team, avg(e.productivityScore) AS avgScore
WHERE team >= 5
RETURN m.name AS manager, team, round(avgScore, 2) AS avgScore ORDER BY team DESC
```
Час (медіана 5 запусків): 13.1 мс

| manager | team | avgScore |
|---|---|---|
| Іван Шевчук | 13 | 6.9 |
| Олена Коваль | 10 | 7.11 |

## C09
CQ C09 (аналіз впливу, глибина 3): Які процеси зачепить зміна кореневого процесу «Управління персоналом»?

```cypher
MATCH path = (root:Process {id: 'personnelManagement'})-[:HAS_SUB_PROCESS*1..3]->(p:Process)
RETURN p.id AS process, p.kind AS kind, length(path) AS depth ORDER BY depth, process
```
Час (медіана 5 запусків): 16.1 мс

| process | kind | depth |
|---|---|---|
| appraisal1 | Appraisal | 1 |
| motivation1 | Motivation | 1 |
| recruitment1 | Recruitment | 1 |
| training1 | Training | 1 |
| attestation2026 | Attestation | 2 |
| interview1 | Interview | 2 |
| onboarding1 | Onboarding | 2 |

## C10
CQ C10 (аналіз впливу, глибина 4): Кого зачепить зміна вимог до компетенції «negotiation» (компетенція <- посада <- співробітник -> керівник ланцюжком до 2 рівнів)?

```cypher
MATCH (c:Competence {id: 'negotiation'})<-[:REQUIRES_COMPETENCE]-(p:Position)<-[:OCCUPIES]-(e:Employee)
OPTIONAL MATCH (e)-[:DIRECT_MANAGER*1..2]->(m:Employee)
RETURN p.name AS position, count(DISTINCT e) AS affectedEmployees, collect(DISTINCT m.name) AS managersToNotify
ORDER BY affectedEmployees DESC
```
Час (медіана 5 запусків): 16.4 мс

| position | affectedEmployees | managersToNotify |
|---|---|---|
| Рекрутер | 3 | ['Назар Кузьмич', 'Олена Коваль', 'Роман Остапчук'] |
| Керівник команди | 3 | ['Олена Коваль'] |
| HR-менеджер | 2 | ['Олена Коваль'] |

## Ручна перевірка (перерахунок із CSV без Cypher)

- C03: збіг = **True**

- C05: збіг = **True**

- C08: збіг = **True**
