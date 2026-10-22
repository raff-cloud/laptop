# 147 Major St - BIM clash model generator
# Coordinates in feet. x = across the lot (0 = south/left exterior face of the existing brick wall, 16.67 = party wall CL with 149 Major)
# y = front-to-back (0 = face of front main wall, + toward rear). z = up from basement slab (geodetic 107.63).
import json, math
FT = 0.3048
def el(geo): return round((geo - 107.63) / FT, 3)
L = dict(SLAB=0.0, FFL0=el(110.52), FFL1=el(113.85), FFL2=el(116.90), TOP=el(119.60), ROOF=el(119.92), GRADE=el(109.93))
# floor build-ups (3/4 subfloor + 3/4 finish = 1.5")
L['J0T'] = round(L['FFL0'] - 0.125, 3); L['J0B'] = round(L['J0T'] - 11.25/12, 3)          # ex. 2x12 under main floor
L['J1T'] = round(L['FFL1'] - 0.125, 3); L['J1B'] = round(L['J1T'] - 11.25/12, 3)          # ex. 2x12 under 2nd floor
L['J2T'] = round(L['FFL2'] - 0.125, 3); L['J2B'] = round(L['J2T'] - 9.5/12, 3)            # 9-1/2" TJI under 3rd floor
L['CEIL0'] = round(L['J1B'] - 0.05, 3); L['CEIL1'] = round(L['J2B'] - 0.05, 3); L['CEIL2'] = round(L['TOP'], 3)
E = []
def box(id, name, cat, lvl, x0, x1, y0, y1, z0, z1, mat, **kw):
    d = dict(id=id, name=name, cat=cat, shape='box', lvl=lvl, x0=round(min(x0,x1),3), x1=round(max(x0,x1),3), y0=round(min(y0,y1),3), y1=round(max(y0,y1),3), z0=round(z0,3), z1=round(z1,3), mat=mat)
    d.update(kw); E.append(d); return d
def cyl(id, name, cat, lvl, x, y, z0, z1, dia, mat, axis='z', **kw):
    r = dia/24
    if axis == 'z': d = dict(x0=x-r, x1=x+r, y0=y-r, y1=y+r, z0=z0, z1=z1)
    d2 = dict(id=id, name=name, cat=cat, shape='cyl', lvl=lvl, axis=axis, d=dia, mat=mat, **{k: round(v,3) for k,v in d.items()})
    d2.update(kw); E.append(d2); return d2

