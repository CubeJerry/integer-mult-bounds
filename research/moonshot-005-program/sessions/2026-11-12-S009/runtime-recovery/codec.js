/* Standalone recovery utilities; no Node, network or file dependencies.
   Own implementation from RFC1951/RFC1952 format definitions. */
function need(q,m){if(!q)throw Error(m);}
function fromBase64(s){
 const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",tab=new Int16Array(128).fill(-1);for(let i=0;i<64;i++)tab[abc.charCodeAt(i)]=i;
 const a=[];let n=0,b=0;
 for(const c of s){if(c==="=")break;const x=c.charCodeAt(0);if(c===" "||c==="\n"||c==="\r"||c==="\t")continue;need(x<128&&tab[x]>=0,"base64 digit");b=(b<<6)|tab[x];n+=6;if(n>=8){n-=8;a.push((b>>n)&255);}}
 return Uint8Array.from(a);
}
function utf8(a){let s="",i=0,chunk=[];while(i<a.length){let c=a[i++];if(c>=128){let n=c<224?1:c<240?2:3;let v=c&((1<<(6-n))-1);for(let j=0;j<n;j++){need(i<a.length&&(a[i]&192)===128,"UTF8 continuation");v=(v<<6)|(a[i++]&63);}c=v;}if(c>65535){c-=65536;chunk.push(0xd800+(c>>10),0xdc00+(c&1023));}else chunk.push(c);if(chunk.length>4000){s+=String.fromCharCode(...chunk);chunk=[];}}return s+String.fromCharCode(...chunk);}
function ascii(s){need([...s].every(c=>c.charCodeAt(0)<128),"ASCII only");return Uint8Array.from([...s].map(c=>c.charCodeAt(0)));}
function crc32(a){let c=0xffffffff;for(const v of a){c^=v;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}return(c^0xffffffff)>>>0;}
function sha256(input){
 const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 const h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],a=new Uint8Array(Math.ceil((input.length+9)/64)*64),w=new Uint32Array(64);
 need(input.length<0x20000000,"bounded SHA input");a.set(input);a[input.length]=128;const bits=input.length*8;for(let j=0;j<4;j++)a[a.length-1-j]=(bits>>>8*j)&255;
 const rr=(x,n)=>(x>>>n)|(x<<(32-n));
 for(let p=0;p<a.length;p+=64){for(let j=0;j<16;j++)w[j]=((a[p+4*j]<<24)|(a[p+4*j+1]<<16)|(a[p+4*j+2]<<8)|a[p+4*j+3])>>>0;
 for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[j-7]+(rr(y,17)^rr(y,19)^(y>>>10)))>>>0;}
 let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){const t1=(H+(rr(E,6)^rr(E,11)^rr(E,25))+((E&F)^((~E)&G))+K[j]+w[j])>>>0,t2=((rr(A,2)^rr(A,13)^rr(A,22))+((A&B)^(A&C)^(B&C)))>>>0;H=G;G=F;F=E;E=(D+t1)>>>0;D=C;C=B;B=A;A=(t1+t2)>>>0;}const v=[A,B,C,D,E,F,G,H];for(let j=0;j<8;j++)h[j]=(h[j]+v[j])>>>0;}
 return h.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function gunzip(a){
 need(a.length>=18&&a[0]===31&&a[1]===139&&a[2]===8,"gzip header");const flags=a[3];need(!(flags&224),"gzip reserved flags");let p=10;
 if(flags&4){need(p+2<a.length,"gzip extra");const n=a[p]|(a[p+1]<<8);p+=2+n;}
 for(const flag of[8,16])if(flags&flag){while(p<a.length&&a[p])p++;need(p<a.length,"gzip string");p++;}
 if(flags&2){need((crc32(a.subarray(0,p))&65535)===(a[p]|(a[p+1]<<8)),"header CRC");p+=2;}
 const le=i=>(a[i]|(a[i+1]<<8)|(a[i+2]<<16)|(a[i+3]<<24))>>>0,expected=le(a.length-4),out=new Uint8Array(expected);need(expected<100000000,"bounded inflate");
 let bit=p*8,nout=0,final=0;
 function read(n){need(bit+n<=(a.length-8)*8,"deflate truncation");let v=0;for(let j=0;j<n;j++,bit++)v|=((a[bit>>3]>>(bit&7))&1)<<j;return v;}
 function tree(lens){const count=new Int32Array(16),next=new Int32Array(16),maps=Array.from({length:16},()=>new Map());for(const l of lens){need(l>=0&&l<=15,"huffman length");if(l)count[l]++;}
 let code=0,left=1;for(let l=1;l<=15;l++){left=left*2-count[l];need(left>=0,"oversubscribed huffman");code=(code+count[l-1])<<1;next[l]=code;}
 lens.forEach((l,s)=>{if(l)maps[l].set(next[l]++,s);});return maps;}
 function symbol(t){let c=0;for(let l=1;l<=15;l++){c=(c<<1)|read(1);const s=t[l].get(c);if(s!==undefined)return s;}throw Error("invalid Huffman symbol");}
 const LB=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258],LE=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0],DB=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577],DE=[0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13];
 while(!final){final=read(1);const type=read(2);need(type!==3,"reserved deflate block");if(type===0){bit=(bit+7)&~7;const n=read(16),inv=read(16);need((n^inv)===65535&&nout+n<=out.length,"stored block");for(let i=0;i<n;i++)out[nout++]=read(8);continue;}
 let lt,dt;if(type===1){lt=tree(Array.from({length:288},(_,i)=>i<144?8:i<256?9:i<280?7:8));dt=tree(Array(32).fill(5));}
 else{const nl=read(5)+257,nd=read(5)+1,nc=read(4)+4,order=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15],cl=Array(19).fill(0);for(let i=0;i<nc;i++)cl[order[i]]=read(3);const ct=tree(cl),ls=[];
 while(ls.length<nl+nd){const q=symbol(ct);if(q<16)ls.push(q);else{let v=0,n;if(q===16){need(ls.length>0,"repeat prior code");v=ls[ls.length-1];n=read(2)+3;}else if(q===17)n=read(3)+3;else if(q===18)n=read(7)+11;else throw Error("code length");need(ls.length+n<=nl+nd,"code repeat overflow");for(let j=0;j<n;j++)ls.push(v);}}
 need(ls[256]>0,"missing end code");lt=tree(ls.slice(0,nl));dt=tree(ls.slice(nl));}
 for(;;){const q=symbol(lt);if(q<256){need(nout<out.length,"inflate output overflow");out[nout++]=q;}else if(q===256)break;else{need(q>=257&&q<=285,"reserved length");const k=q-257,n=LB[k]+read(LE[k]),dc=symbol(dt);need(dc<30,"reserved distance");const d=DB[dc]+read(DE[dc]);need(d<=nout&&nout+n<=out.length,"distance/output bounds");for(let j=0;j<n;j++){out[nout]=out[nout-d];nout++;}}}
 }
 need(nout===expected&&Math.ceil(bit/8)===a.length-8,"gzip size/trailing data");need(crc32(out)===le(a.length-8),"gzip data CRC");return out;
}
