# Slack Data Bot

A Slack slash command bot that lets you query a database using plain English. Type a question, get a formatted table — no SQL knowledge required.

---

## Demo

```
User:  /ask-data show total revenue by region for 2025-09-01

Bot:   ⏳ Processing: `show total revenue by region for 2025-09-01`...

Bot:   ✅ Query Result — 3 row(s)

       region | revenue     | orders
       -------+-------------+-------
       North  | 125,000.50  | 310
       South  | 54,000.00   | 820
       West   | 40,500.00   | 190

       SQL Executed:
       SELECT region, SUM(revenue), SUM(orders)
       FROM public.sales_daily
       WHERE date = '2025-09-01'
       GROUP BY region;
```

---

## Features

- Natural language to SQL conversion using LangChain + Qwen2.5-Coder
- Instant acknowledgment in Slack while query processes in background
- Clean, aligned table formatting in Slack
- SQL transparency — shows the generated query alongside results
- Error handling — failed queries return a readable error message in Slack

---

## Tech Stack

| | Technology |
|---|---|
| Web Framework | FastAPI |
| AI / NL→SQL | LangChain + Qwen2.5-Coder-32B (HuggingFace) |
| Database | Neon PostgreSQL |
| Deployment | Render |

---

## Database Schema

```sql
CREATE TABLE public.sales_daily (
    date        date            NOT NULL,
    region      text            NOT NULL,
    category    text            NOT NULL,
    revenue     numeric(12,2)   NOT NULL,
    orders      integer         NOT NULL,
    created_at  timestamptz     NOT NULL DEFAULT now(),
    PRIMARY KEY (date, region, category)
);
```

---

## Usage

In any Slack channel where the bot is present, type:

```
/ask-data <your question in plain English>
```

### Example Queries

```
/ask-data show total revenue by region for 2025-09-01
/ask-data which category had the most orders on 2025-09-02
/ask-data show all data for the North region
/ask-data what is the total revenue across all regions and categories
/ask-data compare revenue between Electronics and Grocery
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/slack/ask-data` | Slack slash command handler |
| `GET` | `/docs` | Interactive API documentation |

---

## Environment Variables

| Variable | Description |
|---|---|
| `HF_TOKEN` | HuggingFace API token |
| `SLACK_BOT_TOKEN` | Slack bot OAuth token (`xoxb-...`) |
| `SLACK_SIGNING_SECRET` | Slack app signing secret |
| `DATABASE_URL` | Neon PostgreSQL connection string |

---

## Known Limitations

- Single table support — queries are scoped to `sales_daily`
- No SQL validation — generated SQL is executed directly
- Render free tier sleeps after 15 minutes of inactivity — first request after idle may be slow
- HuggingFace free inference API may be slow under heavy load

---

## Planned Improvements

- [ ] CSV export for query results
- [ ] Chart generation for date range queries
- [ ] Query result caching
- [ ] Multi-table support
- [ ] Slack request signature verification

---

## License

MIT
