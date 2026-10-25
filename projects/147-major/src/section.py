# Revised Section A-A (as found Oct 25) - one geometry list, rendered to SVG (viewer tab) and PDF (11x17 at 3/16"=1'-0")
import json
M = json.load(open('model.json')); L = M['levels']
F0, F1, F1R, F2, TOP, ROOF, GR = L['FFL0'], L['FFL1'], L['FFL1R'], L['FFL2'], L['TOP'], L['ROOF'], L['GRADE']
J0T, J0B, J1T, J1B, J1TR, J1BR, J2T, J2B = L['J0T'], L['J0B'], L['J1T'], L['J1B'], L['J1TR'], L['J1BR'], L['J2T'], L['J2B']
CM, CF, CB, DK, OTB, OTR = L['C_MAS'], L['C_FAM'], L['C_BATH'], L['DECK'], L['OLDTB'], L['OLDTR']
VF, ST, VR, AD, RW = 13.25, 28.0, 40.2, 43.67, 55.97
P = []   # (kind, cls, data)
def rect(y0, z0, y1, z1, cls): P.append(('rect', cls, (y0, z0, y1, z1)))
def line(y0, z0, y1, z1, cls): P.append(('line', cls, (y0, z0, y1, z1)))
def poly(pts, cls): P.append(('poly', cls, pts))
def text(y, z, s, cls='t', anchor='start', rot=0): P.append(('text', cls, (y, z, s, anchor, rot)))
def joists(y0, y1, top, depth, cls, sp=1.333):
    rect(y0, top - depth, y1, top, cls + 'band')
    y = y0 + 0.4
    while y < y1 - 0.2: rect(y, top - depth, y + 0.125, top, cls); y += sp
def fi(v):
    f = int(v); i = round((v - f) * 12 * 4) / 4
    if i >= 12: f += 1; i -= 12
    return f"{f}'-{i:g}\""
def dim(y, z0, z1, label, cls='dim'):
    line(y, z0, y, z1, cls); line(y - 0.35, z0, y + 0.35, z0, cls); line(y - 0.35, z1, y + 0.35, z1, cls)
    text(y + 0.45, (z0 + z1) / 2, label, 'dimt')
# ground / slab
rect(-6, GR - 0.6, 62, GR, 'grade')
rect(-3.7, -0.35, RW + 0.5, 0, 'slab')
# exterior walls (front / rear)
rect(-0.6, 0, 0.0, J0B, 'fdn'); rect(RW, 0, RW + 0.55, J0B, 'fdn')
for z0, z1 in [(F0, J1B), (F1, J2B)]: rect(-0.5, z0, 0.15, z1, 'extw')
rect(RW, F0, RW + 0.5, J1BR, 'extw'); rect(RW, F1R, RW + 0.5, J2B, 'extw'); rect(RW, F2, RW + 0.5, TOP, 'extw')
rect(6.67, F2, 7.16, F2 + 3.33, 'extw')   # 40"H knee wall at bedroom 3
# floors (David site visit: 2x10 main house, 2x8 kitchen wing, 12" I-joists addition; rear 2nd floor ~13" lower)
joists(0.6, 56.0, J0T, 11.25 / 12, 'j')
rect(-0.5, F0 - 0.06, RW, F0, 'floor')
joists(0.15, ST, J1T, 9.25 / 12, 'j'); joists(ST, AD, J1TR, 7.25 / 12, 'j'); joists(AD, RW, J1TR, 1.0, 'j')
rect(0.15, F1 - 0.06, ST, F1, 'floor'); rect(ST, F1R - 0.06, RW, F1R, 'floor')
rect(ST - 0.15, F1R, ST + 0.15, F1, 'floor')
rect(7.16, F2 - 0.06, RW, F2, 'floor')
# zone 1: existing platform at the original peak (joists on joists)
joists(0.15, VF, DK, DK - CM - 0.04, 'jy', 1.0); line(0.15, CM, VF, CM, 'ceil')
# zone 2: blue old joists over the 105" ceiling, knee wall + sleepers to the 3rd-floor deck
joists(VF, ST, OTB, 5.5 / 12, 'jb'); line(VF, CF, ST, CF, 'ceil')
rect(VF, OTB, ST, DK, 'void'); rect(VF, DK - 0.125, ST, DK, 'sleep')
# zone 3: red old joists over the 99" ceiling
joists(ST, VR, OTR, 5.5 / 12, 'jr'); line(ST, CB, VR, CB, 'ceil')
rect(ST, OTR, VR, DK, 'void'); rect(ST, DK - 0.125, VR, DK, 'sleep')
for y in (VF, ST, VR - 0.3): rect(y, OTB if y < ST else OTR, y + 0.3, DK - 0.125, 'kw')
# mech room + zone 4: new 9-1/2" TJIs at full depth
joists(VR, 56.0, J2T, 9.5 / 12, 'jn'); line(VR, L['CEIL1'], RW, L['CEIL1'], 'ceil')
# ducts
rect(VF + 0.3, OTB + 0.03, ST - 0.3, OTB + 0.70, 'ductx'); text(VF + 0.4, CF - 1.5, 'A + Z are 8" deep - void here is only ~6"', 'callx')
rect(ST + 0.3, OTR + 0.03, VR - 0.4, OTR + 0.70, 'duct'); text((ST + VR) / 2, OTR + 0.36, 'Trunk C 18x8 + return Y 16x8 (void ~25")', 'ductt', 'middle')
rect(0.9, CM - 0.68, VF, CM, 'duct'); rect(0.75, CM - 0.85, VF, CM, 'bulk'); text((0.9 + VF) / 2, CM - 0.45, 'A 10x8 in bulkhead', 'ductt', 'middle')
rect(VR + 0.2, J2B - 0.68, RW - 0.3, J2B, 'duct'); rect(VR + 0.05, J2B - 0.85, RW - 0.2, L['CEIL1'], 'bulk'); text((VR + RW) / 2, J2B - 0.45, 'C / B + branches in bulkhead', 'ductt', 'middle')
rect(41.84, F1R, 43.6, F1R + 5.3, 'equip'); text(42.72, F1R + 2.6, 'F-2', 'eqt', 'middle')
rect(1.96, 0, 4.32, 5.3, 'equip'); text(3.14, 2.6, 'F-1', 'eqt', 'middle')
rect(4.3, J0B - 0.5, 31.0, J0B, 'duct'); text(18, J0B - 0.25, 'F-1 trunks D / F / E under basement joists', 'ductt', 'middle')
# stairs
def stairs(y0, y1, z0, z1, n):
    pts = []
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n; z = z0 + (z1 - z0) * i / n
        pts += [(y, z), (y + (y1 - y0) / n, z)] if i < n else [(y, z)]
    poly(pts, 'stair')
