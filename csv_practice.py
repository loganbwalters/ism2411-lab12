# 1. Doing this in Excel would mean manually opening the file, adding a Total column, and setting up filters.
# Python makes it easier because a script can do all of this automatically. We can reuse the script with other files, and it can handle a lot of data.

# 2. # A store could save each sale in a file to keep track of what was sold and when. Append mode ("a") adds new information without deleting the old information.
# Write mode ("w") would erase the old information every time.



# Exercise 1: Confirm the file exists and can be opened

import csv
from datetime import datetime
from pathlib import Path

sales = Path("sales.csv")
cleaned = Path("cleaned.csv")
log_file = Path("sales.log")

if not sales.exists():
    raise FileNotFoundError(f"Expected file at {sales}")
with open(sales, newline="") as f:
    row_count = sum(1 for _ in csv.reader(f))
print(f"Found {sales.name}: {row_count} lines (1 header + {row_count - 1} data rows)")

# Exercise 2: Read and print raw rows (all values are strings)

with open(sales, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Exercise 3: Skip the header with next()

with open(sales, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)

# Exercise 4: Compute totals

total_revenue = 0.0
with open(sales, newline="") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for product, price, quantity in reader:
        price = float(price)
        quantity = int(quantity)
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")

# Exercise 5: Filter (total > $100) and write cleaned.csv

original_count = 0
written_count = 0
with open(sales, newline="") as infile, \
        open(cleaned, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)  # skip input header
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for product, price, quantity in reader:
        original_count += 1
        price = float(price)
        quantity = int(quantity)
        total = price * quantity
        if total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {cleaned.name}")

# Exercise 6: csv.DictReader

dict_total = 0.0
with open(sales, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:,.2f}")
print(f"Total revenue: ${dict_total:,.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))

# Exercise 7: Sales summary by product

summary = {}
with open(sales, newline="") as f:
    for row in csv.DictReader(f):
        revenue = float(row["price"]) * int(row["quantity"])
        summary[row["product"]] = summary.get(row["product"], 0.0) + revenue
for product in sorted(summary):
    print(f"{product}: ${summary[product]:,.2f}")

# Exercise 8: Append-mode run log

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:,.2f}\n")
class log_file:
    ...

print(f"Appended entry to {log_file.name}")