from pathlib import Path
import json
import sympy as s

# Actual spectral sign points for seven independent sqrt-translation axes.
points=[]
for eta in [0,1,2,4,8,16,32,64,3,127]:
 translations=[(-1)**(2*(eta&w).bit_count()) for w in range(128)]
 gaussian=s.I**(2*eta.bit_count())
 assert set(translations)=={1}
 assert gaussian==(-1)**eta.bit_count()
 points.append({'duplicated_frequency':eta,'body_gaussian_sign':int(gaussian),'all128_collective_translations':1})
assert (-1)**(1&1).bit_count()!=(-1)**(0&1).bit_count()
# An independent noncommutative matrix control of the source tag identity.
I=s.eye(4);P=s.diag(1,1,0,0)
N=s.Matrix([[2,3,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,1]])
assert P*(N-I)==N-I and (N-I)*P==N-I
A=s.Matrix([[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1]])
U=s.Matrix([[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
plus=U*N*A;minus=U*(I-2*P)*N*A
assert minus*plus.inv()==U*(I-2*P)*U.inv()
actual=(I-minus*plus.inv())/2
assert actual.rank()==2 and actual**2==actual
assert actual!=s.diag(1,0,0,0) # A claimed one-recipient fission loses tag rank.
assert actual!=P # Ordinary mixing does not make the tag a coordinate projector.
# A legitimate routing/control instance with a genuinely bodyless selected row.
W=s.Matrix([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])
Q=s.diag(3,1,1,1);targetP=Q*W*P*W.inv()*Q.inv()
assert targetP==s.diag(0,1,1,0)
E=s.Matrix([[1,0,0,0],[0,0,0,1]])
assert E*targetP==s.zeros(2,4)
assert E*Q*W*N==E*Q*W
assert E*Q*W*P==s.zeros(2,4)
out={'status':'PASS_INDEPENDENT_FRESH_BODY_TAG_CONTROLS','engine':'integer spectral points and exact SymPy rational matrices','sign_points':points,'tag_identity_rank':int(actual.rank()),'bodyless_native_deletion_control':True,'negative_controls':{'per_column_translation_scope_extension_rejected':True,'incorrect_one_recipient_tag_rejected':True,'arbitrary_mixing_not_automatically_endpoint_diagonal':True},'scope':'finite controls supplement universal tag, query-only kernel and concavity proof; no circuit search or general multiplication lower bound','no_new_kappa':True}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
