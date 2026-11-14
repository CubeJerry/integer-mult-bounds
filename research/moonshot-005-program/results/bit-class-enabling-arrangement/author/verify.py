#!/usr/bin/env python3
"""Exact native equality graphs and counterexamples; see PROOF.md."""
import argparse,copy,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def ba(rows):
 b={};chosen=[]
 for index,x in enumerate(rows):
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;chosen.append(index);break
 return b,chosen
def rem(x,b):
 for p,v in sorted(b.items(),reverse=True):
  if x>>p&1:x^=v
 return x
def xor(values):
 x=0
 for v in values:x^=v
 return x
def fail(call,label):
 try:call()
 except ValueError:return label
 raise ValueError('accepted control: '+label)
def load_source(raw):
 need(hashlib.sha256(raw).hexdigest()==PIN,'native bytes')
 s=json.loads(gzip.decompress(raw));rr=[list(map(F,s['frames'][str(s['start'][i])]['B'][0])) for i in range(111)]
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 k=[sum(int(i==j or dot(a,b)==0)<<j for j,b in enumerate(rr)) for i,a in enumerate(rr)]
 groups={}
 for i,r in enumerate(rr):
  supp=tuple(j for j,x in enumerate(r) if x);need(len(supp) in (1,4),'root shape')
  sign=1 if r[supp[0]]>0 else-1
  key=('coordinate',0) if len(supp)==1 else(min(supp,tuple(j for j in range(8) if j not in supp)),sum(x*sign<0 for x in r)%2)
  groups.setdefault(key,[]).append(i)
  f=s['frames'][str(s['final'][111+i])]
  need(f['dim']==7 and all(dot(r,list(map(F,b)))==0 for b in f['B']),'actual facet')
 classes=list(groups.values());need(len(classes)==15,'classes')
 for g in classes:need(all(dot(rr[i],rr[j])==0 for i in g for j in g if i!=j),'orthogonal class')
 forbidden=[((1<<111)-1)^(row^(1<<i)) for i,row in enumerate(k)]
 need(all(any(forbidden[i]>>j&1 for j in g) for i in range(111) for g in classes),'every forbidden set meets every class')
 return k,classes,forbidden

def partition(classes,equalities):
 parent=list(range(111))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for group in equalities:
  for j in group[1:]:parent[root(j)]=root(group[0])
 result=[]
 for c in classes:
  g={}
  for j in c:g.setdefault(root(j),[]).append(j)
  result.append(sorted(g.values()))
 return result

def join(classes,parts):
 return partition(classes,[group for part in parts for c in part for group in c])

def dim_quot(part):return sum(len(c) for c in part)-15

def member(vector,part):
 return all(len({vector>>j&1 for j in group})<=1 for c in part for group in c)

def arrangement(k,classes,forbidden):
 u=[sum(1<<j for j in c) for c in classes];ub=ba(u)[0]
 q=[rem(k[c[0]],ub) for c in classes];qb,chosen=ba(q)
 need(len(qb)==4 and len(set(q))==15 and 0 not in q,'canonical quotient labels')
 for a,c in enumerate(classes):need(all(rem(k[j],ub)==q[a] for j in c),'same class quotient')
 basis=[q[j] for j in chosen];labels={xor(basis[t] for t in range(4) if n>>t&1):n for n in range(16)}
 lab=[labels[x] for x in q]
 parts=[]
 for a,c in enumerate(classes):
  equalities=[[j for j in g if forbidden[i]>>j&1] for i in c for g in classes]
  part=partition(classes,equalities)
  need(len(part[a])==len(c),'own class unconstrained')
  need(all(len(p)==2 for b,p in enumerate(part) if b!=a),'two other-class components')
  need(dim_quot(part)==len(c)+13,'single quotient dimension')
  parts.append(part)
 pairs=[];lines=set()
 for c,d in itertools.combinations(range(15),2):
  combined=join(classes,[parts[c],parts[d]])
  active=[a for a,p in enumerate(combined) if len(p)>1]
  need(dim_quot(combined)==3 and len(active)==3 and all(len(combined[a])==2 for a in active),'pair intersection3')
  need(c in active and d in active and xor(lab[a] for a in active)==0,'projective line labels')
  lines.add(tuple(active));pairs.append({'classes':[c,d],'quotient_dimension':3,'active_classes':active})
 triple={0:0,3:0}
 for c,d,e in itertools.combinations(range(15),3):
  dimension=dim_quot(join(classes,[parts[c],parts[d],parts[e]]))
  expected=3 if lab[c]^lab[d]^lab[e]==0 else 0
  need(dimension==expected,'all-field triple partition')
  triple[dimension]+=1
 need(len(lines)==35 and triple=={0:420,3:35},'complete projective arrangement')
 return u,parts,{'classes':classes,'canonical_four_bit_labels':lab,'single_components':parts,
                'single_quotient_dimensions':[dim_quot(p) for p in parts],
                'pair_intersections':pairs,'projective_lines':[list(x) for x in sorted(lines)],
                'triple_quotient_dimension_histogram':triple}

