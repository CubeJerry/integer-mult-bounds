// Finite exact controls for the modular Walsh proof. Run with Node.js 20+.
// BigInt is used throughout the arithmetic. These checks do not simulate
// the large adaptive routing program or its asymptotic resource bounds.

function assert(condition, description) {
  if (!condition) throw new Error(description);
}

function abs(value) {
  return value < 0n ? -value : value;
}

function mod(value, modulus) {
  return ((value % modulus) + modulus) % modulus;
}

function inverse(value, modulus) {
  let a = mod(value, modulus);
  let b = modulus;
  let first = 1n;
  let second = 0n;
  while (b !== 0n) {
    const quotient = a / b;
    [a, b] = [b, a - quotient * b];
    [first, second] = [second, first - quotient * second];
  }
  if (a !== 1n) throw new Error("nonunit");
  return mod(first, modulus);
}

function divideSmall(residue, denominator, modulus) {
  if (denominator === 1n) return residue;
  const inverseOfModulus = inverse(modulus % denominator, denominator);
  const correction = mod(-residue * inverseOfModulus, denominator);
  const numerator = residue + correction * modulus;
  assert(numerator % denominator === 0n, "division must be ordinary and exact");
  const result = numerator / denominator;
  assert(result >= 0n && result < modulus, "quotient outside its canonical range");
  assert(mod(denominator * result, modulus) === residue, "quotient has wrong residue");
  return result;
}

function scale(residue, numerator, denominator, modulus) {
  return divideSmall(mod(numerator * residue, modulus), denominator, modulus);
}

function center(residue, modulus) {
  return 2n * residue > modulus ? residue - modulus : residue;
}

function expectNonunit(thunk) {
  try {
    thunk();
  } catch (error) {
    if (error.message === "nonunit") return true;
    throw error;
  }
  throw new Error("expected a nonunit to be rejected");
}

function floorSqrt(n) {
  if (n < 2n) return n;
  let estimate = 1n << BigInt(Math.ceil(n.toString(2).length / 2));
  while (true) {
    const next = (estimate + n / estimate) / 2n;
    if (next >= estimate) return estimate;
    estimate = next;
  }
}

function parity(n) {
  let result = 0;
  while (n > 0) {
    result ^= 1;
    n &= n - 1;
  }
  return result;
}

function sign(exponent) {
  return exponent % 2 === 0 ? 1n : -1n;
}

function newtonTable(m) {
  const square = 4n * BigInt(m);
  const root = floorSqrt(square);
  const window = Number(root * root === square ? root : root + 1n);
  const lower = Math.floor(m / 2) - window;
  const degree = Math.ceil(m / 2) + window - lower;
  const values = [];
  for (let count = 0; count <= m; count++) {
    let binomial = 1n;
    let polynomial = 1n;
    for (let h = 1; h <= degree; h++) {
      const product = binomial * BigInt(count - lower - h + 1);
      assert(product % BigInt(h) === 0n, "generalized binomial is integral");
      binomial = product / BigInt(h);
      polynomial += (-2n) ** BigInt(h) * binomial;
    }
    values.push(polynomial);
  }
  return { lower, degree, values };
}

function supportedModulus(seeds, degree, values) {
  let support = 2n;
  for (let i = 2; i <= Math.max(seeds, degree); i++) support *= BigInt(i);
  for (const value of values) {
    for (const gamma of [-1n, 1n]) {
      for (const target of [-1n, 1n]) {
        const gap = gamma * value - target;
        if (gap !== 0n) support *= abs(gap);
      }
    }
  }
  return 1n + (support << 32n);
}

const smallModulus = 1n + (2n * 3n * 5n * 7n * 11n << 41n);
let scalarCases = 0;
for (const a of [-51n, 0n, 1n, 105n]) {
  for (const b of [1n, 2n, 3n, 7n, 15n, 49n, 55n]) {
    for (const z of [0n, 1n, 22n, smallModulus - 1n]) {
      const reference = mod(z * a * inverse(b, smallModulus), smallModulus);
      assert(scale(z, a, b, smallModulus) === reference, "small scalar mismatch");
      scalarCases++;
    }
  }
}
expectNonunit(() => divideSmall(1n, 6n, 15n));

// All actual node spacings and Newton update divisors are units modulo 73.
// This particular nonzero numerator gap is divisible by 73.
const adverse = newtonTable(63);
const gap63 = sign(adverse.lower) * adverse.values[0] - 1n;
assert(adverse.lower === 15 && adverse.degree === 33, "wrong adverse parameters");
assert(gap63 === -4510048854467219030016n && gap63 % 73n === 0n, "missing-gap witness");
expectNonunit(() => divideSmall(1n, abs(gap63), 73n ** 3n));

