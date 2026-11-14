#!/usr/bin/env python3
"""Exact three-half elimination, ordinary codec binding and full tariff."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def word(*parts):
    st=[]
    for part in parts:
        for k,v in part:
            if k=='Q':
                v%=4
                if not v:continue
            if st and st[-1][0]==k and(k=='Q'or st[-1][1]==v):
                _,old=st.pop()
                if k=='Q'and(old+v)%4:st.append((k,(old+v)%4))
            else:st.append((k,v))
    return st
def inverse(w):return word([(k,-v if k=='Q'else v)for k,v in reversed(w)])
def Q(k=1):return word([('Q',k)])
def R(s,prime=False):return [('R',('Rprime'if prime else'R')+str(s))]
def Ap(s):return word(Q(),R(s))
def Am(s):return word(R(s,True),Q())
def transported_inverse(s,sign):
    return inverse(Am(s))if sign=='+'else word(Q(2),inverse(Ap(s)),Q(2))
def correction(s,t,left,right):
    b=Ap(t)if right=='+'else Am(t)
    return word(inverse(b),transported_inverse(s,left))
def N(s,prime=False):return word(Q(-1),R(s,prime),Q())
def C(s,t):return word(Q(-1),R(t,True),Q(2),R(s),Q())
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))for col in zip(*B)]for row in A]
def neg(A):return [[-x for x in row]for row in A]
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def inv(A):
    n=len(A);W=[list(map(F,row))+unit for row,unit in zip(A,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n)if W[i][j]);W[j],W[k]=W[k],W[j]
        c=W[j][j];W[j]=[x/c for x in W[j]]
        for i in range(n):
            if i!=j:
                c=W[i][j];W[i]=[x-c*y for x,y in zip(W[i],W[j])]
    return[row[n:]for row in W]
def blk(A,B,C,D):return[a+b for a,b in zip(A,B)]+[c+d for c,d in zip(C,D)]
def main(out,codec_path):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,s in pins.items():need(hashlib.sha256((HERE/p).read_bytes()).hexdigest()==s,'source pin '+p)
    codec=json.loads(codec_path.read_text());need(codec['status']=='PASS_LITERAL_ORDINARY_R0_CODEC','actual finite R service')
    half=json.loads((HERE/'source/HALF-PRICE.json').read_text());need(half['half_profile']=={'2':112,'3':112,'5':112,'6':112},'actual standalone half profile')
    table={}
    for signs in itertools.product('+-',repeat=2):
        a,b=signs
        if signs==('+','+'):expected=word(R(2),Q(2),R(1,True));kind='ordinary'
        elif signs==('+','-'):expected=word(N(2,True),Q(2),R(1,True));kind='one_Nprime'
        elif signs==('-','+'):expected=word(R(2),Q(2),N(1));kind='one_N'
        else:expected=C(1,2);kind='two_stage_C'
        need(correction(1,2,a,b)==expected,'universal source-bound correction table')
        table[a+b]={'kind':kind,'reduced_free_product_word':expected}
    orientations=[]
    for signs in itertools.product('+-',repeat=3):
        kinds=[table[''.join(signs[i:i+2])]['kind']for i in range(2)]
        orientations.append({'orientations':''.join(signs),'two_correction_kinds':kinds,'both_corrections_have_displayed_ordinary_form':kinds==['ordinary','ordinary']})
    need(sum(x['both_corrections_have_displayed_ordinary_form']for x in orientations)==1,'only plus plus plus has displayed ordinary corrections')
    a=[[F(1),F(1)],[F(0),F(1)]];b=[[F(1),F(0)],[F(2),F(1)]];f=[[F(2),F(1)],[F(1),F(1)]]
    D1=[[F(2),F(1)],[F(1),F(1)]];D2=[[F(1),F(2)],[F(0),F(1)]];D3=[[F(1),F(0)],[F(3),F(1)]]
    I=eye(2);Z=[[F(0)]*2 for _ in range(2)];U=lambda x:blk(I,x,Z,I);L=lambda x:blk(I,Z,x,I);delta=lambda x:blk(x,Z,Z,x)
    c=mm(mm(mm(inv(b),D1),inv(a)),inv(D1));e=mm(mm(mm(inv(f),D2),inv(b)),inv(D2))
    first=mm(delta(D1),U(a));middle=mm(delta(D2),L(neg(b)));last=mm(delta(D3),U(f))
    whole=mm(last,mm(blk(I,Z,Z,e),mm(middle,mm(blk(c,Z,Z,I),first))))
    Ey=mm(mm(mm(D3,D2),inv(b)),D1)
    Ex=neg(mm(mm(mm(mm(mm(D3,inv(f)),D2),inv(b)),D1),inv(a)))
    need(whole==blk(Z,Ey,Ex,Z),'all4 noncommuting arbitrary input columns')
    badc=mm(mm(mm(D1,inv(b)),inv(a)),inv(D1));bad=mm(last,mm(blk(I,Z,Z,e),mm(middle,mm(blk(badc,Z,Z,I),first))))
    bade=mm(mm(mm(D2,inv(f)),inv(b)),inv(D2));bad2=mm(last,mm(blk(I,Z,Z,bade),mm(middle,mm(blk(c,Z,Z,I),first))))
    need(bad!=whole and bad2!=whole,'wrong interstage correction orders rejected')
    terminal=word(Q(),Am(2));need(terminal==word(Q(2),N(2,True)),'exact first coded endpoint repair')
    def power(r):
        den=10**40;n=r**199*den**200;lo=0;hi=r*den+1
        while hi-lo>1:
            mid=(hi+lo)//2
            if mid**200<=n:lo=mid
            else:hi=mid
        need(lo**200<=n<(lo+1)**200,'fresh directed200th root');return F(lo,den),F(lo if lo**200==n else lo+1,den)
    def moment(profile):
        a=b=F(0)
        for r,c in profile.items():
            lo,hi=power(r);a+=c*(lo if c>=0 else hi);b+=c*(hi if c>=0 else lo)
        return a,b
    paid={2:336,3:336,5:336,6:336};room=moment({25:224,2:-336,3:-336,5:-336,6:-336});gate=power(224)
    need(room[0]>0 and gate[0]>room[1],'one modular unitary N or C exceeds optimistic room')
    result={'status':'PASS_EXACT_THREE_HALF_SOURCE_REDUCTION','source_pins':pins,'correction_table':table,'all8_orientations':orientations,
       'all_plus_c':'R2 Q^2 Rprime1','all_plus_e':'R3 Q^2 Rprime2','all_plus_endpoint_order':['G2^-1 Dtot y','-G3^-1 G2^-1 G1^-1 Dtot x'],
       'F_definition':'F_s=Q R_s','G_definition':'G_s=Rprime_s Q','all_plus_no_query_no_idle':True,
       'all_plus_source_profile':paid,'optimistic_unproved_target_profile':{25:224},'optimistic_room':[str(z)for z in room],
       'one_modular_unitary_service_moment_lower_bound':[str(z)for z in gate],'generic_noncommuting_control_all4_columns':True,
       'wrong_c_order_rejected':True,'wrong_e_order_rejected':True,'R0_codec_sha256':hashlib.sha256(codec_path.read_bytes()).hexdigest(),
       'ordinary_counts_excluding_child_lowering':{'half_boundary_port_monomials':2016,'interstage_route_monomials':896,
         'interstage_Q_squared_translations':224,'destination_sign_scalings':448,'R0_codec_calls':4,
         'R0_codec_ADD':4*codec['counts']['ADD'],'R0_codec_SCALE':4*codec['counts']['SCALE'],'R0_codec_SWAP':4*codec['counts']['SWAP']},
       'paid_half_moves':1344,'half_scalar_ADD':1344,'conservative_unfused_child_monomial_legs':2688,
       'scope':'Canonical three-half diagonal-correction template and modular full-unitary o(V)-ordinary services only. Coded endpoint is actual, proposed rank25 target is not achieved.','new_kappa':False}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print({'status':result['status'],'room':float(room[0]),'gate':float(gate[0])})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--codec',type=Path,default=HERE/'R0-CODEC.json');a=p.parse_args();main(a.output,a.codec)