LV = {'B': (L['SLAB'], L['J0B']), 'G': (L['FFL0'], L['CEIL0']), 'S': (L['FFL1'], L['CEIL1']), 'T': (L['FFL2'], L['TOP'])}
STRUCT_TOP = {'B': L['J0T'], 'G': L['J1T'], 'S': L['J2T'], 'T': L['ROOF']}
# ---------------------------------------------------------------- walls (from permit vectors A6-A9, 13.5 pt/ft)
WALLS = {
 'B': [
  ('Ex. stone/brick fdn - south', 0.0, 0.85, -0.2, 28.7, 'parge', True),
  ('Ex. fdn - south wing (kitchen)', 4.2, 5.05, 28.7, 43.5, 'parge', True),
  ('Ex. fdn - rear wing south (42" opening cut)', 4.25, 5.1, 48.44, 56.5, 'parge', True),
  ('Ex. fdn - rear wing south (pier)', 4.2, 5.05, 43.5, 44.94, 'parge', True),
  ('Ex. fdn - party wall', 16.25, 16.67, -0.4, 56.5, 'parge', True),
  ('Ex. fdn - front (S of bay)', 0.0, 1.64, -0.2, 0.62, 'parge', True),
  ('Ex. fdn - old rear wall W', 5.05, 11.68, 43.5, 44.34, 'brick', True),
  ('Ex. fdn - old rear wall E', 14.19, 16.25, 43.5, 44.34, 'brick', True),
  ('Ex. fdn - rear', 4.27, 16.67, 55.6, 56.5, 'parge', True),
  ('New 10" block fdn - addition S', 0.12, 0.96, 43.66, 56.53, 'concrete', True),
  ('New 10" block fdn - addition rear', 0.12, 4.27, 55.72, 56.53, 'concrete', True),
  ('New 10" block fdn - addition front', 0.12, 4.21, 43.66, 44.5, 'concrete', True),
  ('Storage partition', 0.85, 7.36, 5.67, 5.99, 'drywall', False),
  ('Storage partition E', 9.87, 11.32, 5.67, 5.99, 'drywall', False),
  ('Storage/cold room wall', 10.99, 11.32, 0.8, 5.99, 'drywall', False),
  ('Bath partition N', 5.01, 10.38, 34.79, 35.11, 'drywall', False),
  ('Bath partition E', 10.06, 10.38, 37.62, 43.5, 'drywall', False),
 ],
 'G': [
  ('Ex. brick - south', 0.0, 0.85, 0.0, 28.73, 'brick', True),
  ('Ex. brick - dining rear return', 0.0, 5.05, 27.95, 28.3, 'brick', True),
  ('Ex. dbl brick - kitchen wing south', 4.18, 5.0, 28.3, 43.68, 'brick', True),
  ('Ex. demising stud wall (party)', 16.44, 16.87, 0.0, 43.68, 'drywall', True),
  ('New demising wall (party, addition)', 16.2, 16.87, 43.68, 56.0, 'drywall', True),
  ('Front wall S of bay', 0.0, 1.62, 0.0, 0.62, 'brick', True),
  ('Front wall at porch', 9.97, 13.01, -0.3, 0.55, 'brick', True),
  ('Front wall N (entry)', 15.52, 16.67, -0.34, 0.5, 'brick', True),
  ('Foyer wall W', 10.99, 11.32, 0.8, 5.99, 'drywall', False),
  ('Foyer wall S', 9.87, 11.32, 5.67, 5.99, 'drywall', False),
  ('Foyer wall S (E)', 15.0, 16.0, 5.67, 5.99, 'drywall', False),
  ('Chimney breast', 0.85, 1.9, 4.9, 9.8, 'brick', False),
  ('Pantry/storage wall', 2.03, 7.24, 44.27, 44.52, 'drywall', False),
  ('Pantry back', 5.05, 7.24, 43.68, 43.9, 'drywall', False),
  ('Addition S wall (5/8 X, <1.2 m to lot line)', 0.12, 0.69, 43.68, 56.55, 'siding', True),
  ('Powder wall N', 0.69, 1.71, 50.15, 50.49, 'drywall', False),
  ('Powder wall N2', 2.03, 4.69, 50.15, 50.49, 'drywall', False),
  ('Powder/family wall', 4.69, 5.03, 48.02, 55.96, 'drywall', False),
  ('Storage wall', 1.62, 2.03, 44.27, 45.19, 'drywall', False),
  ('Rear wall S', 0.12, 5.03, 55.96, 56.48, 'siding', True),
 ],
 'S': [
  ('Ex. brick - south', 0.0, 0.85, -0.5, 26.4, 'brick', True),
  ('New frame - south (over side yard)', 0.0, 0.45, 26.4, 44.5, 'siding', True),
  ('Addition S wall', 0.12, 0.69, 44.5, 56.4, 'siding', True),
  ('Demising wall (party)', 16.44, 16.87, -0.5, 44.2, 'drywall', True),
  ('New demising wall (party, addition)', 16.2, 16.87, 44.2, 56.4, 'drywall', True),
  ('Front wall', 0.0, 16.67, -0.6, 0.15, 'brick', True),
  ('Primary closet wall', 0.85, 11.1, 12.9, 13.25, 'drywall', False),
  ('Linen', 7.6, 9.5, 13.25, 15.6, 'drywall', False),
  ('Family rm wall E', 12.55, 12.9, 13.25, 26.4, 'drywall', False),
  ('Family rm rear wall', 0.45, 12.9, 26.4, 26.75, 'drywall', False),
  ('Bath wall N', 3.7, 9.6, 27.4, 27.7, 'drywall', False),
  ('Bath wall E', 9.6, 9.92, 27.4, 33.4, 'drywall', False),
  ('Bath/laundry wall', 3.7, 9.6, 36.3, 36.6, 'drywall', False),
  ('Laundry/WIC wall', 4.4, 13.8, 40.2, 40.5, 'drywall', False),
  ('WIC / mech wall', 8.5, 8.8, 40.5, 44.2, 'drywall', False),
  ('Mech rm E wall', 13.5, 13.8, 40.5, 44.2, 'drywall', False),
  ('Bedroom 2 front wall', 0.69, 13.24, 43.93, 44.27, 'drywall', False),
  ('Rear wall', 0.0, 16.67, 55.97, 56.5, 'siding', True),
 ],
 'T': [
  ('40"H knee wall (front)', 0.0, 16.44, 6.67, 7.16, 'drywall', True),
  ('South wall (existing)', 0.0, 0.5, 7.16, 21.67, 'siding', True),
  ('South wall (addition)', 0.12, 0.69, 21.67, 56.4, 'siding', True),
  ('Ex./new demising wall (party)', 16.44, 16.87, 6.5, 21.67, 'drywall', True),
  ('New demising wall (party, addition)', 16.2, 16.87, 21.67, 56.4, 'drywall', True),
  ('Bedroom 3 / ensuite', 0.5, 4.94, 21.67, 22.01, 'drywall', False),
  ('Bedroom 3 / ensuite E', 7.11, 10.19, 21.67, 22.01, 'drywall', False),
  ('Vanity wall (ensuite / hall)', 9.58, 9.92, 22.01, 31.13, 'drywall', False),
  ('Ensuite wall S', 4.18, 4.75, 28.21, 44.25, 'drywall', False),
  ('Tub alcove wall', 0.5, 4.75, 28.21, 28.3, 'drywall', False),
  ('Hall wall', 9.58, 13.37, 30.81, 31.13, 'drywall', False),
  ('Shower / WIC wall', 4.75, 12.62, 37.26, 37.5, 'drywall', False),
  ('WIC rear wall', 0.71, 12.92, 43.91, 44.25, 'drywall', False),
  ('WIC E wall', 12.3, 12.62, 37.5, 43.95, 'drywall', False),
  ('Rear wall (12\' slider)', 0.0, 16.67, 55.97, 56.5, 'siding', True),
 ],
}
# windows / doors (elevations A10-A12) -> (id, name, level, wall-axis, x/y position range, sill, head above floor)
WIN = [
 # ('id','name','lvl', ori 'x' (in a wall running along x, i.e. front/rear) or 'y' (side wall), line coord, a, b, sill, head)
 ('WN-B1', 'Ex. basement window 24x24 (south)', 'B', 'y', 0.4, 13.6, 15.6, 5.55, 7.55),
 ('WN-G1', 'Ex. bay centre window', 'G', 'x', -3.5, 4.4, 7.2, 2.6, 8.0),
 ('WN-G2', 'Ex. bay side window S', 'G', 'x', -2.2, 2.0, 3.3, 2.6, 8.0),
 ('WN-G3', 'Ex. bay side window N', 'G', 'x', -2.2, 8.3, 9.6, 2.6, 8.0),
 ('WN-G4', 'Ex. kitchen window over sink (44")', 'G', 'y', 4.55, 32.69, 36.37, 3.6, 7.5),
 ('DR-G1', 'Rear 10\' sliding door 120x84', 'G', 'x', 56.2, 5.3, 15.3, 0.0, 7.0),
 ('WN-G5', 'Rear 34x80 unit (storage)', 'G', 'x', 56.2, 1.4, 4.2, 0.0, 6.67),
 ('WN-G6', 'South window (dining, 12.67 sf)', 'G', 'y', 0.4, 21.2, 23.6, 3.0, 7.0),
 ('WN-S1', 'Rear 144x78 window', 'S', 'x', 56.2, 2.0, 14.0, 1.5, 8.0),
 ('WN-S2', 'South window (bath, 10.6 sf)', 'S', 'y', 0.2, 30.0, 32.4, 3.5, 7.5),
 ('WN-S3', 'Front windows (primary)', 'S', 'x', -0.2, 3.0, 13.0, 2.5, 7.5),
 ('DR-T1', 'Rear 12\' sliding door 144x84 to balcony', 'T', 'x', 56.2, 2.3, 14.3, 0.0, 7.0),
 ('WN-T1', 'South 120x60 window (fire shutter)', 'T', 'y', 0.2, 46.0, 56.0 - 0.0, 2.5, 7.5),
 ('WN-T2', 'South 34x64 window (ensuite)', 'T', 'y', 0.2, 23.4, 26.2, 2.4, 7.7),
]
FFL = {'B': 0.0, 'G': L['FFL0'], 'S': L['FFL1'], 'T': L['FFL2']}
def wall_boxes():
    n = 0
    for lv, ws in WALLS.items():
        z0, z1 = FFL[lv], STRUCT_TOP[lv] if lv != 'T' else L['TOP']
        if lv == 'B': z1 = L['J0B']
        if lv == 'G': z1 = L['J1B']
        if lv == 'S': z1 = L['J2B']
        for (nm, x0, x1, y0, y1, mat, ext) in ws:
            n += 1
            wid = f'W{lv}{n}'
            th = min(x1-x0, y1-y0)
            nm2 = f'{nm} ({th*12:.1f}")'
            # split around windows in this wall
            cuts = []
            for (wid_, wn, wl, ori, c, a, b, s, h) in WIN:
                if wl != lv: continue
                if ori == 'y' and x0-0.3 <= c <= x1+0.3 and a < y1 and b > y0: cuts.append(('y', a, b, s, h))
                if ori == 'x' and y0-0.3 <= c <= y1+0.3 and a < x1 and b > x0: cuts.append(('x', a, b, s, h))
            if not cuts:
                box(wid, nm2, 'wall', lv, x0, x1, y0, y1, z0, z1, mat); continue
            if (x1-x0) < (y1-y0):  # wall along y
                pos = y0; k = 0
                for (_, a, b, s, h) in sorted(cuts, key=lambda c: c[1]):
                    a = max(a, y0); b = min(b, y1)
                    if a > pos: box(f'{wid}{"abcdefgh"[k]}', nm2, 'wall', lv, x0, x1, pos, a, z0, z1, mat); k += 1
                    if s > 0.01: box(f'{wid}s{k}', nm2, 'wall', lv, x0, x1, a, b, z0, z0+s, mat)
                    box(f'{wid}h{k}', nm2, 'wall', lv, x0, x1, a, b, z0+h, z1, mat); pos = b; k += 1
                if pos < y1: box(f'{wid}{"abcdefgh"[k]}', nm2, 'wall', lv, x0, x1, pos, y1, z0, z1, mat)
            else:
                pos = x0; k = 0
                for (_, a, b, s, h) in sorted(cuts, key=lambda c: c[1]):
                    a = max(a, x0); b = min(b, x1)
                    if a > pos: box(f'{wid}{"abcdefgh"[k]}', nm2, 'wall', lv, pos, a, y0, y1, z0, z1, mat); k += 1
                    if s > 0.01: box(f'{wid}s{k}', nm2, 'wall', lv, a, b, y0, y1, z0, z0+s, mat)
                    box(f'{wid}h{k}', nm2, 'wall', lv, a, b, y0, y1, z0+h, z1, mat); pos = b; k += 1
                if pos < x1: box(f'{wid}{"abcdefgh"[k]}', nm2, 'wall', lv, pos, x1, y0, y1, z0, z1, mat)
