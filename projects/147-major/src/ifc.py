import json, uuid, string, datetime
M = json.load(open('model.json')); L = M['levels']
FT = 0.3048
CH = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_$'
def gid():
    n = uuid.uuid4().int; s = ''
    for _ in range(22): s = CH[n % 64] + s; n //= 64
    return s
lines = []; k = [0]
def add(s):
    k[0] += 1; lines.append(f'#{k[0]}={s};'); return f'#{k[0]}'
def q(s): return "'" + s.replace("\\", "\\\\").replace("'", "''").encode('ascii', 'replace').decode().replace('?', '-') + "'"
def f(v): return f'{v:.4f}'.rstrip('0').rstrip('.') + ('.' if '.' not in f'{v:.4f}'.rstrip('0').rstrip('.') else '')
def pt(x, y, z): return add(f'IFCCARTESIANPOINT(({f(x)},{f(y)},{f(z)}))')
org = add(f"IFCORGANIZATION($,{q('PalmView Custom Homes')},$,$,$)")
per = add(f"IFCPERSON($,{q('PalmView')},$,$,$,$,$,$)")
po = add(f'IFCPERSONANDORGANIZATION({per},{org},$)')
app = add(f"IFCAPPLICATION({org},'1.0',{q('PalmView clash model')},'PVCM')")
ts = int(datetime.datetime(2026, 10, 22).timestamp())
oh = add(f'IFCOWNERHISTORY({po},{app},$,.ADDED.,$,$,$,{ts})')
O = pt(0, 0, 0); Z = add('IFCDIRECTION((0.,0.,1.))'); X = add('IFCDIRECTION((1.,0.,0.))')
A3 = add(f'IFCAXIS2PLACEMENT3D({O},{Z},{X})')
ctx = add(f"IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,{A3},$)")
body = add(f"IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Body','Model',*,*,*,*,{ctx},$,.MODEL_VIEW.,$)")
u1 = add("IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.)"); u2 = add("IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.)"); u3 = add("IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.)")
ua = add(f'IFCUNITASSIGNMENT(({u1},{u2},{u3}))')
proj = add(f"IFCPROJECT('{gid()}',{oh},{q('147 Major St - Addition')},{q('BIM clash model, HVAC LO# 113963 vs permit 26 167838 BLD 00')},$,$,$,({ctx}),{ua})")
def lp(rel, x=0, y=0, z=0):
    a = add(f'IFCAXIS2PLACEMENT3D({pt(x, y, z)},$,$)'); return add(f'IFCLOCALPLACEMENT({rel},{a})')
site_lp = lp('$'); site = add(f"IFCSITE('{gid()}',{oh},{q('147 Major St, Toronto')},$,$,{site_lp},$,$,.ELEMENT.,$,$,$,$,$)")
bld_lp = lp(site_lp); bld = add(f"IFCBUILDING('{gid()}',{oh},{q('147 Major St - semi-detached')},$,$,{bld_lp},$,$,.ELEMENT.,$,$,$)")
STO = {}
for code, nm, z in [('B', 'Basement (107.63)', 0), ('G', 'Main floor (110.52)', L['FFL0']), ('S', 'Second floor (113.85)', L['FFL1']), ('T', 'Third floor (116.90)', L['FFL2']), ('R', 'Roof', L['TOP']), ('X', 'Site', L['GRADE'])]:
    slp = lp(bld_lp); s = add(f"IFCBUILDINGSTOREY('{gid()}',{oh},{q(nm)},$,$,{slp},$,$,.ELEMENT.,{f(z*FT)})")
    STO[code] = (s, slp, [])
add(f"IFCRELAGGREGATES('{gid()}',{oh},$,$,{proj},({site}))"); add(f"IFCRELAGGREGATES('{gid()}',{oh},$,$,{site},({bld}))")
add(f"IFCRELAGGREGATES('{gid()}',{oh},$,$,{bld},({','.join(v[0] for v in STO.values())}))")
CLS = {'wall': 'IFCWALL', 'beam': 'IFCBEAM', 'joist': 'IFCMEMBER', 'window': 'IFCWINDOW', 'door': 'IFCDOOR', 'stair': 'IFCSTAIRFLIGHT', 'cabinet': 'IFCFURNITURE', 'counter': 'IFCFURNITURE',
       'fixture': 'IFCSANITARYTERMINAL', 'equip': 'IFCUNITARYEQUIPMENT', 'finish': 'IFCCOVERING', 'roof': 'IFCROOF', 'site': 'IFCBUILDINGELEMENTPROXY', 'bulkhead': 'IFCCOVERING', 'trim': 'IFCBUILDINGELEMENTPROXY'}
