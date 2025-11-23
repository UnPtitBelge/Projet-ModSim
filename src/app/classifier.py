"""Classifier for 2x2 linear systems (trace/determinant stability).

This module provides a `Classifier` class with a `classify(tr, det)` method
that returns a structured `ClassificationResult`. A top-level `classify`
function is also provided for backwards compatibility with older callers
and tests that expect a simple function returning a Markdown string.
"""

from typing import Callable

from models import ClassificationResult

__all__ = ["Classifier", "classify"]


class Classifier:
    def __init__(
        self, eps: float = 1e-8, formatter: Callable[[str], str] | None = None
    ):
        self.eps = eps
        self.formatter = formatter  # Optional formatter for other output

    def classify(self, tr: float, det: float) -> ClassificationResult:
        Delta = tr**2 - 4 * det

        if det < 0:
            label = "Saddle"
            stability = "unstable"
            markdown = f"**Saddle** — det < 0\nΔ = {Delta:.3g} < 0"
            return ClassificationResult(label, stability, Delta, markdown)

        if abs(Delta) < self.eps:
            if tr == 0 and det == 0:
                markdown = "Degenerate origin (0,0)"
                return ClassificationResult("Degenerate", "neutral", Delta, markdown)
            stability = "stable" if tr < 0 else "unstable"
            markdown = f"**Degenerate node ({stability})** — Δ ≈ 0"
            return ClassificationResult("Degenerate node", stability, Delta, markdown)

        if Delta < 0:
            if abs(tr) < self.eps:
                markdown = "**Center** — Tr A ≈ 0, Δ < 0"
                return ClassificationResult("Center", "neutral", Delta, markdown)
            stability = "stable (spiral sink)" if tr < 0 else "unstable (spiral source)"
            return ClassificationResult(
                "Spiral", stability, Delta, f"**{stability}** — Δ < 0"
            )

        stability = "stable (node sink)" if tr < 0 else "unstable (node source)"
        return ClassificationResult(
            "Node", stability, Delta, f"**{stability}** — Δ > 0"
        )


def classify(tr: float, det: float) -> str:
    """Backwards-compatible function returning a Markdown string.

    This wraps the `Classifier` class and returns the `.markdown` field when
    available so older callers that expect a string keep working.
    """
    result = Classifier().classify(tr, det)
    # Return markdown string if present, else fall back to str(result)
    return getattr(result, "markdown", str(result))
