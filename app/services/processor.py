import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    model="Qwen/Qwen2.5-Coder-32B-Instruct:fastest",
    temperature=0.1,
)

SYSTEM_PROMPT = """
You are a SQL expert. You have access to a PostgreSQL database with the following table:

Table: public.sales_daily
Columns:
  - date        (date)       : the date of sales
  - region      (text)       : sales region e.g. North, South, East, West
  - category    (text)       : product category e.g. Electronics, Grocery, Fashion
  - revenue     (numeric)    : total revenue for that day/region/category
  - orders      (integer)    : number of orders
  - created_at  (timestamptz): when the record was created

Rules:
  - Output ONLY a single valid PostgreSQL SELECT statement
  - No explanations, no markdown, no code blocks
  - End the query with a semicolon
  - When using UNION or UNION ALL with ORDER BY and LIMIT,
    always wrap each SELECT statement in parentheses
  - ALWAYS include the relevant metric columns in the SELECT output
    e.g. if the question asks about maximum orders, include SUM(orders) AS total_orders
    e.g. if the question asks about highest revenue, include SUM(revenue) AS total_revenue
  - NEVER return just one column unless the question explicitly asks for only one value
  - Always use meaningful aliases for aggregated columns
    e.g. SUM(revenue) AS total_revenue, SUM(orders) AS total_orders, COUNT(*) AS total_records
  - When the question asks for maximum or minimum of something,
    always SELECT both the group column AND the aggregated metric
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

chain = prompt | llm


def process_question(question: str) -> tuple:
    try:
        response = chain.invoke({"question": question})
        sql = response.content.strip()
        return sql, None
    except Exception as e:
        return None, str(e)
