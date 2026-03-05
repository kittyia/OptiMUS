$
"max" & sum_(t=1)^T sum_(s=1)^S y_(s t)
\ "s.t." & sum_(v=1)^t sum_(s=1)^S p_(s v t) y_(s v) + sum_(v=0)^6 sum_(s=1)^S tilde(p)_(s v t) e_(s v) <= C, forall t in {1,2,dots, T}
\ & y_(s t) <= d_(s t), forall s in {1, 2, dots, S}, forall t in {1, 2, dots, T}
\ & sum_(v=1)^t p_(s v t) y_(s v) + sum_(v=0)^6 tilde(p)_(s v t) e_(s v) = x_(s t), forall s in {1, 2, dots, S}, forall t in {1, 2, dots, T}
\ & x_(s t)>=0; y_(s t) >= 0 , forall s in {1, 2, dots, S}, forall t in {1, 2, dots, T}
$