"""ЛР 9: повний прогін у Neo4j 5 + GDS. Результати -> results/*.json, docs/*.md, docs/*.png.

    python scripts/run_all.py            # усі результати 2–5
    python scripts/run_all.py --only r4  # лише один результат (r2|r3|r4|r5)
    python scripts/run_all.py --live-llm # text-to-Cypher через Anthropic API (потрібен ANTHROPIC_API_KEY)

Підключення: змінні NEO4J_URI (bolt://localhost:7687), NEO4J_USER (neo4j), NEO4J_PASSWORD (з .env).
"""
import argparse
import csv
import json
import os
import random
import re
import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"; DOCS = ROOT / "docs"
RES.mkdir(exist_ok=True); DOCS.mkdir(exist_ok=True)
SEED = 42


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def statements(path: Path):
    text = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines()
                     if not l.strip().startswith("//") and not l.strip().startswith(":"))
    return [s.strip() for s in text.split(";") if s.strip()]


def query_text(path: Path):
    return "\n".join(l for l in path.read_text(encoding="utf-8").splitlines() if not l.strip().startswith("//")).strip()


def header(path: Path):
    return " ".join(l.strip("/ ").strip() for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("//"))


def run(drv, q, **params):
    with drv.session() as s:
        r = s.run(q, **params)
        rows = [rec.data() for rec in r]
        summ = r.consume()
    return rows, summ


def counts(drv):
    n = run(drv, "MATCH (n) RETURN count(n) AS n")[0][0]["n"]
    r = run(drv, "MATCH ()-[r]->() RETURN count(r) AS n")[0][0]["n"]
    return n, r


def dump(name, obj):
    (RES / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def md_table(rows, cols=None):
    if not rows:
        return "_(порожньо)_\n"
    cols = cols or list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- Результат 2
def r2(drv):
    print("== Результат 2: обмеження, індекси, імпорт")
    run(drv, "MATCH (n) DETACH DELETE n")
    for s in statements(ROOT / "import/01_constraints_indexes.cypher"):
        run(drv, s)
    run(drv, "CALL db.awaitIndexes(300)")
    cons = run(drv, "SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties")[0]
    idx = run(drv, "SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state WHERE type <> 'LOOKUP'")[0]
    imp = statements(ROOT / "import/02_import.cypher")
    runs = []
    for i in (1, 2):
        t = time.perf_counter()
        for s in imp:
            run(drv, s)
        n, r = counts(drv)
        runs.append({"run": i, "nodes": n, "rels": r, "seconds": round(time.perf_counter() - t, 2)})
        print(f"   імпорт #{i}: {n} вузлів, {r} зв'язків")
    by_label = run(drv, "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY label")[0]
    by_type = run(drv, "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS n ORDER BY n DESC")[0]
    viol = []
    for s in statements(ROOT / "import/03_constraint_violation.cypher"):
        try:
            run(drv, s); viol.append({"query": s, "error": None})
        except Neo4jError as e:
            viol.append({"query": s, "code": e.code, "message": e.message})
            print(f"   порушення: {e.code}")
    out = {"constraints": cons, "indexes": idx, "import_runs": runs, "idempotent": runs[0]["nodes"] == runs[1]["nodes"]
           and runs[0]["rels"] == runs[1]["rels"], "by_label": by_label, "by_type": by_type, "violations": viol}
    dump("r2_import", out)
    plot_counts(by_label, by_type)
    with open(DOCS / "import_log.md", "w", encoding="utf-8") as f:
        f.write(f"# Журнал імпорту ({datetime.now():%Y-%m-%d %H:%M})\n\n## Запуски імпорту\n" + md_table(runs))
        f.write(f"\nІдемпотентність: **{out['idempotent']}**\n\n## SHOW CONSTRAINTS\n" + md_table(cons))
        f.write("\n## SHOW INDEXES\n" + md_table(idx) + "\n## Порушення обмежень\n")
        for v in viol:
            f.write(f"\n```cypher\n{v['query']}\n```\n`{v.get('code')}`: {v.get('message')}\n")
        f.write("\n## Вузли за мітками\n" + md_table(by_label) + "\n## Зв'язки за типами\n" + md_table(by_type))


def plot_counts(by_label, by_type):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    ax[0].barh([r["label"] for r in by_label], [r["n"] for r in by_label], color="#4c78a8")
    ax[0].set_title("Вузли за мітками"); ax[0].invert_yaxis()
    ax[1].barh([r["type"] for r in by_type], [r["n"] for r in by_type], color="#f58518")
    ax[1].set_title("Зв'язки за типами"); ax[1].invert_yaxis(); ax[1].tick_params(labelsize=7)
    fig.tight_layout(); fig.savefig(DOCS / "fig_counts.png", dpi=150); plt.close(fig)


# ---------------------------------------------------------------- Результат 3
def timed(drv, q, reps=5):
    rows, _ = run(drv, q)
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); run(drv, q); ts.append((time.perf_counter() - t) * 1000)
    return rows, round(statistics.median(ts), 1)


