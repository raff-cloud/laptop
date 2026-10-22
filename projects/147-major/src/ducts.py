import json, math
B = json.load(open('model_base.json')); E = B['E']; L = B['L']
J0B, J0T, J2T = L['J0B'], L['J0T'], L['J2T']
G0, S0, T0 = L['FFL0'], L['FFL1'], L['FFL2']
D = []
def seg(id, name, lvl, sys, size, x0, x1, y0, y1, z0, z1, axis=None, src=False, **kw):
    d = dict(id=id, name=name, cat='duct', shape='box', lvl=lvl, x0=round(min(x0,x1),3), x1=round(max(x0,x1),3), y0=round(min(y0,y1),3), y1=round(max(y0,y1),3), z0=round(z0,3), z1=round(z1,3), axis=axis, sys=sys, size=size, mat=sys, source=src, connected=True)
    d.update(kw); D.append(d); return d
def run(id, name, lvl, sys, w_in, h_in, a, b, z_top, along, c):
    """rect run. along='y': c = x centreline, a..b = y extent. along='x': c = y centreline"""
    w = w_in/12; h = h_in/12
    if along == 'y': return seg(id, name, lvl, sys, f'{w_in}x{h_in}', c-w/2, c+w/2, a, b, z_top-h, z_top, axis='y')
    return seg(id, name, lvl, sys, f'{w_in}x{h_in}', a, b, c-w/2, c+w/2, z_top-h, z_top, axis='x')
def rnd(id, name, lvl, sys, dia, a, b, z_c, along, c, **kw):
    r = dia/24
    if along == 'y': return seg(id, name, lvl, sys, f'{dia}"Ø', c-r, c+r, a, b, z_c-r, z_c+r, axis='y', **kw)
    if along == 'x': return seg(id, name, lvl, sys, f'{dia}"Ø', a, b, c-r, c+r, z_c-r, z_c+r, axis='x', **kw)
def vert(id, name, lvl, sys, w_in, d_in, x, y, z0, z1, **kw):
    return seg(id, name, lvl, sys, f'{w_in}x{d_in}' if d_in else f'{w_in}"Ø', x-w_in/24, x+w_in/24, y-(d_in or w_in)/24, y+(d_in or w_in)/24, z0, z1, axis='z', **kw)
def term(id, name, lvl, sys, x0, x1, y0, y1, z0, z1, **kw):
    return seg(id, name, lvl, sys, 'grille', x0, x1, y0, y1, z0, z1, axis='t', **kw)

