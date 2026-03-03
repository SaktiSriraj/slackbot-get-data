import asyncio
import httpx
from fastapi import APIRouter, Form, Response
from app.services.processor import process_question
from app.services.query_executor import run_query
from app.utils.formatter import format_results, format_error
from app.services.cache import get_cached, set_cache, clear_cache

router = APIRouter()

async def handle_question(response_url: str, question: str):
    try:
        cached = get_cached(question)

        if cached:
            await asyncio.sleep(2)
            message = cached["result"] + f"\n\n_⚡ Cached result from {cached['cached_at']}_"
            async with httpx.AsyncClient() as client:
                await client.post(response_url, json={"text": message})
            return

        sql, err = process_question(question)
        print(f"Generated SQL: {sql}, Error: {err}")

        if err:
            message = format_error(err)
        else:
            data, err = run_query(sql)
            print(f"Query data: {data}, Error: {err}")
            if err:
                message = format_error(err, sql)
            else:
                message = format_results(data, sql)
                set_cache(question, message, sql)

    except Exception as e:
        print(f"CRITICAL ERROR in handle_question: {str(e)}")
        message = format_error(str(e))

    async with httpx.AsyncClient() as client:
        await client.post(response_url, json={"text": message})


@router.post("/ask-data")
async def ask_data(
    response: Response,
    text: str = Form(...),
    response_url: str = Form(...)
):
    response.headers["X-Slack-No-Retry"] = "1"
    asyncio.create_task(handle_question(response_url, text))
    return {
        "response_type": "in_channel",
        "text": f":hourglass: Processing: `{text}`..."
    }


@router.post("/clear-cache")
async def clear_cache_command(
    response_url: str = Form(...)
):
    clear_cache()
    async with httpx.AsyncClient() as client:
        await client.post(response_url, json={
            "text": ":broom: *Cache cleared!* Next queries will fetch fresh data from the database."
        })
    return {
        "response_type": "in_channel",
        "text": ":hourglass: Clearing cache..."
    }