stairs(19.3, 28.3, 0, F0, 11); stairs(16.4, 28.3, F0, F1R, 17); stairs(15.0, 28.3, F1, F2, 16)
# roofs
poly([(-0.8, J2B - 0.2), (6.67, F2 + 3.33), (6.67, F2 + 3.6), (-0.8, J2B + 0.1)], 'roofs')
rect(6.3, TOP, 56.6, ROOF + 0.15, 'roof')
# level lines + labels
for z, lab in [(0, 'FIN. BASEMENT SLAB  107.63'), (GR, 'ESTABLISHED GRADE  109.93'), (F0, 'FIN. GROUND FLOOR  110.52'), (F1, 'FIN. SECOND FLOOR (front)  113.85'),
               (F1R, 'FIN. SECOND FLOOR (rear)  ~13" lower'), (F2, 'FIN. THIRD FLOOR  116.90'), (TOP, 'TOP OF DBL PLATE  119.60')]:
    line(-6, z, 61.5, z, 'lvl'); text(61.7, z, lab, 'lvlt')
# zone dims (ceiling heights)
dim(10.0, F1, CM, fi(CM - F1)); text(1.0, F1 + 5.6, '1  primary bedroom', 'zone')
dim(14.2, F1, CF, fi(CF - F1)); text(20.5, F1 + 1.4, '2  family rm / stair', 'zone')
dim(31.0, F1R, CB, fi(CB - F1R)); text(33.0, F1R + 2.6, '3  hall / bath / laundry', 'zone')
dim(53.0, F1R, L['CEIL1'], fi(L['CEIL1'] - F1R)); text(46.0, F1R + 5.6, '4  bedroom 2', 'zone')
dim(12.0, F0, L['CEIL0'], fi(L['CEIL0'] - F0)); dim(36.0, F0, L['CEIL0R'], fi(L['CEIL0R'] - F0)); dim(50.0, F0, L['CEIL0A'], fi(L['CEIL0A'] - F0))
dim(15.0, 0, J0B, fi(J0B)); dim(30.0, F2, TOP, fi(TOP - F2))
text(1.5, F0 + 6.5, 'EXIST. LIVING / DINING', 'room'); text(30, F0 + 6.5, 'KITCHEN', 'room'); text(45, F0 + 6.5, 'FAMILY ROOM', 'room')
text(19, F2 + 5.5, 'BEDROOM 3 / ENSUITE / W.I.C.', 'room'); text(46, F2 + 5.5, 'PRIMARY BEDROOM', 'room'); text(6, 4.5, 'BASEMENT', 'room')
# callouts
text(0.6, DK + 0.5, 'Existing platform at the original peak - joists on joists (yellow)', 'cally')
text(VF + 0.4, CF - 0.55, 'Blue old joists over the 105" ceiling (2x6 assumed)', 'callb')
text(ST + 0.4, CB - 0.55, 'Red old joists over the 99" ceiling (2x6 assumed)', 'callr')
text(ST + 0.6, DK + 1.35, 'Knee wall + sleepers bring the deck to 116.90 (green)', 'callg')
text(ST + 0.2, F1 + 0.35, '2R step (~13")', 'call')
text(VR + 3.0, DK + 0.5, 'New 9-1/2" TJI (mech rm + addition)', 'call')
text(-5.6, -1.6, 'FRONT (Major St)', 'call'); text(52.0, -1.6, 'REAR', 'call')

