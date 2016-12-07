# Elo Ranking System
Implementation of Elo ranking algorithm with difference in score taken into account. R is Elo score,
`K_d` is score difference multiplicative factor, K_b is base scaling factor, O is outcome (1 for win, 0 for loss),
E is player expectation (calculated below).

```
R_new = R_old + K_d * K_b (O - E)
```
# Calculating Expectations
These are calculated for players `a` and `b` respectively
```
E_a = 1 / (1 + 10^((R_b - R_a) / 400)
```
```
E_b = 1 / (1 + 10^((R_a - R_b) / 400)
```
