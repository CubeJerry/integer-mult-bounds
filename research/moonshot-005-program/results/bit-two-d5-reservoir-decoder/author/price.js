function priceTwoD5(profile) {
 const scale=10n**40n,memo=new Map();
 function root(r){if(memo.has(r))return memo.get(r);const n=BigInt(r)**199n*scale**200n;let x=BigInt(r)*scale;for(let k=0;k<1000;k++){const y=(199n*x+n/x**199n)/200n;if(y>=x)break;x=y;}while(x**200n>n)x--;while((x+1n)**200n<=n)x++;if(!(x**200n<=n&&n<(x+1n)**200n))throw Error("root certificate");const v=x**200n===n?[x,x]:[x,x+1n];memo.set(r,v);return v;}
 const term=(o,r,c)=>o[r]=(o[r]||0)+c;
 function form(o){let lo=0n,hi=0n;for(const [r,c0]of Object.entries(o)){const c=BigInt(c0),[a,b]=root(Number(r));lo+=c*(c<0n?b:a);hi+=c*(c<0n?a:b);}return [lo,hi];}
 const decimal=(a,d)=>{let sign=a<0n?"-":"";if(a<0n)a=-a;let s=sign+(a/d)+".",t=a%d;for(let k=0;k<36;k++){t*=10n;s+=(t/d);t%=d;}return s;};
 const encode=(v,d=scale)=>({lower_numerator:String(v[0]),upper_numerator:String(v[1]),denominator:String(d),lower_decimal:decimal(v[0],d),upper_decimal:decimal(v[1],d)});
 const sixB={127:37,64:74,1:-74};for(let j=1;j<=8;j++){term(sixB,7*j+1,74);term(sixB,7*j,-74);}
 const margins={};for(const q of [7,8]){const t={...sixB};for(const [r,c]of Object.entries(profile))term(t,r,-6*c);term(t,8,-6*q);margins[q]=encode(form(t),6n*scale);}
 return {exponent:"199/200",profile,moment:encode(form(profile)),limiting_complete_BIT_allowance:encode(form(sixB),6n*scale),optimistic_margin_after_additional_full_lifetimes:margins,scale:String(scale),root_intervals:Object.fromEntries([...memo].sort((a,b)=>a[0]-b[0]).map(([r,v])=>[r,v.map(String)])),scope:"Only the closed one-row partial source is priced. Margins subtract bare full lifetimes but omit all their further source, decoder, and restoration operations; they are necessary screens, not a completion."};
}
