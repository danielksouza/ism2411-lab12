# ISM2411 Lab 12 - Read a Sales CSV, Write a Cleaned Report#
# REFLECTION
#
#Q1: Python ETL pipeline vs. Excel
# In Excel I would open the file, append a Total column, filter, and manually 
# save a copy. With Python, I can perform the same read-transform-write 
# operations in code that I can quickly execute on any file. Also, Python
# would work with much larger files than Excel can handle, and I would have
# a documented record of exactly what was done. That said, because Excel
# is easier to use (share) for people who don’t code
# and allows for visual editing, charts, and quick one-off data examination, 
# it may still be preferable in those situations

# Q2: Append-mode log file
# One example could be a server that “logs” each time someone tries to log in,
# or a retail operation that uses a point-of-sale system to record every sale.
# Each would be a new line with the time stamped beside it. We should use append 
# mode ("a") because we only want to add to the end of the file and preserve 
# previous content; using write mode ("w") would overwrite the content every
#  time the program is executed.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

print("=== Exercise 1: Get the file ===")
with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE} with no error.")

print("\n=== Exercise 2: Read and print raw rows ===")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)          # every value is a string, even the numbers

print("\n=== Exercise 3: Skip the header ===")
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)   # consumes the first row
    print("Header:", header)
    for row in reader:      # loop now starts at the first data row
        print(row)

print("\n=== Exercise 4: Compute totals ===")
total_revenue = 0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

print("\n=== Exercise 5: Filter and write ===")
rows_read = 0
rows_written = 0
with open(SALES_FILE, "r", newline="") as infile, \
        open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        rows_read += 1
        price = float(row[1])
        quantity = int(row[2])
        total = price * quantity
        if total > 100:
            writer.writerow([row[0], price, quantity, round(total, 2)])
            rows_written += 1
print(f"Rows in original: {rows_read}")
print(f"Rows written to {CLEANED_FILE}: {rows_written}")

print("\n=== Exercise 6: csv.DictReader ===")

#Comparison: csv.reader returns lists and I have to remember which column is which
# (row\[1\]) - fast and simple but if I reorder columns later it will be problematic
# csv.DictReader uses dictionary keys (row"\("price"\") - easier to read and less prone
# to errors if columns are reordered - I would use this for most real-world situations
dict_total = 0
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dict_total += float(row["price"]) * int(row["quantity"])
print(f"Total revenue (DictReader): ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))

print("\n=== Exercise 7: Sales summary by product ===")
summary = {}
with open(SALES_FILE, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        revenue = float(row["price"]) * int(row["quantity"])
        summary[row["product"]] = summary.get(row["product"], 0) + revenue
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

print("\n=== Exercise 8: Append mode log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:.2f}\n")
print(f"Appended one line to {LOG_FILE}")