"""Input-independent same-Reference geometry and bridge-port producer.
Source arithmetic is separately charged; no online payload is present.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from fractions import Fraction as Q
from halo_core_sources import need


def layout_for(shape):
    from core_layout import Layout
    active=tuple(k+shape.ell for k in shape.ks)
    lengths=tuple(reversed(active))+((shape.spectator_width,) if shape.spectator_width else ())
    return Layout(lengths,tuple(range(shape.g)),shape.ell)


def source_family(runtime,references,shape,archive,caps,interiors=None):
    """Family rows stay in halo/MSB order; retained Core reverses each row.

interiors=None uses the unmodified production Partition. Explicit tuples use
the validated admitted-partition adapter and do not establish production carve.
"""
    from core_roots import Partition
    from admitted_context import AdmittedPartition
    need(len(references)==len(caps)==len(archive.plans)==len(archive.source_ids)==shape.g,
         'one complete source and plan per halo axis')
    if interiors is not None:need(len(interiors)==shape.g,'complete admitted interior descriptors')
    for i,(ref,plan) in enumerate(zip(references,archive.plans)):
        need(ref.description_hash==archive.source_ids[i],'same immutable Core and halo source')
        need(ref.target_size==plan.period==1<<(shape.ks[i]+shape.ell),'same physical periodic axis')
        need(0<plan.gap<=ref.narrow_gap,'funded actual narrow source gap')
        need(plan.halfwidth>=2*ref.spec.source_halfwidth+2,
             'generic factory uses the inherited conservative physical source band')
        need(plan.period-shape.length>=plan.halfwidth,'ordinary complete principal window')
        need(plan.halo<=shape.halo<shape.boundary,'saved and kept row dependency margin')
        need(2*plan.data_width==shape.payload_width,'shared exact complex carrier')
    layout=layout_for(shape);family=[]
    for c in range(layout.labels):
        starts=layout.core_starts(c);row=[]
        for i,ref in enumerate(references):
            origin=starts[shape.g-1-i]
            if interiors is None:
                p=Partition(runtime,ref,'narrow',origin,shape.length,caps[i])
            else:
                p=AdmittedPartition(runtime,ref,'narrow',origin,shape.length,caps[i],interiors[i])
            p.validate();row.append(p)
        family.append(row)
    return layout,family


def bridge_values(plans,allocation):
    """Use one sum of all normalizer shifts, with one final rounded return."""
    need(plans,'nonempty active group')
    q,halo_width=plans[0].bits,plans[0].data_width
    need(all(p.bits==q and p.data_width==halo_width for p in plans),'common halo grid and carrier')
    P,width=allocation['P'],allocation['width'];U=sum(p.normalizer_shift for p in plans)
    need(P>=q and width>=halo_width+P-q,'complete exact input lift carrier')
    return halo_width,width,q,P,P+U-q


def prepare_bridge_counts(plans,allocation):
    from cardinal_counts import Count
    return tuple(Count.literal(value) for value in bridge_values(plans,allocation))


def admit_radii(n,Rin,Rhalo,allocation,plans):
    need(type(n) is int and n>=1 and Rin>=1 and Rhalo>=Rin,'whole-field radius domain')
    need(all(p.radius==Rhalo for p in plans),'shared halo input/output carrier radius')
    need(all((1<<p.normalizer_shift)*p.gap>=1 for p in plans),'normalized section contractions')
    need(allocation['R0']**2>=(1<<n)*Rin**2,'all contexts and spectators in Core radius')
    epsilon=Q(1,1<<allocation['target']);U=sum(p.normalizer_shift for p in plans);A=1<<U
    need(Rhalo>=Rin+2*epsilon/A,'actual rounded normalized Core output carrier')
    return dict(records=1<<n,input_radius=Rin,carrier_radius=Rhalo,
                normalizer=A,core_error=str(epsilon),normalizer_shift_sum=U)
