// An explicit fixed-head implementation of one adaptive Walsh scalar.
// Run the self-test with: node modular-scalar-machine.mjs
// The program below uses head-local symbols only. The Tape and test adapters supply the simulation.
const LEFT = '[', RIGHT = ']', BLANK = '_';

class Tape {
  constructor(symbols = []) {
    this.cells = [LEFT, ...symbols];
    this.head = 1;
    this.highest = 1;
    this.operations = 0;
  }
  read() {
    this.operations++;
    return this.cells[this.head] ?? BLANK;
  }
  write(symbol) {
    this.operations++;
    this.cells[this.head] = symbol;
  }
  move(direction) {
    this.operations++;
    this.head += direction;
    if (this.head < 0) throw new Error('head crossed its left boundary');
    this.highest = Math.max(this.highest, this.head);
  }
}

function rewind(tape) {
  while (tape.read() !== LEFT) tape.move(-1);
  tape.move(1);
}
function toHighBit(tape) {
  while (tape.read() !== RIGHT) tape.move(1);
  tape.move(-1);
}
function allocateWord(parts, extra, word) {
  for (const part of parts) {
    while (part.read() !== RIGHT) {
      word.write(0);
      word.move(1);
      part.move(1);
    }
    rewind(part);
  }
  for (let i=0; i<extra; i++) {
    word.write(0);
    word.move(1);
  }
  word.write(RIGHT);
  rewind(word);
}
function clearWord(word) {
  while (word.read() !== RIGHT) {
    word.write(0);
    word.move(1);
  }
  rewind(word);
}
function copyWord(source, target) {
  while (target.read() !== RIGHT) {
    const bit = source.read();
    target.write(bit === RIGHT ? 0 : bit);
    target.move(1);
    if (bit !== RIGHT) source.move(1);
  }
  // A narrower target is permitted only when the lost high bits are zero.
  while (source.read() !== RIGHT) {
    if (source.read() !== 0) throw new Error('copy overflow');
    source.move(1);
  }
  rewind(source);
  rewind(target);
}
function isZero(word) {
  let yes=true;
  while (word.read() !== RIGHT) {
    if (word.read() === 1) yes=false;
    word.move(1);
  }
  rewind(word);
  return yes;
}
function isOne(word) {
  let yes=word.read() === 1;
  word.move(1);
  while (word.read() !== RIGHT) {
    if (word.read() !== 0) yes=false;
    word.move(1);
  }
  rewind(word);
  return yes;
}
function compareWords(a, b) {
  let order=0;
  while (a.read() !== RIGHT || b.read() !== RIGHT) {
    const x=a.read(), y=b.read();
    const v=x===RIGHT?0:x, w=y===RIGHT?0:y;
    if (v !== w) order=v<w?-1:1;
    if (x!==RIGHT) a.move(1);
    if (y!==RIGHT) b.move(1);
  }
  rewind(a);
  rewind(b);
  return order;
}
// Replace target by target +/- source with a one-bit carry or borrow.
function accumulate(source, target, direction) {
  let carry=0;
  while (target.read() !== RIGHT) {
    const x=source.read();
    const sum=target.read()+direction*(x===RIGHT?0:x)+carry;
    target.write((sum+2)%2);
    carry=sum<0?-1:(sum>=2?1:0);
    target.move(1);
    if (x!==RIGHT) source.move(1);
  }
  if (carry) throw new Error('addition overflow or subtraction underflow');
  while (source.read() !== RIGHT) {
    if (source.read() !== 0) throw new Error('high arithmetic overflow');
    source.move(1);
  }
  rewind(source);
  rewind(target);
}
function shiftIn(word, bit) {
  let carry=bit;
  while (word.read() !== RIGHT) {
    const next=word.read();
    word.write(carry);
    carry=next;
    word.move(1);
  }
  if (carry) throw new Error('shift overflow');
  rewind(word);
}
function reduceOnce(value, modulus) {
  if (compareWords(value,modulus)>=0) accumulate(modulus,value,-1);
}

// Prefix invariant: dividend prefix = quotient prefix * divisor + remainder.
// If supplied, quotient has the same capacity as dividend.
function divideWords(dividend, divisor, quotient, remainder) {
  clearWord(remainder);
  toHighBit(dividend);
  if (quotient) toHighBit(quotient);
  while (dividend.read() !== LEFT) {
    shiftIn(remainder,dividend.read());
    const take=compareWords(remainder,divisor)>=0;
    if (take) accumulate(divisor,remainder,-1);
    if (quotient) {
      quotient.write(take?1:0);
      quotient.move(-1);
    }
    dividend.move(-1);
  }
  dividend.move(1);
  if (quotient) quotient.move(1);
}
// The running value starts at zero. Reduce after the double and after the addition.
function multiplyShort(value, factor, modulus, result) {
  clearWord(result);
  toHighBit(factor);
  while (factor.read() !== LEFT) {
    shiftIn(result,0);
    if (modulus) reduceOnce(result,modulus);
    if (factor.read() === 1) {
      accumulate(value,result,1);
      if (modulus) reduceOnce(result,modulus);
    }
    factor.move(-1);
  }
  factor.move(1);
}
function modularDifference(a,b,modulus,result) {
  if (compareWords(a,b)>=0) {
    copyWord(a,result);
    accumulate(b,result,-1);
  } else {
    copyWord(modulus,result);
    accumulate(b,result,-1);
    accumulate(a,result,1);
  }
}

