"""Join the two S028 trees, while preserving the genuine common 35 input fields."""
import numpy as np

def attachments(icore,zo,terms,lane):
    protected={0,1,5}
    allowed={i for i in icore if zo[i]==7 and set(lane[64*terms[i,10][0]:64*(1+terms[i,10][0])])<=protected}
    if allowed!={3,27,38,81,84,88}:raise ValueError('native aperture-constrained anchor cover')
    return allowed

def connect(inputs,outputs,assigned,leaves,allowed,jcore,icore,adj,no):
    a=min(allowed);j=min(adj[a] & jcore)if isinstance(adj[a],set)else min(set(adj[a])&jcore)
    if (a,j)in assigned:raise ValueError('native bridge must join the two previous trees')
    Y=inputs[j]+[('B',a,j,False)]+outputs[a];A=[('T',a,10,False)]
    F=A+Y+no(A)
    def conjugate(i):
        t=[('T',i,10,False)];return no(t)+F+t
    inputs[10]=F
    for i,k,kind in leaves:
        if kind=='source':inputs[k]=conjugate(i)+inputs[k]
    for i in icore:outputs[i]=outputs[i]+no(conjugate(i))
    assigned.add((a,j));leaves.append([a,j,'bridge']);return a,j
def probes(i,icore,terms,lane):
    excluded={0,1,5}
    if i in icore:
        k=terms[i,10][0];excluded.update(map(int,lane[64*k:64*(k+1)]))
    return sorted(set(range(8))-excluded)
