$
max_(O_t,dots,O_T) & sum_(tau=t)^T {sum_(s=tau-L+1)^tau sum_(k=1)^K p^k S^k_(tau+1,s) - c_tau^F (sum_(s=tau-L)^tau sum_(k=1)^K O_(tau,s)^k - overline(F)_tau)}
// state dynamics for all $tau=t,dots,T$ and $k=1,dots,K$
\ "s.t." & S'_(tau,s)^k = S_(tau,s)^k - epsilon_(tau,s)^k && forall s in {tau-L, dots, tau-1}, tau in {t,dots,T}, k in {1,dots,K}
\ & S'_(tau, tau)^k = I'_tau^k && forall tau in {t,dots,T}, k in {1,dots,K}
\ & S_(tau+1,s)^k = S'_(tau,s)^k - O_(tau, s)^k && forall s in {tau-L+1, dots, tau}, tau in {t,dots,T}, k in {1,dots,K}
// maximum stay
\ & O_(tau, tau-L)^k = S'_(tau, tau-L)^k && forall tau in {t, dots, T}, k in {1, dots, K}
// pool size
\ & sum_(s=tau-L+1)^tau sum_(k=1)^K S_(tau+1, s)^k <= C_tau && forall tau in {t, dots, T}
//  end of horizon
\ & S_(T+1) = 0
\ & S_tau >= 0, O_tau >= 0 && forall tau in {t, dots, T}
$