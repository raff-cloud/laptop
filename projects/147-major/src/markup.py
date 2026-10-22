import json, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor
SRC = '/root/.claude/uploads/8f9fd665-bf8b-5e11-bfc8-a02fabbfa285/70d892b3-Attachment20621958.PDF'
M = json.load(open('model.json')); Q = json.load(open('questions.json'))
by = {e['id']: e for e in M['elements']}
O = {'B': (6, 276.54, 96.54), 'G': (7, 276.78, 94.02), 'S': (8, 276.96, 94.26), 'T': (9, 276.84, 94.26)}
S = 13.5; H = 1224
RED = HexColor('#D32F2F'); AMB = HexColor('#E08A00'); BLU = HexColor('#1F5FBF')
# markers: (sheet level, element ids or explicit box ft, label, colour)
def bb(ids):
    xs0 = min(by[i]['x0'] for i in ids); xs1 = max(by[i]['x1'] for i in ids); ys0 = min(by[i]['y0'] for i in ids); ys1 = max(by[i]['y1'] for i in ids)
    return xs0, xs1, ys0, ys1
MK = [
 ('S', bb(['D2-A']), 'Q1', RED), ('S', bb(['D2-C']), 'Q1', RED), ('S', bb(['R2-Z', 'R2-Z2']), 'Q1', RED), ('S', bb(['R2-Y']), 'Q1', RED),
 ('S', bb(['D2-B', 'S-28', 'S-33']), 'Q2', RED), ('T', bb(['T-25', 'T-28']), 'Q2', RED),
 ('B', bb(['S-23b', 'S-10b', 'S-8b']), 'Q3', RED), ('G', (13.5, 16.2, 43.3, 44.6), 'Q3', RED),
 ('B', bb(['S-9v']), 'Q4', RED), ('G', bb(['T-9']), 'Q4', RED), ('B', bb(['R-M3', 'R-M5', 'R-8Rv']), 'Q4', RED), ('G', bb(['T-8R']), 'Q4', RED),
 ('T', bb(['T-3R', 'R-3Rv']), 'Q5', RED),
 ('T', bb(['R-1Rv']), 'Q6', AMB), ('T', bb(['R-2Rv']), 'Q6', AMB), ('S', bb(['R-5Rv']), 'Q6', AMB), ('S', bb(['R-6Rv']), 'Q6', AMB), ('G', bb(['R-9Rv']), 'Q6', AMB), ('B', bb(['S-24v']), 'Q6', AMB),
 ('S', bb(['R-4Rv', 'T-4R']), 'Q7', RED),
 ('G', (4.9, 7.2, 28.2, 43.8), 'Q8', RED), ('G', (13.3, 16.3, 31.5, 40.5), 'Q8', AMB),
 ('G', (4.0, 7.2, 37.3, 40.2), 'Q9', RED),
 ('B', bb(['D-F0', 'EQ-HWT', 'D-PL1']), 'Q10', RED),
 ('S', (13.2, 16.4, 14.8, 28.5), 'Q11', BLU), ('T', (13.2, 16.4, 14.8, 28.5), 'Q11', BLU),
 ('S', (0.8, 14.5, 0.3, 6.7), 'Q13', AMB),
 ('G', bb(['T-16']), 'S1', AMB), ('G', bb(['T-12']), 'S2', AMB), ('B', bb(['D-E']), 'S3', AMB),
]
for f in ('X-B1',): pass
TITLE = {q['title'].split(' · ')[0]: q['title'].split(' · ', 1)[1] for q in Q['questions']}
TITLE.update({'S1': 'Supply 16 boot tight to the bay corner', 'S2': 'Supply 12 kick register under the pantry', 'S3': 'Trunk E ends ½" off the old rear wall'})
rd = PdfReader(SRC); wr = PdfWriter()
# cover sheet
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(792, 1224))
c.setFont('Helvetica-Bold', 22); c.drawString(54, 1150, '147 Major St — HVAC clash mark-up')
c.setFont('Helvetica', 11)
c.drawString(54, 1128, 'HVAC Designs LO# 113963 (HVA 26 167838) vs permit 26 167838 BLD 00 · PalmView BIM review · Oct 22, 2026')
c.drawString(54, 1112, 'Two systems: F-1 basement (basement + main floor from below) · F-2 2nd-floor mech room (2nd + 3rd floors from the 3rd-floor joist space).')
y = 1080
c.setFont('Helvetica-Bold', 12); c.drawString(54, y, 'Questions / open items'); y -= 20
for q in Q['questions']:
    c.setFillColor(RED); c.setFont('Helvetica-Bold', 10); c.drawString(54, y, q['title'].split(' · ')[0]); c.setFillColor(Color(0, 0, 0))
    c.setFont('Helvetica-Bold', 10); c.drawString(92, y, q['title'].split(' · ', 1)[1][:95]); y -= 13
    c.setFont('Helvetica', 9)
    words = (q['detail'] + f"  Owner: {q['owner']}. Status: {q['status'].upper()}.").split(); line = ''
    for w in words:
        if c.stringWidth(line + ' ' + w, 'Helvetica', 9) > 640: c.drawString(92, y, line); y -= 11; line = w
        else: line = (line + ' ' + w).strip()
    c.drawString(92, y, line); y -= 17
