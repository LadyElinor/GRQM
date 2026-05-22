# GR_QM Toy Model Specification (v1)

Date: 2026-03-01  
Scope: auditable first-cycle proxy model for GR↔QM testability workflow

---

## 1) Model class and intent

This is a **minisuperspace-inspired ODE toy model** for testing workflow mechanics (null tests, convergence, uncertainty decomposition, replication), not a direct cosmological fit.

State vector:
\[
y(t)=\begin{bmatrix}a(t)\\v(t)\end{bmatrix},\quad v=\dot a
\]

Domain used in v1:
\[
t\in[0,3],\ a(t)>0
\]

---

## 2) Baseline equation (M0)

\[
\dot a=v,
\qquad
\dot v=-\frac{\Omega_m}{2a^2}+\Omega_\Lambda a
\]

Locked parameters:
- \(\Omega_m=0.3\)
- \(\Omega_\Lambda=0.7\)

Initial conditions:
- \(a(0)=0.1\)
- \(v(0)=1.5\)

---

## 3) Semiclassical-correction variant (M1)

\[
\dot a=v,
\qquad
\dot v=-\frac{\Omega_m}{2a^2}+\Omega_\Lambda a + \frac{\alpha_{QG}}{a^n}
\]

Locked correction settings for primary run:
- \(\alpha_{QG}=10^{-7}\)
- \(n=5\)

Assumption perturbation for sensitivity:
- keep all else fixed, switch \(n=5\to4\)

Interpretation: \(\alpha_{QG}/a^n\) is a phenomenological semiclassical proxy term (not derived from a unique UV completion).
