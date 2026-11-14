#!/usr/bin/env python3
"""Read-only local publication URL audit; no network or Git operations."""
from pathlib import Path
from urllib.parse import urlsplit,parse_qs,urlencode
from hashlib import sha256
import argparse,json

def require(ok,message):
    if not ok:raise ValueError(message)

def main():
    p=argparse.ArgumentParser();p.add_argument('--links',type=Path,required=True)
    p.add_argument('--refs',type=Path,required=True);args=p.parse_args()
    raw=args.links.read_bytes();rows=json.loads(raw);refs=json.loads(args.refs.read_text())
    require(len(rows)==26,'frozen26-contribution review scope')
    require(refs['status']=='PASS' and len(refs['rows'])==26,'all live-ref results present')
    by_package={r['package']:r for r in refs['rows']};report=[];urls=0
    require(len(by_package)==26 and len({r['branch'] for r in rows})==26,'unique package and branch inventory')
    for row in rows:
        name=row['package'];branch=row['branch'];commit=row['remote_commit'];remote=by_package[name]
        require(remote['pass'] and remote['branch']==branch and remote['actual_commit']==commit==remote['remote_commit'],name+': live ref matches recorded commit')
        require(remote['actual_ref']=='refs/heads/'+branch and remote['type']=='commit',name+': exact ref identity')
        expected='https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:'+branch
        require(row['compare_url']==expected,name+': compare target')
        require(row['title'] and '\n' not in row['title'] and not row['title'].startswith('Research:'),name+': recorded descriptive title')
        descriptions=[]
        for key in ('description_url','full_description_url'):
            if key not in row:continue
            parsed=urlsplit(row[key]);prefix='/CubeJerry/integer-mult-bounds/blob/'+commit+'/research/'+name+'/'
            require(parsed.scheme=='https' and parsed.netloc=='github.com' and parsed.path.startswith(prefix),name+': exact committed description target')
            require(parsed.path[len(prefix):] in ('PR-DESCRIPTION.md','PR-BODY.md') and not parsed.query and not parsed.fragment,name+': description leaf')
            descriptions.append(row[key])
        require(row['description_url'] in row['short_pr_body'],name+': concise body links full committed draft')
        checks=[]
        for field,body_field,mode in [('prefill_url','body','expand'),('prefilled_url','body','expand'),('short_prefilled_url','short_pr_body','quick_pull')]:
            if field not in row:continue
            url=row[field];parsed=urlsplit(url)
            require(parsed.scheme+'://'+parsed.netloc+parsed.path==expected and not parsed.fragment,name+': prefill target '+field)
            parameters=[(mode,'1'),('title',row['title']),('body',row[body_field])]
            require(parsed.query==urlencode(parameters),name+': exactly one standard urlencode '+field)
            require(parse_qs(parsed.query,keep_blank_values=True)=={k:[v] for k,v in parameters},name+': exact decoded title/body '+field)
            require('\n' in row[body_field],name+': real Markdown newlines '+field)
            checks.append({'url_field':field,'length':len(url),'title_body_roundtrip':True,
                           'body_sha256':sha256(row[body_field].encode()).hexdigest(),
                           'body_newlines':row[body_field].count('\n')});urls+=1
        require(any(x['url_field']=='short_prefilled_url' for x in checks),name+': concise prefill present')
        report.append({'package':name,'branch':branch,'commit':commit,'live_ref_match':True,
                       'compare_target':True,'committed_description_target':True,
                       'encoded_urls':checks,'status':'PASS'})
    print(json.dumps({'status':'PASS_PUBLICATION_REFS_AND_LOCAL_URLS','review_links_sha256':sha256(raw).hexdigest(),
                     'contributions':len(report),'encoded_url_variants':urls,'live_refs_checked_utc':refs['checked_utc'],
                     'scope':'26 existing contributions only; branch refs fetched once. No repeated HTTP/form tests, scientific replays, commits or branch mutations. Correct encoding does not establish authenticated form rendering.',
                     'packages':report},indent=2,sort_keys=True))

if __name__=='__main__':main()