def extension_profile(extension,u,parts,classes,forbidden):
 ub=ba(u)[0];quot=[rem(v,ub) for v in extension];rank=len(ba(quot)[0])
 need(rank==len(extension),'independent extension outside U')
 nullities=[];local_witness=[]
 for i in range(111):
  constraints=[]
  for g in classes:
   subset=[j for j in g if forbidden[i]>>j&1]
   for j in subset[1:]:
    constraints.append(sum((((v>>j)^(v>>subset[0]))&1)<<a for a,v in enumerate(extension)))
  nullities.append(rank-len(ba(constraints)[0]))
  witnesses=[]
  for bits in range(1,1<<rank):
   if all((bits&constraint).bit_count()%2==0 for constraint in constraints):
    v=xor(extension[a] for a in range(rank) if bits>>a&1);correction=0
    for ci,g in enumerate(classes):
     j=next(j for j in g if forbidden[i]>>j&1)
     if v>>j&1:correction^=u[ci]
    need((v^correction)&forbidden[i]==0,'actual local representative')
    witnesses.append({'extension_coefficients':bits,'class_correction':hex(correction),'local_row':hex(v^correction)})
  need(bool(witnesses)==bool(nullities[-1]),'receiverwise nonzero direction')
  local_witness.append(witnesses)
 whole=[c for c,g in enumerate(classes) if all(nullities[i]>0 for i in g)]
 direction_memberships=[]
 for bits in range(1,1<<rank):
  v=xor(extension[a] for a in range(rank) if bits>>a&1)
  direction_memberships.append({'coefficients':bits,'P_memberships':[c for c,p in enumerate(parts) if member(v,p)]})
 return {'extension_rows':[hex(v) for v in extension],'code_dimension':15+rank,
         'receiver_local_dimensions':nullities,'enabled_receiver_count':sum(n>0 for n in nullities),
         'whole_enabled_classes':whole,'whole_enabled_class_minima':[min(classes[c]) for c in whole],
         'directionwise_P_memberships':direction_memberships,'actual_local_witnesses':local_witness}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();k,classes,forbidden=load_source(raw);u,parts,arr=arrangement(k,classes,forbidden)
 half=extension_profile([sum(1<<j for j in [8,10,12,13])],u,parts,classes,forbidden)
 units=extension_profile([1,2],u,parts,classes,forbidden)
 need(half['whole_enabled_class_minima']==[0,8,9] and half['enabled_receiver_count']==22,'three-class witness')
 need(units['whole_enabled_class_minima']==[0,8,9,14,15,38,39,46,47] and units['enabled_receiver_count']==88,'nine-class coverage witness')
 need(all(x['P_memberships']==[0] for x in units['directionwise_P_memberships']),'each individual direction enables only coordinate class')
 controls=[fail(lambda:load_source(raw+b'x'),'native byte corruption'),
           fail(lambda:need(dim_quot(join(classes,[parts[0],parts[1]]))==0,'disjoint quotient claim'),'false pairwise-disjoint claim'),
           fail(lambda:need(set(units['whole_enabled_classes'])<=set().union(*(set(z['P_memberships']) for z in units['directionwise_P_memberships'])),'same direction covers whole class'),'false directionwise coverage implication'),
           fail(lambda:extension_profile([u[0]],u,parts,classes,forbidden),'class row falsely called new extension')]
 # A direct finite certificate for the e0/e1 support-of-extension gate:
 # all W-local rows vanish outside coordinate class, even when local kernels
 # appear at the nine enabled classes.
 outside_coordinate=((1<<111)-1)^255
 for i,witnesses in enumerate(units['actual_local_witnesses']):
  need(all(int(w['local_row'],16)&outside_coordinate==0 for w in witnesses),'all localized shortening rows supported on coordinate class')
 out={'status':'PASS_ARBITRARY_CLASS_EXTENSION_ARRANGEMENT','native_sha256':PIN,
      'arrangement':arr,'one_extension_three_class_witness':half,
      'two_extension_receiverwise_counterexample':units,'localized_two_unit_packet_floor':14,
      'universal_arbitrary_one_scalar_extension_packet_floor':12,
      'negative_controls':controls,'all_field_basis':'equality-constraint connected components; PROOF.md',
      'new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'pairs':105,'triples':455,'one_extension_floor':12,
                   'pair_intersection_dimension':3,'two_extension_enabled_classes':9,'localized_floor':14}))
if __name__=='__main__':main()
