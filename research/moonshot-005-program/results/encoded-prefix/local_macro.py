"""Exact six-input proof witness for the first changed-main coding macro."""
from fractions import Fraction as F
import json

def plus(a,b,c=1):
 for j,x in b.items():
  y=a.get(j,F(0))+c*x
  if y:a[j]=y
  else:a.pop(j,None)
def run():
 labels=['Ua','Va','Ud','Vd','B','C'];r={a:{i:F(1)} for i,a in enumerate(labels)};program=[]
 def add(a,b,c=1):program.append(['ADD',a,b,str(c),3]);plus(r[a],r[b],F(c))
 add('Va','Ua',-1);add('Vd','Ud',-1)
 for a,b,c in [('Ua','B',1),('B','Ua',-1),('Ua','B',1),('B','C',1),('C','B',-1),('B','C',1),('C','Ud',1),('Ud','C',-1),('C','Ud',1)]:add(a,b,c)
 add('Va','Vd');add('Vd','Va',-1);add('Va','Vd');add('Va','Ua');add('Vd','Ud')
 expected={'Ua':{4:F(1)},'Va':{4:F(1),2:F(-1),3:F(1)},'Ud':{0:F(-1)},'Vd':{1:F(-1)},'B':{5:F(1)},'C':{2:F(1)}}
 if r!=expected or len(program)!=16:raise ValueError('macro identity')
 inverse={}
 for i,expression in enumerate([{'Ud':-1},{'Vd':-1},{'C':1},{'Va':1,'Ua':-1,'C':1},{'Ua':1},{'B':1}]):
  row={}
  for a,c in expression.items():plus(row,r[a],F(c))
  if row!={i:F(1)}:raise ValueError('inverse identity')
  inverse[str(i)]=expression
 return {'status':'PASS_EXACT_CHANGED_MAIN_LOCAL_MACRO','source_events':[5617,5625],'roles':{'a':203,'b':498,'c':572,'d':221},'adds':16,'moves':0,'new_owned':0,'program':program,'output_rows':{a:[[i,str(c)] for i,c in sorted(row.items())] for a,row in r.items()},'inverse':inverse,'scope':'All six independent input arrays, cochart3; illustrative macro, not spliced into prefix transcript.'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