wall_boxes()
# bay walls (angled - approximated by 3 short boxes)
for i, (x0, x1, y0, y1) in enumerate([(0.8, 2.0, -2.0, 0.0), (1.6, 9.4, -3.75, -2.95), (8.5, 10.8, -2.4, -0.3)]):
    for lv in ('B',):
        box(f'BAYB{i}', 'Ex. bay foundation', 'wall', 'B', x0, x1, y0, y1, 0, L['J0B'], 'parge')
for (wid_, nm, lv, ori, c, a, b, s, h) in WIN:
    z = FFL[lv]
    if ori == 'x':
        box(wid_, nm, 'window' if not wid_.startswith('DR') else 'door', lv, a, b, c-0.08, c+0.08, z+s, z+h, 'glass', glaz='clear', ori='x')
    else:
        box(wid_, nm, 'window', lv, c-0.08, c+0.08, a, b, z+s, z+h, 'glass', glaz='clear', ori='y')
# bay walls on G (glass mostly)
box('WG-BAY-S', 'Bay wall S (brick)', 'wall', 'G', 0.85, 2.0, -2.0, 0.0, L['FFL0'], L['FFL0']+2.6, 'brick')
box('WG-BAY-C', 'Bay wall C (brick below sill)', 'wall', 'G', 1.6, 9.4, -3.75, -2.95, L['FFL0'], L['FFL0']+2.6, 'brick')
box('WG-BAY-N', 'Bay wall N (brick)', 'wall', 'G', 8.5, 10.8, -2.4, -0.3, L['FFL0'], L['FFL0']+2.6, 'brick')
box('WG-BAY-HD', 'Bay head', 'wall', 'G', 0.85, 10.8, -3.75, -2.95, L['FFL0']+8.0, L['J1B'], 'brick')
box('DR-G0', 'Front entry door', 'door', 'G', 13.01, 15.52, 0.1, 0.35, L['FFL0'], L['FFL0']+6.9, 'door')

