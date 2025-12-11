"""
Style System Architecture

Complete documentation of the centralized style system for Projet-ModSim.

## Table of Contents
1. Design Principles
2. Color System
3. Typography System
4. Component System
5. HTML/CSS Configuration
6. Usage Patterns
7. Adding New Styles
8. Conversion Notes
9. Benefits & Best Practices
10. Troubleshooting

---

## Design Principles

1. **Single Source of Truth**: All colors, typography, and spacing defined in one place
2. **Composability**: Style functions return dicts that can be spread/combined
3. **No Inline CSS**: All styling through Python functions or centralized constants
4. **Immutable Palette**: PALETTE is a frozen dataclass to prevent runtime changes
5. **Component-Based**: Reusable style functions for common UI patterns
6. **Maintainability**: Easy to update, test, and refactor styles
7. **Performance**: No style recalculation or duplication
8. **Scalability**: Simple to add new colors/components as needed

---

## Color System (palette.py)

The PALETTE is the foundation of all visual design. It includes:

### Primary Colors
- `primary`: #C65D3B (terra cotta) - main brand color
- `primary_light`: #D97855 (light terra cotta)
- `primary_dark`: #A34A28 (dark terra cotta)

### UI Colors
- `bg`: #F9F3EE (warm cream background)
- `surface`: #FFF9F5 (very light warm white)
- `text`: #3D2E27 (deep warm brown)
- `text_muted`: #8B7366 (muted warm brown)
- `border`: #E5D5C8 (warm beige)

### Specialty Colors
- `accent_amber`: #E8A870 (warm sand/amber)
- `accent_red`: #B85A45 (burnt sienna)
- `secondary`: #3B7C8C (teal blue)
- `mouvement_uniforme`: #E8A870 (for special points)

### Stability Categories (NEW)
- `stability_stable`: #589689 (sage green - stable)
- `stability_marginal`: #D9925D (warm terracotta orange - marginal)
- `stability_unstable`: #B85A45 (burnt sienna - unstable)

### Poincaré Zones
Each zone has base, hover, and active states with opacity:
- Upper left: Warm Sand (amber)
- Upper right: Burnt Sienna (red)
- Lower left: Sage Green
- Lower right: Light Terra
- Lower axis: Warm Gray

## Typography System (text.py, typography.py)

### TEXT Dictionary
Standard text styles used throughout the app:
```python
TEXT = {
    "h1": {...},  # Large headings
    "h2": {...},  # Section headings
    "h3": {...},  # Subsection headings
    "p": {...},   # Body text
    "code": {...},  # Code/math text
    "label": {...}  # Form labels
}
```

### TYPOGRAPHY Object
Metrics and constants:
- Font families (sans-serif, monospace)
- Font sizes and weights
- Line heights and spacing

## Component System (components/)

### Layout Components (layout.py)
Functions returning style dicts:
- `app_container()`: Full app wrapper
- `sidebar_container()`: Sidebar wrapper
- `content_wrapper(margin_left_px=SIDEBAR_WIDTH)`: Main content
- `page_text_container(max_width)`: Text column with max-width
- `graph_container()`: Graph wrapper with height
- `section_card()`: Card/section styling
- `spacing_section()`: Vertical spacing
- `nav_button()`: Button styling

### Sidebar Components (sidebar.py)
- `sidebar_container()`: Base sidebar styling
- `sidebar_header()`: "Menu" title styling
- `nav_link(active=False, level=0)`: Navigation links
- `stability_badge()`: Special Stabilité page badge
- `poincare_badge()`: Special Poincaré page badge
- `chaos_badge()`: Special Chaos page badge

### Plot Components (plot/theme.py)
- `FIGURE_THEME`: Complete figure styling dict
- `apply_to_figure(fig, theme)`: Apply theme to plotly figure
- `apply_zone_fill(fig, zones)`: Apply zone colors to heatmaps

## HTML/CSS System (html_head.py)

Centralized HTML template with:
- MathJax configuration for LaTeX math rendering
- Chaos mode CSS (.chaos-mode class)
- Global HTML structure

Generate with: `get_index_string()`

## Usage Patterns

### Using Palette Colors
```python
from src.app.style.palette import PALETTE

html.Div(
    [html.P("Stable system", style={"color": PALETTE.stability_stable})],
    style={"backgroundColor": PALETTE.surface}
)
```

### Using Text Styles
```python
from src.app.style.text import TEXT

html.H1("Title", style=TEXT["h1"])
html.P("Paragraph", style={**TEXT["p"], "marginTop": "12px"})
```

### Using Component Functions
```python
from src.app.style.components.layout import section_card, nav_button
from src.app.style.components.sidebar import nav_link, chaos_badge

html.Div(
    [html.H2("Section", style=nav_button())],
    style=section_card()
)
html.A("Link", href="/page", style=nav_link(active=True))
```

### Combining Styles
```python
# Spread existing styles and override
style={**TEXT["h3"], "color": PALETTE.primary, "marginBottom": "20px"}
```

## Adding New Styles

### New Color
1. Add to PALETTE in `palette.py`
2. Use via `PALETTE.new_color`

### New Typography
1. Add to TEXT dict in `text.py`
2. Use via `TEXT["new_style"]`

### New Component
1. Create function in `components/layout.py` or `components/sidebar.py`
2. Return dict with CSS-in-JS properties (camelCase keys)
3. Export in `__all__`

### New Global CSS/JS
1. Add to HTML template in `html_head.py`
2. Update `get_index_string()` function

## Conversion Notes (camelCase)

CSS to CSS-in-JS conversion (used throughout):
- `background-color` → `backgroundColor`
- `margin-left` → `marginLeft`
- `padding-top` → `paddingTop`
- `border-radius` → `borderRadius`
- `box-shadow` → `boxShadow`
- etc.

---

## Benefits of This System

✅ **Consistent visual design** across all pages
✅ **Easy to update** colors/typography (one place to change)
✅ **No duplicate style definitions** - single source of truth
✅ **Type-safe** with immutable PALETTE
✅ **Composable styles** that can be combined
✅ **Clear component hierarchy** and reusability
✅ **Easy onboarding** for new developers
✅ **No CSS file management** or import issues
✅ **Dynamic styling** based on app state (Chaos mode, active links, etc)
✅ **Performance** - no unnecessary style recalculation
✅ **Testable** - all style functions can be unit tested
✅ **Scalable** - simple to extend with new styles

---

## Best Practices

### 1. Always Use Constants
❌ Bad:
```python
style={"color": "#EA580C", "fontSize": "16px"}
```

✅ Good:
```python
style={"color": PALETTE.primary, **TEXT["p"]}
```

### 2. Spread Existing Styles
❌ Bad:
```python
style={
    "fontSize": TEXT["p"]["fontSize"],
    "fontFamily": TEXT["p"]["fontFamily"],
    "color": PALETTE.primary,
    "lineHeight": TEXT["p"]["lineHeight"]
}
```

✅ Good:
```python
style={**TEXT["p"], "color": PALETTE.primary}
```

### 3. Use Functions for Complex Styles
❌ Bad:
```python
style={
    "padding": "16px",
    "backgroundColor": PALETTE.surface,
    "border": f"1px solid {PALETTE.border}",
    "borderRadius": "8px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
}
```

✅ Good:
```python
style=section_card()
```

### 4. Keep Custom Properties Minimal
```python
# Override just what's needed
style={
    **section_card(),
    "marginTop": "20px",
    "color": PALETTE.stability_stable
}
```

### 5. Leverage Component Functions
```python
# Responsive layout
html.Div(
    [...content...],
    style={**page_text_container(920), **spacing_section(40)}
)
```

---

## Real-World Examples

### Example 1: Stability Category Display
```python
from dash import html
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
from src.app.style.components.layout import section_card

html.Div(
    [
        html.H3(
            "Stable Equilibrium",
            style={**TEXT["h3"], "color": PALETTE.stability_stable}
        ),
        html.P(
            "All nearby trajectories converge to this point.",
            style={**TEXT["p"], "marginTop": "12px"}
        )
    ],
    style=section_card()
)
```

### Example 2: Graph Section
```python
from dash import dcc, html
from src.app.style.components.layout import graph_container, section_card
from src.app.style.text import TEXT

html.Div(
    [
        html.H2("Phase Portrait", style=TEXT["h2"]),
        html.Div(
            [dcc.Graph(figure=fig)],
            style=graph_container()
        )
    ],
    style=section_card()
)
```

### Example 3: Navigation Links
```python
from dash import html
from src.app.style.components.sidebar import nav_link, chaos_badge

html.Div(
    [
        html.A("Home", href="/", style=nav_link()),
        html.A("Poincaré", href="/poincare", style=nav_link(active=True)),
        html.A("Chaos", href="/chaos", style=chaos_badge()),
    ]
)
```

### Example 4: Responsive Container
```python
from dash import html
from src.app.style.components.layout import (
    page_text_container, spacing_section, section_card
)
from src.app.style.text import TEXT

html.Div(
    [
        html.H1("Title", style=TEXT["h1"]),
        html.Div([...content...], style=spacing_section(20)),
        html.Div([...more content...], style=section_card()),
    ],
    style=page_text_container(920)
)
```

### Example 5: Conditional Styling
```python
from dash import html
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT

def stability_label(is_stable):
    color = PALETTE.stability_stable if is_stable else PALETTE.stability_unstable
    label = "Stable" if is_stable else "Unstable"
    
    return html.Span(
        label,
        style={**TEXT["label"], "color": color}
    )
```

---

## File Structure

```
src/app/style/
├── palette.py              # Color constants (PALETTE)
├── text.py                 # Typography styles (TEXT)
├── typography.py           # Font metrics (TYPOGRAPHY)
├── theme.py                # Theme utilities
├── html_head.py            # HTML template & CSS
├── components/
│   ├── layout.py           # Layout component functions
│   ├── sidebar.py          # Sidebar component functions
│   └── tooltip.py          # Tooltip styling
├── plot/
│   └── theme.py            # Plot theming utilities
├── README.md               # This file
└── COMPONENTS_REFERENCE.md # Quick reference guide
```

---

## Integration Points

### In app.py
```python
from .style.html_head import get_index_string
app.index_string = get_index_string()
```

### In page components
```python
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
from src.app.style.components.layout import section_card
```

### In callbacks
```python
# Styles don't need to be in callbacks
# They're static unless you need dynamic colors
# Use PALETTE constants for conditional colors
```

---

## Troubleshooting

### Issue: Color not showing up
**Cause**: Typo in PALETTE constant
**Solution**: Check spelling and use IDE autocomplete
```python
# Wrong
style={"color": PALETTE.primray}  # Typo!

# Right
style={"color": PALETTE.primary}
```

### Issue: Style override not working
**Cause**: Order of spread operator matters
**Solution**: Put overrides after spread
```python
# Wrong - gets overridden
style={**{"color": PALETTE.primary}, **TEXT["p"]}

# Right
style={**TEXT["p"], "color": PALETTE.primary}
```

### Issue: Margins/padding look wrong
**Cause**: Might need to spread multiple styles
**Solution**: Combine component functions
```python
style={**section_card(), **spacing_section(20)}
```

### Issue: Font size inconsistent
**Cause**: Not using TEXT constants
**Solution**: Always spread TEXT style
```python
# Wrong
style={"fontSize": "16px"}

# Right
style={**TEXT["p"]}
```

---

## Migration Guide (For Existing Code)

### Step 1: Identify hardcoded styles
```python
# Find patterns like:
style={"color": "#EA580C"}
style={"backgroundColor": "#FEF5F1"}
style={"fontSize": "16px"}
```

### Step 2: Map to PALETTE or TEXT
```python
style={"color": PALETTE.primary}
style={"backgroundColor": PALETTE.bg}
style={**TEXT["p"]}
```

### Step 3: Use component functions if available
```python
style=section_card()  # Instead of manual padding/border
```

---

## Performance Considerations

✅ **Efficient**: Style dicts are lightweight Python objects
✅ **Cached**: Component functions return new dicts (Dash handles caching)
✅ **No runtime compilation**: Everything pre-defined
✅ **Memory efficient**: PALETTE is frozen (immutable, shared)
✅ **Fast rendering**: No CSS calculations in browser

---

## Future Enhancements

Possible improvements (not yet implemented):

1. **CSS Variables**: Export PALETTE as CSS vars for runtime theming
2. **Dark Mode**: Add dark_palette variant
3. **Responsive Breakpoints**: Screen-size aware styles
4. **Animation Library**: Reusable animation styles
5. **Storybook Integration**: Component documentation
6. **Theme Export**: JSON/YAML theme files

---

## Questions & Support

For questions about the style system:
1. Check `COMPONENTS_REFERENCE.md` for quick lookup
2. Review examples in this file
3. Check usage in existing components (e.g., `poincare/layout.py`)
4. Refer to `STYLE_AUDIT.md` for comprehensive audit

---

## Version History

- **v1.0** (Dec 11, 2025): Initial centralized style system
  - PALETTE with all colors
  - TEXT dictionary for typography
  - Component functions for layout/sidebar
  - HTML/CSS moved to html_head.py
  - Stability category colors added
"""
