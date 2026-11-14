
function runQuadraticSignChecks() {
  function need(ok,msg){if(!ok)throw Error(msg);}
  function pop(x){let n=0;while(x){x&=x-1;n++;}return n;}
  function parity(x){return pop(x)&1;}
  function rank(rows){let p=new Map();for(let v of rows){while(v){let k=31-Math.clz32(v);if(p.has(k))v^=p.get(k);else{p.set(k,v);break;}}}return p.size;}
  function qeval(w,linear,q,pairs){let v=parity(w&linear);for(let k=0;k<pairs.length;k++){const [i,j]=pairs[k];v^=((q>>k)&1)*((w>>i)&1)*((w>>j)&1);}return v;}
  function majorizes(a,b){a=[...a].sort((x,y)=>y-x);b=[...b].sort((x,y)=>y-x);need(a.length===b.length,'length');let x=0,y=0,g=[];for(let k=0;k<a.length;k++){x+=a[k];y+=b[k];need(x>=y,'majorization partial sum');g.push(x-y);}need(x===y&&g.some(x=>x>0),'equal total and strict');return g;}
  const spectra=[],queries=[];
  for(const d of [2,3,4]){
    const pairs=[];for(let i=0;i<d;i++)for(let j=i+1;j<d;j++)pairs.push([i,j]);
    let forms=0,maxwidth=0;
    for(let linear=0;linear<(1<<d);linear++)for(let q=0;q<(1<<pairs.length);q++){
      const cols=[];for(let i=0;i<d;i++)if((linear>>i)&1)cols.push(1<<i,1<<i);
      for(let k=0;k<pairs.length;k++)if((q>>k)&1){const [i,j]=pairs[k];cols.push(1<<i,1<<j,(1<<i)^(1<<j),(1<<i)^(1<<j),(1<<i)^(1<<j));}
      need(cols.length<=2*d+5*pairs.length,'width');
      for(let w=0;w<(1<<d);w++){const phase=cols.reduce((v,z)=>v+parity(w&z),0)%4;need(phase===2*qeval(w,linear,q,pairs),'actual simultaneous spectrum');}
      forms++;maxwidth=Math.max(maxwidth,cols.length);
    }
    spectra.push({d,quadratic_sign_forms:forms,maximum_construction_width:maxwidth});
    const upper=[];for(let i=0;i<d;i++)for(let j=i;j<d;j++)upper.push([i,j]);
    const hist={};let checked=0;
    for(let mask=0;mask<(1<<upper.length);mask++){
      const rows=Array(d).fill(0),directions=[];
      for(let k=0;k<upper.length;k++)if((mask>>k)&1){const [i,j]=upper[k];rows[i]^=1<<j;if(i!==j)rows[j]^=1<<i;if(i===j)directions.push(1<<i);else directions.push(1<<i,1<<j,(1<<i)^(1<<j));}
      const rho=rank(rows),off=rows.some((x,i)=>x&~(1<<i));const probs=[];
      for(const linear of [1,2]){let count=0;for(let q=0;q<(1<<pairs.length);q++){let predicted=0;for(let i=0;i<d;i++)predicted^=((linear>>i)&1)*((rows[i]>>i)&1);for(let k=0;k<pairs.length;k++){const [i,j]=pairs[k];predicted^=((q>>k)&1)*((rows[i]>>j)&1);}let actual=0;for(const w of directions)actual^=qeval(w,linear,q,pairs);need(actual===predicted,'sign depends only on B');count+=actual;}probs.push(count);}
      const den=1<<pairs.length;
      if(off)need(probs[0]===den/2&&probs[1]===den/2,'off-diagonal average');
      else need(probs[0]===den*(rows[0]&1)&&probs[1]===den*((rows[1]>>1)&1),'diagonal average');
      const weight=(probs[0]+probs[1])/den;need(Number.isInteger(weight),'integer weight');
      need(weight===0||(weight===1&&rho>=1)||(weight===2&&rho>=2),'all exponent query inequality');
      const phases=Array.from({length:1<<d},(_,z)=>directions.reduce((v,w)=>v+parity(w&z),0)%4);
      let support=0;
      for(let x=0;x<(1<<d);x++){let re=0,im=0;for(let z=0;z<(1<<d);z++){const sign=parity(x&z)?-1:1;switch(phases[z]){case 0:re+=sign;break;case 1:im+=sign;break;case 2:re-=sign;break;case 3:im-=sign;break;}}const norm=re*re+im*im;if(norm){need(norm===(1<<(2*d-rho)),'exact Gaussian magnitude');support++;}}
      need(support===(1<<rho),'true Gaussian rank');const key=rho+','+weight;hist[key]=(hist[key]||0)+1;checked++;
    }
    queries.push({d,symmetric_matrices:checked,rank_weight_histogram:hist});
  }
  need(qeval(3,1,0,[[0,1]])===1&&qeval(3,1,1,[[0,1]])===0,'nonaxis incidence control');
  need(rank([2,1])===2,'alternating rank control');
  const want=Array.from({length:4},(_,w)=>2*qeval(w,0,1,[[0,1]]));
  need(!Array.from({length:4},(_,z)=>Array.from({length:4},(_,w)=>parity(w&z))).some(a=>a.every((x,i)=>x===want[i])),'one column cannot realize every sign pattern');

  function canonicalControl() {
    const operations=[['MOVE',3,0,1],['ADD',2,3,-1],['MOVE',3,1,509],['MOVE',1,0,1],['ADD',1,0,1],['MOVE',1,1,509],['MOVE',0,1,511],['MOVE',2,1,511]];
    const profile={};let cases=0;
    const mulI=(v,k)=>{k=((k%4)+4)%4;return k===0?v:k===1?[-v[1],v[0]]:k===2?[-v[0],-v[1]]:[v[1],-v[0]];};
    for(let z=0;z<512;z++){
      const loc=[1,0,1,0],rows=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>[+(i===j),0]));
      for(const op of operations){if(op[0]==='MOVE'){const [_,v,from,to]=op;need(loc[v]===from&&(from&to)===from,'actual nested canonical contact');const mask=from^to;for(let j=0;j<4;j++)rows[v][j]=mulI(rows[v][j],pop(mask&z));loc[v]=to;if(z===0){const k=pop(mask);profile[k]=(profile[k]||0)+1;}}else{const [_,v,u,sign]=op;need(loc[v]===loc[u]&&v!==u,'cochart ADD');for(let j=0;j<4;j++){rows[v][j][0]+=sign*rows[u][j][0];rows[v][j][1]+=sign*rows[u][j][1];}}}
      need(loc.join(',')==='511,509,511,509','canonical original endpoints');
      const f=pop(z&508),aa=z&1,bb=(z>>1)&1;
      const expected=Array.from({length:4},()=>Array.from({length:4},()=>[0,0]));
      expected[0][0]=mulI([1,0],f+bb);expected[1][1]=mulI([1,0],f+aa);expected[1][0]=mulI([1,0],f);expected[2][2]=mulI([1,0],f+bb);expected[2][3]=mulI([-1,0],f+aa+bb);expected[3][3]=mulI([1,0],f+aa);
      need(JSON.stringify(rows)===JSON.stringify(expected),'all canonical original columns');
      cases++;
    }
    need(JSON.stringify(profile)===JSON.stringify({1:2,7:2,8:2}),'complete canonical invoice');
    return {exact_character_cases:cases,independent_original_inputs:4,events:8,owned:0,movement_profile:profile,scope:'Coordinate-chart control and phase equations, not a new compiled full native artifact.'};
  }
  const canonical_control=canonicalControl();
  return {
    canonical_control,
    status:'PASS_EXACT_QUADRATIC_SPECTRUM_GAUSSIAN_RANK_AND_MAJORIZATION_CONTROLS',
    runtime:'Pure JavaScript exact integer arithmetic in orchestration V8; no unavailable local executor used.',
    spectrum:spectra,queries,
    all_arm_seed_partial_sum_gaps:majorizes([28,28,16,16,16,16,0,0,0,0,0,0],[14,14,14,14,9,9,9,9,7,7,7,7]),
    native_price_partial_sum_gaps:majorizes([14,9,9,0,0,0],[8,8,7,7,1,1]),
    negative_controls:['Nonaxis rank-one query has one averaged incidence','Alternating B has rank2','One column does not realize every quadratic sign pattern'],
    universal_proof:'Separate written argument; finite d2..4 checks are not extrapolated to all d,V,t.',
    complete_supplier_or_new_kappa:false
  };
}
