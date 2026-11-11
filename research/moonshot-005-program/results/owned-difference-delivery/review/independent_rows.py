"""Independent exact forward replay on all1480 dirty entering columns."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
 if not b:raise ValueError(s)
def add(a,b,c):
 for k,v in b.items():
  x=a.get(k,F(0))+c*v
  if x:a[k]=x
  else:a.pop(k,None)
def run(src,cert):
 raw=src.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));c=json.loads(cert.read_text());checks={x['before_event']:x for x in c['witnesses']}
 mains=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);rows=[{r:F(1)} if r<w['public'] else {} for r in range(w['public']+w['owned_fields'])];frames=w['initial'][:]+[None]*w['owned_fields'];out=[]
 for i,e in enumerate(w['program']):
  if i in checks:
   a=checks[i];need(e==a['move'],'source occurrence');res=rows[e[1]].copy()
   for r,v in a['witness']:need(r!=e[1] and frames[r]==e[3],'current cochart');add(res,rows[r],-F(v))
   need(res and not set(res)&mains,'nonzero pure dirty-helper residual');need(res=={r:F(v) for r,v in a['common_value_residual_on_entering_helpers']},'full forward residual')
   mutant=res.copy();r,v=a['witness'][0];add(mutant,rows[r],2*F(v));need(bool(set(mutant)&mains),'wrong sign rejected')
   out.append({'event':i,'terms':len(a['witness']),'dirty_residual_support':len(res),'example_dirty_input':min(res),'example_residual':str(res[min(res)])})
  op,r=e[:2]
  if op in ('INIT','CLEAR'):rows[r]={};frames[r]=e[2] if op=='INIT' else None
  elif op=='MOVE':need(frames[r]==e[2],'MOVE chart');frames[r]=e[3]
  elif op=='SCALE':rows[r]={k:F(e[2])*v for k,v in rows[r].items()}
  elif op in ('ADD','COPY'):
   need(r!=e[2] and frames[r]==frames[e[2]]==e[4],'source scalar chart')
   if op=='COPY':need(not rows[r],'full dirty-input COPY-zero')
   add(rows[r],rows[e[2]],F(e[3]))
 need(len(out)==10,'ten witnesses');a=next(x for x in out if x['event']==33272);need(a['dirty_residual_support']==1 and a['example_dirty_input']==749 and a['example_residual']=='1','input749 residual')
 return {'status':'PASS_INDEPENDENT_FULL_DIRTY_INPUT_FORWARD_REVIEW','native_sha256':PIN,'certificate_sha256':hashlib.sha256(cert.read_bytes()).hexdigest(),'public_columns':1480,'main_columns':400,'source_events':len(w['program']),'checked':out,'controls':['ten wrong-sign changes rejected','ten ordinaryvalue identities fail on purehelper residual','helper749 at33272 gives residual1'],'scope':'Exact source identities, not physical delta availability or supplier admission.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.source,a.certificate),indent=2))