BAY = J0T - 0.33        # 6" round centred in a 2x12 bay (main floor)
BELOW = J0B - 0.26      # 6" round hung under the joists
# ---------------- F-1 (basement) supply
seg('D-PL1', 'F-1 supply plenum + coil', 'B', 'supply', 'plenum', 1.96, 4.32, 6.59, 8.30, 5.3, J0B, src=True, axis='z')
run('D-F0', 'Plenum takeoff to trunk F (12x6)', 'B', 'supply', 12, 6, 4.32, 8.24, J0B, 'x', 7.47)
run('D-D', 'Supply trunk D 14x6 (front)', 'B', 'supply', 14, 6, -1.79, 6.59, J0B, 'y', 2.84)
run('D-F', 'Supply trunk F 24x6', 'B', 'supply', 24, 6, 7.97, 31.0, J0B, 'y', 7.24)
run('D-FE1', 'Trunk F→E 45° transition (modelled as L)', 'B', 'supply', 14, 6, 6.24, 11.9, J0B, 'x', 31.5)
run('D-FE2', 'Trunk F→E 45° transition (modelled as L)', 'B', 'supply', 14, 6, 31.0, 35.68, J0B, 'y', 11.32)
run('D-E', 'Supply trunk E 14x6 (rear)', 'B', 'supply', 14, 6, 35.68, 43.46, J0B, 'y', 11.32)
# branches (x = in joist bay; y = hung below joists)
OUT = []   # (outlet id, name, sys, path)
def outlet(oid, name, sys, path, lvl): OUT.append(dict(id=oid, name=name, sys=sys, path=path, lvl=lvl))
# front trunk D
rnd('S-13a', 'Supply 13 branch 6"', 'B', 'supply', 6, 2.84, 5.83, BAY, 'x', -1.53)
rnd('S-13b', 'Supply 13 branch 6"', 'B', 'supply', 6, -2.5, -1.53, BAY, 'y', 5.8)
term('T-13', 'S/A 13 floor boot - bay (existing)', 'G', 'supply', 5.26, 6.34, -2.67, -2.34, BAY, G0+0.02)
outlet('T-13', 'S/A 13 bay window (ex.)', 'supply', ['D-PL1', 'D-D', 'S-13a', 'S-13b'], 'G')
term('T-16', 'S/A 16 floor boot - living rm front (new)', 'G', 'supply', 1.96, 2.30, -0.21, 0.87, BAY, G0+0.02)
outlet('T-16', 'S/A 16 living rm front (new)', 'supply', ['D-PL1', 'D-D'], 'G')
term('T-18', 'S/A 18 basement ceiling (new)', 'B', 'supply', 1.82, 2.15, 3.84, 4.92, J0B-0.1, J0B)
outlet('T-18', 'S/A 18 basement storage', 'supply', ['D-PL1', 'D-D'], 'B')
rnd('S-19', 'Supply 19 branch 6"', 'B', 'supply', 6, 3.42, 7.8, BAY, 'x', 0.82)
term('T-19', 'S/A 19 basement ceiling', 'B', 'supply', 7.85, 8.18, 0.23, 1.31, J0B-0.1, J0B)
outlet('T-19', 'S/A 19 basement storage', 'supply', ['D-PL1', 'D-D', 'S-19'], 'B')
rnd('S-15', 'Supply 15 branch 6"', 'B', 'supply', 6, 3.42, 11.78, BAY, 'x', 3.13)
term('T-15', 'S/A 15 foyer floor boot (existing)', 'G', 'supply', 11.79, 12.12, 2.79, 3.87, BAY, G0+0.02)
outlet('T-15', 'S/A 15 foyer (ex.)', 'supply', ['D-PL1', 'D-D', 'S-15'], 'G')
rnd('S-20', 'Supply 20 branch 6"', 'B', 'supply', 6, 3.42, 15.11, BAY, 'x', 5.32)
term('T-20', 'S/A 20 basement ceiling (cold room side)', 'B', 'supply', 15.08, 15.42, 4.72, 5.80, J0B-0.1, J0B)
outlet('T-20', 'S/A 20 basement', 'supply', ['D-PL1', 'D-D', 'S-20'], 'B')
# trunk F
rnd('S-17', 'Supply 17 branch 6"', 'B', 'supply', 6, 8.24, 15.11, BAY, 'x', 17.36)
term('T-17', 'S/A 17 basement ceiling (new)', 'B', 'supply', 15.08, 15.42, 16.76, 17.84, J0B-0.1, J0B)
outlet('T-17', 'S/A 17 basement', 'supply', ['D-PL1', 'D-F0', 'D-F', 'S-17'], 'B')
rnd('S-21', 'Supply 21 branch 6"', 'B', 'supply', 6, 2.08, 6.24, BAY, 'x', 22.54)
term('T-21', 'S/A 21 basement ceiling', 'B', 'supply', 1.74, 2.08, 22.0, 23.08, J0B-0.1, J0B)
outlet('T-21', 'S/A 21 basement', 'supply', ['D-PL1', 'D-F0', 'D-F', 'S-21'], 'B')
rnd('S-14', 'Supply 14 branch 6"', 'B', 'supply', 6, 1.96, 6.24, BAY, 'x', 27.35)
term('T-14', 'S/A 14 dining floor boot (existing)', 'G', 'supply', 1.92, 3.01, 27.22, 27.55, BAY, G0+0.02)
outlet('T-14', 'S/A 14 dining (ex.)', 'supply', ['D-PL1', 'D-F0', 'D-F', 'S-14'], 'G')
rnd('S-22', 'Supply 22 branch 6"', 'B', 'supply', 6, 8.24, 10.05, BAY, 'x', 32.4)
term('T-22', 'S/A 22 basement ceiling', 'B', 'supply', 10.02, 10.35, 31.6, 32.7, J0B-0.1, J0B)
outlet('T-22', 'S/A 22 basement', 'supply', ['D-PL1', 'D-F0', 'D-F', 'D-FE1', 'S-22'], 'B')
# trunk E
rnd('S-24', 'Supply 24 branch 6"', 'B', 'supply', 6, 10.38, 10.74, BAY, 'x', 38.45)
vert('S-24v', 'S/A 24 low-wall stack in bath E wall (6" round in 2x4 wall)', 'B', 'supply', 6, 0, 10.22, 38.45, 1.2, BAY, inwall='Bath partition E')
term('T-24', 'S/A 24 low-wall grille - basement bath', 'B', 'supply', 10.0, 10.1, 37.9, 39.0, 0.8, 1.3)
outlet('T-24', 'S/A 24 basement bath (LW)', 'supply', ['D-PL1', 'D-F0', 'D-F', 'D-FE1', 'D-FE2', 'D-E', 'S-24', 'S-24v'], 'B')
rnd('S-12', 'Supply 12 branch 6"', 'B', 'supply', 6, 6.78, 10.74, BAY, 'x', 40.69)
term('T-12', 'S/A 12 toe-kick register (pantry)', 'G', 'supply', 6.61, 6.94, 40.34, 41.40, BAY, G0+0.3)
outlet('T-12', 'S/A 12 kitchen in-kick (ex.)', 'supply', ['D-PL1', 'D-F0', 'D-F', 'D-FE1', 'D-FE2', 'D-E', 'S-12'], 'G')
for (oid, yb, xb, ye, label, tgt, extra) in [
    ('23', 41.01, 15.57, 48.5, 'basement ceiling (rear)', None, None),
    ('10', 41.64, 14.88, 55.08, 'family rm floor boot - slider (ex. relocated)', (14.40, 15.52, 55.19, 55.52), None),
    ('8', 42.20, 14.32, 54.78, 'family rm floor boot - slider (new)', (10.09, 11.20, 55.19, 55.52), 10.64),
    ('11', 42.80, 13.61, 54.16, 'family rm floor boot - slider (new)', (5.86, 6.99, 55.19, 55.52), 6.39),
    ('9', 43.24, 13.04, 51.75, 'powder rm low-wall (ex. relocated)', None, 4.51)]:
    rnd(f'S-{oid}a', f'Supply {oid} branch 6"', 'B', 'supply', 6, 11.9, xb, BAY, 'x', yb)
    rnd(f'S-{oid}b', f'Supply {oid} branch 6" (crosses joists - hung below)', 'B', 'supply', 6, yb, ye, BELOW, 'y', xb)
    path = ['D-PL1', 'D-F0', 'D-F', 'D-FE1', 'D-FE2', 'D-E', f'S-{oid}a', f'S-{oid}b']
    if extra is not None:
        rnd(f'S-{oid}c', f'Supply {oid} branch 6"', 'B', 'supply', 6, min(extra, xb), max(extra, xb), BAY, 'x', ye); path.append(f'S-{oid}c')
    if oid == '23':
        term('T-23', 'S/A 23 basement ceiling', 'B', 'supply', 15.42, 15.75, 47.98, 49.06, J0B-0.1, J0B)
    elif oid == '9':
        vert('S-9v', 'S/A 9 riser into powder E wall (6" round)', 'B', 'supply', 6, 0, 4.3, 51.9, BAY, G0+1.2, inwall='Powder/family wall')
        term('T-9', 'S/A 9 low-wall grille - powder', 'G', 'supply', 4.13, 4.46, 51.35, 52.43, G0+0.6, G0+1.1); path.append('S-9v')
    else:
        x0, x1, y0, y1 = tgt
        rnd(f'S-{oid}d', f'Supply {oid} boot leg', 'B', 'supply', 6, ye-0.25, 55.35, BELOW, 'y', (x0+x1)/2); path.append(f'S-{oid}d')
        term(f'T-{oid}', f'S/A {oid} {label}', 'G', 'supply', x0, x1, y0, y1, BAY, G0+0.02)
    outlet(f'T-{oid}', f'S/A {oid} {label}', 'supply', path, 'G' if oid not in ('23',) else 'B')
