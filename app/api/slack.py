import asyncio
import httpx
from fastapi import APIRouter, Form
from app.services.processor import process_question
from app.services.query_executor import run_query
from app.utils.formatter import format_results, format_error

router = APIRouter()


async def handle_question(response_url: str, question: str):
    sql, err = process_question(question)

    if err:
        message = format_error(err)
    else:
        data, err = run_query(sql)
        if err:
            message = format_error(err, sql)
        else:
            message = format_results(data, sql)

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
