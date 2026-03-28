"""
rendering — atomic design system render package
================================================
Provides the unified RenderContext (DrawioCtx / PptxCtx) and a
molecule registry that resolves molecule names to renderer objects.

Quick usage
-----------
    from rendering.context import DrawioCtx, PptxCtx
    from rendering.molecules import MOLECULE_REGISTRY

    ctx = DrawioCtx(xml_root, ds)          # or PptxCtx(slide, ds)
    mol = MOLECULE_REGISTRY["kpi-card"]
    mol.render(ctx, props, x, y, w, h)
"""
