import json, re
M = json.load(open('model_ducts.json')); E = M['E']; L = M['L']; OUT = M['OUT']
by = {e['id']: e for e in E}
TOL = 1/12
def gap(a, b):
    g = 0; inside = True; vol = 1
    for ax in 'xyz':
        lo = max(a[ax+'0'], b[ax+'0']); hi = min(a[ax+'1'], b[ax+'1'])
        if hi <= lo: inside = False; g = max(g, lo-hi)
        else: vol *= (hi-lo)
    return (0 if inside else g), (vol if inside else 0)
def pgap(a, b):
    gx = max(0, max(a['x0'], b['x0']) - min(a['x1'], b['x1'])); gy = max(0, max(a['y0'], b['y0']) - min(a['y1'], b['y1'])); gz = max(0, max(a['z0'], b['z0']) - min(a['z1'], b['z1']))
    return max(gx, gy) if gz <= 1.6 else 9
def jdir(j): return 'x' if (j['x1']-j['x0']) > (j['y1']-j['y0']) else 'y'
TGT = {'joist', 'beam', 'wall', 'window', 'door', 'cabinet', 'counter', 'fixture', 'stair', 'equip'}
OWN = {'D-PL1': {'EQ-F1', 'EQ-EXF', 'EQ-HWT'}, 'R-XD': {'EQ-F1', 'EQ-EXF'}, 'D2-PL': {'EQ-F2', 'EQ-HRV2'}, 'R2-XD': {'EQ-F2', 'EQ-HRV2'}}
ducts = [e for e in E if e['cat'] == 'duct']
clashes = []
for d in ducts:
    for t in E:
        if t['cat'] not in TGT or t['id'] == d['id']: continue
        if t['id'] in OWN.get(d['id'], set()): continue
        if t['cat'] == 'equip' and t['id'] in ('EQ-EXF',): continue
        g, vol = gap(d, t)
        if g > TOL: continue
        ax = d.get('axis')
        if t['cat'] == 'joist':
            if ax in ('z', 't'): continue                       # boots / stacks shift within the bay
            if ax == jdir(t): continue                          # parallel run - sits in the bay
            if vol == 0: continue
        if t['cat'] == 'wall' and t['mat'] == 'kneewall':
            if vol > 0: clashes.append(dict(a=d['id'], b=t['id'], an=d['name'], bn=t['name'], kind='SOFT', vol=0))
            continue
        if t['cat'] == 'wall':
            masonry = t['mat'] in ('parge', 'concrete', 'brick')
            if d['z0'] >= t['z1'] - 0.01: continue                 # duct runs above the top plate (in the joist space)
            host = d.get('inwall') and re.fullmatch(d['inwall'] + r'[a-z]*\d*', t['id'])
            if host and not masonry: continue
            if ax in ('x', 'y') and not masonry:
                wdir = 'x' if (t['x1']-t['x0']) > (t['y1']-t['y0']) else 'y'
                if wdir != ax: continue                          # crosses a partition - framed opening
            if ax == 't' and not masonry: continue              # grille set in its wall
            if ax == 't' and masonry and vol == 0: continue
        if t['cat'] == 'stair' and vol == 0: continue
        if t['cat'] in ('window', 'door') and vol == 0 and ax != 't': continue
        kind = 'HARD' if vol > 0.004 else 'SOFT'
        clashes.append(dict(a=d['id'], b=t['id'], an=d['name'], bn=t['name'], kind=kind, vol=round(vol, 3)))
# grille vs feature-wall finish / mirrors (ensuite)
for d in ducts:
    if d.get('axis') != 't': continue
    for t in E:
        if t['cat'] == 'finish' and t['mat'] in ('tile', 'bluetile') and t['z1'] - t['z0'] > 1:
            g, vol = gap(d, t)
            if g <= 0.01: clashes.append(dict(a=d['id'], b=t['id'], an=d['name'], bn=t['name'], kind='HARD', vol=round(max(vol, 0.01), 3)))
# main-floor ceiling must stay clear (two-system design)
for d in ducts:
    rear = (d['y0'] + d['y1']) / 2 >= 28
    jb, jt = (L['J1BR'], L['J1TR']) if rear else (L['J1B'], L['J1T'])
    if d['lvl'] in ('G', 'S') and d['z1'] > jb + 0.01 and d['z0'] < jt - 0.01 and d.get('axis') != 't':
        clashes.append(dict(a=d['id'], b='J1A-1', an=d['name'], bn='Main-floor ceiling (must stay duct-free)', kind='HARD', vol=0.01))