# ---------------------------------------------------------------- floors / finishes
box('SLAB', 'Ex. basement slab', 'finish', 'B', 0.0, 16.67, -3.7, 56.5, -0.3, 0.0, 'concrete')
box('F-G1', 'Red oak 3/4x2-1/4 plain cut (ML-084), stained on site', 'finish', 'G', 0.85, 16.0, -3.5, 43.68, L['FFL0']-0.06, L['FFL0'], 'oak')
box('F-G2', 'Red oak - family room', 'finish', 'G', 5.03, 16.0, 44.52, 55.96, L['FFL0']-0.06, L['FFL0'], 'oak')
box('F-G3', 'Powder floor - Ciot Nuances chevron (ML-030)', 'finish', 'G', 0.69, 4.69, 50.49, 55.96, L['FFL0']-0.06, L['FFL0'], 'tile')
box('F-S1', 'Red oak - 2nd floor (family room raised area ML-085)', 'finish', 'S', 0.45, 16.0, 0.15, 55.97, L['FFL1']-0.06, L['FFL1'], 'oak')
box('F-T1', 'Red oak - 3rd floor', 'finish', 'T', 0.45, 16.0, 6.9, 55.97, L['FFL2']-0.06, L['FFL2'], 'oak')
box('F-T2', 'Ensuite floor - Ciot Boost Stone 24x24 + electric heat (ML-049/070)', 'finish', 'T', 0.5, 9.58, 22.01, 28.21, L['FFL2']-0.05, L['FFL2']+0.01, 'tile')
box('F-T3', 'Ensuite floor (vanity/WC)', 'finish', 'T', 4.75, 9.58, 28.21, 37.26, L['FFL2']-0.05, L['FFL2']+0.01, 'tile')
box('F-T4', 'Shower feature wall - Kyushu Verde 2x10 (ML-047)', 'finish', 'T', 5.08, 9.51, 37.1, 37.26, L['FFL2'], L['FFL2']+7.5, 'bluetile')
box('F-T5', 'Vanity wall tile - Boost Stone 24x24 (ML-049, 90 sf)', 'finish', 'T', 9.5, 9.58, 22.3, 30.9, L['FFL2'], L['FFL2']+8.6, 'tile')

