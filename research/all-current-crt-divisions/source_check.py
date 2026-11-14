"""Read-only source/dependency/dispatch certificate, independent of replay."""
from pathlib import Path
from hashlib import sha256,sha1
import ast,json,sys,types
HERE=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise ValueError(s)
def raw_sites(raw):
    rows=[]
    class Calls(ast.NodeVisitor):
        def __init__(self):self.function=[]
        def visit_FunctionDef(self,node):
            self.function.append(node.name);self.generic_visit(node);self.function.pop()
        def visit_Call(self,node):
            if isinstance(node.func,ast.Attribute) and node.func.attr=='divmod':
                rows.append({'function':self.function[-1],'line':node.lineno,'expression':ast.unparse(node)})
            self.generic_visit(node)
    Calls().visit(ast.parse(raw));return rows
def binding_scope(raw):
    tree=ast.parse(raw)
    need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='old_raw'
                 for n in ast.walk(tree)),'no original-provider call in all-call binding')
    need(not any(isinstance(n,ast.Attribute) and n.attr in('phase','eligible') for n in ast.walk(tree)),
         'no ordinal or half selector')
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='divide']
    need(len(calls)==1 and ast.unparse(calls[0])=='owner.divide(obj, n, d)','one unconditional exact child dispatch')

def main():
    pins=json.loads((HERE/'SOURCE-PINS.json').read_text())['files']
    for pin in pins:
        raw=(HERE/pin['local']).read_bytes()
        need(len(raw)==pin['bytes'] and sha256(raw).hexdigest()==pin['sha256'],'exact dependency bytes')
        need(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob'],'exact dependency Git object')
    research=HERE/'inputs/divider/inputs/headers/inputs/keypass/inputs/route/inputs/point/inputs/predecessor/research'
    sources=[research/'encoded-current-crt/producer.py',research/'encoded-crt-leaf-payload/frozen/inverse_producer.py']
    inventory=[]
    for path in sources:
        sites=raw_sites(path.read_bytes())
        need([x['function'] for x in sites]==['remainder','inverse'],'exhaustive two-site source grammar')
        need([x['expression'] for x in sites]==['self.raw.divmod(value, modulus)','self.raw.divmod(r0, r1)'],
             'exact operands at both admitted source sites')
        inventory.append({'source':str(path.relative_to(HERE)),'sites':sites})
    raw=(HERE/'all_binding.py').read_text();binding_scope(raw)
    try:binding_scope(raw.replace('return owner.divide(obj,n,d)','return old_raw(obj,n,d)'))
    except ValueError:pass
    else:raise ValueError('fallback source mutant escaped')
    path=HERE/'inputs/divider/divider.py';d=types.ModuleType('B11_unchanged_divider');d.__file__=str(path);sys.modules[d.__name__]=d
    exec(compile(path.read_bytes(),str(path),'exec'),d.__dict__);code,_,meta=d.compile_divider()
    need(len(code)==336150 and meta['tapes']==68 and
         d.digest(code)=='d36e8220def8efb2baed793d0bea6f0a19b0903b5b005b730652b5bb7d121194','exact unchanged child graph')
    print(json.dumps({'status':'PASS','source_objects':len(pins),'source_sites':inventory,'locations':len(code),
                     'graph':d.digest(code),'old_provider_call_expressions':0,'phase_selectors':0,
                     'fallback_source_mutant_rejected':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
