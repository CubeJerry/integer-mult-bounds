function pricePayloadFork(profile) {
 const scale=10n**40n, memo=new Map(), pow=x=>x**200n;
 function root(r){if(memo.has(r))return memo.get(r);r=BigInt(r);if(r===1n){const v=[scale,scale];memo.set(1,v);return v;}const N=r**199n*scale**200n;let x=r*scale;for(let i=0;i<1000;i++){let y=(199n*x+N/(x**199n))/200n;if(y>=x)break;x=y;}while(pow(x)>N)x--;while(pow(x+1n)<=N)x++;if(!(pow(x)<=N&&N<pow(x+1n)))throw Error("root interval");const v=[x,x+1n];memo.set(Number(r),v);return v;}
 function form(terms){let lo=0n,hi=0n;for(const [r,c0] of Object.entries(terms)){let c=BigInt(c0),[a,b]=root(Number(r));lo+=c*(c>=0n?a:b);hi+=c*(c>=0n?b:a);}return [lo,hi];}
 const addTerm=(T,r,c)=>T[r]=(T[r]||0)+c;
 const sixB={127:37,64:74,1:-74};for(let j=1;j<=8;j++){addTerm(sixB,7*j+1,74);addTerm(sixB,7*j,-74);}
 const cost=form(profile),budget=form(sixB),isolation={7:222,8:3};for(const [r,c] of Object.entries(profile))addTerm(isolation,r,-c);
 const margins={};for(const q of [7,8]){const terms={...sixB};for(const[r,c]of Object.entries(profile))addTerm(terms,r,-6*c);addTerm(terms,8,-6*q);margins[q]=form(terms);}
 const dec=(a,d=scale,places=30)=>{const sign=a<0n?"-":"";if(a<0n)a=-a;let whole=a/d,rem=a%d,s="";for(let i=0;i<places;i++){rem*=10n;s+=(rem/d).toString();rem%=d;}return sign+whole+"."+s;};
 const enc=(v,d=scale)=>({lower_numerator:v[0].toString(),upper_numerator:v[1].toString(),denominator:d.toString(),lower_decimal:dec(v[0],d),upper_decimal:dec(v[1],d)});
 return {exponent:"199/200",root_interval_method:"integer 200th roots; exact inequalities a^200 <= r^199 * scale^200 < (a+1)^200",scale:scale.toString(),profile,moment:enc(cost),limiting_complete_BIT_allowance:enc(budget,6n*scale),saving_vs_optimistic_three_isolated_Hub_lifetimes:enc(form(isolation)),optimistic_remaining_margin_after_extra_full_lifetimes:Object.fromEntries(Object.entries(margins).map(([q,v])=>[q,enc(v,6n*scale)])),root_intervals:Object.fromEntries([...memo.entries()].sort((a,b)=>a[0]-b[0]).map(([r,v])=>[r,v.map(String)])),scope:"Complete partial word only; no completed supplier, cover/compiler admission or new kappa. Further packet counts are necessary optimistic screens, not completions."};
}

if(typeof module!=="undefined")module.exports={pricePayloadFork};
