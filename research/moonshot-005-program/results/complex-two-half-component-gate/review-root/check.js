
function reviewTwoHalfGate() {
 const need=(x,m)=>{if(!x)throw Error(m)},p=5;
 const inv=a=>{for(let b=1;b<p;b++)if(a*b%p===1)return b;throw Error("nonunit")};
 const rank=A=>{A=A.map(r=>r.slice());let k=0;for(let c=0;c<A[0].length&&k<A.length;c++){let i=k;while(i<A.length&&!A[i][c])i++;if(i===A.length)continue;[A[k],A[i]]=[A[i],A[k]];const z=inv(A[k][c]);A[k]=A[k].map(x=>x*z%p);for(let j=k+1;j<A.length;j++){const v=A[j][c];A[j]=A[j].map((x,a)=>(x-v*A[k][a]%p+p)%p);}k++;}return k};
 let p1=0,p2=0;for(let code=0;code<625;code++){let q=code,T=[];for(let i=0;i<4;i++){T.push(q%5);q=Math.floor(q/5);}
 need(rank([[T[0],T[1],1],[T[2],T[3],0],[1,0,0]])>=2,"p1 cross-rank");
 need(rank([[T[0],T[1],1,0],[T[2],T[3],0,1],[1,0,0,0],[0,1,0,0]])===4,"p2 cross-rank");p1++;p2++;}
 const S=10n**24n,roots={};
 function root(n){if(roots[n])return roots[n];const N=BigInt(n)**199n*S**200n;let x=BigInt(n)*S;
 for(;;){const y=(199n*x+N/x**199n)/200n;if(y>=x)break;x=y;}
 while((x+1n)**200n<=N)x++;while(x**200n>N)x--;
 const out=[x,x**200n===N?x:x+1n];need(out[0]**200n<=N&&out[1]**200n>=N,"Newton exact root");return roots[n]=out;}
 const moment=terms=>{let l=0n,u=0n;for(const[n,c]of terms){const[a,b]=root(n),k=BigInt(c);l+=k*(k<0n?b:a);u+=k*(k<0n?a:b);}return[l,u];};
 const two=moment([[16,2],[15,1],[1,-2],[7,-4],[8,-2]]),mixed=moment([[23,3],[22,1],[1,-3],[7,-9],[8,-3]]),full=moment([[23,4],[1,-4],[7,-9],[8,-3]]);
 need(two[0]>0n&&two[1]<S&&mixed[0]>0n&&mixed[1]<S&&full[0]>0n,"endpoint margins");
 const allocations=[];for(let a=0;a<=3;a++)for(let b=0;b<=3;b++)for(let c=0;c<=3;c++)for(let d=0;d<=3;d++){const idle=a+b+c+d-6;if(idle<0||idle>6)continue;const ranks=[7*a+2,7*b+2,7*c+2,7*d+1],v=moment(ranks.map(r=>[r,1]).concat([[1,-4],[7,-3-idle],[8,-3]]));need(v[1]<0n,"optimistic allocation exclusion");allocations.push({ranks,idle,lower:v[0],upper:v[1]});}
 need(allocations.length===150,"all150 allocations");
 const best=allocations.reduce((a,b)=>a.upper>b.upper?a:b);
 return{status:"PASS_ROOT_TWO_HALF_REVIEW",finite_cross_rank_controls:{prime:p,p1_arbitrary_active_corners:p1,p2_arbitrary_active_corners:p2},prices:{method:"integer Newton200th root with exact final bracketing",scale:S.toString(),two_half_no_query:two.map(String),three_half_mixed_no_query:mixed.map(String),three_half_full_one_query:full.map(String),all_one_query_mixed_allocations:allocations.length,best_one_query_mixed:{...best,lower:best.lower.toString(),upper:best.upper.toString()}},new_complete_kappa:false};
}
if(typeof module!=="undefined")module.exports={reviewTwoHalfGate};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(reviewTwoHalfGate(),null,2));
