from decimal import Decimal


def format_results(data: list, sql: str) -> str:
    if not data:
        return "✅ Query ran successfully but returned no results."

    # Normalize Decimal → clean string
    cleaned_data = []
    for row in data:
        cleaned_row = {}
        for k, v in row.items():
            if isinstance(v, Decimal):
                cleaned_row[k] = f"{float(v):,.2f}"
            else:
                cleaned_row[k] = str(v)
        cleaned_data.append(cleaned_row)

    # Column widths
    headers = list(cleaned_data[0].keys())
    col_widths = {h: len(h) for h in headers}
    for row in cleaned_data:
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(row[h])))

    # Build table
    def format_row(row_data):
        return " | ".join(str(row_data[h]).ljust(col_widths[h]) for h in headers)

    separator  = "-+-".join("-" * col_widths[h] for h in headers)
    header_row = format_row({h: h for h in headers})
    rows       = [format_row(row) for row in cleaned_data]
    table      = "\n".join([header_row, separator] + rows)

    return (
        f":white_check_mark: *Query Result* — `{len(data)}` row(s)\n\n"
        f"```\n{table}\n```\n\n"
        f"*SQL Executed:*\n"
        f"```\n{sql}\n```"
    )


def format_error(error: str, sql: str = None) -> str:
    
    message = f":x: *Something went wrong*\n\n```{error}```"
    if sql:
        message += f"\n\n*Generated SQL:*\n```{sql}```"
    return message
