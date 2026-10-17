# Tip Math

The check, in whole cents. Four people, one check, and a penny nobody can split.

## What it computes

- **The tip truth** - your percent on the amount you chose: 20% of $48.60 is $9.72 - the check comes to $58.32.
- **The tax truth** - tip on the pre-tax or post-tax number: on $100.00 at 8% tax and 20%, tipping on the tax costs $1.60 more.
- **The split truth** - whole cents, nobody shorted: $127.43 across 4 is $31.85 each with 3 cents left over.

## Boundary

Arithmetic only. You choose the tip percent and whether it goes on the tax; Tip Math never says what is polite or what to leave.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, in whole cents.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (16 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/tipmath/
Repo: https://github.com/iLanis-agent/tipmath
