"""Direct, inverse-first and plane-by-plane checks of the root binary CRT."""
from collections import Counter
from functools import cache
from pathlib import Path
from random import Random
import json
import runpy
import sys

here = Path(__file__).resolve().parent
ff = runpy.run_path(str(here/"verify-fibre-join.py"))
radix = runpy.run_path(str(here/"verify-trace-shears.py"))
chirp = runpy.run_path(str(here/"verify-packed-chirp.py"))
fast = runpy.run_path(str(here/"verify-factor-directory.py"))
mul, power = ff["mul"], ff["power"]
divide, horner = ff["divmod_binary"], ff["field_poly_eval"]


def transpose(rows):
    return list(map(list,zip(*rows)))


def upper(rows):
    data = [row.copy() for row in rows]
    step = 1
    while step < len(data):
        for start in range(0,len(data),step*2):
            for j in range(start,start+step):
                data[j] = [x^y for x,y in zip(data[j],data[j+step])]
        step *= 2
    return data


def shear(data, scalar, slope, field):
    if scalar == 0:
        return data
    n = len(data)
    def rotate(row, pos):
        pos %= n
        return row[-pos:] + row[:-pos] if pos else row
    scales = [power(scalar,j,field) for j in range(n)]
    inv = power(scalar,2**(field.bit_length()-1)-2,field)
    unscales = [power(inv,j,field) for j in range(n)]
    rows = [rotate([mul(w,scales[j],field) for w in row],slope*j)
            for j,row in enumerate(data)]
    return [[mul(w,unscales[i],field) for w in rotate(row,-slope*i)]
            for i,row in enumerate(upper(rows))]


def chart(data, t, v, w, a, field, reverse=False):
    b = field.bit_length()-1
    inv = lambda z: power(z,(1 << b)-2,field)
    va, wa, ta = (power(x,a,field) for x in (v,w,t))
    lower, upper_scale = mul(va,inv(v),field), mul(w,inv(v),field)
    diag2 = wa ^ mul(lower,w,field)
    assert diag2 != 0
    ops = [('row',t,0),('col',ta,0),('col',lower,1),
           ('scale',v,diag2),('row',upper_scale,1)]
    for op,x,y in (reversed(ops) if reverse else ops):
        if op == 'scale':
            if reverse:
                x,y = inv(x),inv(y)
            xs,ys = ([power(z,i,field) for i in range(len(data))] for z in (x,y))
            data = [[mul(value,mul(xs[i],ys[j],field),field) for j,value in enumerate(row)]
                    for i,row in enumerate(data)]
        elif op == 'row':
            data = shear(data,x,y,field)
        else:
            data = transpose(shear(transpose(data),x,y,field))
    return data


def axis_eval(coeffs,g,field,backward=False):
    b=field.bit_length()-1
    if backward:
        folded=chirp['dft_chirp'](coeffs[:-1],g,field,b,inverse=True)
        return [coeffs[-1],*folded[1:],folded[0]^coeffs[-1]]
    folded=[coeffs[0]^coeffs[-1],*coeffs[1:-1]]
    return chirp['dft_chirp'](folded,g,field,b)+[coeffs[0]]


def apply_axes(rows,g,field,backward=False):
    rows = [axis_eval(row,g,field,backward) for row in rows]
    return transpose([axis_eval(row,g,field,backward) for row in transpose(rows)])


@cache
def shape(c):
    a=1 << c
    field,fs,pairs=ff['make_context'](c)
    b=3*c
    gamma=ff['normal'](b)
    sub=[gamma[i]^gamma[i+c]^gamma[i+2*c] for i in range(c)]
    elts=[ff['from_word'](i,sub) for i in range(a)]
    g=next(t for t in elts if t and len({power(t,j,field) for j in range(a-1)})==a-1)
    directions=[z^power(z,a,field) for z in (1 << i for i in range(b))]
    v=next(z for z in directions if z)
    w=next(z for z in directions if mul(v,power(z,a,field),field)!=mul(z,power(v,a,field),field))
    grid=[power(g,j,field) for j in range(a-1)]+[0]
    return a,field,fs,pairs,g,v,w,grid


def plane(values,t,c,backward=False):
    a,field,_,_,g,v,w,_=shape(c)
    h=a*a
    if backward:
        coeffs=apply_axes(values,g,field,True)
        wide=[row+[0]*a for row in coeffs]+[[0]*(2*a) for _ in range(a)]
        raw=chart(wide,t,v,w,a,field,True)
        out=[0]*(2*h)
        for i,row in enumerate(raw):
            for j,val in enumerate(row):
                if val:
                    assert i+j <= 2*a-2
                    out[i+a*j] ^= val
        assert not any(out[2*h-2*a+1:])
        for index,hi in enumerate(out[h:]):
            if hi:
                assert index+a < h
                out[index] ^= mul(hi,t,field)
                out[index+1] ^= hi
                out[index+a] ^= hi
        return out[:h]
    matrix=[[values[i+a*j] if i<a and j<a else 0 for j in range(2*a)]
            for i in range(2*a)]
    raw=chart(matrix,t,v,w,a,field)
    reduced=[[0]*a for _ in range(a)]
    for i,row in enumerate(raw):
        for j,val in enumerate(row):
            if val:
                assert i+j<=2*a-2
                reduced[i if i<a else i-a+1][j if j<a else j-a+1] ^= val
    return apply_axes(reduced,g,field)