# ---------------- F-1 returns
seg('R-XD', 'F-1 return drop 20x12', 'B', 'return', '20x12', 2.0, 3.67, 8.30, 13.12, 4.0, J0B, axis='z', src=True)
run('R-X', 'Return trunk X 28x8', 'B', 'return', 28, 8, 3.43, 15.75, J0B, 'x', 9.81)
term('T-7R', 'R/A 7R floor return 30x8 - living rm (new)', 'G', 'return', 15.0, 15.65, 8.55, 11.05, J0B, G0+0.02)
outlet('T-7R', 'R/A 7R living rm FRA 30x8', 'return', ['R-XD', 'R-X'], 'G')
rnd('R-9Ra', 'Return 9R 7" (foyer LW)', 'B', 'return', 7, 3.56, 11.0, BAY, 'x', 4.09)
rnd('R-9Rb', 'Return 9R 7" (drops to F-1 - crosses joists)', 'B', 'return', 7, 4.09, 8.30, J0B-0.3, 'y', 3.56)
vert('R-9Rv', 'R/A 9R stack in foyer W wall (7" round in 2x4 wall)', 'G', 'return', 7, 0, 11.15, 4.26, BAY, G0+1.2, inwall='Foyer wall W')
term('T-9R', 'R/A 9R low-wall 14x8 - foyer (new)', 'G', 'return', 10.96, 11.0, 3.64, 4.89, G0+0.5, G0+1.2)
outlet('T-9R', 'R/A 9R foyer LW 14x8', 'return', ['R-XD', 'R-9Rb', 'R-9Ra', 'R-9Rv'], 'G')
run('R-M0', 'Return main (dashed, size not labelled) - assumed 14x8', 'B', 'return', 14, 8, 3.67, 6.54, J0B, 'x', 11.81)
run('R-M', 'Return main (dashed, size not labelled) - assumed 14x8', 'B', 'return', 14, 8, 11.81, 32.73, J0B-0.55, 'y', 6.54)
rnd('R-M2', 'Return main 45° to rear (modelled as L, 8")', 'B', 'return', 8, 6.54, 10.55, J0B-1.05, 'x', 32.4)
rnd('R-M3', 'Return to 8R along E trunk (8")', 'B', 'return', 8, 32.4, 43.1, J0B-1.05, 'y', 10.55)
rnd('R-M4', 'Return to 8R along old rear fdn wall (8")', 'B', 'return', 8, 5.9, 10.55, J0B-1.05, 'x', 43.1)
rnd('R-M5', 'Return to 8R through old rear fdn wall (8")', 'B', 'return', 8, 43.1, 44.1, J0B-1.05, 'y', 5.92)
vert('R-8Rv', 'R/A 8R stack up to pantry/storage wall (6" round)', 'B', 'return', 6, 0, 5.92, 44.1, J0B-1.4, G0+1.2, inwall='Pantry/storage wall')
term('T-8R', 'R/A 8R low-wall 14x8 - family rm (new)', 'G', 'return', 5.29, 6.54, 44.52, 44.56, G0+0.5, G0+1.2)
outlet('T-8R', 'R/A 8R family rm LW 14x8', 'return', ['R-XD', 'R-M0', 'R-M', 'R-M2', 'R-M3', 'R-M4', 'R-M5', 'R-8Rv'], 'G')

