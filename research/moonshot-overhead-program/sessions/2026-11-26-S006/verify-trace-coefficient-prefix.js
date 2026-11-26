"use strict";

// Compare the fixed scans on binary coefficients with ordinary polynomial
// long division. The small-field cases also check the actual bundle roots.
const assert = require("node:assert/strict");

function traceDegrees(c) {
  const terms = new Set();
  for (const value of [1, 2 ** c, 2 ** (2 * c)]) {
    for (const degree of [value, 2 * value]) {
      if (terms.has(degree)) terms.delete(degree);
      else terms.add(degree);
    }
  }
  return [...terms].sort((left, right) => left - right);
}

function lowProduct(bits, lowerDegrees) {
  const out = new Uint8Array(bits.length);
  for (const shift of lowerDegrees)
    for (let i = 0; i < bits.length - shift; i++) out[i + shift] ^= bits[i];
  return out;
}
function topProduct(bits, lowerDegrees) {
  const out = new Uint8Array(bits.length);
  for (const shift of lowerDegrees)
    for (let i = 0; i < shift; i++) out[i] ^= bits[bits.length - shift + i];
  return out;
}
function add(left, right) {
  const out = left.slice();
  for (let i = 0; i < out.length; i++) out[i] ^= right[i];
  return out;
}
function divideRecord(bits, degrees) {
  const h = bits.length / 2;
  const low = bits.slice(0, h);
  const high = bits.slice(h);
  const lowerDegrees = degrees.slice(0, -1);
  assert.equal(degrees.at(-1), h);
  assert.ok(lowerDegrees.every(degree => degree <= h / 2));
  const quotient = add(high, topProduct(high, lowerDegrees));
  return [add(low, lowProduct(quotient, lowerDegrees)), quotient];
}
function joinRecord(low, quotient, degrees) {
  const lowerDegrees = degrees.slice(0, -1);
  const out = new Uint8Array(2 * low.length);
  out.set(add(low, lowProduct(quotient, lowerDegrees)), 0);
  out.set(add(quotient, topProduct(quotient, lowerDegrees)), low.length);
  return out;
}
function pack(bits) {
  let value = 0n;
  for (let end = bits.length; end > 0; end -= 32) {
    const begin = Math.max(0, end - 32);
    let limb = 0;
    for (let i = end - 1; i >= begin; i--) limb = 2 * limb + bits[i];
    value = (value << BigInt(end - begin)) + BigInt(limb);
  }
  return value;
}
function bitLength(value) {
  return value === 0n ? 0 : value.toString(2).length;
}
function ordinaryDivide(f, divisor, h) {
  let quotient = 0n;
  for (let shift = bitLength(f) - h - 1; shift >= 0; shift--) {
    if ((f >> BigInt(shift + h)) & 1n) {
      quotient |= 1n << BigInt(shift);
      f ^= divisor << BigInt(shift);
    }
  }
  return [f, quotient];
}
function sparseTimes(value, degrees) {
  let product = 0n;
  for (const degree of degrees) product ^= value << BigInt(degree);
  return product;
}

let state = 0x52512467;
function randomWord() {
  state ^= state << 13;
  state ^= state >>> 17;
  state ^= state << 5;
  return state >>> 0;
}
function input(q, pattern) {
  const bits = new Uint8Array(q);
  if (pattern === 0) return bits;
  if (pattern === 1) return bits.fill(1);
  if (pattern === 2) {
    for (const i of [0, 1, q / 2 - 1, q / 2, 3 * q / 4, q - 1]) bits[i] = 1;
    return bits;
  }
  for (let j = 0; j < q; j += 32) {
    const word = randomWord();
    for (let bit = 0; bit < 32 && j + bit < q; bit++) bits[j + bit] = (word >>> bit) & 1;
  }
  return bits;
}

