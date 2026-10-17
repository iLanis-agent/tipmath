#!/usr/bin/env python3
# Tip Math oracle - mirrors engine.js.
import json, math

def _cents(x):
    return math.floor(x * 100 + 0.5)

def _usd(c):
    d, r = divmod(c, 100)
    return f"${d:,}.{r:02d}"

def _money(x, msg):
    if not math.isfinite(x) or x <= 0:
        raise ValueError(msg)
    return _cents(x)

def _pct(x, msg):
    if not math.isfinite(x) or x < 0 or x > 100:
        raise ValueError(msg)
    return x

def _n(x):
    return str(int(x)) if x == int(x) else repr(x)

def tip_truth(subtotal, tip_pct):
    sc = _money(subtotal, "enter a bill over $0")
    _pct(tip_pct, "tip percent must be 0 to 100")
    tc = math.floor(sc * tip_pct / 100 + 0.5)
    return f"{_n(tip_pct)}% of {_usd(sc)} is {_usd(tc)} - the check comes to {_usd(sc + tc)}."

def tax_truth(subtotal, tax_pct, tip_pct):
    sc = _money(subtotal, "enter a bill over $0")
    _pct(tax_pct, "tax percent must be 0 to 100")
    _pct(tip_pct, "tip percent must be 0 to 100")
    tax_c = math.floor(sc * tax_pct / 100 + 0.5)
    pre = math.floor(sc * tip_pct / 100 + 0.5)
    post = math.floor((sc + tax_c) * tip_pct / 100 + 0.5)
    diff = post - pre
    head = f"Tip on {_usd(sc)} is {_usd(pre)}; on {_usd(sc + tax_c)} with tax it is {_usd(post)}"
    if diff == 0:
        return head + " - no difference."
    return head + f" - tipping on the tax costs {_usd(diff)} more."

def split_truth(total, people):
    tc = _money(total, "enter a total over $0")
    if not math.isfinite(people) or people < 1 or people != math.floor(people):
        raise ValueError("people must be a whole number, at least 1")
    people = int(people)
    base, extra = divmod(tc, people)
    if people == 1:
        return f"{_usd(tc)} for one person is {_usd(tc)}."
    if extra == 0:
        return f"{_usd(tc)} across {people} is {_usd(base)} each, exactly."
    lo = people - extra
    return (f"{_usd(tc)} across {people} is {_usd(base)} each with {extra} cent" + ("" if extra == 1 else "s") +
            " left over - " + str(extra) + " " + ("person pays " if extra == 1 else "people pay ") +
            f"{_usd(base + 1)} and {lo} " + ("pays " if lo == 1 else "pay ") + f"{_usd(base)}.")

CASES = [
    ("tipTruth", (48.60, 20)),
    ("tipTruth", (86.40, 18)),
    ("tipTruth", (1234.5, 15)),
    ("tipTruth", (50, 0)),
    ("tipTruth", (0, 20)),
    ("tipTruth", (50, 120)),
    ("taxTruth", (48.60, 8.875, 20)),
    ("taxTruth", (100, 8, 20)),
    ("taxTruth", (50, 0, 20)),
    ("taxTruth", (50, 8, -1)),
    ("splitTruth", (127.43, 4)),
    ("splitTruth", (120, 4)),
    ("splitTruth", (100.01, 2)),
    ("splitTruth", (99.99, 1)),
    ("splitTruth", (127.43, 0)),
    ("splitTruth", (127.43, 2.5)),
]
FNS = {"tipTruth": tip_truth, "taxTruth": tax_truth, "splitTruth": split_truth}
out = []
for name, args in CASES:
    try:
        e = FNS[name](*args)
    except ValueError as ex:
        e = "ERR:" + str(ex)
    out.append({"fn": name, "args": list(args), "expected": e})
with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