def manual_checks():
    """Незалежний перерахунок C03, C05, C08 із CSV без Cypher."""
    d = ROOT / "data"
    emp = {r["id"]: r for r in csv.DictReader(open(d / "nodes_Employee.csv", encoding="utf-8"))}
    pos = {r["id"]: r for r in csv.DictReader(open(d / "nodes_Position.csv", encoding="utf-8"))}
    mgr = {r["from"]: r["to"] for r in csv.DictReader(open(d / "rels_DIRECT_MANAGER__Employee__Employee.csv", encoding="utf-8"))}
    occ = {r["from"]: r["to"] for r in csv.DictReader(open(d / "rels_OCCUPIES__Employee__Position.csv", encoding="utf-8"))}
    olena = next(k for k, v in emp.items() if v["name"] == "Олена Коваль")

    def reaches(e, target, depth=5):
        while depth and e in mgr:
            e = mgr[e]; depth -= 1
            if e == target:
                return True
        return False
    c03 = sum(reaches(e, olena) for e in emp)
    agg = defaultdict(list)
    for e, p in occ.items():
        agg[pos[p]["name"]].append(float(emp[e]["productivityScore"]))
    c05 = sorted(({"position": k, "employees": len(v), "avgScore": round(sum(v) / len(v), 2)} for k, v in agg.items()),
                 key=lambda r: -r["employees"])
    team = defaultdict(list)
    for e, m in mgr.items():
        team[m].append(float(emp[e]["productivityScore"]))
    c08 = sorted(({"manager": emp[m]["name"], "team": len(v), "avgScore": round(sum(v) / len(v), 2)}
                  for m, v in team.items() if len(v) >= 5), key=lambda r: -r["team"])
    return {"C03": [{"subordinates": c03}], "C05": c05, "C08": c08}


def same(a, b):
    norm = lambda rows: sorted(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()},
                                          ensure_ascii=False, sort_keys=True) for r in rows)
    return norm(a) == norm(b)


def r3(drv):
    print("== Результат 3: запити Cypher")
    out = []
    for f in sorted((ROOT / "queries").glob("C*.cypher")):
        rows, ms = timed(drv, query_text(f))
        out.append({"id": f.stem, "cq": header(f), "query": query_text(f), "rows": rows, "ms": ms})
        print(f"   {f.stem}: {len(rows)} рядків, {ms} мс")
    man = manual_checks()
    checks = [{"id": k, "match": same(next(o["rows"] for o in out if o["id"] == k), v), "manual": v} for k, v in man.items()]
    dump("r3_queries", {"queries": out, "manual_checks": checks})
    with open(DOCS / "cypher_results.md", "w", encoding="utf-8") as f:
        f.write("# Результати запитів Cypher (Neo4j)\n")
        for o in out:
            f.write(f"\n## {o['id']}\n{o['cq']}\n\n```cypher\n{o['query']}\n```\nЧас (медіана 5 запусків): {o['ms']} мс\n\n"
                    + md_table(o["rows"]))
        f.write("\n## Ручна перевірка (перерахунок із CSV без Cypher)\n")
        for c in checks:
            f.write(f"\n- {c['id']}: збіг = **{c['match']}**\n")


# ---------------------------------------------------------------- Результат 4
def plan_ops(p, acc=None):
    acc = acc if acc is not None else []
    acc.append({"op": p.get("operatorType"), "rows": p.get("rows"), "dbHits": p.get("dbHits")})
    for c in p.get("children", []):
        plan_ops(c, acc)
    return acc