function fieldMul(x, y, q, modulus) {
  let z = 0;
  while (y) {
    if (y & 1) z ^= x;
    y >>>= 1;
    x <<= 1;
    if (x & q) x ^= modulus;
  }
  return z;
}
function fieldPower(x, degree, q, modulus) {
  let result = 1;
  while (degree) {
    if (degree % 2) result = fieldMul(result, x, q, modulus);
    x = fieldMul(x, x, q, modulus);
    degree = Math.floor(degree / 2);
  }
  return result;
}
function fieldEval(bits, x, q, modulus) {
  let value = 0;
  for (let i = bits.length - 1; i >= 0; i--) value = fieldMul(value, x, q, modulus) ^ bits[i];
  return value;
}

const moduli = new Map([[3, 11], [6, 67], [9, 515], [12, 4105]]);
const summary = { degrees: [], ordinaryDivisions: 0, polynomialIdentities: 0,
  prefixRoundTrips: 0, fieldEvaluations: 0, fieldPointsClassified: 0,
  negativeControls: { missingFeedback: false, wrongOrder: false, omittedTerm: false } };

for (const b of [3, 6, 9, 12, 15, 18]) {
  const c = b / 3, q = 2 ** b, m = c - 1;
  const base = traceDegrees(c), v = base.at(-1);
  const modulus = moduli.get(b);
  const byValue = new Map();
  if (modulus) {
    for (let z = 0; z < q; z++) {
      const t = z ^ fieldPower(z, 2 ** c, q, modulus) ^ fieldPower(z, 2 ** (2 * c), q, modulus);
      const value = fieldMul(t, t, q, modulus) ^ t;
      assert.equal(value, base.reduce((s, degree) => s ^ fieldPower(z, degree, q, modulus), 0));
      if (!byValue.has(value)) byValue.set(value, []);
      byValue.get(value).push(z);
      summary.fieldPointsClassified++;
    }
    assert.equal(byValue.size, q / v);
    assert.ok([...byValue.values()].every(points => points.length === v));
  }
  const patterns = b <= 12 ? 9 : 4;
  for (let pattern = 0; pattern < patterns; pattern++) {
    const original = input(q, pattern);
    let records = [original];
    const used = [];
    for (let depth = 0; depth <= m; depth++) {
      let back = records;
      for (const degrees of used.slice().reverse()) {
        const preceding = [];
        for (let i = 0; i < back.length; i += 2)
          preceding.push(joinRecord(back[i], back[i + 1], degrees));
        back = preceding;
      }
      assert.deepEqual(back[0], original);
      summary.prefixRoundTrips++;
      if (depth === m) break;
      const degrees = base.map(degree => degree * 2 ** (m - depth - 1));
      const h = degrees.at(-1), divisor = sparseTimes(1n, degrees);
      const next = [];
      for (const parent of records) {
        const [low, high] = divideRecord(parent, degrees);
        const a = pack(low), vhigh = pack(high), f = pack(parent);
        assert.equal(a ^ sparseTimes(vhigh, degrees), f);
        summary.polynomialIdentities++;
        if (b <= 12) {
          assert.deepEqual([a,vhigh], ordinaryDivide(f, divisor, h));
          summary.ordinaryDivisions++;
        }
        if (vhigh !== pack(parent.slice(h))) summary.negativeControls.missingFeedback = true;
        if ((vhigh ^ sparseTimes(a, degrees)) !== f) summary.negativeControls.wrongOrder = true;
        if ((a ^ sparseTimes(vhigh, degrees.slice(1))) !== f) summary.negativeControls.omittedTerm = true;
        next.push(low, high);
      }
      records = next;
      used.push(degrees);
    }
    if (modulus) {
      for (const [value, points] of byValue) {
        const samples = b <= 9 ? points : [points[0], points[Math.floor(points.length / 2)], points.at(-1)];
        for (const z of samples) {
          let y = 0;
          for (let j = records.length - 1; j >= 0; j--)
            y = fieldMul(y, value, q, modulus) ^ fieldEval(records[j], z, q, modulus);
          assert.equal(y, fieldEval(original,z,q,modulus));
          summary.fieldEvaluations++;
        }
      }
    }
  }
  summary.degrees.push({degree:b, levels:m, kernelSize:v, inputs:patterns});
}
assert.ok(Object.values(summary.negativeControls).every(Boolean));
console.log(JSON.stringify(summary, null, 2));
