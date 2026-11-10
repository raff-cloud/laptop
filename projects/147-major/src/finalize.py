import json
M=json.load(open('model.json')); L=M['levels']; E=M['elements']; by={e['id']:e for e in E}
fd=[e for e in E if e['name'].startswith('Ex. fdn - rear wing south (42')][0]
M['clashes'].append(dict(a='S-9v',b=fd['id'],an=by['S-9v']['name'],bn='Old rear-wing foundation wall + sill plate (10")',kind='HARD',vol=0.05))
CD=L['C_DROP']
for k,(nm,x0,x1,y0,y1,fl) in enumerate([('master bedroom',0.98,16.44,0.15,13.25,L['FFL1']),('family rm / hall',0.98,13.3,13.25,28.0,L['FFL1']),
        ('hall / laundry / W.I.C. (existing ceiling on red joists)',5.0,16.44,28.0,40.2,L['FFL1R']),('mech room',5.0,16.2,40.2,43.67,L['FFL1R']),('bedroom 2',0.69,16.2,44.27,55.97,L['FFL1R'])]):
    E.append(dict(id=f'BH-{k+1}',name=f'Dropped ceiling (Nov 10) - {nm}',cat='bulkhead',shape='box',lvl='S',x0=x0,x1=x1,y0=y0,y1=y1,z0=round(CD-0.04,3),z1=round(CD,3),mat='bulkhead',clear=round(CD-fl,2)))
def fi(v): 
    f=int(v); i=round((v-f)*12*4)/4
    if i>=12: f+=1;i-=12
    return f"{f}'-{i:g}\""
rooms=[('Family room (main, rear)','11\'-2" x 11\'-5"',(11+2/12,11+5/12),(16.2-5.03,55.96-44.52)),
       ('Bedroom 2 (2nd, rear)','15\'-6" x 11\'-8"',(15.5,11+8/12),(16.2-0.69,55.97-44.27)),
       ('Primary bedroom (3rd, rear)','15\'-6" x 11\'-8"',(15.5,11+8/12),(16.2-0.69,55.97-44.25)),
       ('Bedroom 3 (3rd, front)','15\'-9" x 14\'-6"',(15.75,14.5),(16.44-0.5,21.67-7.16))]
M['rooms']=[dict(room=r,printed=p,model=f'{fi(m[0])} x {fi(m[1])}',d1=round((m[0]-pr[0])*12,1),d2=round((m[1]-pr[1])*12,1)) for r,p,pr,m in rooms]
M['ceil']=[dict(level='Basement (slab to u/s joists)',ft=fi(L['J0B'])),
 dict(level='Main floor - main room (David: 118")',ft=fi(L['CEIL0']-L['FFL0'])),
 dict(level='Main floor - kitchen (David: 9 ft)',ft=fi(L['CEIL0R']-L['FFL0'])),
 dict(level='Main floor - addition / family rm (David: 105")',ft=fi(L['CEIL0A']-L['FFL0'])),
 dict(level='2nd - master bedroom, dropped ceiling (was 105")',ft=fi(L['C_DROP']-L['FFL1'])),
 dict(level='2nd - family rm / stair hall, dropped ceiling (was 105")',ft=fi(L['C_DROP']-L['FFL1'])),
 dict(level='2nd - hall / laundry / W.I.C., existing ceiling on red joists (16" void above)',ft=fi(L['C_DROP']-L['FFL1R'])),
 dict(level='2nd - bath, dropped ceiling (David: 99")',ft=fi(L['C_BATH']-L['FFL1R'])),
 dict(level='2nd - mech room + bedroom 2, dropped ceiling (was ~120")',ft=fi(L['C_DROP']-L['FFL1R'])),
 dict(level='3rd floor (116.90 to top plate 119.60)',ft=fi(L['TOP']-L['FFL2']))]
M['windows']=[dict(id=e['id'],name=e['name'],lvl=e['lvl'],w=fi(max(e['x1']-e['x0'],e['y1']-e['y0'])),sill=fi(e['z0']-({'B':0,'G':L['FFL0'],'S':L['FFL1'],'T':L['FFL2']}[e['lvl']] if not (e['lvl']=='S' and e['y0']>=27.9) else L['FFL1R'])),head=fi(e['z1']-({'B':0,'G':L['FFL0'],'S':L['FFL1'],'T':L['FFL2']}[e['lvl']] if not (e['lvl']=='S' and e['y0']>=27.9) else L['FFL1R']))) for e in E if e['cat'] in('window','door') and e['mat']=='glass']
json.dump(M,open('model.json','w'))
print('ok'); print(M['rooms']); print(M['ceil']); print(len(M['windows']),'windows')
