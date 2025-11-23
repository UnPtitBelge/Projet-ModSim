import pytest

from src import Classifier


def test_saddle_case():
    # det < 0 -> saddle
    out = Classifier().classify(0.0, -1.0)
    assert "Saddle" in out


def test_degenerate_origin():
    out = Classifier().classify(0.0, 0.0)
    assert out == "Degenerate origin (0,0)"


def test_spiral_unstable():
    # Δ < 0 and tr > 0 -> unstable spiral
    out = Classifier().classify(1.0, 1.0)
    assert "unstable (spiral source)" in out


def test_stable_node():
    # Δ > 0 and tr < 0 -> stable node
    out = Classifier().classify(-3.0, 2.0)
    assert "stable (node sink)" in out


if __name__ == "__main__":
    pytest.main(["-q"])