def profile(drv, q):
    t = time.perf_counter()
    rows, s = run(drv, q)
    ms = round((time.perf_counter() - t) * 1000, 1)
    ops = plan_ops(s.profile)
    return {"rows": rows, "ms": ms, "dbHits": sum(o["dbHits"] or 0 for o in ops),
            "operators": [o["op"] for o in ops], "plan": ops}


def r4(drv):
    print("== Результат 4: PROFILE та GDS")
    rnd = random.Random(SEED)
    positions = [r["id"] for r in run(drv, "MATCH (p:Position) RETURN p.id AS id")[0]]
    bench = [{"id": f"bench{i:04d}", "name": f"Бенчмарк {i}", "score": round(rnd.uniform(3, 10), 1),
              "pos": rnd.choice(positions)} for i in range(2000)]
    run(drv, """UNWIND $rows AS r CREATE (e:Employee:Bench {id: r.id, name: r.name, productivityScore: r.score})
                WITH e, r MATCH (p:Position {id: r.pos}) CREATE (e)-[:OCCUPIES]->(p)""", rows=bench)
    print("   додано 2000 тимчасових вузлів :Bench для профілювання")
    run(drv, "DROP INDEX employee_name IF EXISTS"); run(drv, "DROP INDEX employee_score IF EXISTS")
    prof = {}
    for k in ("P1", "P2"):
        prof[f"{k}_before"] = profile(drv, query_text(ROOT / f"queries/{k}_before.cypher"))
    run(drv, "CREATE INDEX employee_name IF NOT EXISTS FOR (n:Employee) ON (n.name)")
    run(drv, "CREATE INDEX employee_score IF NOT EXISTS FOR (n:Employee) ON (n.productivityScore)")
    run(drv, "CALL db.awaitIndexes(300)")
    for k in ("P1", "P2"):
        prof[f"{k}_after"] = profile(drv, query_text(ROOT / f"queries/{k}_after.cypher"))
    for k, v in prof.items():
        print(f"   {k}: dbHits={v['dbHits']}, {v['ms']} мс, оператори={v['operators'][:4]}…")
    run(drv, "MATCH (e:Bench) DETACH DELETE e")

    st = statements(ROOT / "import/04_gds.cypher")
    run(drv, st[0]); proj = run(drv, st[1])[0]
    top10 = run(drv, st[2])[0]; prw = run(drv, st[3])[0]; louv = run(drv, st[4])[0]
    comm = run(drv, st[5])[0]; check = run(drv, st[6])[0]
    print(f"   Louvain: {louv[0]['communityCount']} спільнот, модулярність {louv[0]['modularity']:.3f}")
    dump("r4_gds", {"profile": prof, "projection": proj, "pagerank_top10": top10, "pagerank_write": prw,
                    "louvain": louv, "communities": comm, "stored_check": check})
    plot_pagerank(top10)
    with open(DOCS / "gds_report.md", "w", encoding="utf-8") as f:
        f.write("# Аналіз графа (Neo4j GDS)\n\n## Проєкція\n" + md_table(proj) + "\n## PageRank — топ-10\n" + md_table(top10))
        f.write("\n## Louvain\n" + md_table(louv) + "\n### Спільноти\n" + md_table(comm))
        f.write("\n## Збереження у графі\n" + md_table(check) + "\n## PROFILE до/після\n")
        f.write(md_table([{"запит": k, "dbHits": v["dbHits"], "мс": v["ms"], "рядки": v["rows"],
                           "оператори": " → ".join(v["operators"])} for k, v in prof.items()]))


def plot_pagerank(top10):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh([f"{r['name']} ({r['label']})" for r in top10], [r["pagerank"] for r in top10], color="#54a24b")
    ax.invert_yaxis(); ax.set_xlabel("PageRank"); ax.set_title("PageRank (GDS), топ-10 вузлів")
    fig.tight_layout(); fig.savefig(DOCS / "fig_pagerank.png", dpi=150); plt.close(fig)


