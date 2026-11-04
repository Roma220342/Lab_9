# ЛР 9. Графова база знань у Neo4j

## Вимоги

- Docker Desktop
- Python 3.12+
- Neo4j 5.26 Enterprise (Evaluation) + GDS
- Python-бібліотека `neo4j` 5.28
- `rdflib` 7.6

## Запуск проєкту

1. Перейдіть до папки проєкту:

```bash
cd ЛР9_артефакти
```

2. Створіть та активуйте віртуальне середовище:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Встановіть залежності:

```bash
pip install -r requirements.txt
```

4. Створіть файл конфігурації та задайте пароль для Neo4j:

```bash
copy .env.example .env
```

5. Підготуйте дані та необхідні файли:

```bash
python scripts/build_data.py
```

6. Запустіть Neo4j через Docker:

```bash
docker compose up -d
```

Neo4j Browser буде доступний за адресою: http://localhost:7474

Після запуску зачекайте приблизно 40 секунд, поки база даних стане доступною.

7. Запустіть усі етапи роботи:

```bash
python scripts/run_all.py
```

Результати виконання зберігаються у відповідних папках `results/`, `docs/`, `tests/`, `claims/` та `llm_log/`.

Для запуску окремого етапу:

```bash
python scripts/run_all.py --only r4
```

## Text-to-Cypher

Для перевірки Text-to-Cypher використовуються підготовлені запити з файлу `tests/t2c_llm_offline.jsonl`.

Також доступний режим генерації запитів через API:

```bash
python scripts/run_all.py --live-llm
```

Для цього необхідно задати змінну середовища `ANTHROPIC_API_KEY`. API-ключ зберігається у змінних середовища та не додається до коду проєкту.

## Скріншоти для звіту

Усі запити виконуються в Neo4j Browser (http://localhost:7474). Кожен запит потрібно запускати окремо та зберігати скриншот результату.

| № | Що потрібно показати | Файл або запит |
|---|---|---|
| 1 | Створені обмеження та індекси | `SHOW CONSTRAINTS` і `SHOW INDEXES` |
| 2 | Помилка порушення обмеження унікальності | `import/03_constraint_violation.cypher` (перший CREATE) |
| 3 | Кількість вузлів і зв'язків після першого та другого імпорту | `MATCH (n) RETURN count(n)` і `MATCH ()-[r]->() RETURN count(r)` |
| 4 | Візуалізація графа співробітника та його зв'язків | `MATCH p=(e:Employee {id:'petro'})-[*..2]-() RETURN p LIMIT 60` |
| 5 | Пошук найкоротшого шляху (shortestPath) | `queries/C04.cypher` |
| 6 | Аналіз впливу у графі | `queries/C10.cypher` |
| 7 | Порівняння PROFILE P1 до та після створення індексу | `queries/P1_*.cypher` |
| 8 | Порівняння PROFILE P2 до та після створення індексу | `queries/P2_*.cypher` |
| 9 | Результати PageRank та виявлення спільнот Louvain | `import/04_gds.cypher` |
| 10 | Привілеї ролі лише для читання | `SHOW ROLE t2c_reader PRIVILEGES` |

### Додаткові інструкції для PROFILE

Перед виконанням PROFILE P1 необхідно створити тестові вузли:

```bash
python scripts/run_all.py --only r4
```

Для отримання плану виконання до створення індексу виконайте в Neo4j Browser:

```cypher
DROP INDEX employee_name
```

Після цього зробіть скриншот результату PROFILE P1. Далі створіть індекс і повторіть запит для порівняння планів виконання.

## Додаткові матеріали

У папці `docs/` знаходяться графічні матеріали:

- `graph_schema.png` — схема графової бази знань.
- `fig_counts.png` — діаграма кількості вузлів та зв'язків.
- `fig_pagerank.png` — візуалізація результатів PageRank.

## Примітки

- Для створення ролі лише для читання потрібна версія Neo4j Enterprise. У Community Edition використовується механізм `execute_read`.
- Тестові вузли `:Bench`, необхідні для PROFILE, створюються та видаляються автоматично під час виконання відповідного етапу.
- Після завершення роботи результати всіх етапів доступні у папці `results/`.