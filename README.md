# MCP Server — Olist Warehouse (DuckDB + FastMCP)

MCP server em Python que expõe um warehouse analítico local para agentes de IA consultarem dados do [dataset Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) em linguagem natural.

O agente pode listar tabelas, inspecionar schemas e executar queries SQL de leitura — tudo protegido por uma conexão read-only e validação de query.

```
Claude Desktop (host) → MCP client → olist-warehouse server → DuckDB (olist.duckdb)
```

---

## Stack

| Ferramenta | Papel |
|---|---|
| Python 3.10+ | linguagem |
| [DuckDB](https://duckdb.org/) | banco analítico local ("warehouse") |
| [FastMCP](https://gofastmcp.com/) | framework para construir o MCP server |
| Dataset Olist (Kaggle) | dados de e-commerce brasileiro |

---

## Primitivos MCP implementados

**Tools** — ações que o modelo pode executar:
- `list_tables` — lista todas as tabelas disponíveis
- `describe_table(table)` — mostra colunas e tipos de uma tabela
- `run_query(sql)` — executa um SELECT/WITH e retorna até 100 linhas

**Resource** — dado de leitura que o modelo pode puxar:
- `schema://catalog` — catálogo completo com todas as tabelas e colunas

**Prompt** — template reutilizável:
- `analisar_receita` — instrui o modelo a calcular receita por categoria de produto

---

## Como rodar

### Pré-requisitos

- Python 3.10+
- Node.js (apenas se quiser testar com o MCP Inspector)
- Conta gratuita no [Kaggle](https://www.kaggle.com/) para baixar os dados

### 1. Clone o repositório e crie o ambiente virtual

```bash
git clone https://github.com/seu-usuario/mcp-olist.git
cd mcp-olist
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. Instale as dependências

```bash
pip install fastmcp duckdb
```

### 3. Baixe o dataset

Acesse o [dataset Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), baixe e extraia os CSVs na pasta `data/`:

```
data/
  olist_customers_dataset.csv
  olist_orders_dataset.csv
  olist_order_items_dataset.csv
  olist_order_payments_dataset.csv
  olist_order_reviews_dataset.csv
  olist_products_dataset.csv
  olist_sellers_dataset.csv
  olist_geolocation_dataset.csv
  product_category_name_translation.csv
```

### 4. Carregue os dados no DuckDB

```bash
python load_data.py
```

Isso cria o arquivo `olist.duckdb` com todas as tabelas inferidas automaticamente.

### 5. Verifique o server

```bash
.venv\Scripts\fastmcp.exe inspect server.py   # Windows
.venv/bin/fastmcp inspect server.py           # Linux/macOS
```

Deve retornar: 3 Tools, 1 Prompt, 1 Resource.

### 6. Conectar ao Claude Desktop

Edite o arquivo de configuração do Claude Desktop:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Adicione a seção `mcpServers` com o caminho absoluto para o Python do venv e o `server.py`:

```json
{
  "mcpServers": {
    "olist-warehouse": {
      "command": "/caminho/absoluto/para/.venv/bin/python",
      "args": ["/caminho/absoluto/para/server.py"]
    }
  }
}
```

> **Importante:** use sempre caminhos absolutos. Caminhos relativos falham porque o Claude Desktop inicia o server a partir de sua própria pasta de instalação.

Reinicie o Claude Desktop. Um ícone de ferramentas aparecerá no chat indicando que o server está conectado.

### 7. Testar no MCP Inspector (opcional)

```bash
npx @modelcontextprotocol/inspector
```

Acesse `localhost:6274` no navegador. Na interface, preencha:

- **Command:** caminho absoluto para o Python do venv (ex: `C:\caminho\para\.venv\Scripts\python.exe`)
- **Arguments:** `server.py`

Clique em **Connect** para executar tools interativamente.

---

## Exemplos de perguntas no Claude Desktop

- *"Quais as 10 categorias de produto com maior receita?"*
- *"Qual o produto mais caro da base?"*
- *"Quantos pedidos foram entregues com atraso?"*
- *"Liste os 5 estados com mais clientes."*

---

## Segurança

- Conexão com o banco em modo `read_only=True` — o agente não consegue modificar dados
- `run_query` rejeita qualquer statement que não comece com `SELECT` ou `WITH`
