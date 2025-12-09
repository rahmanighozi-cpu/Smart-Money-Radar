def format_usd(value):
    return f"${value:,.2f}"

def format_number(value):
    return f"{value:,.0f}"

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0
