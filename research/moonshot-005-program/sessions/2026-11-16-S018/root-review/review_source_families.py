#!/usr/bin/env python3
"""Independent current-source and six-formal-mask verification."""
from pathlib import Path
import argparse,hashlib,json
from optimize_word import independent_replay
def trace(w,inject=None):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};ss=[]
 for k,(op,n,*q)in enumerate(w['operations']):
  if inject and k in inject:
   for dst,row in inject[k]:v[dst]^=row
  ss.append((v.copy(),at.copy()))
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='MOVE':at[n]=q[0]
  elif op=='CLEAR':del v[n],at[n]
 return ss,(v,at)
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','hub','family','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();prog=a.repo/'research/moonshot-005-program';base=prog/'results/bit-canonical-mask-source/author/early-paid46/WORD.json';old=json.loads(base.read_bytes());hub=json.loads(a.hub.read_bytes());fam=json.loads(a.family.read_bytes());assert hashlib.sha256(base.read_bytes()).hexdigest()=='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
 hs,_=trace(hub);fs,_=trace(fam)
 for w in [old,hub,fam]:independent_replay(w)
 assert sorted(o for o in old['operations']if o[0]=='MOVE')==sorted(o for o in hub['operations']if o[0]=='MOVE')
 cuts=[];fields=['KEEP_C0','KEEP_C1','KEEP_C2','ZFIRST3','ZFIRST4','ZFIRST5'];readers=[[3,21],[76,64],[80,65],[4],[74],[78]];inject={};caps=[]
 for j in range(6):
  packet=f'P{j}';start=next(k for k,o in enumerate(hub['operations'])if o[0]=='ADD'and o[2]==packet and hs[k][1][packet]=='Hub');v,at=hs[start];assert all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111));cuts.append(start);inject[start]=[(packet,1<<(222+j))]
  cap=hub['operations'].index(['ADD',packet,fields[j]]);caps.append(cap);assert hub['operations'][cap+1]==['ADD',fields[j],packet];assert not any(o[0]=='ADD'and o[1]==packet for o in hub['operations'][start:cap])
 ms,mfinal=trace(hub,inject)
 for j in range(6):
  marker=1<<(222+j);assert ms[caps[j]+1][0][fields[j]]&marker
  affected=[i for i in range(111)if mfinal[0][f'Y{i}']&marker];assert sorted(affected)==sorted(readers[j]);assert not any(mfinal[0][f'X{i}']&marker for i in range(111))
 assert all(not o[1].startswith('Y')for o in hub['operations']if o[0]=='ADD')
 live=next(k for k,o in enumerate(fam['operations'])if o[0]=='CLEAR');fv,fa=fs[live]
 for j,rec in enumerate(fam['arbitrary_first_retentions']):
  assert fv[fields[j]]==int(rec['new_row_hex'],16);assert rec['readers']==readers[j];assert rec['old_row_hex']==hex(hs[caps[j]][0][f'P{j}']);assert int(rec['mask_hex'],16)==int(rec['old_row_hex'],16)^int(rec['new_row_hex'],16);assert rec['donors']==[f'X{i}'for i in range(111)if int(rec['mask_hex'],16)>>i&1]
 out={'status':'PASS_ROOT_SNAPSHOT_SOURCE_AND_UNIVERSAL_SIX_MASK_REVIEW','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'hub_word_sha256':hashlib.sha256(a.hub.read_bytes()).hexdigest(),'family_word_sha256':hashlib.sha256(a.family.read_bytes()).hexdigest(),'all111_raw_Hub_cuts':cuts,'formal_independent_mask_columns':6,'complete_symbolic_columns':228,'first_retention_fields':fields,'exact_mask_endpoint_sensitivities':readers,'no_original_mask_contamination':True,'movement_multiset_unchanged_for_Hub_release':True,'arbitrary_family_bits':666,'new_complete_kappa':False,'scope':'Actual native words and universal linear mask identity; width lifting uses fixed binary operations. No shared delivery to unfinished receivers or full supplier.'};a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
