"""ЛР 9, результат 1–2: RDF (ЛР 7/8) -> LPG CSV для Neo4j.

1. Читає онтологію-дані ЛР 7 (models/onto_data.ttl).
2. Збагачує їх 24 синтетичними співробітниками E-007…E-030 (як у ЛР 8, seed 42) -> data/kb.ttl.
3. Відображає індивіди на мітки LPG, об'єктні властивості -> типи зв'язків,
   властивості даних -> властивості вузлів; додає походження (source, confidence, validFrom).
4. Пише data/nodes_<Label>.csv, data/rels_<TYPE>__<From>__<To>.csv та генерує import/02_import.cypher.
5. Малює схему графа docs/graph_schema.png.

Запуск:  python scripts/build_data.py --lr7 ../ЛР7_артефакти/models/onto_data.ttl
"""
import argparse
import csv
import random
import re
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, OWL, RDFS, XSD

ROOT = Path(__file__).resolve().parents[1]
HR = Namespace("http://example.org/hr#")
SEED = 42

# --- відображення класів OWL -> (мітка LPG, kind) ---------------------------
CLASS_TO_LABEL = {
    "Employee": "Employee", "Manager": "Employee", "Recruiter": "Employee",
    "Candidate": "Candidate", "Position": "Position", "Course": "Course",
    "HardSkill": "Competence", "SoftSkill": "Competence",
    "Resume": "Document", "PositionProfile": "Document", "TrainingPlan": "Document",
    "HRProcess": "Process", "Recruitment": "Process", "Interview": "Process",
    "Onboarding": "Process", "Training": "Process", "Appraisal": "Process",
    "Attestation": "Process", "Motivation": "Process",
    "Dismissal": "Decision", "Promotion": "Decision",
    "KPI": "Metric", "Productivity": "Metric", "Turnover": "Metric",
    "Salary": "Reward", "Bonus": "Reward",
    "HRIS": "System", "LMS": "System",
    "DecisionRule": "Rule", "SituationTemplate": "Template",
}
SUFFIX_TO_LABEL = [("Event", "Event"), ("State", "State"), ("Action", "Action"), ("Sensor", "Sensor")]
NAME_PROPS = ["fullName", "positionTitle", "courseTitle", "label"]

FIRST = ["Тарас", "Оксана", "Богдан", "Христина", "Юрій", "Наталія", "Остап", "Ірина", "Василь",
         "Галина", "Степан", "Леся", "Назар", "Уляна", "Максим", "Ольга", "Роман", "Дарина",
         "Олег", "Мирослава", "Тетяна", "Святослав", "Зоряна", "Ярослав"]
LAST = ["Гнатюк", "Яремчук", "Федина", "Ткачук", "Кравець", "Романюк", "Олійник", "Мороз",
        "Пономаренко", "Бойко", "Левицький", "Савченко", "Кузьмич", "Литвин", "Демчук",
        "Головатий", "Остапчук", "Захарчук", "Павлюк", "Стасюк", "Семенко", "Гуменюк", "Дорош", "Вовк"]


def local(u):
    return str(u).split("#")[-1]


