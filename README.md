# ЛР 9. Графова база знань у Neo4j

## Вимоги
Docker Desktop, Python 3.12+. Версії: Neo4j 5.26 Enterprise (evaluation) + GDS, `neo4j` 5.28, rdflib 7.6, seed = 42.

## Запуск з нуля
```bash
cd ЛР9_артефакти
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env                      # задайте NEO4J_PASSWORD
python scripts/build_data.py                # data/*.csv, import/02_import.cypher, docs/graph_schema.png
docker compose up -d                        # Neo4j Browser: http://localhost:7474 (зачекайте ~40 с)
python scripts/run_all.py                   # результати 2–5 -> results/, docs/, tests/, claims/, llm_log/
```
Окремий результат: `python scripts/run_all.py --only r4`.
Text-to-Cypher: за замовчуванням беруться запити з `tests/t2c_llm_offline.jsonl` (згенеровані LLM у чат-сесії, як у ЛР 8);
`--live-llm` викликає API (ключ лише у змінній `ANTHROPIC_API_KEY`, у код не потрапляє).

## Скріншоти для звіту (Neo4j Browser, http://localhost:7474)
Виконуйте запити по одному й робіть знімки. Файли — у `import/` та `queries/`.

| № | Що зняти | Звідки |
|---|---|---|
| 1 | `SHOW CONSTRAINTS` і `SHOW INDEXES` | Результат 2 |
| 2 | Помилка `ConstraintValidationFailed` | `import/03_constraint_violation.cypher` (перший CREATE) |
| 3 | Лічильники: `MATCH (n) RETURN count(n)` і `MATCH ()-[r]->() RETURN count(r)` після 1-го та 2-го імпорту | Результат 2 (також `docs/import_log.md`) |
| 4 | Візуальний граф: `MATCH p=(e:Employee {id:'petro'})-[*..2]-() RETURN p LIMIT 60` | Результат 1/3 |
| 5 | C04 (shortestPath) у режимі Graph | `queries/C04.cypher` |
| 6 | C10 (аналіз впливу) | `queries/C10.cypher` |
| 7 | PROFILE P1 до/після (плани NodeByLabelScan → NodeIndexSeek) | `queries/P1_*.cypher` (спершу створіть 2000 :Bench вузлів — це робить `run_all.py --only r4`; у Browser виконайте `DROP INDEX employee_name` для «до») |
| 8 | PROFILE P2 до/після | `queries/P2_*.cypher` |
| 9 | Топ-10 PageRank і спільноти Louvain | `import/04_gds.cypher` |
| 10 | `SHOW ROLE t2c_reader PRIVILEGES` | `import/05_readonly_role.cypher` |

Готові рисунки: `docs/graph_schema.png`, `docs/fig_counts.png`, `docs/fig_pagerank.png`.

## Примітки
- Чернетка звіту має 108 вузлів / 312 зв'язків (kb.ttl ЛР 8, якого немає на диску); скрипт відтворює дані з ЛР 7 + 24 синтетичні
  співробітники (104 / 319). Після запуску числа у звіті треба замінити на фактичні з `results/r2_import.json`.
- Роль лише для читання потребує Enterprise; на Community скрипт використовує `execute_read` і зазначає це у `results/r5_t2c.json`.
- `:Bench` вузли створюються й видаляються автоматично лише на час PROFILE.
