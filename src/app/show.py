"""
Compatibility wrapper: expose `build_template(classify_func)`.

This module provides a small adapter so the original call-site
`show.build_template(classify)` continues to work while the plotting
implementation lives in `plot.py`.
"""

from typing import Any, Callable

from models import AppConfig
from plot import PoincarePlot

__all__ = ["build_template"]


def build_template(classify_func: Callable[[float, float], Any]):
    """
    Build and return the Panel template by delegating to `PoincarePlot`.

    Parameters
    ----------
    classify_func:
        A callable taking (tr, det) and returning a string (or any object
        renderable as text). It may also be an object with a `.classify`
        method (in which case it will be used directly).

    Returns
    -------
    A Panel template/layout as constructed by `PoincarePlot.render_template()`.
    """
    # If the passed value is a plain function, adapt it to an object with
    # a `.classify` attribute expected by `PoinCarePlot`.
    if callable(classify_func) and not hasattr(classify_func, "classify"):

        class _FuncAdapter:
            def __init__(self, f: Callable[[float, float], Any]) -> None:
                self.classify = f

        classifier_obj = _FuncAdapter(classify_func)
    else:
        # It may already be a Classifier-like object with `.classify`.
        classifier_obj = classify_func

    config = AppConfig()
    plot = PoincarePlot(config, classifier_obj)

    # Some plot implementations register events during construction;
    # calling `register_events` is harmless and kept for compatibility.
    try:
        plot.register_events()
    except Exception:
        # Tolerate environments where explicit registration isn't needed.
        pass

    return plot.render_template()