# ---------------------------------------------------------------- Результат 5
SPARQL_PREFIX = "PREFIX hr: <http://example.org/hr#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
EMP = "VALUES ?cls { hr:Employee hr:Manager hr:Recruiter } ?e a ?cls ."
PAIRS = [
    ("T05", "Хто є безпосереднім керівником Петра Бондаря?",
     "SELECT ?name WHERE { ?e hr:fullName ?n ; hr:directManager ?m . FILTER(STR(?n) = \"Петро Бондар\") ?m hr:fullName ?name }",
     "MATCH (:Employee {name:'Петро Бондар'})-[:DIRECT_MANAGER]->(m) RETURN m.name AS name"),
    ("T08", "Хто транзитивно підпорядкований Івану?",
     "SELECT DISTINCT ?e WHERE { ?e hr:directManager+ hr:ivan }",
     "MATCH (e:Employee)-[:DIRECT_MANAGER*1..10]->(:Employee {id:'ivan'}) RETURN DISTINCT e.id AS e"),
    ("T13", "Який керівник має найбільше безпосередніх підлеглих?",
     "SELECT ?m (COUNT(?e) AS ?n) WHERE { ?e hr:directManager ?m } GROUP BY ?m ORDER BY DESC(?n) LIMIT 1",
     "MATCH (e)-[:DIRECT_MANAGER]->(m) RETURN m.id AS m, count(e) AS n ORDER BY n DESC LIMIT 1"),
    ("T16", "Для кожної посади: скільки співробітників мають оцінку ≥ 7?",
     "SELECT ?t (COUNT(?e) AS ?n) WHERE { ?e hr:occupies ?p ; hr:productivityScore ?s . ?p hr:positionTitle ?t "
     "FILTER(?s >= 7) } GROUP BY ?t",
     "MATCH (e:Employee)-[:OCCUPIES]->(p:Position) WHERE e.productivityScore >= 7 RETURN p.name AS t, count(e) AS n"),
    ("T19", "Хто пропрацював в організації понад 60 місяців?",
     "SELECT ?e WHERE { " + EMP + " ?e hr:tenureMonths ?t FILTER(?t > 60) }",
     "MATCH (e:Employee) WHERE e.tenureMonths > 60 RETURN e.id AS e"),
]


def r5(drv, live):
    print("== Результат 5: SPARQL vs Cypher, text-to-Cypher")
    from rdflib import Graph
    g = Graph(); g.parse(ROOT / "data/kb.ttl")
    cmp_rows = []
    for tid, q, sp, cy in PAIRS:
        t = time.perf_counter(); srows = list(g.query(SPARQL_PREFIX + sp)); sms = (time.perf_counter() - t) * 1000
        crows, cms = timed(drv, cy, reps=3)
        sv = sorted(tuple(str(x).split("#")[-1] for x in r) for r in srows)
        cv = sorted(tuple(str(x) for x in r.values()) for r in crows)
        cmp_rows.append({"id": tid, "question": q, "sparql": sp, "cypher": cy, "rows_sparql": len(srows),
                         "rows_cypher": len(crows), "equal_values": sv == cv, "ms_sparql": round(sms, 1),
                         "ms_cypher": cms, "len_sparql": len(sp), "len_cypher": len(cy)})
        print(f"   {tid}: SPARQL {len(srows)} / Cypher {len(crows)} рядків, збіг значень={sv == cv}")
    dump("r5_sparql_vs_cypher", cmp_rows)
    with open(DOCS / "sparql_vs_cypher.md", "w", encoding="utf-8") as f:
        f.write("# SPARQL (rdflib, kb.ttl) vs Cypher (Neo4j)\n\n" + md_table(
            cmp_rows, ["id", "question", "rows_sparql", "rows_cypher", "equal_values", "ms_sparql", "ms_cypher",
                       "len_sparql", "len_cypher"]))
        for r in cmp_rows:
            f.write(f"\n### {r['id']}\n```sparql\n{r['sparql']}\n```\n```cypher\n{r['cypher']}\n```\n")
    t2c(drv, live)


WRITE_RE = re.compile(r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|LOAD\s+CSV|CALL\s+dbms|CALL\s+apoc)\b", re.I)


def schema_info(drv):
    labels = {r["label"] for r in run(drv, "CALL db.labels() YIELD label")[0]}
    types = {r["relationshipType"] for r in run(drv, "CALL db.relationshipTypes() YIELD relationshipType")[0]}
    props = {r["propertyKey"] for r in run(drv, "CALL db.propertyKeys() YIELD propertyKey")[0]}
    pat = run(drv, "MATCH (a)-[r]->(b) RETURN DISTINCT labels(a)[0] AS a, type(r) AS t, labels(b)[0] AS b ORDER BY t")[0]
    return labels, types, props, pat


