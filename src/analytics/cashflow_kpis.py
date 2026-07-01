def free_cash_flow(cfo, cfi):
    if cfo is None or cfi is None:
        return None
    return cfo + cfi


def cfo_quality_score(cfo_list, pat_list):
    ratios = []
    for cfo, pat in zip(cfo_list, pat_list):
        if pat == 0 or pat is None or cfo is None:
            continue
        ratios.append(cfo / pat)

    if not ratios:
        return None

    avg = sum(ratios) / len(ratios)

    if avg > 1:
        return "High Quality"
    elif avg >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(cfi, sales):
    if sales == 0 or sales is None or cfi is None:
        return None
    return abs(cfi) / sales * 100


def fcf_conversion(fcf, operating_profit):
    if operating_profit == 0 or operating_profit is None:
        return None
    return fcf / operating_profit * 100


def capital_allocation_pattern(cfo, cfi, cff):
    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return patterns.get(signs, "Unknown")