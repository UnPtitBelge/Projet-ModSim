"""Classifier for 2x2 linear systems (trace/determinant stability).

This module provides the `classify(tr, det)` function which returns a
short Markdown-friendly description of the equilibrium type and stability.
"""


def classify(trval, detval):
    """Classify the stability region given trace `trval` and determinant `detval`.

    The logic mirrors the original implementation: compute Delta = Tr^2 - 4*det
    and classify into saddle, degenerate node, center/spiral, or node.
    """
    Delta = trval**2 - 4 * detval

    # Saddle (det < 0)
    if detval < 0:
        return f"**Saddle** — det < 0\nΔ = {Delta:.3g} < 0"

    # Degenerate (Δ ≈ 0)
    if abs(Delta) < 1e-8:
        if trval == 0 and detval == 0:
            return "Degenerate origin (0,0)"
        stability = "stable" if trval < 0 else "unstable"
        return f"**Degenerate node ({stability})** — Δ ≈ 0"

    # Complex eigenvalues (Δ < 0)
    if Delta < 0:
        if abs(trval) < 1e-8:
            return "**Center** — Tr A ≈ 0, Δ < 0"
        stability = "stable (spiral sink)" if trval < 0 else "unstable (spiral source)"
        return f"**{stability}** — Δ < 0"

    # Δ > 0 & det > 0 -> node (real eigenvalues)
    stability = "stable (node sink)" if trval < 0 else "unstable (node source)"
    return f"**{stability}** — Δ > 0"
