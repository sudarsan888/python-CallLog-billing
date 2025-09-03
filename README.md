# python-CallLog-billing
Telecom Call Log Billing Automation (Python)
# Vodafone Billing (Python)

Simple Python script to generate a mobile bill from call logs.

## Files
- python-billing.py  — billing script
- 9986019198.txt    — sample input (text file)
- .gitignore

## Run (locally)
1. Download or clone the repo.
2. Open terminal in repo folder.
3. Run:
   python python-billing.py 9986019198.txt

## Input format
Each input line:
custid#date#time#duration#calltype

Example:
9986019198#01-09-2025#10:00#180#std

Rates:
- STD = ₹2/min
- ISD = ₹7.5/min
- Tax = 10%
