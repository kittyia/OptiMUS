$
"min" & sum_(k in C) sum_(j=1)^M e_(j k) + lambda sum_(k in C) sum_(j=1)^M delta_(j k) + mu s
\ "s.t" & sum_(j=1)^M pi_(i j) = 1 & forall i in S
\ & sum_(i in A_k) pi_(i j) - c_k <= e_(j k) & 1<=j<=M, forall k in C
\ & -delta_(j k) <= sum_(i in A_k ) pi_(i j) - abs(A_k)/M <= delta_(j k) & forall 1<=j<=M, forall k in C
\ & s >= s_j^t - E & 0<=t<=T, 1<=j<=M
\ & s_j^t >= sum_(k in C_t) e_(j k) & 0<=t<=T, 1<=j<=M
\ & pi_(i j) in {0, 1} & forall i in S, 1<=j<=M
\ & delta_(j k), e_(j k), s >= 0 & 1<=j<=M, forall k in C
$