hard = {}
for c in M['clashes']: hard.setdefault(c['a'], []).append(f"{c['kind']}: {c['bn']}")
pset_t = add(f"IFCPROPERTYSINGLEVALUE('Source',$,IFCLABEL('147 Major clash model Oct 22 2026'),$)")
for e in M['elements']:
    cat = e['cat']
    cls = CLS.get(cat, 'IFCBUILDINGELEMENTPROXY')
    if cat == 'duct':
        cls = 'IFCAIRTERMINAL' if e.get('axis') == 't' else 'IFCDUCTSEGMENT'
    sto = STO.get(e['lvl'], STO['X'])
    cx, cy = (e['x0'] + e['x1']) / 2 * FT, -(e['y0'] + e['y1']) / 2 * FT   # y flipped so the street faces -y
    z0 = e['z0'] * FT; h = max(0.002, (e['z1'] - e['z0']) * FT)
    plc = lp(sto[1], cx, cy, z0)
    if e['shape'] == 'cyl' and e.get('axis') == 'z':
        prof = add(f"IFCCIRCLEPROFILEDEF(.AREA.,$,$,{f(e['d'] / 24 * FT)})")
    else:
        prof = add(f"IFCRECTANGLEPROFILEDEF(.AREA.,$,$,{f(max(0.002, (e['x1'] - e['x0']) * FT))},{f(max(0.002, (e['y1'] - e['y0']) * FT))})")
    sol = add(f'IFCEXTRUDEDAREASOLID({prof},{A3},{Z},{f(h)})')
    rep = add(f"IFCSHAPEREPRESENTATION({body},'Body','SweptSolid',({sol}))")
    pds = add(f'IFCPRODUCTDEFINITIONSHAPE($,$,({rep}))')
    nm = e['name'][:120]
    tag = e['id']
    if cls in ('IFCWALL', 'IFCBEAM', 'IFCMEMBER', 'IFCFURNITURE', 'IFCSANITARYTERMINAL', 'IFCUNITARYEQUIPMENT', 'IFCDUCTSEGMENT', 'IFCAIRTERMINAL', 'IFCBUILDINGELEMENTPROXY', 'IFCSTAIRFLIGHT', 'IFCROOF'):
        if cls == 'IFCSTAIRFLIGHT': ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$,$,$,$,$)")
        elif cls in ('IFCROOF',): ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$)")
        elif cls == 'IFCFURNITURE': ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$)")
        else: ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$)")
    elif cls in ('IFCWINDOW', 'IFCDOOR'):
        ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},{f(h)},{f(max(e['x1'] - e['x0'], e['y1'] - e['y0']) * FT)},$,$,$)")
    elif cls == 'IFCCOVERING':
        ent = add(f"{cls}('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$)")
    else:
        ent = add(f"IFCBUILDINGELEMENTPROXY('{gid()}',{oh},{q(nm)},$,$,{plc},{pds},{q(tag)},$)")
    sto[2].append(ent)
    props = [pset_t]
    if cat == 'duct':
        props.append(add(f"IFCPROPERTYSINGLEVALUE('System',$,IFCLABEL({q(e['sys'] + (' F-2' if e['lvl'] in ('S', 'T') else ' F-1'))}),$)"))
        props.append(add(f"IFCPROPERTYSINGLEVALUE('Size',$,IFCLABEL({q(str(e.get('size')))}),$)"))
    if tag in hard:
        props.append(add(f"IFCPROPERTYSINGLEVALUE('Clashes',$,IFCTEXT({q(' | '.join(sorted(set(hard[tag])))[:900])}),$)"))
    ps = add(f"IFCPROPERTYSET('{gid()}',{oh},'PalmView_Coordination',$,({','.join(props)}))")
    add(f"IFCRELDEFINESBYPROPERTIES('{gid()}',{oh},$,$,({ent}),{ps})")
for code, (s, slp, ents) in STO.items():
    if ents: add(f"IFCRELCONTAINEDINSPATIALSTRUCTURE('{gid()}',{oh},$,$,({','.join(ents)}),{s})")
hdr = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [ReferenceView]'),'2;1');
FILE_NAME('147-Major-model.ifc','2026-10-22T12:00:00',('PalmView Custom Homes'),('PalmView Custom Homes'),'PalmView clash model','PalmView clash model','');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
"""
open('147-Major-model.ifc', 'w').write(hdr + '\n'.join(lines) + '\nENDSEC;\nEND-ISO-10303-21;\n')
print(len(lines), 'IFC entities')