// Interface: four unsigned, nonempty, low-bit-first input words and one sign bit.
// x and M can have any common K-bit format; 0 <= x < M and M >= 2.
// The two coefficient parts fit in B bits; the denominator is positive.
// All heads enter and leave successful calls at their first word cell.
function modularScalar(x, magnitude, negative, denominator, modulus) {
  const scratch=[];
  function word(parts,extra=0) {
    const t=new Tape();
    scratch.push(t);
    allocateWord(parts,extra,t);
    return t;
  }
  if (isZero(modulus) || isOne(modulus) || compareWords(x,modulus)>=0) {
    throw new Error('invalid residue input');
  }
  if (isZero(denominator)) throw new Error('zero denominator');
  const z=word([modulus],1), spare=word([modulus],1), output=word([modulus]);
  multiplyShort(x,magnitude,modulus,z);
  if (negative && !isZero(z)) {
    copyWord(modulus,spare);
    accumulate(z,spare,-1);
    copyWord(spare,z);
  }
  if (isOne(denominator)) {
    copyWord(z,output);
  } else {
    const short=()=>word([denominator],1);
    const r0=short(), r1=short(), rNew=short(), quotient=short();
    const t0=short(), t1=short(), tNew=short(), product=short();
    const zero=short(), negativeZ=short(), zMod=short(), r=short();
    copyWord(denominator,r0);
    divideWords(modulus,denominator,null,r1);
    t1.write(1);
    // ri = ti * M (mod denominator), with both ti residues kept canonical.
    while (!isZero(r1)) {
      divideWords(r0,r1,quotient,rNew);
      multiplyShort(t1,quotient,denominator,product);
      modularDifference(t0,product,denominator,tNew);
      copyWord(r1,r0);
      copyWord(rNew,r1);
      copyWord(t1,t0);
      copyWord(tNew,t1);
    }
    if (!isOne(r0)) throw new Error('nonunit denominator');
    divideWords(z,denominator,null,zMod);
    modularDifference(zero,zMod,denominator,negativeZ);
    multiplyShort(negativeZ,t0,denominator,r);
    const numerator=word([modulus,denominator],1);
    const answer=word([modulus,denominator],1);
    multiplyShort(modulus,r,null,numerator);
    accumulate(z,numerator,1);
    divideWords(numerator,denominator,answer,rNew);
    if (!isZero(rNew)) throw new Error('inexact final division');
    copyWord(answer,output);
  }
  // Rewind happens in every word routine. Clear parked work before returning it for reuse.
  for (const t of scratch) if (t!==output) clearWord(t);
  return {output,tapes:[x,magnitude,denominator,modulus,...scratch]};
}

// Independent finite oracle and harness. No whole-word operation below is used by the machine.
function inputWord(n,width) {
  const bits=[];
  for (let i=0; i<width; i++) {
    bits.push(Number(n & 1n));
    n >>= 1n;
  }
  if (n!==0n) throw new Error('test word too narrow');
  return new Tape([...bits,RIGHT]);
}
function decode(word) {
  let out=0n;
  for (let i=word.cells.indexOf(RIGHT)-1; i>0; i--) {
    out=2n*out+BigInt(word.cells[i]);
  }
  return out;
}
function egcd(a,b) {
  let x=1n,y=0n;
  while(b!==0n) {
    const q=a/b;
    [a,b]=[b,a%b]; [x,y]=[y,x-q*y];
  }
  return [a,x];
}
function verify() {
  let checked=0, nonunits=0, maxTapes=0, maxCellRatio=0, maxWorkRatio=0;
  const sizes=[];
  function one(x,a,b,M,K,B) {
    const [g,inv]=egcd(b,M);
    let result;
    try {
      result=modularScalar(inputWord(x,K),inputWord(a<0n?-a:a,B),a<0n,
        inputWord(b,B),inputWord(M,K));
    } catch (err) {
      if (g!==1n && err.message==='nonunit denominator') {
        nonunits++;
        return;
      }
      throw err;
    }
    if (g!==1n || decode(result.output)!==((x*a*inv%M)+M)%M) {
      throw new Error('oracle mismatch');
    }
    if (result.tapes.some(t=>t.head!==1)) throw new Error('displaced return head');
    const work=result.tapes.reduce((v,t)=>v+t.operations,0);
    const cells=result.tapes.reduce((v,t)=>v+1+t.highest,0);
    if (cells>7*K+16*B+58) throw new Error('tape capacity exceeded');
    const wr=work/(K*B+B**3+K+B), cr=cells/(K+B+1);
    maxWorkRatio=Math.max(maxWorkRatio,wr);
    maxCellRatio=Math.max(maxCellRatio,cr);
    maxTapes=Math.max(maxTapes,result.tapes.length);
    checked++;
    return {K,B,work,cells};
  }
  for (let m=2; m<=13; m++) for (let x=0; x<m; x++) {
    for (let a=-3; a<=3; a++) for (let b=1; b<=6; b++) {
      one(BigInt(x),BigInt(a),BigInt(b),BigInt(m),m.toString(2).length,3);
    }
  }
  // Include leading zero pads, signed inputs, composite and even moduli,
  // modulus-sized residues, and consecutive Fibonacci Euclidean inputs.
  for (const K of [8,16,32,64,96,128]) for (const B of [3,7,12]) {
    if (B>K) continue;
    const mask=(1n<<BigInt(B))-1n;
    const denom=mask<3n?3n:mask;
    const target=1n<<BigInt(K-1);
    const M=(target/denom+1n)*denom+1n;
    const record=one(M-1n,-(mask-1n),denom,M,K,B);
    if(record) sizes.push(record);
  }
  for (const [b,M] of [[13n,21n],[89n,144n],[1597n,2584n],[10946n,17711n]]) {
    one(M-1n,-7n,b,M,M.toString(2).length+2,b.toString(2).length+2);
  }
  return {valid:checked,rejectedNonunits:nonunits,maxTapes,maxCellRatio,maxWorkRatio,sizes};
}
console.log(JSON.stringify(verify(),null,2));