CSS = {
 'grade': ('var(--sg)', 'none', 0), 'slab': ('var(--sc)', 'none', 0), 'fdn': ('var(--sc)', 'var(--sk)', .6), 'extw': ('var(--sw)', 'var(--sk)', .6),
 'floor': ('var(--sk)', 'none', 0), 'jband': ('none', 'none', 0), 'j': ('var(--sj)', 'none', 0), 'jnband': ('none', 'none', 0), 'jn': ('var(--sn)', 'none', 0),
 'jbband': ('none', 'none', 0), 'jb': ('#2F67CF', 'none', 0), 'jrband': ('none', 'none', 0), 'jr': ('#D33A2C', 'none', 0),
 'void': ('rgba(46,160,90,.14)', '#2E9E5A', 1.2), 'sleep': ('#2E9E5A', 'none', 0), 'jyband': ('none', 'none', 0), 'jy': ('#D9A400', 'none', 0), 'ceil': ('none', 'var(--sk)', 1.4), 'ductx': ('rgba(211,47,47,.25)', '#D32F2F', 1.2), 'kw': ('#2E9E5A', 'none', 0), 'duct': ('var(--sd)', 'var(--sk)', .5), 'bulk': ('rgba(229,138,0,.18)', '#E08A00', 1),
 'equip': ('var(--se)', 'var(--sk)', .5), 'stair': ('none', 'var(--sk)', .8), 'roof': ('var(--sr)', 'none', 0), 'roofs': ('var(--sr)', 'none', 0),
 'lvl': ('none', 'var(--sl)', .5), 'dim': ('none', 'var(--sk)', .7)}
TXT = {'t': (9, 'var(--sk)', 400), 'dimt': (9.5, 'var(--sk)', 700), 'lvlt': (8.5, 'var(--sm)', 500), 'zone': (10, 'var(--sk)', 700), 'room': (8.5, 'var(--sm)', 600),
       'call': (8.5, 'var(--sk)', 500), 'callb': (8.5, '#2F67CF', 700), 'callr': (8.5, '#D33A2C', 700), 'callg': (8.5, '#2E9E5A', 700), 'cally': (8.5, '#B07F00', 700), 'callx': (8.5, '#D32F2F', 700), 'ductt': (7.5, 'var(--sk)', 600), 'eqt': (8.5, '#FFFFFF', 700)}
