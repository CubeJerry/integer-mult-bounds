"""Independent local-scan review; author hardware, Count and oracles unused.
Small integer Count substitutes are observation metadata, not a production
implementation or evidence for inherited Count cost bounds.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import ast
import hashlib
import json
import sys
from contextlib import contextmanager
from pathlib import Path

def need(value, message):
    if not value:
        raise ValueError(message)

class Tape:
    def __init__(self, body=(), origin=7):
        self.origin = self.head = origin
        self.cells = {origin - 1: 2}
        self.cells.update({origin + i: x for i, x in enumerate(body)})
        self.reads = self.writes = self.moves = 0
    def read(self):
        self.reads += 1
        return self.cells.get(self.head, 4)
    def write(self, value):
        need(value in range(14), 'fixed alphabet'); self.writes += 1
        if value == 4: self.cells.pop(self.head, None)
        else: self.cells[self.head] = value
    def step(self, direction):
        need(direction in (-1, 1), 'unit move'); self.moves += 1
        self.head += direction
        need(self.head >= self.origin - 1, 'ancestor crossed')
    def append(self, value):
        need(self.read() == 4, 'empty append'); self.write(value); self.step(1)
    def rewind(self):
        self.step(-1)
        while self.read() != 2: self.step(-1)
        self.step(1)
    def clear(self):
        self.rewind()
        while self.read() != 4: self.write(4); self.step(1)
        self.rewind()
    def observed(self):
        out = []; pos = self.origin
        while self.cells.get(pos, 4) != 4: out.append(self.cells[pos]); pos += 1
        return out
    @property
    def actions(self): return self.reads + self.writes + self.moves

@contextmanager
def owned(*values): yield values

class Count:
    @staticmethod
    def literal(value):
        need(type(value) is int and value >= 0, 'observer metadata'); return value

def subtract(a, b):
    need(a >= b, 'nonnegative difference'); return a - b

def bit(source, target=None):
    value = source.read(); need(value in (0, 1), 'payload bit')
    if target is not None: target.append(value)
    source.step(1); return value

def copy_bits(source, target, length):
    for _ in range(length): bit(source, target)

NAMES = ('convert_word', 'convert_field', 'increment_address',
         'copy_context_payload', 'copy_catalogue_frame')

def load(path, replacement=None):
    source = path.read_text()
    if replacement:
        before, after = replacement
        need(source.count(before) == 1, 'unique mutation target')
        source = source.replace(before, after)
    bodies = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    need(tuple(n.name for n in bodies) == NAMES, 'exact named review functions')
    program = ast.Module(body=bodies, type_ignores=[])
    namespace = dict(Count=Count, owned=owned, subtract=subtract,
        compare=lambda a,b: (a>b)-(a<b), positive=lambda n: need(n>0,'positive width'),
        indices=range, bit=bit, copy_bits=copy_bits, need=need,
        BLANK=4, RIGHT=3, PART_END=5, BLOCK_START=6, BLOCK_END=7, FRAME_END=8)
    exec(compile(program, str(path), 'exec'), namespace)
    digest = hashlib.sha256(ast.dump(program, include_attributes=False).encode()).hexdigest()
    return namespace, digest

def encode(value, width): return [(value >> j) & 1 for j in range(width)]
def signed(bits):
    value = sum(b << j for j,b in enumerate(bits))
    return value - (1 << len(bits)) if bits[-1] else value
def rejection(call):
    try: call()
    except ValueError: return True
    return False

def check(path):
    n, source_digest = load(path)
    conversions = invalid = 0; receipt = hashlib.sha256()
    for before in range(1, 11):
        for after in range(1, 12):
            for value in range(-(1 << (before-1)), 1 << (before-1)):
                source, target = Tape(encode(value, before)), Tape()
                valid = -(1 << (after-1)) <= value < 1 << (after-1)
                if not valid:
                    need(rejection(lambda: n['convert_word'](source,target,before,after)),
                         'nonredundant signed bits rejected')
                    invalid += 1; continue
                n['convert_word'](source,target,before,after)
                actual = target.observed()
                need(len(actual)==after and signed(actual)==value, 'independent signed value')
                need(source.head==source.origin+before, 'exact consumed extent')
                receipt.update(bytes(actual)); conversions += 1
    field_cases = 0
    for records in (1,3,7):
        for before,after in ((3,8),(8,3),(7,7)):
            values = [((j*5+2)%7)-3 for j in range(2*records)]
            source,target = Tape([b for x in values for b in encode(x,before)]),Tape()
            n['convert_field'](source,target,before,after)
            actual = target.observed()
            need([signed(actual[i:i+after]) for i in range(0,len(actual),after)]==values,
                 'complete ordered real/imaginary field')
            field_cases += 1
    address_cases = context_cases = 0; max_ratio = (0,1)
    for g,m in ((1,1),(1,5),(2,1),(2,3),(3,2),(4,2)):
        total = 1 << (g*m); address = Tape([0]*(g*m))
        for j in range(total):
            need(address.observed()==encode(j,g*m), 'literal LSF local coordinate')
            ended = n['increment_address'](address)
            need(ended==(j+1==total), 'exact final carry')
        address_cases += 1
        for width in (1,3,11):
            for contexts in (1,3,5):
                size = 2*width*total
                payload = [int(((i*13+i//7+i//size*5)%19)<9) for i in range(contexts*size)]
                source,odometer = Tape(payload),Tape(); joined = []
                for c in range(contexts):
                    target = Tape(); start = odometer.actions
                    n['copy_context_payload'](source,target,odometer,g,m,width)
                    cost = odometer.actions-start
                    need(cost<=64*(total+g*m+1), 'amortized address head travel')
                    if cost*max_ratio[1] > max_ratio[0]*(total+g*m+1):
                        max_ratio = (cost,total+g*m+1)
                    need(target.observed()==payload[c*size:(c+1)*size], 'complete context direct offsets')
                    need(not odometer.observed() and odometer.head==odometer.origin, 'address retired')
                    joined += target.observed()
                need(joined==payload and source.read()==4, 'all contexts reassembled')
                context_cases += 1
    frames = ([6,0,1,5,1,0,3,7],[6,1,1,0,5,7],[6,0,5,7])
    source = Tape([v for frame in frames for v in (*frame,8)])
    for frame in frames:
        target = Tape(); n['copy_catalogue_frame'](source,target)
        need(target.observed()==list(frame) and target.head==target.origin, 'exact frame transport')
    need(source.read()==4, 'all frames consumed')
    need(rejection(lambda:n['copy_catalogue_frame'](Tape([6,0,5,7]),Tape())), 'absent frame delimiter')
    bad,_ = load(path,("need(bit(source)==sign,'exact signed carrier shrink')","bit(source)"))
    source,target = Tape(encode(4,4)),Tape(); bad['convert_word'](source,target,4,3)
    need(signed(target.observed())!=4, 'removed shrink guard changes value')
    bad,_ = load(path,('for _ in indices(axes):','for _ in range(1):'))
    source,target = Tape([j%2 for j in range(32)]),Tape()
    bad['copy_context_payload'](source,target,Tape(),2,2,1)
    need(len(target.observed())!=32 or source.read()!=4, 'missing axis shortens context')
    return dict(status='PASS_INDEPENDENT_CORE_TRANSPORT', reviewed_functions=NAMES,
        algorithm_ast_sha256=source_digest, exact_conversions=conversions,
        nonredundant_shrinks_rejected=invalid, complete_complex_fields=field_cases,
        exhaustive_address_domains=address_cases, context_split_rejoins=context_cases,
        catalogue_frames=len(frames), local_address_cost_ratio=max_ratio,
        conversion_receipt_sha256=receipt.hexdigest(), negative_controls=3,
        scope='Local scans/widths/context transport only; no Count cost, native H, source pages or complete physical Core claim.')

if __name__=='__main__':
    need(len(sys.argv)==2,'give exact reviewed physical_join.py path')
    print(json.dumps(check(Path(sys.argv[1])),indent=2,sort_keys=True))
