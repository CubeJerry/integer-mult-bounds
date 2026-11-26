// Independent review of the fixed-head Walsh scalar, including its exact receipt.
// Save beside modular-scalar-machine.mjs and run node verify-scalar-heads.mjs.
// A different location for the primary source may be given as the first argument.
//
// Four distinct, nonempty marked words supply x, |a|, b and M. The sign is
// finite control. In the reducing short multiply, each double and subsequent
// addition is separately reduced, so its K+1-bit word suffices. Every division
// remainder fits B+1 bits. The Euclidean clocks are O(B) decreasing steps
// at O(B^2) head operations each, including multiplication by the quotient.
// For 0<=r<b and 0<=z<M, z+rM<bM, within the K+B+1-bit numerator. The scans
// give O(KB+B^3) initial-to-restored-head work. The long path uses four
// input words, three K-scale words, twelve short words and two long dividend
// words. Including both marks yields at most 7K+16B+58 cells on 21 tapes.
// Each successful return leaves all heads on the low digit, input contents
// unchanged and designated scratch digits zero with their right marks intact.
//
// The generated cases also compare the unique canonical modular congruence,
// include B>K and exercise leading zeros, zero magnitudes and nonunits.
// These are exact finite controls for the stated primitive. The full kernel
// and its asymptotic resource bounds are supported by the separate proof.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";

const path = process.argv[2] ?? new URL("./modular-scalar-machine.mjs", import.meta.url);
const source = readFileSync(path, "utf8");
const size = Buffer.byteLength(source, "utf8");
const digest = createHash("sha1").update("blob " + size + "\0").update(source).digest("hex");
if (digest !== "ac42d10bf0575fc7b39dd46d370840f9106a9282") {
  throw Error("expected the pinned fixed-head source, found " + digest);
}
const footer = "console.log(JSON.stringify(verify(),null,2));";
const trimmed = source.trimEnd();
if (!trimmed.endsWith(footer)) throw Error("missing pinned demonstration footer");
const declarations = trimmed.slice(0, -footer.length);
const machine = new Function(declarations + "\nreturn { Tape, modularScalar };")();

function auditFixedHeads({ Tape, modularScalar }) {
  const LEFT = "[";
  const RIGHT = "]";
  const abs = n => n < 0n ? -n : n;

  function input(value, width) {
    if (width < 1 || value < 0n) throw Error("invalid test input");
    const digits = [];
    for (let i = 0; i < width; i++) {
      digits.push(Number(value & 1n));
      value >>= 1n;
    }
    if (value !== 0n) throw Error("test word too narrow");
    return new Tape([...digits, RIGHT]);
  }

  function decode(tape) {
    const stop = tape.cells.indexOf(RIGHT);
    if (tape.cells[0] !== LEFT || stop < 2) throw Error("invalid output marks");
    let value = 0n;
    for (let i = stop - 1; i > 0; i--) {
      const bit = tape.cells[i];
      if (bit !== 0 && bit !== 1) throw Error("invalid output digit");
      value = 2n * value + BigInt(bit);
    }
    return value;
  }

  function gcd(a, b) {
    while (b !== 0n) [a, b] = [b, a % b];
    return a;
  }

  // A unit has a unique canonical solution to b*y = x*a mod M. The
  // oracle checks this identity without reusing either extended-Euclid code.
  let total = 0;
  let valid = 0;
  let nonunits = 0;
  let widerCoefficient = 0;
  let zeroMagnitude = 0;
  let maxValidK = 0;
  let maxValidB = 0;

  function one(x, a, b, M, K, B) {
    const words = [input(x,K), input(abs(a),B), input(b,B), input(M,K)];
    const snapshot = words.map(tape => tape.cells.join(""));
    const unit = gcd(b,M) === 1n;
    let run;
    try {
      run = modularScalar(words[0], words[1], a < 0n, words[2], words[3]);
    } catch (error) {
      if (unit || error.message !== "nonunit denominator") throw error;
      nonunits++;
      total++;
      return;
    }
    if (!unit) throw Error("accepted a nonunit denominator");
    const y = decode(run.output);
    if (y < 0n || y >= M || (b*y - x*a) % M !== 0n) throw Error("congruence");
    if (words.some((t,i) => t.cells.join("") !== snapshot[i])) throw Error("input modified");
    for (const tape of run.tapes) {
      if (tape.head !== 1 || tape.highest > tape.cells.indexOf(RIGHT)) {
        throw Error("displaced head or excursion past the word mark");
      }
    }
    for (const tape of run.tapes.slice(4)) {
      if (tape === run.output) continue;
      if (tape.cells.slice(1, tape.cells.indexOf(RIGHT)).some(bit => bit !== 0)) {
        throw Error("uncleared scratch digits");
      }
    }
    const visited = run.tapes.reduce((sum,tape) => sum + tape.highest + 1, 0);
    if (run.tapes.length > 21 || visited > 7*K+16*B+58) throw Error("workspace cap");
    valid++;
    total++;
    if (B > K) widerCoefficient++;
    if (a === 0n) zeroMagnitude++;
    maxValidK = Math.max(maxValidK, K);
    maxValidB = Math.max(maxValidB, B);
  }

  let state = 0x4c4142;
  function random32() {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state;
  }
  function randomBits(count) {
    let x = 0n;
    for (let i = 0; i < count; i += 32) x = (x << 32n) | BigInt(random32());
    return x % (1n << BigInt(count));
  }

  for (let i = 0; i < 3200; i++) {
    const K = 2 + random32() % 95;
    const B = 1 + random32() % 43;
    const M = 2n + randomBits(1 + random32() % (K-1));
    const x = randomBits(K) % M;
    const candidateB = 1n + randomBits(Math.max(1, B-1));
    const b = candidateB >= (1n << BigInt(B)) ? 1n : candidateB;
    const a = i % 19 === 0 ? 0n : randomBits(B) * (i % 2 === 0 ? -1n : 1n);
    one(x,a,b,M,K,B);
  }

  const edgeCases = [
    [0n,0n,1n,2n,10,27],
    [1n,1n,2n**71n+1n,2n,2,72],
    [1n,-1n,2n**91n+1n,3n,2,96],
    [1n,2n**65n-1n,2n**63n-1n,2n,2,66],
    [0n,-6n,1n,17n,90,12]
  ];
  for (const args of edgeCases) one(...args);

  const receipt = {total, valid, nonunits, widerCoefficient, zeroMagnitude, maxValidK, maxValidB};
  const expected = {
    total: 3205, valid: 2113, nonunits: 1092, widerCoefficient: 440,
    zeroMagnitude: 173, maxValidK: 96, maxValidB: 72
  };
  if (JSON.stringify(receipt) !== JSON.stringify(expected)) throw Error("unexpected receipt");
  return receipt;
}

console.log(JSON.stringify(auditFixedHeads(machine), null, 2));