# ---------------------------------------------------------------- joists & beams
J = 0
def joists(prefix, name, lvl, top, depth, ori, spacing_in, a0, a1, s0, s1, mat='lumber', w=0.125):
    """ori='x': joists span along x (side-to-side), repeated along y from s0..s1. a0..a1 = span extent"""
    global J
    s = s0 + 0.5
    k = 0
    while s < s1 - 0.2:
        k += 1
        if ori == 'x': box(f'{prefix}-{k}', name, 'joist', lvl, a0, a1, s, s + w, top - depth, top, mat)
        else: box(f'{prefix}-{k}', name, 'joist', lvl, s, s + w, a0, a1, top - depth, top, mat)
        s += spacing_in / 12
# main floor framing (seen from basement)
joists('J0A', 'Ex. 2x12 @16" (main floor)', 'B', L['J0T'], 11.25/12, 'x', 16, 0.85, 16.25, 0.62, 28.3)
joists('J0B', 'Ex. 2x12 @16" (main floor, kitchen wing)', 'B', L['J0T'], 11.25/12, 'x', 16, 5.05, 16.25, 28.3, 43.5)
joists('J0C', 'Ex. 2x12 @16" (family room, to remain)', 'B', L['J0T'], 11.25/12, 'x', 16, 5.1, 16.25, 44.34, 55.6)
joists('J0D', 'New 2x12 @16" (addition strip)', 'B', L['J0T'], 11.25/12, 'x', 16, 0.96, 4.25, 44.5, 55.72)
# 2nd floor framing
joists('J1A', 'Ex. 2x12 @16" (2nd floor)', 'G', L['J1T'], 11.25/12, 'x', 16, 0.85, 16.0, 0.62, 43.5)
joists('J1B', 'New 11-7/8" TJI 230 @16" (2nd floor over family rm)', 'G', L['J1T'], 11.875/12, 'x', 16, 0.45, 16.0, 43.97, 55.9, 'lvl')
box('BM-G1', '2-1 3/4x11 7/8 2.0E Microlam LVL (FL)', 'beam', 'G', 5.05, 16.0, 43.68, 43.97, L['J1T']-11.875/12, L['J1T'], 'lvl')
box('BM-G2', 'LVL 3 (DRP) over 10\' slider', 'beam', 'G', 5.0, 16.0, 55.6, 55.9, L['J1B']-0.5, L['J1T'], 'lvl')
box('BM-G3', 'WB2 (DRP) rear storage', 'beam', 'G', 0.2, 5.0, 55.6, 55.9, L['J1B']-0.5, L['J1T'], 'lvl')
# 3rd floor framing (2nd floor ceiling) - permit A8 labels
J2T = L['J2T']
joists('J2A', 'New 9-1/2" TJI 360 @12" (3rd floor, front)', 'S', J2T, 9.5/12, 'x', 12, 0.85, 16.0, 0.15, 12.95, 'lvl')
box('BM-S1', 'New LVL5 (FL) - closet line', 'beam', 'S', 0.85, 16.0, 12.95, 13.25, J2T-9.5/12, J2T, 'lvl')
joists('J2B', 'Ex. 2x12 @16" hung off new header (family rm)', 'S', J2T, 11.25/12, 'x', 16, 0.85, 12.9, 13.25, 26.4)
box('BM-S2', 'New LVL5 (FL) - stair side', 'beam', 'S', 12.9, 13.2, 13.25, 26.6, J2T-11.25/12, J2T, 'lvl')
box('BM-S3', 'New LVL5 (FL) - stair head', 'beam', 'S', 11.0, 16.0, 26.4, 26.7, J2T-11.875/12, J2T, 'lvl')
joists('J2C', 'New 11-7/8" TJI 210 @16" (3rd floor mid)', 'S', J2T, 11.875/12, 'x', 16, 0.45, 13.2, 26.7, 33.0, 'lvl')
joists('J2D', 'New 9-1/2" TJI 230 @16" (3rd floor)', 'S', J2T, 9.5/12, 'x', 16, 0.45, 16.0, 33.0, 46.3, 'lvl')
box('BM-S4', 'New LVL4 (FL)', 'beam', 'S', 0.45, 16.0, 46.3, 46.6, J2T-9.5/12, J2T, 'lvl')
joists('J2E', 'CANT. 9-1/2" TJI 230 @16" (bedroom 2 ceiling / balcony)', 'S', J2T, 9.5/12, 'y', 16, 46.6, 60.4, 1.75, 14.5, 'lvl')
box('BM-S5', 'LVL 1 (CANT) - south', 'beam', 'S', 1.2, 1.5, 46.6, 60.4, J2T-9.5/12, J2T, 'lvl')
box('BM-S6', 'LVL 1 (CANT) - north', 'beam', 'S', 14.6, 14.9, 46.6, 60.4, J2T-9.5/12, J2T, 'lvl')
box('BM-S7', 'WB1 (DRP) - south wall over kitchen wing', 'beam', 'S', 0.5, 1.0, 26.6, 33.5, J2T-9.5/12-0.6, J2T-9.5/12, 'lvl')
# roof
box('RF-1', 'Flat roof: membrane / 9-1/2" eng. roof joists @16" / R31 spray foam', 'roof', 'R', -0.2, 16.87, 6.3, 56.6, L['TOP'], L['ROOF']+0.15, 'membrane')
box('RF-2', 'Ex. front roof (to remain)', 'roof', 'R', -0.3, 16.9, -0.8, 6.5, L['FFL2'], L['FFL2']+4.2, 'shingle')
box('RF-3', 'Bay roof', 'roof', 'R', 0.6, 11.0, -4.0, -0.2, L['FFL1']-0.6, L['FFL1']-0.2, 'shingle')
box('BAL-1', '3rd floor balcony deck (cantilever)', 'site', 'R', 1.3, 14.9, 56.5, 60.5, L['FFL2']-0.9, L['FFL2']-0.1, 'deck')
box('SITE-G', 'Grade', 'site', 'X', -14, 31, -16, 70, L['GRADE']-0.5, L['GRADE'], 'grass')
box('SITE-W', 'Front walk / porch', 'site', 'X', 11.0, 16.6, -5.0, -0.3, L['GRADE'], L['FFL0']-0.1, 'concrete')