def prompt_v1(labels, pat):
    rels = "\n".join(f"(:{p['a']})-[:{p['t']}]->(:{p['b']})" for p in pat)
    return ("Роль: консультант з графового моделювання. Перетвори питання українською на ОДИН запит Cypher для Neo4j 5.\n"
            f"Мітки вузлів: {', '.join(sorted(labels))}.\nДозволені шаблони зв'язків:\n{rels}\n"
            "Ідентифікатор вузла — властивість id, людська назва — name. Поверни лише запит, без пояснень.")


def llm_queries(questions, prompt, live):
    if not live:
        off = {j["id"]: j for j in map(json.loads, open(ROOT / "tests/t2c_llm_offline.jsonl", encoding="utf-8"))}
        return {q["id"]: (off[q["id"]]["llm"], off[q["id"]]["model"]) for q in questions}
    import anthropic  # pip install anthropic; ключ лише в змінній ANTHROPIC_API_KEY
    client = anthropic.Anthropic()
    model = os.environ.get("T2C_MODEL", "claude-sonnet-5-5")
    out, log = {}, []
    for q in questions:
        msg = client.messages.create(model=model, max_tokens=400, temperature=0, system=prompt,
                                     messages=[{"role": "user", "content": q["question"]}])
        text = msg.content[0].text.strip().strip("`").removeprefix("cypher").strip()
        out[q["id"]] = (text, model)
        log.append({"id": q["id"], "raw": msg.content[0].text})
    (ROOT / "llm_log").mkdir(exist_ok=True)
    (ROOT / "llm_log/t2c_raw.jsonl").write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in log), encoding="utf-8")
    return out


def check_schema(q, labels, types, props):
    bad = []
    for m in re.finditer(r"\(\s*\w*\s*:\s*(\w+)", q):
        if m.group(1) not in labels: bad.append(f"мітка {m.group(1)}")
    for m in re.finditer(r"\[\s*\w*\s*:\s*(\w+)", q):
        if m.group(1) not in types: bad.append(f"тип {m.group(1)}")
    for m in re.finditer(r"\{([^}]*)\}", q):
        for k in re.findall(r"(\w+)\s*:", m.group(1)):
            if k not in props: bad.append(f"властивість {k}")
    for k in re.findall(r"\b[a-z]\w*\.(\w+)", q):
        if k not in props: bad.append(f"властивість {k}")
    if re.search(r"\*\s*\]", q): bad.append("необмежений шлях *")
    return sorted(set(bad))


def add_limit(q):
    return q if re.search(r"\bLIMIT\s+\d+", q, re.I) else q.rstrip().rstrip(";") + " LIMIT 100"