# ---------------- F-2 (2nd floor mech room) - trunks in the 3rd floor joist space as drawn
TOP2 = J2T - 0.05
seg('D2-PL', 'F-2 supply plenum + coil', 'S', 'supply', 'plenum', 9.32, 11.67, 41.84, 43.6, L['FFL1R']+5.3, TOP2, src=True, axis='z')
run('D2-C0', 'Supply trunk C 18x8 (from F-2)', 'S', 'supply', 18, 8, 4.88, 9.32, TOP2, 'x', 42.74)
run('D2-C', 'Supply trunk C 18x8', 'S', 'supply', 18, 8, 27.88, 44.72, TOP2, 'y', 5.63)
run('D2-A0', 'Supply trunk A 10x8 (off C)', 'S', 'supply', 10, 8, 1.55, 4.88, TOP2, 'x', 27.13)
run('D2-A', 'Supply trunk A 10x8 (front, along S wall)', 'S', 'supply', 10, 8, 0.91, 27.55, TOP2, 'y', 1.96)
run('D2-B0', 'Supply trunk B 12x8 (off C)', 'S', 'supply', 12, 8, 0.94, 6.38, TOP2, 'x', 45.22)
run('D2-B', 'Supply trunk B 12x8 (rear, along S wall)', 'S', 'supply', 12, 8, 44.72, 55.73, TOP2, 'y', 1.44)
SB = J2T - 0.33
def up(oid, x0, x1, y0, y1, label, path, lvl='T'):
    term(f'T-{oid}', label, lvl, 'supply', x0, x1, y0, y1, SB, T0+0.02)
    outlet(f'T-{oid}', label, 'supply', path, lvl)
