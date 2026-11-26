import «compiler-butterfly-stream»

/-! Byte-serializable complete transition table of the modular butterfly. -/

open OAI.Computability.IntegerMultiplication S008.Compiler

private def letters : List Letter := [.blank,.home,.bit false,.bit true,.delimiter,.count]
private def stages : List Butterfly.Stage := Butterfly.flagsList.map .forward ++
  [.returning false false,.returning false true,.returning true false,.returning true true,.halt]

private def lc : Letter → Nat
  | .blank => 0 | .home => 1 | .bit false => 2 | .bit true => 3 | .delimiter => 4 | .count => 5

private def sc : Butterfly.Stage → Nat
  | .forward f => 8*Butterfly.val f.sc+4*Butterfly.val f.db+2*Butterfly.val f.sb+Butterfly.val f.dc
  | .returning u v => 16+2*Butterfly.val u+Butterfly.val v
  | .halt => 20

private def opcode (v : Letter × TM.Move) : Nat := 3*lc v.1 + match v.2 with
  | .left => 0 | .stay => 1 | .right => 2

private def writeTable {Q : Type} (qs : List Q) (step : TM.Rule Letter Q Butterfly.Port)
    (code : Q → Nat) : IO Unit := do
  for q in qs do
    for a in letters do
      for b in letters do
        for m in letters do
          for u in letters do
            for v in letters do
              let read : Butterfly.Port → Letter := fun
                | .a => a | .b => b | .m => m | .sum => u | .diff => v
              match step q read with
              | none => IO.println "-"
              | some (q',act) =>
                IO.println s!"{code q'} {opcode (act .a)} {opcode (act .b)} {opcode (act .m)} {opcode (act .sum)} {opcode (act .diff)}"

private def stc : ButterflyStream.Stage → Nat
  | .dispatch => 0 | .call part => 1+sc part | .skip => 22 | .marker => 23
  | .rewind => 24 | .origin => 25 | .done => 26

def main (args : List String) : IO Unit :=
  if args == ["--stream"] then
    writeTable ([.dispatch] ++ stages.map .call ++ [.skip,.marker,.rewind,.origin,.done]) ButterflyStream.rule stc
  else writeTable stages Butterfly.rule sc
