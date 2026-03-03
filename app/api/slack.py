import asyncio

import httpx
from app.services.processor import process_question
from app.services.query_executor import run_query
from app.utils.formatter import format_error, format_results
from fastapi import APIRouter, Form
from services.cache import get_cached, set_cache, clear_cache

router = APIRouter()


async def handle_question(response_url: str, question: str):
    cached = get_cached(question)
    if cached:
        message = cached["result"] + f"/n/n Cached result from {cached['cached_at']}_"
        async with httpx.AsyncClient() as client:
            await client.post(response_url, json={"text": message})
        return

    try:
        sql, err = process_question(question)
        print(f"Generated SQL: {sql}, Error: {err}")  # ← add this

        if err:
            message = format_error(err)
        else:
            data, err = run_query(sql)
            print(f"Query data: {data}, Error: {err}")  # ← add this
            if err:
                message = format_error(err, sql)
            else:
                message = format_results(data, sql)

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")             # ← add this
        message = format_error(str(e))

    async with httpx.AsyncClient() as client:
        await client.post(response_url, json={"text": message})

@router.post("/ask-data")
async def ask_data(
    text: str = Form(...),
    response_url: str = Form(...)
):

    asyncio.create_task(handle_question(response_url, text))

    return {
        "response_type": "in_channel",
        "text": f":hourglass: Processing: `{text}`..."
    }

@router.post("/clear-cache")
async def clear_cache_command(response_url: str = Form(...)):
    clear_cache()
    async with httpx.AsyncClient() as client:
        await client.post(response_url, json={
            "text": ":broom: *Cache Cleared!* Next queries will fetch fresh data from the database."
        })
    return {
        "response_type": "in_channel",
        "text": ":hourglass: Clearing Cache"
    }
