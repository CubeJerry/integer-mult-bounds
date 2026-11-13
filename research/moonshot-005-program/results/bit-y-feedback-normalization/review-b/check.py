"""Independent actual-native two-target Y-mediated feedback control."""
import argparse,collections,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(raw));fr={int(k):v for k,v in s['frames'].items()};zero=s['start'][111];hub=s['final'][0];line=s['start'][1];yi=111;yj=112;p=222;c=223;ops=[]
 assert all(s['start'][111+i]==zero and s['final'][i]==hub for i in range(111))
 def add(op):ops.append(op)
 add(['INIT',c,zero]);add(['ADD',c,yi,zero]);add(['MOVE',yi,zero,line]);add(['ADD',yi,1,line])
 for i in range(111):add(['MOVE',i,s['start'][i],hub])
 add(['INIT',p,hub]);add(['ADD',p,0,hub]);add(['ADD',p,1,hub]);ex=len(ops);add(['MOVE',p,hub,line]);add(['ADD',yi,p,line]);add(['ADD',p,yi,line]);ground=len(ops);add(['MOVE',p,line,zero]);purge=len(ops);add(['ADD',p,c,zero]);add(['CLEAR',c,zero]);add(['ADD',yj,p,zero]);add(['CLEAR',p,zero]);add(['MOVE',yi,line,s['final'][yi]])
 for j in range(1,111):add(['MOVE',111+j,zero,s['final'][111+j]])
 def subset(x,y):return fr[x]['dim']<=fr[y]['dim'] and all(sum(F(a)*F(b) for a,b in zip(u,v))==0 for u in fr[x]['B'] for v in fr[y]['A'])
 def replay(program):
  rows={i:1<<i for i in range(222)};loc=dict(enumerate(s['start'][:222]));bill=collections.Counter();counts=collections.Counter();life=peak=0;snap={}
  for t,e in enumerate(program):
   op,r=e[:2];counts[op]+=1
   if op=='INIT':assert r>=222 and r not in rows;rows[r]=0;loc[r]=e[2];life+=1
   elif op=='CLEAR':assert r>=222 and loc[r]==e[2] and rows[r]!=0;del rows[r];del loc[r]
   elif op=='ADD':assert loc[r]==loc[e[2]]==e[3];rows[r]^=rows[e[2]]
   elif op=='MOVE':
    x,y=e[2:];assert loc[r]==x;d=fr[y]['dim']-fr[x]['dim'];assert d and (subset(x,y) if d>0 else r>=222 and subset(y,x));loc[r]=y;bill[abs(d)]+=1
   else:raise AssertionError(op)
   peak=max(peak,len(rows)-222)
   if t==ex-1:snap['T']=rows[p]
   if t==ground:snap['G0']=rows[p]
  assert set(rows)==set(range(222)) and all(loc[i]==s['final'][i] for i in range(222));return rows,dict(bill),dict(counts),life,peak,snap
 rows,bill,counts,life,peak,snap=replay(ops);expected={i:1<<i for i in range(222)};expected[yi]^=1;expected[yj]^=2;assert rows==expected and snap=={'T':3,'G0':(1<<yi)^2}
 assert bill=={7:222,1:2,6:1} and counts=={'INIT':2,'ADD':8,'MOVE':225,'CLEAR':2} and life==peak==2
 assert rows[yi]^snap['T']^(1<<yi)==2 and rows[yj]^snap['G0']^(1<<yi)^(1<<yj)==0
 controls=[]
 for name,pr in [('omit_ground_purge',ops[:purge]+ops[purge+1:]),('reverse_feedback_order',ops[:ex+1]+[ops[ex+2],ops[ex+1]]+ops[ex+3:])]:
  rr,*_=replay(pr);assert rr!=expected;controls.append({'name':name,'wrong_public_rows':[i for i in expected if rr[i]!=expected[i]]})
 # G0_x=e1 alone cannot span the lost e0; actual T_x=e0+e1 restores it.
 assert (snap['G0']&((1<<111)-1))==2 and (snap['T']&((1<<111)-1))==3
 out={'status':'PASS_NATIVE_Y_FEEDBACK_UNKNOWN_INPUT_AND_HISTORICAL_CONTROL','source_sha256':hashlib.sha256(raw).hexdigest(),'all222_original_columns':True,'completed_Y_ports':[0,1],'other109_Y_rows_unchanged':True,'all111_X_restored':True,'packet_X_support_after_purge':[1],'first_ground_packet_has_original_y0':True,'unknown_y_canceled_by_actual_stationary_ground_cache':True,'scalar_ops':counts,'paid_profile':bill,'lifetimes':life,'peak':peak,'two_nonzero_clears':True,'kernel_history_necessary':True,'G0_x':'x1','T_x':'x0+x1','Y0_local_x_remainder':'x1 at actualL1 subsetF0','negative_controls':controls,'scope':'Actual native-chart partial two-target word; supports normalization, does not evade arrival theorem or complete111 targets. Physical compiler/erasure remain.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');word={'public':222,'owned_fields':2,'start':s['start'][:222],'final':s['final'][:222],'frames':s['frames'],'program':ops,'scope':out['scope']};(a.output/'WORD.json.gz').write_bytes(gzip.compress((json.dumps(word,separators=(',',':'))+'\n').encode(),mtime=0));print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