def ceil(oid, x0, x1, y0, y1, label, path):
    term(f'T-{oid}', label, 'S', 'supply', x0, x1, y0, y1, L['CEIL1']-0.06, SB)
    outlet(f'T-{oid}', label, 'supply', path, 'S')
A = ['D2-PL', 'D2-C0', 'D2-C', 'D2-A0', 'D2-A']; Bp = ['D2-PL', 'D2-C0', 'D2-C', 'D2-B0', 'D2-B']; C = ['D2-PL', 'D2-C0', 'D2-C']
rnd('S-35', 'Supply 35 branch 6"', 'S', 'supply', 6, 2.38, 5.31, SB, 'x', 1.02)
ceil('35', 5.29, 6.37, 0.85, 1.18, 'S/A 35 primary bedroom ceiling (front)', A + ['S-35'])
rnd('S-36', 'Supply 36 branch 6"', 'S', 'supply', 6, 2.38, 13.36, SB, 'x', 1.42)
ceil('36', 13.32, 14.40, 1.26, 1.59, 'S/A 36 primary bedroom ceiling (front)', A + ['S-36'])
up('32', 0.87, 1.20, 13.90, 14.98, 'S/A 32 bedroom 3 floor (3rd)', A)
up('31', 0.87, 1.20, 18.78, 19.87, 'S/A 31 bedroom 3 floor (3rd)', A)
ceil('38', 2.87, 3.95, 27.22, 27.55, 'S/A 38 hall ceiling (2nd)', A[:4])
ceil('37', 5.61, 6.70, 32.63, 32.97, 'S/A 37 bath ceiling (2nd)', C)
up('30', 5.03, 5.37, 30.92, 32.0, 'S/A 30 ensuite floor (3rd) - heated tile', C)
rnd('S-29', 'Supply 29 branch 6"', 'S', 'supply', 6, 6.38, 11.97, SB, 'x', 39.31)
up('29', 12.0, 12.33, 38.8, 39.88, 'S/A 29 3rd floor hall / WIC', C + ['S-29'])
rnd('S-33', 'Supply 33/34 branch 6"', 'S', 'supply', 6, 1.94, 12.49, SB, 'x', 53.26)
ceil('33', 11.88, 12.96, 53.5, 53.84, 'S/A 33 bedroom 2 ceiling', Bp + ['S-33'])
ceil('34', 3.74, 4.83, 53.56, 53.89, 'S/A 34 bedroom 2 ceiling', Bp + ['S-33'])
rnd('S-28', 'Supply 28 branch 6"', 'S', 'supply', 6, 1.94, 13.24, SB-0.02, 'x', 54.23)
rnd('S-28b', 'Supply 28 boot leg', 'S', 'supply', 6, 54.23, 55.5, SB, 'y', 13.23)
up('28', 12.69, 13.77, 55.40, 55.73, 'S/A 28 primary bedroom floor at 12\' slider', Bp + ['S-28', 'S-28b'])
rnd('S-27', 'Supply 27 branch 6"', 'S', 'supply', 6, 1.94, 9.83, SB-0.02, 'x', 54.75)
up('27', 9.41, 10.49, 55.34, 55.67, 'S/A 27 primary bedroom floor at 12\' slider', Bp + ['S-27'])
rnd('S-26', 'Supply 26 branch 6"', 'S', 'supply', 6, 1.94, 5.57, SB-0.02, 'x', 55.25)
up('26', 5.04, 6.12, 55.34, 55.67, 'S/A 26 primary bedroom floor at 12\' slider', Bp + ['S-26'])
up('25', 1.24, 2.32, 55.34, 55.67, 'S/A 25 primary bedroom floor at 12\' slider', Bp)
# F-2 returns
seg('R2-XD', 'F-2 return drop 22x8 / 24x10', 'S', 'return', '24x10', 9.32, 11.67, 40.9, 41.84, L['FFL1R']+0.5, TOP2, axis='z', src=True)
run('R2-Y', 'Return trunk Y 16x8', 'S', 'return', 16, 8, 29.0, 40.9, TOP2, 'y', 10.19)
run('R2-Z', 'Return trunk Z 10x8', 'S', 'return', 10, 8, 13.96, 26.2, TOP2, 'y', 8.86)
run('R2-Z2', 'Return Z→Y transition (45°, modelled as L)', 'S', 'return', 10, 8, 26.2, 29.43, TOP2, 'y', 8.86)
run('R2-Z3', 'Return Z→Y transition', 'S', 'return', 10, 8, 8.45, 11.0, TOP2, 'x', 29.02)
RZ = ['R2-XD', 'R2-Y', 'R2-Z3', 'R2-Z2', 'R2-Z']
term('T-4R', 'R/A 4R high-wall 14x8 - primary bedroom closet wall', 'S', 'return', 8.23, 9.48, 13.05, 13.15, S0+6.6, S0+7.3)
vert('R-4Rv', 'R/A 4R stack 7" (in closet wall, through LVL5 line)', 'S', 'return', 7, 0, 8.86, 13.1, S0+7.0, TOP2, inwall='Primary closet wall')
outlet('T-4R', 'R/A 4R primary bedroom HW', 'return', RZ + ['R-4Rv'], 'S')
term('T-5R', 'R/A 5R high-wall 14x8 - family rm / hall', 'S', 'return', 9.47, 9.6, 25.6, 26.9, S0+6.6, S0+7.3)
vert('R-5Rv', 'R/A 5R stack 7" (family rm rear wall)', 'S', 'return', 7, 0, 9.3, 26.55, S0+7.0, TOP2, inwall='Family rm rear wall')
outlet('T-5R', 'R/A 5R family rm HW', 'return', RZ[:4] + ['R-5Rv'], 'S')
term('T-6R', 'R/A 6R high-wall 14x8 - bedroom 2', 'S', 'return', 7.7, 10.31, 44.27, 44.32, L['FFL1R']+6.6, L['FFL1R']+7.3)
run('R-6Ra', 'R/A 6R run 14x8', 'S', 'return', 14, 8, 41.84, 44.5, TOP2, 'y', 9.0)
vert('R-6Rv', 'R/A 6R stack 7" (bedroom 2 front wall)', 'S', 'return', 7, 0, 9.0, 44.1, L['FFL1R']+7.0, TOP2, inwall='Bedroom 2 front wall')
outlet('T-6R', 'R/A 6R bedroom 2 HW', 'return', ['R2-XD', 'R-6Ra', 'R-6Rv'], 'S')
vert('R-1Rv', 'R/A 1R stack 7" down from 3rd floor (bedroom 3 / ensuite wall)', 'T', 'return', 7, 0, 8.55, 21.84, TOP2-0.3, T0+7.3, inwall='Bedroom 3 / ensuite E')
term('T-1R', 'R/A 1R high-wall 14x8 - bedroom 3', 'T', 'return', 7.91, 9.16, 21.62, 21.67, T0+6.6, T0+7.3)
outlet('T-1R', 'R/A 1R bedroom 3 HW (3rd)', 'return', RZ + ['R-1Rv'], 'T')
vert('R-3Rv', 'R/A 3R stack 7" down in vanity wall', 'T', 'return', 7, 0, 9.75, 26.25, TOP2-0.3, T0+7.3, inwall='Vanity wall (ensuite / hall)')
rnd('R-3Rh', 'R/A 3R tie into Z (7")', 'S', 'return', 7, 9.28, 9.75, TOP2-0.3, 'x', 26.25)
term('T-3R', 'R/A 3R high-wall 14x8 - ensuite vanity wall', 'T', 'return', 9.5, 9.58, 25.61, 26.86, T0+6.6, T0+7.3)
outlet('T-3R', 'R/A 3R ensuite HW (3rd)', 'return', RZ[:4] + ['R-3Rh', 'R-3Rv'], 'T')
vert('R-2Rv', 'R/A 2R stack 7" (3rd floor hall)', 'T', 'return', 7, 0, 12.8, 34.65, TOP2-0.3, T0+7.3)
rnd('R-2Rh', 'R/A 2R tie into Y (7")', 'S', 'return', 7, 10.19, 12.8, TOP2-0.3, 'x', 34.65)
term('T-2R', 'R/A 2R high-wall 14x8 - 3rd floor hall', 'T', 'return', 12.62, 12.66, 34.03, 35.28, T0+6.6, T0+7.3)
outlet('T-2R', 'R/A 2R 3rd floor hall HW', 'return', ['R2-XD', 'R2-Y', 'R-2Rh', 'R-2Rv'], 'T')
# ---------------- exhaust (fans drawn, routes NOT drawn)
for (fid, nm, lvl, x, y, z) in [('X-B1', 'Bath fan 5"Ø - basement bath', 'B', 8.8, 40.6, J0B-0.3), ('X-G1', 'Bath fan 5"Ø - powder (Panasonic 80-110 cfm ML-036)', 'G', 1.67, 51.57, L['CEIL0']-0.3),
                               ('X-S1', 'Bath fan 5"Ø - 2nd floor bath', 'S', 5.3, 34.6, L['CEIL1']-0.3), ('X-S2', 'Exhaust 5"Ø - laundry', 'S', 5.2, 38.0, L['CEIL1']-0.3),
                               ('X-T1', 'Bath fan 5"Ø - ensuite (Panasonic 80-110 cfm ML-068)', 'T', 11.3, 36.1, L['TOP']-0.3)]:
    seg(fid, nm, lvl, 'exhaust', '5"Ø', x-0.45, x+0.45, y-0.45, y+0.45, z, z+0.3, axis='t', connected=False)
    OUT.append(dict(id=fid, name=nm, sys='exhaust', path=[], lvl=lvl, ok=False, why='Fan drawn; duct route to an exterior hood is not on the HVAC sheets.'))
