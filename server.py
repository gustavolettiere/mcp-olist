from fastmcp import FastMCP
from pathlib import Path
import duckdb

mcp = FastMCP("olist-warehouse")
DB_PATH = str(Path(__file__).parent / "olist.duckdb")

def get_conn():
    # read_only evita que o agente altere os dados
    return duckdb.connect(DB_PATH, read_only=True)

@mcp.tool()
def list_tables() -> list[str]:
    """Lista todas as tabelas disponíveis no warehouse."""
    con = get_conn()
    tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
    con.close()
    return tables

@mcp.tool()
def describe_table(table: str) -> str:
    """Mostra as colunas e tipos de uma tabela."""
    con = get_conn()
    rows = con.execute(f"DESCRIBE {table}").fetchall()
    con.close()
    return "\n".join(f"{r[0]}: {r[1]}" for r in rows)

@mcp.tool()
def run_query(sql: str) -> str:
    """Executa uma query SOMENTE-LEITURA (SELECT/WITH) e retorna até 100 linhas."""
    lowered = sql.strip().lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        return "Apenas queries de leitura (SELECT/WITH) são permitidas."
    con = get_conn()
    cur = con.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchmany(100)
    con.close()
    if not rows:
        return "Sem resultados."
    header = " | ".join(cols)
    body = "\n".join(" | ".join(str(v) for v in row) for row in rows)
    return f"{header}\n{body}"

@mcp.resource("schema://catalog")
def catalog() -> str:
    """Catálogo: todas as tabelas e suas colunas."""
    con = get_conn()
    parts = []
    for (t,) in con.execute("SHOW TABLES").fetchall():
        cols = con.execute(f"DESCRIBE {t}").fetchall()
        parts.append(f"## {t}\n" + "\n".join(f"- {c[0]} ({c[1]})" for c in cols))
    con.close()
    return "\n\n".join(parts)

@mcp.prompt()
def analisar_receita() -> str:
    """Template: analisar receita por categoria de produto."""
    return (
        "Usando a tool run_query, calcule a receita total (price + freight_value) "
        "por categoria de produto, juntando order_items e products. "
        "Liste as 10 maiores categorias."
    )

if __name__ == "__main__":
    mcp.run()
