import «compiler-binary-access»

/-! Enumerate the complete literal rule, including every malformed scanned tuple. -/

open OAI.Computability.IntegerMultiplication
open S008.Compiler

private def letters : List Letter := [.blank,.home,.bit false,.bit true,.delimiter,.count]
private def stages : List Binary.Stage :=
  [.prepare .read,.prepare (.first false),.prepare (.first true),
   .prepare (.second false),.prepare (.second true),.prepare .restore,.prepare .suffix,
   .prepare (.home .before),.prepare (.home .after),.prepare (.home .finalOutput),
   .prepare (.home .finalDigits),.prepare .done,
   .useWord (.seek .check),.useWord (.seek .scan),.useWord (.seek .done),.useWord .copy,
   .useWord (.home .bank),.useWord (.home .index),.useWord (.home .value),.useWord .done,
   .erase,.back,.done]

private def letterCode : Letter → Nat
  | .blank => 0 | .home => 1 | .bit false => 2 | .bit true => 3 | .delimiter => 4 | .count => 5

private def unaryCode : Unary.Phase → Nat
  | .read => 0 | .first false => 1 | .first true => 2 | .second false => 3 | .second true => 4
  | .restore => 5 | .suffix => 6 | .home .before => 7 | .home .after => 8
  | .home .finalOutput => 9 | .home .finalDigits => 10 | .done => 11

private def transferCode : Transfer.Stage → Nat
  | .seek .check => 12 | .seek .scan => 13 | .seek .done => 14 | .copy => 15
  | .home .bank => 16 | .home .index => 17 | .home .value => 18 | .done => 19

private def stageCode : Binary.Stage → Nat
  | .prepare p => unaryCode p | .useWord p => transferCode p
  | .erase => 20 | .back => 21 | .done => 22

private def moveCode : TM.Move → Nat
  | .left => 0 | .stay => 1 | .right => 2

private def opCode (v : Letter × TM.Move) : Nat := 3 * letterCode v.1 + moveCode v.2

def main : IO Unit := do
  for mode in [false,true] do
    for q in stages do
      for a in letters do
        for z in letters do
          for v in letters do
            for i in letters do
              for h in letters do
                let read : Binary.Port → Letter := fun
                  | .bank => a | .digits => z | .value => v | .index => i | .work => h
                match Binary.rule mode q read with
                | none => IO.println "-"
                | some (fixed, action) =>
                  IO.println s!"{stageCode fixed} {opCode (action .bank)} {opCode (action .digits)} {opCode (action .value)} {opCode (action .index)} {opCode (action .work)}"