# ---------------------------------------------------------------- stairs (direction per plans A6-A9)
def stair(id, name, lvl, x0, x1, y0, y1, zb, zt, n, rising='+y'):
    run = (y1 - y0) / n; rise = (zt - zb) / n
    for i in range(n):
        if rising == '+y': ya, yb = y0 + i*run, y0 + (i+1)*run
        else: ya, yb = y1 - (i+1)*run, y1 - i*run
        box(f'{id}-{i}', name, 'stair', lvl, x0, x1, ya, yb, zb + i*rise, zb + (i+1)*rise, 'oakstair')
stair('ST-B', 'Ex. basement stair 11R (up to rear)', 'B', 13.65, 16.25, 19.3, 28.3, 0, L['FFL0'], 11, '+y')
stair('ST-G', 'Ex. main stair 17R (up to rear)', 'G', 13.25, 16.0, 16.4, 28.3, L['FFL0'], L['FFL1'], 17, '+y')
stair('ST-S', 'New stair over ex. stair 16R (up to rear, per A8/A9 plans)', 'S', 13.3, 16.0, 15.0, 28.3, L['FFL1'], L['FFL2'], 16, '+y')
stair('ST-X', 'Ex. side basement walkout 10R', 'B', 0.4, 3.4, 29.6, 35.4, 0, L['GRADE'], 10, '+y')

