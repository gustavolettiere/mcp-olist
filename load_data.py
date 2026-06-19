import duckdb, glob, os

con = duckdb.connect("olist.duckdb")
for csv in glob.glob("data/*.csv"):
    base = os.path.splitext(os.path.basename(csv))[0]
    name = base.replace("olist_", "").replace("_dataset", "")
    con.execute(
        f"CREATE OR REPLACE TABLE {name} AS "
        f"SELECT * FROM read_csv_auto('{csv}', header=true)"
    )
    print("carregada:", name)
con.close()
print("Banco olist.duckdb criado com sucesso.")
