"""Independent composition audit using C's separate exact interpreter."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from collections import Counter
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD='fbbae97bf0c71ca5d1f74bbe272e5507690f09d991600fe42f1636f0386c7433'
INTERPRETER='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--variant',choices=['restored','low'],default='restored');a=p.parse_args();low=a.variant=='low';word_pin='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'if low else WORD
 root=a.repo/'research/moonshot-005-program';native=root/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';interpreter=root/'sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py'
 assert digest(native)==NATIVE and digest(a.word)==word_pin and digest(interpreter)==INTERPRETER
 spec=importlib.util.spec_from_file_location('independent_geometry',interpreter);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);need=m.require
 R=json.loads(native.read_text())['native_roots'];word=json.loads(a.word.read_text());charts={n:m.chart(v)for n,v in word['charts'].items()};E=[tuple(int(i==j)for j in range(8))for i in range(8)]
 need(charts['Hub']==m.basis(tuple(E))and not charts['zero'],'ambient charts')
 for i,r in enumerate(R):need(charts[f'L{i}']==m.basis((tuple(r),))and charts[f'F{i}']==m.kernel((tuple(r),)),'native charts')
 configs=[([0,1,6,7],[0,1],[6,7],[2,3]),([2,3,4,5],[2,4],[3,5],[0,1]),([0,1,4,5],[0,5],[1,4],[]),([0,2,5,7],[0,7],[2,5],[])]
 xv={i:frozenset([i])for i in range(111)};xc={i:f'L{i}'for i in range(111)}
 expected={i:frozenset()for i in range(111)};served=set();sources={};yc={i:'zero'for i in range(111)};stages=[]
 for k,(support,ab,cd,couriers)in enumerate(configs):
  tag=f'G{k}';signs=[i for i,r in enumerate(R)if[j for j,x in enumerate(r)if x]==support];need(len(signs)==8,'full sign quartet')
  need(charts[tag]==m.basis(tuple(E[i]for i in support)),'quartet chart')
  local_sources=signs+(support if couriers else[]);need(not(set(local_sources)&set(sources)),'disjoint original source paths')
  for i in local_sources:sources[i]=tag;xc[i]=tag
  for i in couriers:need(yc[i]=='zero'and m.contained(charts[tag],charts[f'F{i}']),'available compatible courier');yc[i]=tag
  current=[];groups={}
  for s in (1,-1):
   for label,pair,other in [('A',ab,cd),('B',cd,ab)]:
    x,y=pair;u,v=other;q=f'{tag}_{label}{s}';vec=tuple(E[x][j]+s*E[y][j]for j in range(8));plane=m.basis((vec,E[u],E[v]));need(charts[q]==plane,'independent query plane')
    local={i for i in signs if R[i][x]==s*R[i][y]}|(set(other)if couriers else set())
    receivers=[i for i,r in enumerate(R)if[j for j in support if r[j]]==sorted(pair)and r[x]==-s*r[y]and i not in served]
    need(len(local)==(6 if couriers else 4),'foreign correction size')
    for i in receivers:
     need(yc[i]=='zero'and not expected[i],'receiver starts once at ground')
     need(i not in local and all(sum(t*z for t,z in zip(R[i],R[j]))==0 for j in local),'foreign neighbours')
     need(m.contained(plane,charts[f'F{i}']),'query inside endpoint facet');expected[i]=frozenset(local);yc[i]=q
    current+=receivers;groups[q]={'receivers':receivers,'summands':sorted(local)}
   for t in (1,-1):
    roles=[i for i in signs if R[i][ab[0]]==s*R[i][ab[1]]and R[i][cd[0]]==t*R[i][cd[1]]]
    name=f'{tag}_PAIR_{s}_{t}';need(len(roles)==2 and charts[name]==m.basis(tuple(tuple(R[i])for i in roles))and len(charts[name])==2,'rank-two pair')
    if low:
     xv[roles[0]]=frozenset(roles);xc[roles[0]]=f'{tag}_B{t}'if s==t else f'{tag}_A{s}';xc[roles[1]]=name
  need(len(current)==len(set(current)),'disjoint query receivers');served.update(current)
  stages.append({'gadget':k,'source_roles':sorted(local_sources),'served_receivers':sorted(current),'queries':groups,'couriers':couriers})
 need([len(s['served_receivers'])for s in stages]==[29,29,16,29],'stage populations')
 need(served==set(range(8,111))and len(sources)==40,'all noncoordinate receivers, forty original paths')
 need(word['Y_correction_rows_hex']==[hex(sum(1<<j for j in expected[i]))for i in range(111)],'declared rows match independent geometry')
 stats,cv,ca=m.replay(word,charts,expected,sorted(served),sorted(sources),check_cut=False)
 need(stats['counts']=={'INIT':111,'ADD':455,'MOVE':508 if low else 540,'CLEAR':111},'full invoice')
 need(stats['movement_profile']==({1:175,2:111,3:4,4:111,5:16,6:16,7:75}if low else{1:191,2:127,3:4,4:143,7:75})and stats['prefix_profile']==({1:175,2:111}if low else{1:191,2:127}),'movement profile')
 need(stats['rank_length']==1554 and stats['dirty_CLEAR']==111 and stats['peak_owned']==111,'length and owned charges')
 need(word['carrier_interface_before_operation']==(836 if low else 884) and len(cv)==333,'actual cut')
 for i in range(111):
  need(cv[f'X{i}']==xv[i]and ca[f'X{i}']==xc[i],'restored X cut')
  need(cv[f'Y{i}']==expected[i]|{111+i}and ca[f'Y{i}']==yc[i],'all-column Y cut')
  need(cv[f'NATIVE_{i}']==frozenset([i])and ca[f'NATIVE_{i}']==f'L{i}','actual native snapshot')
 for name,row in cv.items():
  for j in row:
   if j<111:need(m.contained(charts[f'L{j}'],charts[ca[name]]),'every initial X coefficient native-local')
 need(all(len(charts[c])<7 for c in ca.values()),'no initial facet or Hub field')
 q=m.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(x/6 for x in m.moment(gate));room=(ceiling[0]-q[1],ceiling[1]-q[0]);cap=78 if low else 77;need(cap<room[0]<room[1]<cap+1,'exact future owned move cap')
 controls={}
 choices=[(key,0)for key in ['G0:ground_Y_inverse','G1:ground_Y_inverse','G1:courier_cleanup','G2:early_pair_read','G3:later_pair_read']]
 choices+= [('deferred_sign_inverse_at_Hub',j)for j in [0,5,10,15]]if low else[('G2:X_inverse',0),('G3:X_inverse',0)]
 for key,j in choices:
  alt=copy.deepcopy(word);idx=alt['semantic_operation_indices'][key][j];del alt['operations'][idx]
  if idx<alt['carrier_interface_before_operation']:alt['carrier_interface_before_operation']-=1
  try:m.replay(alt,charts,expected,sorted(served),sorted(sources),check_cut=False)
  except ValueError as error:controls[key+':'+str(j)]=str(error)
  else:raise ValueError('essential mutation accepted: '+key)
 alt=copy.deepcopy(word);idx=alt['semantic_operation_indices']['G2:early_query_arrival'][0];alt['operations'][idx][2]='G2_A1'
 try:m.replay(alt,charts,expected,sorted(served),sorted(sources),check_cut=False)
 except ValueError as error:controls['incomparable_query_shortcut']=str(error)
 else:raise ValueError('unavailable early query accepted')
 inventory=[{'name':n,'chart':ca[n],'rank':len(charts[ca[n]]),'row_hex':hex(sum(1<<j for j in row))}for n,row in sorted(cv.items())]
 need(inventory==json.loads(a.word.with_name('CUT-INVENTORY.json').read_text())['fields'],'independent full cut agrees after derivation')
 result={'status':'PASS_INDEPENDENT_COMPOSED_ALL103_CORRECTION','native_sha256':NATIVE,'word_sha256':word_pin,'variant':a.variant,'independent_interpreter_sha256':INTERPRETER,'cut':word['carrier_interface_before_operation'],'all_public_columns':222,'live_cut_fields':333,'served_receivers':103,'foreign_coefficients':sum(len(x)for x in expected.values()),'completed_diagonal_outputs':0,'X_originals_below_Hub':111,'original_X_rank_histogram':dict(Counter(len(charts[ca[f'X{i}']])for i in range(111))),'native_originals':71,'quartet_originals':8 if low else 40,'raw_rank2_originals':16 if low else 0,'encoded_rank3_originals':16 if low else 0,'stages':stages,'stats':stats,'moment_rational':list(map(str,q)),'necessary_room_rational':list(map(str,room)),'future_positive_owned_moves_at_most':cap,'monotone_public_continuation_chi_upper':111+cap,'all_initial_X_coefficients_native_local':True,'negative_controls':controls,'new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'INDEPENDENT-CUT.json').write_text(json.dumps(inventory,indent=2)+'\n')
 print(result['status'],a.variant,'all103,528 coefficients, chi cap',111+cap,'controls rejected',len(controls))
if __name__=='__main__':main()
