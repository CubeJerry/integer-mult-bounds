import «compiler-indexed-transfer»

/-! Exhaustive comparison oracle for the finite state table used by indexed_access. -/

open OAI.Computability.IntegerMultiplication
open S008.Compiler S008.Compiler.Transfer

private def letters : List Letter := [.blank,.home,.bit false,.bit true,.delimiter,.count]
private def stages : List Stage := [.seek .check,.seek .scan,.seek .done,.copy,
  .home .bank,.home .index,.home .value,.done]

private def letterCode : Letter → Nat
  | .blank => 0 | .home => 1 | .bit false => 2 | .bit true => 3 | .delimiter => 4 | .count => 5

private def stageCode : Stage → Nat
  | .seek .check => 0 | .seek .scan => 1 | .seek .done => 2 | .copy => 3
  | .home .bank => 4 | .home .index => 5 | .home .value => 6 | .done => 7

private def moveCode : TM.Move → Nat
  | .left => 0 | .stay => 1 | .right => 2

private def actionCode (v : Letter × TM.Move) : Nat := 3 * letterCode v.1 + moveCode v.2

def main : IO Unit := do
  for mode in [false,true] do
    for q in stages do
      for a in letters do
        for i in letters do
          for v in letters do
            let read : Port → Letter := fun | .bank => a | .index => i | .value => v
            match S008.Compiler.Transfer.rule mode q read with
            | none => IO.println "-"
            | some (target,action) =>
              IO.println s!"{stageCode target} {actionCode (action .bank)} {actionCode (action .index)} {actionCode (action .value)}"
