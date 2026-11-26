import NodeSymbolic
import NodeTables

/-! The symbolic coordinate oracles below name every input bit independently.
    Certificates give the actual physical clock and visited set on the fixed geometries. -/

namespace S008.SymbolicCases

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource (Table)
open S008.NodeTables (direct copyRole xorRole)
open S008.Symbolic

set_option maxRecDepth 100000
set_option maxHeartbeats 12000000

def variableBit (i : ℕ) : Glyph := .bits (.input i)
def dataBits (start width : ℕ) : List Glyph := (List.range width).map (fun i => variableBit (start+i))
def fixedDigits (s : String) : List Glyph := (S008.NodeTables.decode s).map Glyph.fixed

def directInput (p w gap suffix : ℕ) (e g s : String) : Array (List Glyph) :=
  #[dataBits 0 (p*w*gap*w*suffix),fixedDigits e,fixedDigits g,fixedDigits s]

/-- Interpret destination position in [prefix][y][gap][x][suffix], then read the
    indicated source position in [prefix][x][gap][y][suffix]. -/
def directOutput (p w gap suffix : ℕ) (e g s : String) : Vector WindowS 17 :=
  let data := (List.range (p*w*gap*w*suffix)).map (fun i =>
    let b := i/suffix
    let x := b%w
    let gpos := (b/w)%gap
    let y := (b/(w*gap))%w
    let outer :=  b/(w*gap*w)
    variableBit ((((outer*w+x)*gap+gpos)*w+y)*suffix+i%suffix))
  home #[data,fixedDigits e,fixedDigits g,fixedDigits s]

def roleInput (p j k suffix : ℕ) (desc : List String) : Array (List Glyph) :=
  (dataBits 0 (p*j*suffix) :: dataBits (p*j*suffix) (p*k*suffix) :: desc.map fixedDigits).toArray

/-- A source and a destination bit are named independently even at matching positions. -/
def roleOutput (p j k source dest suffix : ℕ) (xor : Bool) (desc : List String) : Vector WindowS 15 :=
  let alen := p*j*suffix
  let data := (List.range (p*k*suffix)).map (fun i =>
    let old := alen+i
    if i/suffix%k=dest then
       let a := ((i/(suffix*k))*j+source)*suffix+i%suffix
       if xor then Glyph.bits (.xor (.input a) (.input old)) else variableBit a
    else variableBit old)
  home ((dataBits 0 alen :: data :: desc.map fixedDigits).toArray)

def Outcome {k s : ℕ} (p : Table k s) (entry : Fin (s+1)) (data : Array (List Glyph))
    (clock cells : ℕ) (dest : Vector WindowS k) : Prop :=
  ∀ v : ℕ → Bool, ∃ c : TM.Config Letter (Fin (s+1)) (Fin k),
    Trace (TM.advance (S008.NodeSource.rule p)) (S008.NodeSource.physical ((initial entry data).eval v)) clock c ∧
    TM.advance (S008.NodeSource.rule p) c=none ∧
    VisitsAtMost (S008.NodeSource.rule p) (S008.NodeSource.physical ((initial entry data).eval v)) clock cells ∧
    ∀ i : Fin k, c.tape i=(dest[i].eval v).physical

abbrev input9 := directInput 1 3 1 1 "1" "1" "1"
abbrev result9 := directOutput 1 3 1 1 "1" "1" "1"
abbrev input72 := directInput 2 3 2 2 "1" "10" "10"
abbrev result72 := directOutput 2 3 2 2 "1" "10" "10"
abbrev input81 := directInput 1 9 1 1 "10" "1" "1"
abbrev result81 := directOutput 1 9 1 1 "10" "1" "1"
abbrev descriptors := ["11","100","10","1","10"]
abbrev role28 := roleInput 2 3 4 2 descriptors

#guard check direct 168 input9 296 59 result9
#guard check direct 168 input72 1086 190 result72
#guard check direct 168 input81 2521 211 result81
#guard check copyRole 137 role28 490 86 (roleOutput 2 3 4 2 1 2 false descriptors)
#guard check xorRole 137 role28 490 86 (roleOutput 2 3 4 2 1 2 true descriptors)

end S008.SymbolicCases