y -= 6; c.setFont('Helvetica-Bold', 12); c.drawString(54, y, 'Not connected (no route drawn)'); y -= 16; c.setFont('Helvetica', 9)
for r in M['conn']:
    if not r['ok']: c.drawString(66, y, f"• {r['name']}"); y -= 12
y -= 8; c.setFont('Helvetica-Bold', 12); c.drawString(54, y, 'Legend'); y -= 16; c.setFont('Helvetica', 9)
for col, t in [(RED, 'Hard clash / decision needed'), (AMB, 'Soft clash, site check, or stack too deep for its wall'), (BLU, 'Drawing conflict between sheets')]:
    c.setStrokeColor(col); c.setLineWidth(2); c.rect(66, y - 2, 18, 9); c.setFillColor(Color(0, 0, 0)); c.drawString(92, y, t); y -= 14
c.showPage(); c.save(); buf.seek(0)
wr.add_page(PdfReader(buf).pages[0])
for lv in ('B', 'G', 'S', 'T'):
    pg, ox, oy = O[lv]
    page = rd.pages[pg - 1]
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(792, 1224))
    if lv == 'S':
        c.setFillColor(Color(0.88, 0.54, 0, alpha=0.18)); c.setStrokeColor(Color(0, 0, 0, alpha=0))
        for e in M['elements']:
            if e['cat'] == 'bulkhead':
                x0 = ox + e['x0'] * S; x1 = ox + e['x1'] * S; t0 = oy + e['y0'] * S; t1 = oy + e['y1'] * S
                c.rect(x0, H - t1, x1 - x0, t1 - t0, fill=1, stroke=0)
    used = []
    for (l, (x0, x1, y0, y1), lab, col) in MK:
        if l != lv: continue
        X0 = ox + x0 * S - 5; X1 = ox + x1 * S + 5; T0 = oy + y0 * S - 5; T1 = oy + y1 * S + 5
        c.setStrokeColor(col); c.setLineWidth(1.6); c.roundRect(X0, H - T1, X1 - X0, T1 - T0, 6, stroke=1, fill=0)
        c.setFillColor(col); w = c.stringWidth(lab, 'Helvetica-Bold', 8) + 8
        c.roundRect(X1 - 2, H - T0 - 2, w, 12, 3, stroke=0, fill=1); c.setFillColor(Color(1, 1, 1)); c.setFont('Helvetica-Bold', 8); c.drawString(X1 + 2, H - T0 + 1, lab)
        if lab not in used: used.append(lab)
    # legend block bottom-left above title block
    yy = 330; c.setFillColor(Color(1, 1, 1, alpha=0.92)); c.setStrokeColor(RED); c.setLineWidth(1)
    c.rect(24, yy - 14 * len(used) - 22, 330, 14 * len(used) + 28, fill=1, stroke=1)
    c.setFillColor(RED); c.setFont('Helvetica-Bold', 9); c.drawString(32, yy - 10, 'PALMVIEW CLASH REVIEW · OCT 22, 2026')
    c.setFont('Helvetica', 8); c.setFillColor(Color(0, 0, 0))
    for i, lab in enumerate(used): c.drawString(32, yy - 26 - i * 14, f'{lab}  {TITLE.get(lab, "")[:62]}')
    if lv == 'S':
        c.setFillColor(AMB); c.drawString(32, yy - 26 - len(used) * 14 + 2, '')
    c.showPage(); c.save(); buf.seek(0)
    page.merge_page(PdfReader(buf).pages[0]); wr.add_page(page)
wr.add_metadata({'/Title': '147 Major St - HVAC clash mark-up', '/Author': 'PalmView Custom Homes'})
wr.write(open('147-Major-clash-markup.pdf', 'wb'))
print('ok')
