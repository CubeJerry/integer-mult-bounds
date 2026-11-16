#!/usr/bin/env python3
"""Fixed nontrivial continuation: real unknown read, ground-Y preload and Hub inverse."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,chart,replay,require
from ground_output_normalization import evaluate
from price_projection import moment,record
OLD='cc505aaf4aee5e1995b4db22f9b53609856d3ecdc3ea1eb0797f2584e375dfee'
NEW='60c6f8820eefe232ee6c8f5b348be21bd86bb42c13532054fc2548b784cd2da7'
def save(p,z):
 raw=(json.dumps(z,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 for n in ['work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();op=a.work/'A/ascending-canonical3/WORD.json';np=a.work/'C/canonical3-reset-source/MATCHED-CUT-WORD.json';require(hashlib.sha256(op.read_bytes()).hexdigest()==OLD and hashlib.sha256(np.read_bytes()).hexdigest()==NEW,'frozen source pins')
 old,new=json.loads(op.read_text()),json.loads(np.read_text());_,ot,_=replay(old,collect=True);_,nt,_=replay(new,collect=True);oc,nc=old['carrier_interface_before_operation'],new['carrier_interface_before_operation'];ov,oa=ot[oc];nv,na=nt[nc];C={n:chart(z)for n,z in old['charts'].items()}
 group='ASC_GROUP_4';known='H4_1';raw0='CANONICAL_RESET_RAW_0';S=new['targets'];sm=sum(1<<i for i in S)
 require(oa['X27']==na['X27']=='L27'and C[oa[group]]==C[na[group]]==C[oa[known]]==C[na[known]]==C['F4'],'actual cocharted collector opportunity')
 require(ov[known]==1<<6 and nv[known]==0 and ov[group]==nv[group]and not(ov[group]>>27&1),'nontrivial pure-known reset difference beside actual unknown group')
 donors=[i for i in range(N)if ov[group]>>i&1];require(len(donors)==5 and 6 not in donors,'actual unknown correction donors')
 fixed=[['MOVE','X27','F4'],['ADD',group,'X27'],['ADD',known,'X27'],['MOVE','X27','Hub'],['ADD','ZRAW0','Y13'],['ADD',raw0,'Y13']]
 fixed += [z for z in old['operations'][oc:]if z!=['MOVE','X27','Hub']]
 fixed += [['ADD',f'X{i}','X27']for i in donors+[6]]
 # The old legal source gets three genuine native-to-ground known copies.
 prep=[]
 for i in [0,61,67]:prep += [['INIT',f'CANONICAL_RESET_RAW_{i}',f'L{i}'],['ADD',f'X{i}',f'CANONICAL_RESET_RAW_{i}'],['MOVE',f'CANONICAL_RESET_RAW_{i}','zero']]
 oldprefix=prep+old['operations'][:oc]+[['ADD','CANONICAL_RESET_RAW_61','Y61'],['ADD','CANONICAL_RESET_RAW_67','Y67']]
 oldextra=[f'CANONICAL_RESET_RAW_{i}'for i in [0,61,67]]
 def shell(ops,cut,label):
  z={k:copy.deepcopy(new[k])for k in ['source_path','source_sha256','charts']};z.update(schema='canonical3-nontrivial-fixed-continuation-control-v1',operations=ops,targets=S,released_carriers=new['released_carriers'],carrier_interface_before_operation=cut,scope=label);return z
 ow=shell(oldprefix+fixed+[['CLEAR',n]for n in oldextra],len(oldprefix),'Old source with three paid ground copies; fixed continuation restores every X and completes the same48 targets.')
 os,otr,_=replay(ow,collect=True);oldcut=otr[len(oldprefix)]
 # Initial ground preloading occurs after actual raw0 acquisition and before any Y-dependent source work.
 newprefix=copy.deepcopy(new['operations'][:nc]);idx=newprefix.index(['MOVE',raw0,'zero'])+1;newprefix.insert(idx,['ADD',raw0,'Y13'])
 oldowned={z[1]for z in old['operations']if z[0]=='INIT'};newowned={z[1]for z in new['operations']if z[0]=='INIT'};extra=sorted(newowned-oldowned);require(len(extra)==105,'actual105 extra raw source/native records')
 repair=[['ADD','X6','X27']]
 nw=shell(newprefix+fixed+repair+[['CLEAR',n]for n in extra],len(newprefix),'Matched actual known48 source, same literal continuation, real groundY13x0 preparation and real one-ADD Hub inverse.')
 ns,ntr,_=replay(nw,collect=True);newcut=ntr[len(newprefix)]
 for n,z in oldcut[0].items():require(n in newcut[0]and(newcut[0][n]^z)&~sm==0 and C[newcut[1][n]]==C[oldcut[1][n]],('every old named unknown/Y column and chart',n))
 before_inverse=len(newprefix)+len(fixed);require(ntr[before_inverse][0]['X27']==(1<<27)^(1<<6)and ntr[before_inverse][1]['X27']=='Hub','actual nonidentity reset X map')
 require(nw['operations'][len(newprefix):before_inverse]==ow['operations'][len(oldprefix):len(oldprefix)+len(fixed)]==fixed,'same literal fixed continuation')
 controls=[]
 for label,event in [('omit actual initial groundY preload',['ADD',raw0,'Y13']),('omit actual Hub inverse',['ADD','X6','X27'])]:
  bad=copy.deepcopy(nw)
  k=bad['operations'].index(event)if label.startswith('omit actual initial')else len(newprefix)+len(fixed)
  require(bad['operations'][k]==event,'negative control exact event');bad['operations'].pop(k)
  if k<bad['carrier_interface_before_operation']:bad['carrier_interface_before_operation']-=1
  values,locations,_,_=evaluate(bad)
  expected={'Y13':(1<<(N+13))^(1<<0)}if label.startswith('omit actual initial')else{'X27':(1<<27)^(1<<6)}
  for n,z in expected.items():require(values[n]==z,'isolated omitted correction residual')
  for i in range(N):
   for n,z in [(f'X{i}',1<<i),(f'Y{i}',(1<<(N+i))^((1<<i)if i in S else 0))]:
    if n not in expected:require(values[n]==z,'no other residual in isolated negative control')
  try:replay(bad)
  except ValueError as e:controls.append({'control':label,'rejected':str(e),'isolated_residual':expected})
  else:raise ValueError('invalid control accepted')
  if label.startswith('omit actual initial'):unprepared=bad
 a.out.mkdir(parents=True,exist_ok=True);pins={'OLD-CONTROL-WORD':save(a.out/'OLD-CONTROL-WORD.json',ow),'RESET-CONTROL-WORD':save(a.out/'RESET-CONTROL-WORD.json',nw),'MISSING-PRELOAD-WORD':save(a.out/'MISSING-PRELOAD-WORD.json',unprepared)}
 result={'status':'PASS_ACTUAL_CANONICAL3_NONTRIVIAL_FIXED_CONTINUATION','source_old_sha256':OLD,'source_new_sha256':NEW,'word_pins':pins,'old_stats':os,'new_stats':ns,'old_cut':len(oldprefix),'new_cut':len(newprefix),'literal_fixed_continuation':fixed,'actual_unknown_group_donors':donors,'known_proper_difference':{'H4_1':'x6'},'actual_groundY_preload':'Y13 += actual raw x0 before every Y-dependent prefix operation','reset_X_map_before_repair':'X27=x27+x6; all other X raw','actual_Hub_inverse':repair,'old_whole_moment':record(moment(os['movement_profile'])),'reset_whole_moment':record(moment(ns['movement_profile'])),'controls':controls,'scope':'Actual unknown proper data read in a native original, same fixed continuation, matched unknown/Y cut columns, real nontrivial invertible-X Hub repair and actual ground source preload. All48 known outputs and all222 columns. Five global foundations remain open; no all111 or kappa.'}
 save(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in ['status','word_pins','old_stats','new_stats','reset_whole_moment']},indent=2))
if __name__=='__main__':main()
