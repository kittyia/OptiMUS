$
"min" & sum_(i in V_T) sum_(j in V_T\ j!=i) ell(gamma_(i j)) x_(i j)
\ "s.t." & sum_(i in V_T) x_(i j) = 1 &forall j in V_T
\ & sum_(j in V_T) x_(i j) = 1 &forall i in V_T
\ & u_i - u_j + (n-1) x_(i j) + (n-3) x_(j i) <= n - 2  & forall i,j in V_T \\ {s}
\ & -u_i + (n-3) x_(i s) + sum_(j in V_T \\ {s} \ j!=i) x_(j i) <= - 1 & forall i in V_T \\ {s}
\ & u_i + (n-3) x_(s i) + sum_(j in V_T \\ {s} \ j!=i) x_(j i) <= n - 1 & forall i in V_T \\ {s}
\ & sum_((i,j) in L_e) x_(i j) >= 1 & forall e in cal(L)
\ & x_(t s) = 1
\ & sum_(k in V_(i j)) x_(j k) <= 1 - x_(i j) & forall i,j in V_T
\ & sum_(v in B_delta) x_(v u _2) + x_(u_2 u_3) + sum_(v in E_delta) x_(u_3 v) <= 2 & forall delta in F_4
\ & sum_(v in hat(B)_delta) x_(v u_3) + sum_(v in E_delta) x_(u_3 v) <= 1 & forall delta in F_4
\ & sum_(v in B_delta) x_(v u_2) + sum_(v in hat(E)_delta) x_(u_2 v) <= 1 & forall delta in F_4
\ & u_i >= 0 & forall i in V_T
\ & x_(i j) in {0, 1} & forall (i,j) in A_T
$