import os
import sys
import types

import pytest

# Ensure project root is on PYTHONPATH for test environments that don't set it
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.app import create_app  # noqa: E402


@pytest.mark.smoke
def test_app_instantiation_and_layout():
    """
    Smoke test:
    - Instantiates the Dash application via src.app.create_app()
    - Verifies a non-null layout is present
    - Ensures page registry is accessible
    """
    app = create_app()

    # Basic app type checks
    assert app is not None, "create_app() returned None"
    # Avoid importing Dash directly; check by duck-typing essential attributes
    assert hasattr(app, "layout"), "App missing 'layout' attribute"
    assert app.layout is not None, "App layout is None"

    # Page registry should be a dict-like object in Dash
    # Using getattr on the imported dash from within app to avoid tight coupling
    # Note: dash.page_registry may be empty depending on discovery, but it must exist.
    try:
        import dash  # local import to keep test light

        registry = getattr(dash, "page_registry", None)
        assert isinstance(registry, dict), "dash.page_registry must be a dict"
    except Exception as exc:
        pytest.fail(f"Failed to access dash.page_registry: {exc}")


@pytest.mark.smoke
def test_app_layout_structure_contains_container():
    """
    Smoke test:
    Ensures the top-level layout is an HTML container-like component with children.
    This checks that the application builds a valid Div structure.
    """
    app = create_app()
    layout = app.layout

    # Dash html.Div has a 'children' attribute; we duck-type check for that
    assert hasattr(layout, "children"), "Layout should expose 'children'"
    children = getattr(layout, "children", None)
    # Children may be a list or a single component
    assert children is not None, "Layout children is None"

    # If it's a list, ensure it's not empty; if it's a single item, just accept it
    if isinstance(children, (list, tuple)):
        assert len(children) > 0, "Layout children should not be empty"


@pytest.mark.smoke
def test_app_repeated_instantiation_is_stable():
    """
    Smoke test:
    Instantiating the app multiple times should not raise and should yield usable instances.
    """
    app1 = create_app()
    app2 = create_app()

    assert app1 is not None and app2 is not None, "Repeated create_app() returned None"
    assert hasattr(app1, "layout") and hasattr(app2, "layout"), (
        "Instances missing layout"
    )
    assert app1.layout is not None and app2.layout is not None, (
        "Layout is None on one of the instances"
    )
