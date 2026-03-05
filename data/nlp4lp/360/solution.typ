$
"min" & sum_(i in I) sum_(j in J) c_(i j) dot x_(i j) + sum_(k in K) sum_(n in N) c_(k n) dot y_(k n)
\ "s.t." & sum_(i in I_k) sum_(j in J) x_(i j) + sum_(n in N) y_(k n) = 1 & forall k in K
\ & sum_(i in I_v) x_(i j) <= cal(U)_(j v) & forall j in J, v in V
\ & sum_(i in I) x_(i j) <= sum_(v in V) cal(U)_(j v) & forall j in J
\ & x_(i j) in {0, 1} & forall i in I, j in J
\ & y_(k n) in {0, 1} & forall k in K, n in N
$