def t2c(drv, live):
    labels, types, props, pat = schema_info(drv)
    prompt = prompt_v1(labels, pat)
    questions = [json.loads(l) for l in open(ROOT / "tests/t2c.jsonl", encoding="utf-8")]
    llm = llm_queries(questions, prompt, live)
    # read-only роль (Enterprise). Якщо недоступна — лише READ-транзакції.
    ro_driver, ro_mode = None, "execute_read (admin)"
    try:
        for s in statements(ROOT / "import/05_readonly_role.cypher")[:-1]:
            with drv.session(database="system") as s_:
                s_.run(s).consume()
        ro_driver = GraphDatabase.driver(os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
                                         auth=("t2c", "t2c-readonly-pass"))
        ro_driver.verify_connectivity(); ro_mode = "користувач t2c з роллю t2c_reader"
        with ro_driver.session() as s_:
            try:
                s_.run("CREATE (:Probe)").consume(); ro_probe = "ЗАПИС ДОЗВОЛЕНО (!)"
            except Neo4jError as e:
                ro_probe = f"{e.code}: {e.message[:160]}"
    except Exception as e:  # noqa
        ro_probe = f"роль недоступна: {e}"
    print(f"   read-only: {ro_mode}; спроба запису -> {ro_probe[:90]}")
    d = ro_driver or drv
    res = []
    for q in questions:
        text, model = llm[q["id"]]
        r = {"id": q["id"], "question": q["question"], "gold": q["gold"], "llm": text, "model": model}
        r["write_blocked"] = bool(WRITE_RE.search(text))
        r["schema_errors"] = check_schema(text, labels, types, props)
        r["executed"] = add_limit(text)
        r["parse"] = r["exec_ok"] = r["correct"] = False
        if r["write_blocked"]:
            r["error"] = "відхилено фільтром запису до виконання"
            r["correct"] = q["gold"] is None      # правильна поведінка — відмова
        else:
            try:
                with d.session() as s_:
                    s_.run("EXPLAIN " + r["executed"]).consume()
                r["parse"] = True
                with d.session() as s_:
                    rows = s_.execute_read(lambda tx: [x.data() for x in tx.run(r["executed"])])
                r["exec_ok"] = True; r["rows"] = rows
                gold_rows = run(drv, q["gold"])[0]
                r["gold_rows"] = len(gold_rows)
                r["correct"] = same(rows, gold_rows) and not r["schema_errors"]
            except Neo4jError as e:
                r["error"] = f"{e.code}: {e.message[:200]}"
        res.append(r)
        print(f"   {q['id']}: correct={r['correct']} schema={r['schema_errors']} {r.get('error', '')[:60]}")
    n = len(res)
    metrics = {"questions": n, "parsed": sum(r["parse"] for r in res), "schema_ok": sum(not r["schema_errors"] for r in res),
               "readonly_ok": sum(1 for r in res if not r["write_blocked"] or r["gold"] is None),
               "correct": sum(r["correct"] for r in res), "readonly_mode": ro_mode, "readonly_probe": ro_probe,
               "prompt_version": "v1", "prompt": prompt, "live_llm": live}
    metrics["accuracy"] = round(metrics["correct"] / n, 3)
    print(f"   частка коректних: {metrics['correct']}/{n} = {metrics['accuracy']:.1%}")
    (ROOT / "tests/t2c_results.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in res),
                                                   encoding="utf-8")
    dump("r5_t2c", {"metrics": metrics, "results": res})
    write_protocol(res, metrics)
    if ro_driver:
        ro_driver.close()


def write_protocol(res, m):
    (ROOT / "claims").mkdir(exist_ok=True); (ROOT / "llm_log").mkdir(exist_ok=True)
    with open(ROOT / "claims/claims.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "claim", "type", "source", "verification_level", "status", "comment"])
        for r in res:
            ok = r["correct"]
            comment = ("збіг з еталоном" if ok and r["gold"] else "запит на запис відхилено — коректна відмова" if ok
                       else "; ".join(r["schema_errors"]) or r.get("error", "результат не збігся з еталоном"))
            w.writerow([f"t2c-{r['id']}", f"{r['question']} -> {r['llm']}", "факт", r["model"], "V4",
                        "verified" if ok else "rejected", comment])
        w.writerow(["schema-01", "Підкласи OWL (Manager, Recruiter) згорнути в мітку Employee з kind", "правило",
                    "LLM-пропозиція схеми", "V2", "verified", "перевірено виконанням C02–C08"])
    (ROOT / "llm_log/llm_log.md").write_text(
        f"# Журнал LLM (ЛР 9)\n\n- Дата: {datetime.now():%Y-%m-%d}\n- Модель: {res[0]['model']}\n"
        f"- Параметри: temperature={'0' if m['live_llm'] else 'за замовчуванням (чат)'}; seed не підтримується\n"
        f"- Версія підказки: {m['prompt_version']}\n- Сирий вихід: tests/t2c_results.jsonl\n"
        f"- Рішення людини: підтверджено {m['correct']} із {m['questions']}\n\n## Підказка\n```\n{m['prompt']}\n```\n",
        encoding="utf-8")


def main():
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["r2", "r3", "r4", "r5"])
    ap.add_argument("--live-llm", action="store_true")
    a = ap.parse_args()
    drv = GraphDatabase.driver(os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
                               auth=(os.environ.get("NEO4J_USER", "neo4j"), os.environ["NEO4J_PASSWORD"]))
    drv.verify_connectivity()
    ver = run(drv, "CALL dbms.components() YIELD name, versions, edition")[0]
    print("Neo4j:", ver)
    steps = {"r2": r2, "r3": r3, "r4": r4, "r5": lambda d: r5(d, a.live_llm)}
    for k, fn in steps.items():
        if a.only in (None, k):
            fn(drv)
    dump("env", {"neo4j": ver, "time": datetime.now().isoformat()})
    drv.close()
    print("Готово. Результати: results/, docs/, tests/t2c_results.jsonl, claims/, llm_log/")


if __name__ == "__main__":
    main()