OUT.append(dict(id='CB-K-HD', name='Kitchen hood - Elica Trento ETR134S1 insert', sys='exhaust', path=[], lvl='G', ok=False, why='No kitchen exhaust duct on the HVAC sheets. Range is on the south wing wall under the 2nd-floor overhang; termination must stay 1.8 m from soffit vents and intakes (OBC 9.32.3.13).'))
OUT.append(dict(id='EQ-F1', name='Basement return grille (schedule says BAS R/A = 1)', sys='return', path=[], lvl='B', ok=False, why='Schedule lists 1 basement return; no basement return grille is drawn on the basement sheet (only the 7R/8R/9R drops from the main floor).'))
# water heater vent (existing - for coordination)
E.append(dict(id='EQ-HWTV', name='Ex. HWT vent 3"', cat='equip', shape='cyl', lvl='B', axis='z', d=3, mat='steel', x0=5.5, x1=5.75, y0=7.55, y1=7.8, z0=5.4, z1=J0T))

import re as _re
_nm = {}
for e in E:
    if e['cat'] == 'wall' and _re.match(r'W[BGST]\d', e['id']):
        _nm.setdefault(e['name'].rsplit(' (', 1)[0], _re.match(r'(W[BGST]\d+)', e['id']).group(1))
for x in D:
    if x.get('inwall'): x['inwall'] = _nm[x['inwall']]
E.extend(D)
json.dump(dict(E=E, L=L, OUT=OUT), open('model_ducts.json', 'w'))
print('ducts', len(D), 'outlets', len(OUT))
