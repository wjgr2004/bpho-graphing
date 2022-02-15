def convert_to_number(n):
    if not n:
        return 0.0
    try:
        return float(n)
    except ValueError:
        return False
