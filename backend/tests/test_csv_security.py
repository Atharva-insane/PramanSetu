import re

def escape_csv_cell(val):
    if val is None:
        return '""'
    s = str(val)
    if re.match(r'^[=+\-@\t\r]', s):
        s = "'" + s
    s = s.replace('"', '""')
    return f'"{s}"'

payloads = [
    "=SUM(A1:A10)",
    "+123",
    "-123",
    "@calc",
    "\tformula",
    "\rformula",
    '"quoted text"',
    "normal text"
]

print(f"{'INPUT':<20} | {'ESCAPED CSV OUTPUT':<25} | {'SAFE'}")
print("-" * 55)
for p in payloads:
    escaped = escape_csv_cell(p)
    is_safe = escaped.startswith("\"'") if re.match(r'^[=+\-@\t\r]', p) else True
    print(f"{repr(p):<20} | {escaped:<25} | {'PASS' if is_safe else 'FAIL'}")
    assert is_safe

print("\nALL CSV INJECTION REGRESSION TESTS PASSED.")
