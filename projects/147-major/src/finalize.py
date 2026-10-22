import json
M=json.load(open('model.json')); L=M['levels']; E=M['elements']; by={e['id']:e for e in E}
fd=[e for e in E if e['name'].startswith('Ex. fdn - rear wing south (42')][0]
M['clashes'].append(dict(a='S-9v',b=fd['id'],an=by['S-9v']['name'],bn='Old rear-wing foundation wall + sill plate (10")',kind='HARD',vol=0.05))
J2B=L['J2B']; n=0
for b in M['bulkheads']:
    if b['lvl']!='S': continue
    d=by[b['id']]; n+=1; depth=d['z1']-d['z0']; pad=2/12; fl=(L['FFL1R'] if (d['y0']+d['y1'])/2>=28 else L['FFL1'])
    E.append(dict(id=f'BH-{n}',name=f'Bulkhead (Oct 22) - {d["name"].split(" (")[0]}',cat='bulkhead',shape='box',lvl='S',x0=round(d['x0']-pad,3),x1=round(d['x1']+pad,3),y0=round(d['y0']-pad,3),y1=round(d['y1']+pad,3),z0=round(d['z0']-0.1,3),z1=round(J2B,3),mat='bulkhead',clear=round(d['z0']-0.1-fl,2)))
def fi(v): 
    f=int(v); i=round((v-f)*12*4)/4
    if i>=12: f+=1;i-=12
    return f"{f}'-{i:g}\""
rooms=[('Family room (main, rear)','11\'-2" x 11\'-5"',(11+2/12,11+5/12),(16.2-5.03,55.96-44.52)),
       ('Bedroom 2 (2nd, rear)','15\'-6" x 11\'-8"',(15.5,11+8/12),(16.2-0.69,55.97-44.27)),
       ('Primary bedroom (3rd, rear)','15\'-6" x 11\'-8"',(15.5,11+8/12),(16.2-0.69,55.97-44.25)),
       ('Bedroom 3 (3rd, front)','15\'-9" x 14\'-6"',(15.75,14.5),(16.44-0.5,21.67-7.16))]
M['rooms']=[dict(room=r,printed=p,model=f'{fi(m[0])} x {fi(m[1])}',d1=round((m[0]-pr[0])*12,1),d2=round((m[1]-pr[1])*12,1)) for r,p,pr,m in rooms]
M['ceil']=[dict(level='Basement (slab to u/s ex. 2x12)',ft=fi(L['J0B'])),dict(level='Main floor front (FFL 110.52 to ceiling)',ft=fi(L['CEIL0']-L['FFL0'])),
           dict(level='Main floor rear (kitchen / family rm, under lower 2nd floor)',ft=fi(L['CEIL0R']-L['FFL0'])),dict(level='Second floor front (FFL 113.85 to ceiling)',ft=fi(L['CEIL1']-L['FFL1'])),dict(level='Second floor rear (16" lower, to ceiling)',ft=fi(L['CEIL1']-L['FFL1R'])),dict(level='Third floor (FFL 116.90 to top plate 119.60)',ft=fi(L['TOP']-L['FFL2']))]
M['windows']=[dict(id=e['id'],name=e['name'],lvl=e['lvl'],w=fi(max(e['x1']-e['x0'],e['y1']-e['y0'])),sill=fi(e['z0']-({'B':0,'G':L['FFL0'],'S':L['FFL1'],'T':L['FFL2']}[e['lvl']] if not (e['lvl']=='S' and e['y0']>=27.9) else L['FFL1R'])),head=fi(e['z1']-({'B':0,'G':L['FFL0'],'S':L['FFL1'],'T':L['FFL2']}[e['lvl']] if not (e['lvl']=='S' and e['y0']>=27.9) else L['FFL1R']))) for e in E if e['cat'] in('window','door') and e['mat']=='glass']
json.dump(M,open('model.json','w'))
print(n,'bulkheads'); print(M['rooms']); print(M['ceil']); print(len(M['windows']),'windows')
