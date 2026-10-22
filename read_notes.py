# -*- coding: utf-8 -*-
import openpyxl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r"C:\Users\Echo Li\Documents\deepseek-harness\default-workspace\skyguard\data\Track 3 Data.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
for name in ["00_使用说明", "01_数据获取指南"]:
    ws = wb[name]
    print("=" * 70)
    print("SHEET:", name)
    for row in ws.iter_rows(values_only=True):
        if any(c is not None and str(c).strip() != "" for c in row):
            print(" | ".join("" if c is None else str(c) for c in row))
