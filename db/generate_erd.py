from sqlalchemy import create_engine, MetaData
from graphviz import Digraph

DB_PATH = "sqlite:///frozen_v1.db"

engine = create_engine(DB_PATH)
metadata = MetaData()
metadata.reflect(bind=engine)

dot = Digraph("Frozen_v1_ERD", format="svg")
dot.attr(rankdir="LR", fontsize="10")

# Draw tables
for table in metadata.tables.values():
    cols = []
    for col in table.columns:
        col_def = f"{col.name} : {col.type}"
        if col.primary_key:
            col_def = f"<b>{col_def}</b>"
        cols.append(col_def)

    label = f"""<
    <table border="1" cellborder="0" cellspacing="0">
        <tr><td bgcolor="lightgray"><b>{table.name}</b></td></tr>
        {''.join(f"<tr><td align='left'>{c}</td></tr>" for c in cols)}
    </table>
    >"""

    dot.node(table.name, label=label, shape="plaintext")

# Draw foreign keys
for table in metadata.tables.values():
    for fk in table.foreign_keys:
        dot.edge(
            fk.column.table.name,
            table.name,
            label=f"{fk.column.name} → {fk.parent.name}"
        )

dot.render("frozen_v1_erd")
