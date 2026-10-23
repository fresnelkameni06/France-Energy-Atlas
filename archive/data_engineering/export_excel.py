
import sqlite3
from pathlib import Path
import xlsxwriter

DB = Path("data/energy.db")
OUTPUT = Path("data/france_energy_2020_2026.xlsx")

conn = sqlite3.connect(DB)
cursor = conn.execute("SELECT * FROM measurements LIMIT 0")
columns = [column[0] for column in cursor.description]

workbook = xlsxwriter.Workbook(
    str(OUTPUT),
    {"constant_memory": True}
)

header_format = workbook.add_format({
    "bold": True,
    "bg_color": "#17365D",
    "font_color": "white",
    "border": 1
})

total = 0

for year in range(2020, 2027):
    sheet = workbook.add_worksheet(str(year))
    sheet.freeze_panes(1, 0)
    sheet.set_column(0, len(columns) - 1, 20)

    sheet.write_row(0, 0, columns, header_format)

    query = """
        SELECT *
        FROM measurements
        WHERE observation_utc >= ?
          AND observation_utc < ?
        ORDER BY observation_utc
    """

    records = conn.execute(
        query,
        (f"{year}-01-01", f"{year + 1}-01-01")
    )

    count = 0

    for count, record in enumerate(records, start=1):
        sheet.write_row(count, 0, record)

    sheet.autofilter(0, 0, max(count, 1), len(columns) - 1)

    total += count
    print(f"{year}: {count:,} rows exported")

workbook.close()
conn.close()

print(f"\nTotal exported: {total:,}")
print(f"Excel file: {OUTPUT.resolve()}")