# ---------------------------------------------------------------- cabinets / fixtures (permit A7 layout + Oct 12 material list)
G0 = L['FFL0']
box('CB-K-FR', 'Fridge tall cabinet - Miele 36" panel-ready KFNF 9959 iDE (ML-103)', 'cabinet', 'G', 5.0, 7.0, 28.3, 31.3, G0, G0+86.25/12, 'walnut')
box('CB-K-B1', 'Base 34-1/2" + walnut slab', 'cabinet', 'G', 5.0, 6.99, 31.3, 32.69, G0, G0+34.5/12, 'walnut')
box('CB-K-SK', 'Sink base - Blanco Stellar U2 (ML-018)', 'cabinet', 'G', 5.0, 6.99, 32.69, 36.37, G0, G0+34.5/12, 'walnut')
box('CB-K-DW', 'Dishwasher - Miele 24" panel-ready G7186SCVI (ML-105)', 'cabinet', 'G', 5.0, 6.99, 36.37, 37.44, G0, G0+34.5/12, 'walnut')
box('CB-K-RG', 'Range bay - permit shows 30"; Miele HR 1432-3 I is 36" (ML-104)', 'fixture', 'G', 5.0, 7.08, 37.44, 40.07, G0, G0+36/12, 'steel')
box('CB-K-PN', 'Pantry tall (walnut slab, ML-011)', 'cabinet', 'G', 5.0, 6.99, 40.07, 43.68, G0+4/12, G0+86.25/12, 'walnut')
box('CB-K-CT', 'Quartz - Lucent Tranquility White (ML-015)', 'counter', 'G', 5.0, 7.08, 31.3, 40.07, G0+34.5/12, G0+36/12, 'quartz')
box('CB-K-U1', 'Upper 12" (fluted white gloss)', 'cabinet', 'G', 5.0, 6.0, 31.3, 32.6, G0+54/12, G0+86.25/12, 'whitegloss')
box('CB-K-HD', 'Hood surround fluted (ML-009) + Elica Trento ETR134S1 insert (ML-106)', 'cabinet', 'G', 5.0, 6.1, 37.44, 40.07, G0+66/12, G0+86.25/12, 'whitegloss')
box('CB-K-IS', 'Island 3\'-0" x 7\'-6" (permit) - walnut + breakfast bar', 'cabinet', 'G', 10.31, 13.32, 32.21, 39.72, G0, G0+34.5/12, 'walnut')
box('CB-K-IT', 'Island quartz top', 'counter', 'G', 10.25, 13.38, 32.15, 39.78, G0+34.5/12, G0+36/12, 'quartz')
box('CB-P-VN', 'Powder vanity - Teodor Malibu Slim 30" walnut (ML-029)', 'cabinet', 'G', 0.69, 2.4, 50.49, 52.99, G0, G0+2.75, 'walnut')
box('FX-P-WC', 'Powder WC - Kohler Spacity (ML-034)', 'fixture', 'G', 3.09, 4.53, 54.0, 55.9, G0, G0+2.4, 'porcelain')
box('FX-L-W', 'Washer', 'fixture', 'S', 4.45, 6.6, 37.5, 39.9, L['FFL1'], L['FFL1']+3.2, 'appliance')
box('FX-L-D', 'Dryer', 'fixture', 'S', 6.6, 8.75, 37.5, 39.9, L['FFL1'], L['FFL1']+3.2, 'appliance')
T0 = L['FFL2']
box('CB-E-VN', 'Ensuite vanity - Teodor Asher 72" double, walnut (ML-046)', 'cabinet', 'T', 7.75, 9.58, 23.2, 29.2, T0, T0+2.85, 'walnut')
box('FX-E-M1', 'Mirror - GEF Curl 24" arch (ML-075)', 'fixture', 'T', 9.45, 9.55, 23.9, 25.9, T0+3.6, T0+6.6, 'steel')
box('FX-E-M2', 'Mirror - GEF Curl 24" arch (ML-075)', 'fixture', 'T', 9.45, 9.55, 26.5, 28.5, T0+3.6, T0+6.6, 'steel')
box('FX-E-SC', 'Sconces - West Elm Hayes x2 (ML-067)', 'fixture', 'T', 9.4, 9.55, 25.95, 26.45, T0+5.3, T0+6.3, 'steel')
box('FX-E-TB', 'Freestanding tub - MAAX Mirella 67x29 (ML-065)', 'fixture', 'T', 1.27, 3.69, 22.6, 28.18, T0, T0+1.9, 'porcelain')
box('FX-E-SH', 'Glass shower 53x40 + Kerdi-Line 48" (ML-063/081)', 'fixture', 'T', 5.08, 9.51, 33.94, 37.26, T0, T0+6.5, 'showerglass')
box('FX-E-WC', 'WC - TOTO Legato (ML-064)', 'fixture', 'T', 7.6, 9.4, 30.4, 32.6, T0, T0+2.4, 'porcelain')
box('FX-B-WC', 'Ex. basement bath', 'fixture', 'B', 5.2, 7.6, 39.5, 43.3, 0, 2.5, 'porcelain')

