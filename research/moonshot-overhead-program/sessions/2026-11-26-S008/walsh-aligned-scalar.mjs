// Numerically costed specialization of the pinned fixed-head Walsh scalar.
// The data routine uses only the charged tape primitives imported below.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const base = new URL('../../contributions/explicit-overhead/modular-scalar-machine.mjs', import.meta.url);
const source = readFileSync(base, 'utf8');
const hash = createHash('sha1').update('blob ' + Buffer.byteLength(source) + '\0' + source).digest('hex');
assert.equal(hash, 'ac42d10bf0575fc7b39dd46d370840f9106a9282');
const footer = 'console.log(JSON.stringify(verify(),null,2));';
assert(source.trimEnd().endsWith(footer));
const primitives = new Function(source.trimEnd().slice(0, -footer.length) +
  '\nreturn { Tape, allocateWord, clearWord, isZero, isOne, copyWord, accumulate, ' +
  'divideWords, multiplyShort, compareWords, inputWord, decode };')();
const { Tape, allocateWord, clearWord, isZero, isOne, copyWord, accumulate,
  divideWords, multiplyShort, compareWords, inputWord, decode } = primitives;

// Requires 0 <= x < M, M >= 2, b > 0, and b dividing M-1.
// Every input head starts at the low digit. The sign is a finite control bit.
export function alignedScalar(x, magnitude, negative, denominator, modulus) {
  const work = [];
  function word(parts, extra = 0) {
    const tape = new Tape();
    work.push(tape);
    allocateWord(parts, extra, tape);
    return tape;
  }
  if (isZero(modulus) || isOne(modulus) || compareWords(x, modulus) >= 0 ||
      isZero(denominator)) throw Error('malformed scalar input');
  const z = word([modulus], 1);
  const spare = word([modulus], 1);
  const output = word([modulus]);
  multiplyShort(x, magnitude, modulus, z);
  if (negative && !isZero(z)) {
    copyWord(modulus, spare);
    accumulate(z, spare, -1);
    copyWord(spare, z);
  }
  if (isOne(denominator)) {
    copyWord(z, output);
  } else {
    const remainder = word([denominator], 1);
    const r = word([denominator], 1);
    divideWords(z, denominator, null, remainder);
    if (!isZero(remainder)) {
      copyWord(denominator, r);
      accumulate(remainder, r, -1);
    }
    const numerator = word([modulus, denominator], 1);
    const quotient = word([modulus, denominator], 1);
    multiplyShort(modulus, r, null, numerator);
    accumulate(z, numerator, 1);
    divideWords(numerator, denominator, quotient, remainder);
    if (!isZero(remainder)) throw Error('inexact aligned division');
    copyWord(quotient, output);
  }
  for (const t of work) if (t !== output) clearWord(t);
  return { output, tapes: [x, magnitude, denominator, modulus, ...work] };
}

// The remainder of this file is the finite oracle. It does not execute on the tapes.
export function checkScalar(x, a, b, M, K, B, budget) {
  assert.equal((M - 1n) % b, 0n);
  const inputs = [inputWord(x, K), inputWord(a < 0n ? -a : a, B),
    inputWord(b, B), inputWord(M, K)];
  const before = inputs.map(t => t.cells.join(''));
  const { output, tapes } = alignedScalar(inputs[0], inputs[1], a < 0n, inputs[2], inputs[3]);
  const y = decode(output);
  assert(y < M && (b*y - x*a) % M === 0n);
  assert.deepEqual(inputs.map(t => t.cells.join('')), before);
  let transitions = 0, visits = 0;
  for (const t of tapes) {
    assert.equal(t.head, 1);
    assert.equal(t.highest, t.cells.indexOf(']'));
    if (!inputs.includes(t) && t !== output) assert(t.cells.slice(1, -1).every(d => d === 0));
    transitions += t.operations;
    visits += t.highest + 1;
  }
  assert(transitions + 16 <= 2048 * (K+B+3) * (B+3));
  // All eleven statically allocated heads cost one visited home even on the short branch.
  assert(visits + (11-tapes.length)*2 <= 7*K+6*B+28);
  assert(tapes.length <= 11);
  if (budget) {
    budget.count++;
    budget.moreShortDigits += B > K;
    budget.maxTapes = Math.max(budget.maxTapes, tapes.length);
    budget.maxReadsWritesMoves = Math.max(budget.maxReadsWritesMoves, transitions);
  }
  return y;
}

function test() {
  const receipt = { count: 0, moreShortDigits: 0, maxTapes: 0, maxReadsWritesMoves: 0 };
  const bits = n => n.toString(2).length;
  for (let b = 1n; b <= 10n; b++) {
    for (let m = 1n; m <= 7n; m++) {
      const M = m*b + 1n;
      for (let x = 0n; x < M; x++) {
        for (const a of [-11n, -1n, 0n, 1n, 13n]) {
          const K = bits(M) + Number((b + x) % 3n);
          const B = Math.max(bits(b), bits(a < 0n ? -a : a)) + Number((m+x) % 4n);
          checkScalar(x, a, b, M, K, B, receipt);
        }
      }
    }
  }
  // Arbitrarily padded short words and a wide long word with a large composite denominator.
  for (const b of [1n, 73n, 3n**20n, 2n**75n+1n]) {
    const M = 1n + b * (2n**191n+7n);
    for (const a of [0n, -7n, 2n**100n-1n]) checkScalar(M-1n, a, b, M,
      bits(M)+9, Math.max(104,bits(b)), receipt);
  }
  console.log(JSON.stringify(receipt));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) test();
