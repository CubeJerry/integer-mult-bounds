// Run with node verify-outer-caller.mjs. Native arithmetic supplies the finite reference values.
function requireThat(condition, reason) {
  if (!condition) throw new Error(reason);
}
function gcd(a, b) {
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}
function ceilLog2(k) {
  return (BigInt(k) - 1n).toString(2).length;
}
function axes(k) {
  const w = 20 * ceilLog2(k);
  const X = 1n << BigInt(w);
  const window = X / BigInt(k * k);
  let product = 1n, misses = 0;
  const found = [];
  for (let i = 0; i < Math.floor(k / w); i++) {
    let a = X;
    while (a >= X - window && gcd(a, 2n * product) !== 1n) {
      a--;
      misses++;
    }
    requireThat(a >= X - window, 'no witness in actual search window');
    requireThat(found.every(v => gcd(a, v) === 1n) && a % 2n === 1n, 'gcd test mismatch');
    found.push(a);
    product *= a;
  }
  const rem = k % w;
  const volume = product << BigInt(rem);
  requireThat(w * found.length + rem === k, 'axis width sum');
  requireThat(2n * volume >= 1n << BigInt(k), 'less than half occupied');
  return { k, full: found.length, remainder: rem, denied: misses };
}

function choose(n, r) {
  if (r > n) return 0;
  let result = 1;
  for (let i = 1; i <= r; i++) result = result * (n - i + 1) / i;
  return result;
}
const bands = [[2, 3, 5, 7, 11, 13], [17, 19, 23, 29]];
function bandLower(bits) {
  const t = [2, 2]; // Small deliberately active truncations, for the polynomial identity.
  const counts = bands.map((v,j) => v.filter((_, i) => bits[j][i]).length);
  const upper = counts.map((n,j) => {
    let sum = 0;
    for (let i = 0; i <= t[j]; i++) sum += (-1) ** i * choose(n, i);
    return sum;
  });
  const tail = counts.map((n,j) => choose(n, t[j] + 1));
  return upper[0] * upper[1] - tail[0] * upper[1] - tail[1] * upper[0];
}
function bonferroni() {
  const primes = bands.flat(), total = 1 << primes.length;
  let weighted = 0n, absolute = 0n;
  const period = primes.reduce((n,p) => n * BigInt(p), 1n);
  for (let mask = 0; mask < total; mask++) {
    const bits = primes.map((_, i) => Boolean(mask & (1 << i)));
    const lower = bandLower([bits.slice(0,6), bits.slice(6)]);
    const hit = mask === 0 ? 1 : 0;
    requireThat(lower <= hit, 'Bonferroni pointwise sign');
    const count = primes.reduce((n,p,i) => n * (bits[i] ? 1n : BigInt(p-1)), 1n);
    weighted += BigInt(lower) * count;
    absolute += BigInt(hit) * count;
  }
  requireThat(weighted <= absolute && absolute < period, 'independent model');
  // Two odd first-order lower truncations can both be negative.
  requireThat((1-2)*(1-2) > 0, 'wrong-sign adverse control');
  const massUpper = 2 * Math.log(2) + 3 / 32;
  const tailUpper = 5 * (1.5 ** 5 / 120) / (1 - 2.25 / 42);
  requireThat(massUpper < 1.5 && tailUpper < 0.34, 'displayed scalar bounds');
  return { patterns: total, bandMassUpper: massUpper, relativeLossUpper: tailUpper };
}

function toom3(a, b, audit) {
  if (a < 0n) return -toom3(-a, b, audit);
  if (b < 0n) return -toom3(a, -b, audit);
  const bits = Math.max(a.toString(2).length, b.toString(2).length);
  if (bits <= 30) return a * b;
  audit.nodes++;
  const shift = BigInt(Math.ceil(bits / 3)), base = 1n << shift;
  const split = x => [x % base, (x >> shift) % base, x >> (2n * shift)];
  const [a0,a1,a2] = split(a), [b0,b1,b2] = split(b);
  const evalAt = (c0,c1,c2,v) => c0 + v*(c1+v*c2);
  const point = v => toom3(evalAt(a0,a1,a2,v), evalAt(b0,b1,b2,v), audit);
  const c0 = toom3(a0,b0,audit), c4 = toom3(a2,b2,audit);
  const plus = point(1n), minus = point(-1n), twice = point(2n);
  const exact = (x,d) => {
    requireThat(x % d === 0n, 'nonexact interpolation division');
    return x / d;
  };
  const c2 = exact(plus + minus,2n) - c0 - c4;
  const diff = exact(plus - minus,2n);
  const three = exact(twice - c0 - 4n*c2 - 16n*c4,2n) - diff;
  const c3 = exact(three,3n), c1 = diff - c3;
  return c0 + base*(c1 + base*(c2 + base*(c3 + base*c4)));
}
function products() {
  const values = [0n, 1n, -1n], audit = {nodes: 0};
  for (const k of [29,30,31,32,64,95,96,97,129,251,513]) {
    const v = 1n << BigInt(k);
    values.push(v-1n, -(v+3n), v/3n+7n);
  }
  let pairs = 0;
  for (const a of values) for (const b of values) {
    requireThat(toom3(a,b,audit) === a*b, 'Toom product mismatch');
    pairs++;
  }
  return {pairs, recursiveNodes: audit.nodes};
}
const widths = [257,300,600,1200,1540,2640,3120,4096,8320,16384];
console.log(JSON.stringify({axes: widths.map(axes), sieve: bonferroni(), toom: products()}, null, 2));