# bulkheads: runs that cross joists
bulk = []
for d in ducts:
    if d.get('axis') not in ('x', 'y'): continue
    Ln = (d['y1']-d['y0']) if d['axis'] == 'y' else (d['x1']-d['x0'])
    if Ln < 1.5: continue
    if d['lvl'] == 'B' and d['z1'] <= L['J0B'] + 0.01:
        bulk.append(dict(id=d['id'], len_ft=round(Ln, 1), under_ft=round(d['z0'], 2), lvl='B', note='below basement joists'))
    if d['lvl'] == 'S' and d.get('dropped') and not d.get('invoid'):
        fl = L['FFL1R'] if (d['y0'] + d['y1']) / 2 >= 28 else L['FFL1']
        bulk.append(dict(id=d['id'], len_ft=round(Ln, 1), under_ft=round(d['z0'] - 0.1 - fl, 2), lvl='S', note=f"hung under the 3rd-floor joists, boxed - {int(d['z0']-0.1-fl)}'-{round(((d['z0']-0.1-fl)%1)*12)}\" clear (decision Oct 22)"))
# in-wall stacks vs wall cavity
prot = []
for d in ducts:
    if d.get('axis') == 'z' and d.get('inwall'):
        hosts = [e for e in E if e['cat'] == 'wall' and re.fullmatch(d['inwall'] + r'[a-z]*\d*', e['id'])]
        if not hosts: continue
        h = hosts[0]; th = min(h['x1']-h['x0'], h['y1']-h['y0'])
        cav = th*12 - 1.0
        dia = (d['x1']-d['x0'])*12
        if dia > cav + 0.1: prot.append(dict(id=d['id'], inches=round(dia-cav, 1), wall=round(th*12, 1)))
for d in ducts:   # stacks without a declared host
    if d.get('axis') == 'z' and not d.get('inwall') and not d.get('source') and d['id'].startswith('R-') and d['lvl'] in ('S', 'T'):
        prot.append(dict(id=d['id'], inches=round((d['x1']-d['x0'])*12 - 3.5, 1), wall=4.5))
# connectivity
ids = set(by)
conn = []
for o in OUT:
    if o.get('ok') is False:
        conn.append(dict(id=o['id'], name=o['name'], sys=o['sys'], ok=False, path=[], why=o['why'])); continue
    ok = all(p in ids for p in o['path'])
    # each consecutive pair must touch
    for a, b in zip(o['path'], o['path'][1:]):
        g = pgap(by[a], by[b])
        if g > 0.6: ok = False; o.setdefault('broken', []).append([a, b, round(g, 2)])
    if o['id'] in ids and o['path']:
        g = pgap(by[o['path'][-1]], by[o['id']])
        if g > 0.6: ok = False; o.setdefault('broken', []).append([o['path'][-1], o['id'], round(g, 2)])
    conn.append(dict(id=o['id'], name=o['name'], sys=o['sys'], ok=ok, path=o['path'], broken=o.get('broken', [])))
dims = [
 dict(item='Kitchen south wall run (dining corner to storage wall)', permit_in=184.6, cabinet_in=186.5, note=None, src='A7 vector 28.30→43.68 ft; 9/8 cab set text "186 1/2"'),
 dict(item='Range opening', permit_in=29.9, cabinet_in=36.0, note=None, src='A7 shows 30" range; ML-104 Miele HR 1432-3 I is 36"'),
 dict(item='Fridge opening', permit_in=34.2, cabinet_in=36.0, note=None, src='A7 "F" 34"; ML-103 Miele KFNF 9959 iDE 36"'),
 dict(item='Aisle - counter to island', permit_in=39.8, cabinet_in=42.0, note='aisle', src='A7 3\'-4" (NKBA work aisle 42")'),
 dict(item='Aisle - island to stair wall', permit_in=34.9, cabinet_in=36.0, note='aisle', src='A7 2\'-11" (36" walkway min.)'),
 dict(item='Island length', permit_in=90.1, cabinet_in=90.0, note=None, src='A7 3\'-0"x7\'-6"; cab set geometry not readable yet'),
 dict(item='Ensuite vanity wall', permit_in=83.4, cabinet_in=72.0, note='fits', src='A9 7\'-0" vanity zone; ML-046 Asher 72"'),
 dict(item='Tub alcove (wall to wall)', permit_in=74.4, cabinet_in=67.0, note='fits', src='A9 22.01→28.21 ft; ML-065 Mirella 67x29 (3.7" each end)'),
 dict(item='Kitchen window vs sink base', permit_in=44.2, cabinet_in=44.1, note=None, src='A7 window 32.69→36.37; sink base under'),
]
M2 = dict(gaps=[], grade=L['GRADE'], elements=E, clashes=clashes, protrude=prot, bulkheads=bulk, conn=conn, dims=dims, levels=L)
json.dump(M2, open('model.json', 'w'))
from collections import Counter
print('clashes', len(clashes), Counter(c['kind'] for c in clashes))
grp = {}
for c in clashes: grp.setdefault(c['a'], []).append((c['kind'], c['b']))
for k, v in grp.items(): print(' ', k, by[k]['name'][:50], '->', sorted(set(x[1].split('-')[0] + ':' + by.get(x[1], {'cat': '?'})['cat'] if x[1] in by else x[1] for x in v))[:6], Counter(x[0] for x in v))
print('bulk', [(b['id'], b['len_ft']) for b in bulk])
print('prot', prot)
print('not connected', [(c['id'], c.get('broken')) for c in conn if not c['ok']])
