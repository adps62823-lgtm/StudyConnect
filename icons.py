import requests

_cache = {}


def svg(name: str, size: int = 16) -> str:
    """Return a small inline SVG string.

    This function supports three sources:
    1. hardcoded icons (the originals)
    2. remote URLs passed directly as the name (e.g. a GitHub raw svg)
    3. URLs derived from a base online repository if the name matches a
       known icon filename.

    Remote SVGs are fetched lazily and cached for the session.
    """
    s = size
    # local built‑in set
    icons = {
        "book": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M4 19.5A2.5 2.5 0 0 0 6.5 22H20\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 1 4 17.5v-13z\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>",
        "globe": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"12\" cy=\"12\" r=\"9\" stroke=\"currentColor\" stroke-width=\"1.5\"/><path d=\"M2.5 12h19\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\"/><path d=\"M12 2.5c2 3.5 2 6.5 2 9.5s0 6  -2 9.5\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\"/></svg>",
        "target": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"12\" cy=\"12\" r=\"8\" stroke=\"currentColor\" stroke-width=\"1.5\"/><circle cx=\"12\" cy=\"12\" r=\"4\" stroke=\"currentColor\" stroke-width=\"1.2\"/></svg>",
        "heart": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M20 8.5c0 6-8 9.5-8 9.5s-8-3.5-8-9.5A4 4 0 0 1 8 5.5c1.5 0 2.5 1 4 1s2.5-1 4-1a4 4 0 0 1 4 3z\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>",
        "comment": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>",
        "users": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M17 21v-2a4 4 0 0 0-3-3.87\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M7 21v-2a4 4 0 0 1 3-3.87\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><circle cx=\"12\" cy=\"7\" r=\"4\" stroke=\"currentColor\" stroke-width=\"1.2\"/></svg>",
        "stats": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M3 3v18h18\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><rect x=\"6\" y=\"10\" width=\"2\" height=\"7\" stroke=\"currentColor\" stroke-width=\"1.2\"/><rect x=\"10\" y=\"6\" width=\"2\" height=\"11\" stroke=\"currentColor\" stroke-width=\"1.2\"/><rect x=\"14\" y=\"2\" width=\"2\" height=\"15\" stroke=\"currentColor\" stroke-width=\"1.2\"/></svg>",
        "mentor": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M12 2l3 7-3 1-3-1 3-7z\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>",
        # thumb (like) icon similar to Facebook
        "thumb": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M14 9V5a3 3 0 0 0-3-3H7v12h4a3 3 0 0 1 3 3v2h4v-8l2-4-6-2z\" stroke=\"currentColor\" stroke-width=\"1.5\"/></svg>",
        # chat bubble icon for comments
        "chat": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>",
        # theme toggle icons (sun/moon)
        "sun": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"12\" cy=\"12\" r=\"5\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"12\" y1=\"1\" x2=\"12\" y2=\"3\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"12\" y1=\"21\" x2=\"12\" y2=\"23\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"4.22\" y1=\"4.22\" x2=\"5.64\" y2=\"5.64\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"18.36\" y1=\"18.36\" x2=\"19.78\" y2=\"19.78\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"1\" y1=\"12\" x2=\"3\" y2=\"12\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"21\" y1=\"12\" x2=\"23\" y2=\"12\" stroke=\"currentColor\" stroke-width=\"1.5\"/></svg>",
        "moon": f"<svg width=\"{s}\" height=\"{s}\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z\" fill=\"currentColor\"/></svg>",
    }

    # If caller provided a URL directly, fetch it
    if name.startswith("http://") or name.startswith("https://"):
        if name in _cache:
            return _cache[name]
        try:
            resp = requests.get(name, timeout=5)
            if resp.ok:
                svg_data = resp.text
                # inject explicit size attributes if missing
                svg_data = svg_data.replace("<svg", f"<svg width=\"{s}\" height=\"{s}\"")
            else:
                svg_data = ""
        except Exception:
            svg_data = ""
        _cache[name] = svg_data
        return svg_data

    # otherwise look up local set
    if name in icons:
        return icons[name]

    # fallback: try to fetch from central repo as '<name>.svg'
    base = "https://raw.githubusercontent.com/your-org/your-icon-repo/main/"
    url = f"{base}{name}.svg"
    if url in _cache:
        return _cache[url]
    try:
        resp = requests.get(url, timeout=5)
        if resp.ok:
            svg_data = resp.text.replace("<svg", f"<svg width=\"{s}\" height=\"{s}\"")
        else:
            svg_data = ""
    except Exception:
        svg_data = ""
    _cache[url] = svg_data
    return svg_data