# ---------------------------------------------------------------- equipment
box('EQ-F1', 'F-1 Lennox ML196UH070XE36B, 63,900 Btu/h out, 928 cfm + coil (ML14KP1 1.5 ton HP)', 'equip', 'B', 1.96, 4.32, 6.59, 8.30, 0, 5.3, 'equip')
box('EQ-HWT', 'Ex. hot water tank (permit A6)', 'equip', 'B', 4.75, 6.5, 6.8, 8.55, 0, 5.4, 'equipw')
box('EQ-HRV1', 'HRV-1 (VanEE, model not stated)', 'equip', 'B', 3.91, 5.68, 12.55, 13.9, 6.4, 7.9, 'equipw')
box('EQ-EXF', 'Ex. H.E. furnace (permit A6 - to be replaced?)', 'equip', 'B', 1.23, 4.23, 7.63, 10.24, 0, 0.05, 'equipw')
S0 = L['FFL1']
box('EQ-F2', 'F-2 Lennox ML196UH030XE36B, 29,000 Btu/h out, 735 cfm + coil (ML14KP1 2.0 ton HP)', 'equip', 'S', 9.32, 11.67, 41.84, 43.6, S0, S0+5.3, 'equip')
box('EQ-HRV2', 'HRV-2 (VanEE, model not stated)', 'equip', 'S', 10.85, 12.43, 40.6, 41.62, S0+6.4, S0+7.9, 'equipw')

json.dump(dict(E=E, L=L), open('model_base.json', 'w'))
print(len(E), 'elements', L)