def enrich(g: Graph) -> Graph:
    """24 синтетичні співробітники E-007…E-030 (seed 42)."""
    rnd = random.Random(SEED)
    competences = ["pythonProgramming", "teamCommunication", "negotiation", "hrAnalytics"]
    posts = (["pythonDeveloperPost"] * 19) + ["recruiterPost"] * 2 + ["teamLeadPost"] * 2 + ["hrManagerPost"]
    rnd.shuffle(posts)
    leads = []
    today = date(2026, 10, 28)
    for i in range(24):
        n = 7 + i
        e = HR[f"emp{n:03d}"]
        post = posts[i]
        g.add((e, RDF.type, OWL.NamedIndividual))
        g.add((e, RDF.type, HR.Manager if post in ("teamLeadPost", "hrManagerPost") else
               HR.Recruiter if post == "recruiterPost" else HR.Employee))
        g.add((e, HR.employeeId, Literal(f"E-{n:03d}", datatype=XSD.string)))
        g.add((e, HR.fullName, Literal(f"{FIRST[i]} {LAST[i]}", datatype=XSD.string)))
        score = round(rnd.uniform(3.5, 9.6), 1)
        tenure = rnd.randint(3, 96)
        hired = today - timedelta(days=int(tenure * 30.4))
        g.add((e, HR.productivityScore, Literal(score, datatype=XSD.decimal)))
        g.add((e, HR.tenureMonths, Literal(tenure, datatype=XSD.integer)))
        g.add((e, HR.hireDate, Literal(f"{hired.isoformat()}T00:00:00", datatype=XSD.dateTime)))
        g.add((e, HR.occupies, HR[post]))
        g.add((e, HR.inState, HR.stateProbation if tenure <= 3 else HR.stateActive))
        if post in ("teamLeadPost", "hrManagerPost"):
            mgr = "olena"
            leads.append(local(e))
        else:
            mgr = rnd.choice(["olena", "ivan", "ivan"] + leads)
        g.add((e, HR.directManager, HR[mgr]))
        for c in rnd.sample(competences, rnd.randint(1, 3)):
            g.add((e, HR.hasCompetence, HR[c]))
        g.add((HR.hris1, HR.storesRecordOf, e))
        if rnd.random() < 0.5:
            course = rnd.choice(["pythonAdvancedCourse", "negotiationCourse"])
            g.add((e, HR.completedCourse, HR[course]))
            g.add((HR.lms1, HR.storesRecordOf, e))
            ev = HR[f"eventCourse{n:03d}"]
            g.add((ev, RDF.type, OWL.NamedIndividual)); g.add((ev, RDF.type, HR.CourseCompletedEvent))
            g.add((ev, HR.concernsEmployee, e)); g.add((ev, HR.reportedBy, HR.sensorLMS))
            g.add((ev, HR.occurredOn, Literal(f"2026-{rnd.randint(1, 10):02d}-15T00:00:00", datatype=XSD.dateTime)))
        if score < 5.0:
            ev = HR[f"eventLowProd{n:03d}"]
            g.add((ev, RDF.type, OWL.NamedIndividual)); g.add((ev, RDF.type, HR.LowProductivityEvent))
            g.add((ev, HR.concernsEmployee, e)); g.add((ev, HR.reportedBy, HR.sensorKPI))
            g.add((ev, HR.occurredOn, Literal("2026-10-01T00:00:00", datatype=XSD.dateTime)))
    return g


def label_of(g, s):
    for o in g.objects(s, RDF.type):
        c = local(o)
        if c in CLASS_TO_LABEL:
            return CLASS_TO_LABEL[c], c
        for suf, lab in SUFFIX_TO_LABEL:
            if c.endswith(suf):
                return lab, c
    return None, None


def upper_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def to_lpg(g: Graph, synthetic: set):
    inds = set(g.subjects(RDF.type, OWL.NamedIndividual))
    nodes = defaultdict(list)          # label -> [row]
    lab = {}
    for s in sorted(inds, key=str):
        L, kind = label_of(g, s)
        if not L:
            continue
        lab[s] = L
        row = {"id": local(s), "kind": kind}
        for p, o in g.predicate_objects(s):
            if isinstance(o, Literal):
                k = local(p)
                row["name" if k in NAME_PROPS else k] = str(o)
        row.setdefault("name", local(s))
        nodes[L].append(row)

    rels = defaultdict(list)           # (TYPE, A, B) -> [row]
    for s, p, o in g:
        if s in lab and o in lab and p not in (RDF.type,):
            sid, oid = local(s), local(o)
            syn = sid in synthetic or oid in synthetic
            vf = ""
            for dp in (HR.hireDate, HR.occurredOn):
                v = g.value(s, dp)
                if v is not None:
                    vf = str(v)[:10]
            rels[(upper_snake(local(p)), lab[s], lab[o])].append({
                "from": sid, "to": oid,
                "source": "synthetic-enrichment" if syn else "kb.ttl",
                "confidence": 0.8 if syn else 1.0,
                "validFrom": vf or "2026-10-28",
            })
    return nodes, rels


INT_PROPS = {"tenureMonths", "salaryGrade", "courseHours"}
FLOAT_PROPS = {"productivityScore", "kpiTarget", "turnoverRate", "salaryAmount"}


def write_csv(nodes, rels, data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    for f in data_dir.glob("*.csv"):
        f.unlink()
    node_props = {}
    for L, rows in nodes.items():
        cols = ["id", "name", "kind"] + sorted({k for r in rows for k in r} - {"id", "name", "kind"})
        node_props[L] = cols
        with open(data_dir / f"nodes_{L}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["id"]))
    for (T, A, B), rows in rels.items():
        with open(data_dir / f"rels_{T}__{A}__{B}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["from", "to", "source", "confidence", "validFrom"])
            w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r["from"], r["to"])))
    return node_props


def cast(k):
    if k in INT_PROPS:
        return f"toInteger(row.{k})"
    if k in FLOAT_PROPS:
        return f"toFloat(row.{k})"
    if k in ("hireDate", "occurredOn"):
        return f"datetime(row.{k})"
    return f"row.{k}"


