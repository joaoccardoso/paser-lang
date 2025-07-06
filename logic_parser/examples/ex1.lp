// Variable assignments
A := 1
B := 0
C := 1

// Simple AND, OR, NOT
X := A ^ B
Y := ~B
Z := A v B

// XOR, IMPLICATION, BICONDITIONAL
XOR1 := A != B
XOR2 := B != C
IMP1 := A => B
IMP2 := B => C
BIC1 := A <=> C
BIC2 := A <=> B

// Nested expressions and parentheses
NESTED := ~(A ^ (B v C)) => ((A != B) <=> (C ^ 1))

// Comments and blank lines
// The next line checks a complex formula
RESULT := (A ^ ~B) v ((A => C) <=> (B != C))

// Print results
A
B
C
X
Y
Z
XOR1
XOR2
IMP1
IMP2
BIC1
BIC2
NESTED
RESULT