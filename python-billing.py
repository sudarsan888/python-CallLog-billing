# vodafone_billing.py
# Single-file Vodafone billing script — copy, edit INPUT_PATH, and run.

INPUT_PATH = r'C:\Users\Sudarsan R\Desktop\job\avasoft\call log billing automation\input.txt.txt'
STD_RATE_PER_MIN = 2.0
ISD_RATE_PER_MIN = 7.5
TAX_RATE = 0.10

def generate_bill(path):
    try:
        with open(path, 'r') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    if not lines:
        print("Input file is empty.")
        return

    # skip header if first line looks like header
    if lines[0].lower().startswith('custid') or ('#' not in lines[0]):
        lines = lines[1:]

    std_count = isd_count = free_count = 0
    std_duration = isd_duration = free_duration = 0
    custid = None

    for idx, line in enumerate(lines, start=1):
        parts = line.split('#')
        if len(parts) < 5:
            print(f"Skipping malformed line {idx}: {line}")
            continue

        custid = parts[0].strip()
        duration_str = parts[3].strip()
        calltype = parts[-1].strip().lower()

        try:
            duration = int(duration_str)
        except ValueError:
            print(f"Skipping line {idx} — invalid duration '{duration_str}': {line}")
            continue

        if calltype == 'std':
            std_count += 1
            std_duration += duration
        elif calltype == 'isd':
            isd_count += 1
            isd_duration += duration
        elif calltype == 'free':
            free_count += 1
            free_duration += duration   # accumulate free durations (not billed)
        else:
            print(f"Unknown call type on line {idx}: {calltype}")

    # convert seconds to minutes (rounded to 2 decimals)
    std_mins = round(std_duration / 60, 2)
    isd_mins = round(isd_duration / 60, 2)
    free_mins = round(free_duration / 60, 2)

    # compute amounts
    std_amount = std_mins * STD_RATE_PER_MIN
    isd_amount = isd_mins * ISD_RATE_PER_MIN

    std_tax = round(std_amount * TAX_RATE, 2)
    isd_tax = round(isd_amount * TAX_RATE, 2)

    std_final = round(std_amount + std_tax, 2)
    isd_final = round(isd_amount + isd_tax, 2)
    total_bill = round(std_final + isd_final, 2)

    # print summary
    print("\n----- Vodafone Billing Summary -----\n")
    print(f"Customer ID: {custid}\n")
    print(f"STD calls : {std_count}  | total seconds: {std_duration}  | minutes: {std_mins}")
    print(f"ISD calls : {isd_count}  | total seconds: {isd_duration}  | minutes: {isd_mins}")
    print(f"FREE calls: {free_count}  | total seconds: {free_duration}  | minutes: {free_mins}\n")
    print(f"STD charge: {std_mins} mins × ₹{STD_RATE_PER_MIN}/min = ₹{std_amount:.2f}  tax(10%)=₹{std_tax:.2f}  => ₹{std_final:.2f}")
    print(f"ISD charge: {isd_mins} mins × ₹{ISD_RATE_PER_MIN}/min = ₹{isd_amount:.2f}  tax(10%)=₹{isd_tax:.2f}  => ₹{isd_final:.2f}")
    print("-------------------------------------------")
    print(f"Total mobile bill: ₹{total_bill:.2f}\n")

if __name__ == '__main__':
    generate_bill(INPUT_PATH)
