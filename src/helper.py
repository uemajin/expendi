
def bgcolor_positive_or_negative(value):
    if isinstance(value, str):
        value = float(value.replace(',', ''))
    
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"