@cache
def sites(c,t):
    a,field,_,_,_,v,w,grid=shape(c)
    return tuple(tuple(t ^ mul(v,y,field) ^ mul(w,z,field) for z in grid) for y in grid)


def small(c):
    a=1 << c
    field=ff['field_poly'](c)
    gen=chirp['primitive'](field)
    return field,gen,chirp['directory'](c,field,gen)


def forward(f,c,counts):
    a,field,fs,pairs,_,_,_,_=shape(c)
    h=a*a
    rows=radix['convert'](radix['unpack'](f,h,a),True)
    src=[sum(((row >> k)&1) << j for j,row in enumerate(rows)) for k in range(h)]
    sf,g,groups=small(c)
    smaller={u:[] for u in fs}
    for k in range(0,h,c):
        packet=chirp['packet_forward'](src[k:k+c],c,sf,g,groups)
        for u,rs in packet.items():
            smaller[u].extend(rs)
    by_factor={}
    ext=fast['Field'](3*c)
    assert ext.modulus==field
    for p in pairs:
        for t,u in ((p['t'],p['h0']),(p['t']^1,p['h1'])):
            A=[horner(r,t,field) for r in smaller[u]]
            values=plane(A,t,c)
            for ss,vs in zip(sites(c,t),values):
                for x,y in zip(ss,vs):
                    fac=ff['minpoly'](x,field)
                    # Independently recover the binary power-basis coefficients.
                    r=ff['coordinates'](y,ff['basis_pivots'](ff['power_columns'](x,fac.bit_length()-1,field)))
                    fast_fac,fast_r,_=fast['projected_remainder'](ext,x,y)
                    assert (fast_fac,fast_r)==(fac,r)
                    assert by_factor.setdefault(fast_fac,fast_r)==fast_r
                    counts['selected_root_values_checked'] += 1
    ordered=ff['fs_order'](3*c)
    assert set(ordered)==set(by_factor)
    return {u:by_factor[u] for u in ordered}


def backward(records,c,counts):
    a,field,fs,pairs,_,_,_,_=shape(c)
    h=a*a
    assert list(records)==ff['fs_order'](3*c)
    small_records={}
    ext=fast['Field'](3*c)
    assert ext.modulus==field
    for p in pairs:
        for t,u,pivots in ((p['t'],p['h0'],p['p0']),(p['t']^1,p['h1'],p['p1'])):
            grid=[[fast['compose'](ext,records[ff['minpoly'](x,field)],x) for x in row]
                  for row in sites(c,t)]
            A=plane(grid,t,c,True)
            child=[ff['coordinates'](z,pivots) for z in A]
            assert small_records.setdefault(u,child)==child
            counts['inverse_trace_planes'] += 1
    assert set(small_records)==set(fs)
    sf,g,groups=small(c)
    inputs=[]
    for k in range(0,h,c):
        packed={u:small_records[u][k:k+c] for u in fs}
        inputs.extend(chirp['packet_inverse'](packed,c,sf,g,groups))
    trace=[sum(((f >> j)&1) << k for k,f in enumerate(inputs)) for j in range(a)]
    return radix['pack'](radix['convert'](trace,False),h)


def main():
    rng=Random(0x7A01)
    count=Counter()
    if len(sys.argv)==1:
        degrees=(1,2,3,4)
    elif sys.argv[1:]==['--nonterminal-prefix']:
        degrees=(5,)
    else:
        raise SystemExit('Use no argument, or --nonterminal-prefix for the b=15 fixture.')
    for c in degrees:
        a,field,_,pairs,_,v,w,_=shape(c)
        q=a**3
        assert mul(v,power(w,a,field),field)!=mul(w,power(v,a,field),field)
        # This check is on arbitrary K-valued plane functions.
        t=pairs[-1]['t'] ^ 1
        values=[[rng.randrange(q) for _ in range(a)] for _ in range(a)]
        coeff=plane(values,t,c,True)
        for ss,vs in zip(sites(c,t),values):
            assert [chirp['evaluate'](coeff,x,field) for x in ss]==vs
        assert plane(coeff,t,c)==values
        count['arbitrary_K_grid_points']+=a*a
        root=ff['fs_order'](3*c)
        sample=rng.getrandbits(q)
        prefix,divs=radix['source_prefix'](sample,a)
        if c==5:
            assert len(divs)<c-1
        records=forward(radix['undo_source_prefix'](prefix,divs),c,count)
        assert records=={u:divide(sample,u)[1] for u in root}
        restored_sample=backward(records,c,count)
        assert restored_sample==sample and radix['source_prefix'](restored_sample,a)[0]==prefix
        count['source_prefix_blocks_restored']+=len(prefix)
        independent={u:rng.getrandbits(u.bit_length()-1) for u in root}
        restored=backward(independent,c,count)
        assert {u:divide(restored,u)[1] for u in root}==independent
        assert forward(restored,c,count)==independent
        count['full_independent_input_bits']+=q
        count['independent_inverse_FS1_bits']+=q
        count['root_Fs1_factors_each_direction']+=len(root)
        if c==1:
            for bit in range(q):
                column=forward(1 << bit,c,count)
                assert column=={u:divide(1 << bit,u)[1] for u in root}
                assert backward(column,c,count)==1 << bit
                count['entire_smallest_binary_basis']+=1
    print(json.dumps(dict(sorted(count.items())),indent=2))


if __name__=='__main__':
    main()