// Test the actual two Vandermonde inverses and gap division on a multi-defect key.
const arity = 127;
const seeds = 128;
const table = newtonTable(arity);
const M = supportedModulus(seeds, table.degree, table.values);
const key = Array.from({ length: arity }, (_, j) => Number(j < 64 && (j + 1) % 2 === 1));
const target = sign(key.reduce((sum, bit) => sum + bit, 0));
const defects = [];
for (let t = 0; t < seeds; t++) {
  let count = 0;
  let shiftWeight = 0;
  for (let j = 0; j < arity; j++) {
    const shift = parity((j + 1) & t);
    shiftWeight += shift;
    count += key[j] ^ shift;
  }
  const gap = sign(table.lower - shiftWeight) * table.values[count] - target;
  if (gap !== 0n) defects.push({ index: t, gap });
}
assert(defects.length >= 2 && defects.length <= seeds / 16, "multi-defect key");
const indices = defects.map(item => BigInt(item.index));
const lagrange = indices.map((i, row) => {
  let coefficients = [1n];
  let denominator = 1n;
  for (let v = 0; v < indices.length; v++) {
    if (v === row) continue;
    const h = indices[v];
    const next = Array(coefficients.length + 1).fill(0n);
    for (let j = 0; j < coefficients.length; j++) {
      next[j] -= h * coefficients[j];
      next[j + 1] += BigInt(seeds) * coefficients[j];
    }
    coefficients = next;
    denominator *= i - h;
  }
  const numeratorSign = denominator < 0n ? -1n : 1n;
  return coefficients.map(c => scale(1n, numeratorSign * c, abs(denominator), M));
});
const nodes = indices.map(i => scale(1n, i, BigInt(seeds), M));
const V = indices.map((_, row) => nodes.map(x => mod(x ** BigInt(row), M)));
const dot = (a, b) => mod(a.reduce((sum, value, i) => sum + value * b[i], 0n), M);
const input = indices.map((_, row) => mod(BigInt(31 * row - 73), M));
const errors = input.map((z, row) => mod(z * defects[row].gap, M));
const checks = V.map(row => dot(row, errors));
const recovered = lagrange.map((row, i) => {
  const gap = defects[i].gap;
  return scale(dot(row, checks), gap < 0n ? -1n : 1n, abs(gap), M);
});
const lifts = indices.map((_, j) => dot(lagrange.map(row => row[j]), recovered));
assert(recovered.every((z, j) => z === input[j]), "V inverse and true gap");
assert(indices.every((_, j) => dot(V.map(row => row[j]), lifts) === input[j]), "transpose inverse");

// Exercise all selected masks up to seven address bits, including noncontiguous bits.
let exactOutputs = 0;
for (let k = 1; k <= 7; k++) {
  const N = 2 ** k;
  const row = Array.from({ length: N }, (_, j) => BigInt((j * 47 + 11) % 251 - 125));
  for (let mask = 0; mask < N; mask++) {
    const selected = Array.from({ length: k }, (_, i) => i).filter(i => mask & (1 << i));
    const even = selected.length - selected.length % 2;
    const shift = 1n << BigInt(even / 2);
    const values = row.map(z => mod(z * shift, smallModulus));
    for (let i = 0; i < selected.length; i++) {
      const bit = 1 << selected[i];
      const denominator = i < even && i % 2 === 1 ? 2n : 1n;
      for (let j = 0; j < N; j++) {
        if (j & bit) continue;
        const left = values[j];
        const right = values[j | bit];
        values[j] = divideSmall(mod(left + right, smallModulus), denominator, smallModulus);
        values[j | bit] = divideSmall(mod(left - right, smallModulus), denominator, smallModulus);
      }
    }
    for (let j = 0; j < N; j++) {
      let expected = 0n;
      for (let t = 0; t < N; t++) {
        if (((t ^ j) & ~mask) === 0) expected += sign(parity(t & j & mask)) * row[t];
      }
      assert(center(values[j], smallModulus) === expected, "selected numerator");
      exactOutputs++;
    }
  }
}
assert(center(40n, 65n) === -25n, "insufficient recovery modulus must wrap");

// In the finite test J is deliberately chosen from the magnitude to exercise
// the one-step midpoint correction. The production theorem uses w+s+3.
let roundingCases = 0;
let midpointCorrections = 0;
const magnitudes = Array.from({ length: 100 }, (_, i) => BigInt(i));
magnitudes.push((1n << 180n) - 1n, (1n << 180n) + 9067n);
for (let s = 0; s <= 19; s++) {
  const power = 1n << BigInt(s);
  for (const magnitude of magnitudes) {
    const J = BigInt(Math.max(s + 2, magnitude.toString(2).length + 2));
    const approximateScale = floorSqrt(1n << (2n * J - BigInt(s)));
    let rounded = (magnitude * approximateScale + (1n << (J - 1n))) >> J;
    const fourTimesSquared = 4n * magnitude * magnitude;
    if (fourTimesSquared >= power * (2n * rounded + 1n) ** 2n) {
      rounded++;
      midpointCorrections++;
    }
    const low = rounded === 0n || power * (2n * rounded - 1n) ** 2n <= fourTimesSquared;
    const high = fourTimesSquared < power * (2n * rounded + 1n) ** 2n;
    assert(low && high, "incorrect nearest rounding");
    roundingCases++;
  }
}

console.log(JSON.stringify({
  scalarCases,
  nonunitRejected: true,
  rejectedGap63: gap63.toString(),
  arity,
  defectSeeds: defects.map(item => item.index),
  supportedModulusBits: M.toString(2).length,
  exactOutputs,
  roundingCases,
  midpointCorrections
}, null, 2));
