# -*- coding: utf-8 -*-
"""Generate test-evidence chart + project thumbnail with Pillow."""
from PIL import Image, ImageDraw, ImageFont
import openpyxl
from pathlib import Path

ROOT = Path(r"C:\Users\Echo Li\Documents\deepseek-harness\default-workspace\skyguard")
OUT = ROOT / "outputs"


def font(size, bold=False):
    cands = []
    if bold:
        cands = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]
    cands += ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
              "C:/Windows/Fonts/calibri.ttf"]
    for p in cands:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ---- 1) chart: Hailing airport 2025 monthly planned-completion rate -------
wb = openpyxl.load_workbook(ROOT / "data" / "Track 3 Data.xlsx", data_only=True)
ws = wb["01_机场月度运行基线"]
rows = []
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[2] == "海陵国际机场" and r[0] == 2025:
        rows.append((r[1], r[4]))
rows.sort()
months = [m for m, _ in rows]
vals = [v for _, v in rows]
avg = sum(vals) / len(vals)

W, H = 1200, 700
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
L, T, R, B = 110, 70, 1120, 590
ymin, ymax = 0.60, 0.95

def x(i): return L + (i / (len(months) - 1)) * (R - L)
def y(v): return B - (v - ymin) / (ymax - ymin) * (B - T)

# gridlines + y labels
for gv in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
    gy = y(gv)
    d.line([(L, gy), (R, gy)], fill=(225, 225, 225), width=1)
    d.text((L - 60, gy - 8), f"{gv:.2f}", fill=(120, 120, 120), font=font(16))
# x labels
for i, m in enumerate(months):
    d.text((x(i) - 10, B + 8), str(m), fill=(120, 120, 120), font=font(15))
d.text((L, B + 40), "Month (2025)", fill=(60, 60, 60), font=font(18))
d.text((L - 60, 15), "planned-completion rate", fill=(60, 60, 60), font=font(16))

# 12-mo average line (dashed)
ay = y(avg)
for xx in range(L, R, 14):
    d.line([(xx, ay), (xx + 7, ay)], fill=(120, 160, 220), width=2)
d.text((R - 300, ay - 30), f"12-mo self-average = {avg:.3f}", fill=(90, 130, 190), font=font(16))

# trend polyline
pts = [(x(i), y(v)) for i, v in enumerate(vals)]
d.line(pts, fill=(30, 90, 180), width=3)
# points: highlight Jul/Aug anomaly (indices 6,7)
for i, v in enumerate(vals):
    if i in (6, 7):
        d.ellipse([pts[i][0]-7, pts[i][1]-7, pts[i][0]+7, pts[i][1]+7], fill=(200, 60, 60), outline=(150, 30, 30))
    else:
        d.ellipse([pts[i][0]-4, pts[i][1]-4, pts[i][0]+4, pts[i][1]+4], fill=(30, 90, 180))
# annotate anomaly
d.text((x(6) - 40, y(vals[6]) - 45), "designed anomaly (Jul-Aug)", fill=(200, 60, 60), font=font(16, bold=True))

d.text((L, 25), "Hailing Airport 2025 monthly planned-completion rate (simulated)", fill=(20, 20, 20), font=font(20, bold=True))
chart_path = OUT / "baseline_trend.png"
img.save(chart_path)

# ---- 2) thumbnail ---------------------------------------------------------
TW, TH = 1280, 720
t = Image.new("RGB", (TW, TH), (10, 20, 45))
td = ImageDraw.Draw(t)
# simple vertical gradient
for yy in range(TH):
    k = yy / TH
    r = int(10 + (20 - 10) * k)
    g = int(20 + (60 - 20) * k)
    b = int(45 + (120 - 45) * k)
    td.line([(0, yy), (TW, yy)], fill=(r, g, b))
# aircraft trail (dashed arc)
for xx in range(120, 1160, 26):
    td.ellipse([xx, 250 - (xx % 3) * 6, xx + 14, 264 - (xx % 3) * 6], fill=(120, 180, 255))
td.ellipse([1130, 190, 1210, 240], fill=(240, 245, 255))  # "aircraft"
td.polygon([(1150, 215), (1170, 200), (1190, 215), (1170, 240)], fill=(240, 245, 255))

f_title = font(96, bold=True)
f_sub = font(34)
td.text((100, 330), "SkyGuard", fill=(255, 255, 255), font=f_title)
td.text((104, 470), "Explainable AI assistant for flight disruptions", fill=(170, 210, 255), font=f_sub)
td.text((104, 530), "HackSHSID 2026 · Track 3 · Sustainability", fill=(140, 170, 210), font=font(28))
thumb_path = ROOT / "thumbnail.png"
t.save(thumb_path)

print("chart:", chart_path, chart_path.stat().st_size)
print("thumb:", thumb_path, thumb_path.stat().st_size)