def write_import(node_props, rels, path: Path):
    out = ["// ЛР 9, результат 2: імпорт LOAD CSV + MERGE (згенеровано scripts/build_data.py)",
           "// Ідемпотентний: MERGE за id вузла та за парою кінців зв'язку; повторний запуск не створює дублікатів.", ""]
    for L, cols in sorted(node_props.items()):
        sets = ", ".join(f"n.{k} = {cast(k)}" for k in cols if k != "id")
        out += [f"LOAD CSV WITH HEADERS FROM 'file:///nodes_{L}.csv' AS row",
                f"MERGE (n:{L} {{id: row.id}})", f"SET {sets};", ""]
    for (T, A, B) in sorted(rels):
        out += [f"LOAD CSV WITH HEADERS FROM 'file:///rels_{T}__{A}__{B}.csv' AS row",
                f"MATCH (a:{A} {{id: row.from}}), (b:{B} {{id: row.to}})",
                f"MERGE (a)-[r:{T}]->(b)",
                "SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")


def draw_schema(nodes, rels, path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx
    G = nx.MultiDiGraph()
    for L, rows in nodes.items():
        G.add_node(L, n=len(rows))
    for (T, A, B), rows in rels.items():
        G.add_edge(A, B, label=T)
    simple = nx.DiGraph()
    lbl = defaultdict(list)
    for a, b, d in G.edges(data=True):
        simple.add_edge(a, b); lbl[(a, b)].append(d["label"])
    import numpy as np
    pos = nx.kamada_kawai_layout(simple, scale=1.0)
    pos = {k: np.array([v[0] * 1.45, v[1]]) for k, v in pos.items()}
    names = list(pos)
    for _ in range(800):                      # розсування вузлів, що накладаються
        moved = False
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                dv = pos[a] - pos[b]
                dist = float(np.hypot(*dv)) or 1e-3
                if dist < 0.52:
                    push = dv / dist * (0.52 - dist) / 2
                    pos[a] = pos[a] + push; pos[b] = pos[b] - push; moved = True
        if not moved:
            break
    fig, ax = plt.subplots(figsize=(15, 10.5))
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.4, max(xs) + 0.4); ax.set_ylim(min(ys) - 0.35, max(ys) + 0.35)
    nx.draw_networkx_edges(simple, pos, ax=ax, arrows=True, arrowsize=16, edge_color="#888", width=1.2,
                           connectionstyle="arc3,rad=0.12", node_size=4200)
    nx.draw_networkx_nodes(G, pos, node_size=4200, node_color="#cfe3f7", edgecolors="#2b5d8a", linewidths=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={n: f"{n}\n({G.nodes[n]['n']})" for n in G}, font_size=11,
                            font_weight="bold", ax=ax)
    nx.draw_networkx_edge_labels(simple, pos, edge_labels={k: "\n".join(sorted(set(v))) for k, v in lbl.items()},
                                 font_size=8.5, ax=ax, label_pos=0.5, rotate=False,
                                 bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    ax.axis("off")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(); fig.savefig(path, dpi=170); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lr7", default=str(ROOT.parent / "ЛР7_артефакти" / "models" / "onto_data.ttl"))
    a = ap.parse_args()
    g = Graph(); g.parse(a.lr7)
    before = set(g.subjects(RDF.type, OWL.NamedIndividual))
    g = enrich(g)
    synthetic = {local(s) for s in set(g.subjects(RDF.type, OWL.NamedIndividual)) - before}
    g.bind("hr", HR)
    (ROOT / "data").mkdir(exist_ok=True)
    g.serialize(ROOT / "data" / "kb.ttl", format="turtle")
    nodes, rels = to_lpg(g, synthetic)
    props = write_csv(nodes, rels, ROOT / "data")
    write_import(props, rels, ROOT / "import" / "02_import.cypher")
    draw_schema(nodes, rels, ROOT / "docs" / "graph_schema.png")
    nn = sum(len(v) for v in nodes.values()); nr = sum(len(v) for v in rels.values())
    print(f"kb.ttl: {len(g)} triples; nodes={nn}, rels={nr}, labels={len(nodes)}, "
          f"rel types={len({t for t, _, _ in rels})}, csv files={len(nodes) + len(rels)}")
    print("labels:", dict(Counter({L: len(r) for L, r in nodes.items()})))
    print("rel types:", sorted({t for t, _, _ in rels}))


if __name__ == "__main__":
    main()