K = 13.0; Y0, Z1 = -6.5, 43.5
def X(y): return (y - Y0) * K
def Yv(z): return (Z1 - z) * K
def svg():
    w = (62 + 22 - Y0) * K; h = (Z1 + 3) * K
    o = [f'<svg viewBox="0 0 {w:.0f} {h:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Revised section A-A, 147 Major St" style="width:100%;height:auto;font-family:var(--f-mono)">']
    for k, c, d in P:
        if k == 'rect':
            f, s, sw = CSS[c]; y0, z0, y1, z1 = d
            if f == 'none' and s == 'none': continue
            o.append(f'<rect x="{X(y0):.1f}" y="{Yv(z1):.1f}" width="{(y1-y0)*K:.1f}" height="{(z1-z0)*K:.1f}" fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
        elif k == 'line':
            f, s, sw = CSS[c]; y0, z0, y1, z1 = d
            dash = ' stroke-dasharray="6 4"' if c == 'lvl' else ''
            o.append(f'<line x1="{X(y0):.1f}" y1="{Yv(z0):.1f}" x2="{X(y1):.1f}" y2="{Yv(z1):.1f}" stroke="{s}" stroke-width="{sw}"{dash}/>')
        elif k == 'poly':
            f, s, sw = CSS[c]
            pts = ' '.join(f'{X(y):.1f},{Yv(z):.1f}' for y, z in d)
            o.append(f'<{"polyline" if c == "stair" else "polygon"} points="{pts}" fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
        else:
            sz, col, wt = TXT[c]; y, z, s, an, rot = d
            s = s.replace('&', '&amp;').replace('<', '&lt;')
            o.append(f'<text x="{X(y):.1f}" y="{Yv(z)+3:.1f}" font-size="{sz}" fill="{col}" font-weight="{wt}" text-anchor="{an}">{s}</text>')
    o.append('</svg>'); return ''.join(o)
open('section.svg', 'w').write(svg())
# ---- PDF at true 3/16" = 1'-0" on 11x17 landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
PAL = {'var(--sg)': '#9DBF7E', 'var(--sc)': '#B9B6AE', 'var(--sk)': '#1C2321', 'var(--sw)': '#C9C3B6', 'var(--sj)': '#C9A16B', 'var(--sn)': '#B9873F', 'var(--sd)': '#AEB7BE',
       'var(--se)': '#5C666C', 'var(--sr)': '#6E7174', 'var(--sl)': '#8A9590', 'var(--sm)': '#4A5551'}
def col(v):
    if v == 'none': return None
    if v.startswith('rgba'):
        r, g, b, a = [float(x) for x in v[5:-1].split(',')]; return Color(r/255, g/255, b/255, alpha=a)
    return HexColor(PAL.get(v, v))
S = 13.5; W, H = 1224, 792
c = canvas.Canvas('147-Major-Section-AA-revised.pdf', pagesize=(W, H))
ox, oz = 60 + 6.5 * S, 95
def PX(y): return ox + y * S
def PZ(z): return oz + z * S
for k, cl, d in P:
    if k == 'rect':
        f, s, sw = CSS[cl]; y0, z0, y1, z1 = d
        if f == 'none' and s == 'none': continue
        if col(f): c.setFillColor(col(f))
        if col(s): c.setStrokeColor(col(s)); c.setLineWidth(sw * 0.8)
        c.rect(PX(y0), PZ(z0), (y1 - y0) * S, (z1 - z0) * S, fill=1 if col(f) else 0, stroke=1 if col(s) else 0)
    elif k == 'line':
        f, s, sw = CSS[cl]; y0, z0, y1, z1 = d
        c.setStrokeColor(col(s)); c.setLineWidth(sw * 0.8); c.setDash(5, 3) if cl == 'lvl' else c.setDash()
        c.line(PX(y0), PZ(z0), PX(y1), PZ(z1)); c.setDash()
    elif k == 'poly':
        f, s, sw = CSS[cl]; pth = c.beginPath(); pth.moveTo(PX(d[0][0]), PZ(d[0][1]))
        for y, z in d[1:]: pth.lineTo(PX(y), PZ(z))
        if cl != 'stair': pth.close()
        if col(s): c.setStrokeColor(col(s)); c.setLineWidth(sw * 0.8)
        if col(f): c.setFillColor(col(f))
        c.drawPath(pth, fill=1 if col(f) else 0, stroke=1 if col(s) else 0)
    else:
        sz, cc, wt = TXT[cl]; y, z, s, an, rot = d
        c.setFillColor(col(cc) if cc.startswith('var') or cc.startswith('#') else HexColor(cc)); c.setFont('Helvetica-Bold' if wt >= 600 else 'Helvetica', sz * 0.85)
        (c.drawCentredString if an == 'middle' else c.drawString)(PX(y), PZ(z) - 3, s)
c.setFillColor(HexColor('#1C2321')); c.setFont('Helvetica-Bold', 15); c.drawString(40, H - 40, '147 MAJOR ST  -  SECTION A-A  (REVISED, AS FOUND)')
c.setFont('Helvetica', 9)
for i, s in enumerate(['PalmView Custom Homes  ·  coordination drawing  ·  Oct 25, 2026  ·  NOT FOR CONSTRUCTION - for HVAC / framing coordination only',
                       'Permit A12 section + geodetic levels (A10-A12) + David site visit (framing and measured ceilings) + Raff sketch Oct 25 (platform, old joists, knee wall).',
                       'Assumed: old joists 2x6, 3rd-floor deck on 2x4 sleepers (3" build-up) at permit 116.90. Platform zone 1 front, blue 13\'-3" to 28\'-0", red 28\'-0" to 40\'-2" (mech room goes to 120"). Confirm on site.',
                       'Scale 3/16" = 1\'-0" (11x17). Front (Major St) at left. Rear 2nd floor ~13" lower (fits David\'s 118" / 108" / 105" main-floor ceilings and UP 2R).']):
    c.drawString(40, H - 58 - i * 12, s)
c.showPage(); c.save()
print('ok', len(P))
