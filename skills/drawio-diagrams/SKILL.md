---
name: drawio-diagrams
description: >
  Always use when the user asks to create, generate, draw, or design a diagram,
  flowchart, architecture diagram, ER diagram, sequence diagram, class diagram,
  network diagram, or when the user mentions draw.io, drawio, .drawio files, or
  diagram export to PNG/SVG. Also use when adding or updating image-card diagrams
  in a presentation built with the presentation-design skill.
---

# Draw.io Diagram Skill

Creates and maintains draw.io diagrams as native `.drawio` files (mxGraphModel XML).
Integrates with the `presentation-design` skill: diagrams are referenced from
`image-card` slides and rendered to SVG automatically by the build pipeline.

---

## When to use this skill

Use this skill whenever the user:
- Asks to create or update a diagram (architecture, flowchart, ER, sequence, etc.)
- References a `.drawio` file in the project
- Asks to update an `image-card` slide that uses a drawio source
- Asks to add a new diagram page to an existing `.drawio` file

---

## Authoring principle — XML, not code

**Diagrams are XML files, not programs.**

Always author `.drawio` content by writing `mxGraphModel` XML directly — either
by hand, via the MCP preview tool, or by letting the agent generate the XML text.

**Never create a Python script (or any other code generator) to produce a diagram.**
Diagram structure belongs in the `.drawio` XML file itself, not in a program that
emits XML. A Python generator adds an indirection layer, a dependency, and a
maintenance burden for no benefit the XML file alone cannot provide.

> **Note — project-specific exception:** The AI_EAM project contains a pre-existing
> `assets/diagrams/_generate.py` that generates `ai_eam_landscape.drawio`. This
> script was created before this skill existed and must be maintained for that
> project. It is **not** a pattern to follow. Do not create similar scripts for
> new diagrams.

---

## Authoring workflow

### Step 1 — Generate draw.io XML

Generate `mxGraphModel` XML for the requested diagram.
Fetch and follow the full XML reference before writing any XML:
```
https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/xml-reference.md
```

**Basic required structure — always start with this:**
```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- diagram cells with parent="1" -->
  </root>
</mxGraphModel>
```

**CRITICAL XML rules (never violate):**
- NEVER include XML comments `<!-- -->` — forbidden, causes parse errors
- Escape all attribute values: `&amp;` `&lt;` `&gt;` `&quot;`
- Every edge `mxCell` MUST have `<mxGeometry relative="1" as="geometry"/>` as a child
- Every `mxCell` needs a unique `id`
- Include `html=1` in every cell style when the `value` contains HTML

### Step 2 — Preview in chat (optional but recommended)

If the `mcp.draw.io` MCP server is configured, call `create_diagram` with the XML
to render an interactive preview directly in chat before saving:

```
create_diagram(xml="<mxGraphModel>...</mxGraphModel>")
```

The preview includes zoom/pan, layer toggles, and an "Open in draw.io" button.
If the MCP server is not available, skip this step — save directly.

To find domain-specific shapes (AWS, Azure, GCP, Cisco, BPMN, etc.) before
calling `create_diagram`, use `search_shapes`:
```
search_shapes(query="aws lambda")
```
Returns exact style strings for use in the XML.

### Step 3 — Write the `.drawio` file

Write the XML to a `.drawio` file in the project's `assets/diagrams/` directory.
The file is a **named-page** mxfile: wrap the `mxGraphModel` in `<mxfile>` with
`<diagram name="page-name">` so the build pipeline can select it by name.

**Multi-page mxfile format (required for `presentation-design` integration):**
```xml
<mxfile>
  <diagram name="my-diagram-page">
    <mxGraphModel adaptiveColors="auto">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- cells here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

If the `.drawio` file already exists, add or replace only the relevant `<diagram>`
page — preserve all other pages.

**Important — compressed pages:** draw.io sometimes stores diagram content as
base64+zlib compressed text inside `<diagram>`. Our `drawio_svg_renderer.py`
decompresses this automatically. Always write **uncompressed** XML (plain text
inside `<diagram>`).

---

## Always include a legend

**CRITICAL rule:** Every draw.io diagram page MUST include a legend bar anchored to the
bottom of the canvas whenever the diagram uses more than one visual concept
(layer colour, relationship type, shape category, etc.).

### What the legend contains

A legend bar sits at the very bottom of the page (typically the last 40 px) and
consists of two zones:

| Zone | Position | Content |
|---|---|---|
| Element chips | Left-aligned | Colour-coded rounded chips, one per layer/category used on the page |
| Relationship key | Right-aligned | Arrow symbol + label for each relationship type used on the page |

Use `→` for solid/synchronous relationships (serving, composition, assignment) and
`⇢` for dashed/derived relationships (realization, influence).

### When to skip or simplify

- Omit the **element chips** zone when the page uses only a single layer/category
  (the colour is self-evident).
- Omit the **relationship key** zone when the page contains no edges.
- Omit the entire legend only for purely structural pages that use a single shape
  type and no edges (e.g., a simple org-chart with only one box style).

### Implementation — direct XML authoring

Always write the legend directly as `mxCell` XML at the bottom of the diagram.
Place a 1 px separator line at `y = pageHeight - 40`, element chips at
`y = pageHeight - 34`, and relationship key items at the same `y`, right-aligned.

```xml
<!-- 1 px separator line -->
<mxCell id="leg0" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#D0D0D0;strokeColor=none;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="608" width="1200" height="1" as="geometry" />
</mxCell>

<!-- element chip (one per layer colour used) -->
<mxCell id="leg1" value="Strategy" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;
  fillColor=#EDE3FF;strokeColor=#6F42C1;strokeWidth=1.2;
  fontColor=#262626;fontSize=10;fontStyle=1;align=center;verticalAlign=middle;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="614" width="110" height="24" as="geometry" />
</mxCell>

<!-- relationship key item (right-aligned, one per edge type) -->
<mxCell id="leg8" value="&lt;font color='#575757'&gt;&amp;rarr; serving&lt;/font&gt;"
  style="text;html=1;strokeColor=none;fillColor=none;align=left;
  verticalAlign=middle;fontSize=10;fontColor=#575757;fontStyle=0;"
  vertex="1" parent="1">
  <mxGeometry x="1152" y="614" width="128" height="24" as="geometry" />
</mxCell>
```

Adjust `y` values to match `pageHeight - 40` and `pageHeight - 34` for the actual
page height used. Use `⇢` (`&amp;#x21E2;`) for dashed/derived relationships.

---

## No titles, subtitles, or footers inside draw.io diagrams

**CRITICAL rule when using draw.io with `presentation-design`:**

Never add title text, subtitle text, or footer text cells inside a draw.io
diagram. Instead, use the fields provided by the `image-card` in the
presentation definition:

| Content type | Where it belongs |
|---|---|
| Diagram title / heading | `##` slide heading in `presentation-definition.md` |
| Diagram subtitle / context | `caption:` field in the `image-card` YAML |
| Footer / summary text | `footer:` field in the `image-card` YAML |

**Why:** Title and footer cells inside the diagram duplicate content that the
presentation system already renders outside the image. They waste vertical space
inside the diagram canvas, reduce the diagram's information density, and create
visual redundancy.

Do NOT add `text;html=1;...` cells at the top or bottom of a diagram page for
labelling purposes. All labelling must go through the image-card fields.

---

## Integration with `presentation-design`

In the presentation definition (`presentation-definition.md`), `image-card` slides
reference drawio pages using the pattern:

```markdown
- type: image-card
  style_overrides:
    card-padding: 4
  content:
    image: diagrams/filename.drawio#page-name
    image_style: fullbleed
```

The build pipeline (`DrawioSvgRenderer`) converts this to SVG automatically:
1. Parses the `.drawio` XML
2. Renders the named page to SVG (`assets/diagrams/page-name.svg`)
3. Embeds the SVG into the PPTX and drawio output

**CRITICAL — always set `card-padding: 4` for diagram image-cards.**
The default card padding is 16 px on every side. For diagram slides this wastes
28 px of width and 28 px of height. Override it to 4 px per instance:

```yaml
type: image-card
style_overrides:
  card-padding: 4          # reduces border from 16 px to 4 px on all sides
content:
  source: "diagrams/file.drawio#page-name"
  image_style: fullbleed   # diagram fills the entire body area
```

For framed-style image cards (border + contain fit), also override the inner
padding:
```yaml
style_overrides:
  card-padding: 4
  image-framed-padding: 2  # default 8 px → 2 px inner frame padding
```

**To add a new diagram to a presentation:**
1. Create or update the `.drawio` file in `assets/diagrams/`
2. Add the `image-card` entry with `card-padding: 4` in `presentation-definition.md`
3. Run the build: `build_presentation.py <project-dir> --format both`

**File naming convention:**
- `.drawio` source: `assets/diagrams/<topic>.drawio`  (one file can have multiple pages)
- Page name in file: descriptive kebab-case, e.g. `strategic-shift`
- Reference in deck: `diagrams/<topic>.drawio#strategic-shift`
- Generated SVG: `assets/diagrams/strategic-shift.svg` (auto-created by build)

---

## Supported shapes

For standard diagram types (flowcharts, UML, ER diagrams, org charts, timelines,
mind maps) use basic geometric shapes — no shape search needed:

| Shape | Style |
|-------|-------|
| Rectangle | `rounded=1;whiteSpace=wrap;html=1;` |
| Diamond | `rhombus;whiteSpace=wrap;html=1;` |
| Circle | `ellipse;whiteSpace=wrap;html=1;` |
| Database | `shape=cylinder3;whiteSpace=wrap;html=1;` |
| Document | `shape=mxgraph.flowchart.document;whiteSpace=wrap;html=1;` |
| Swimlane | `swimlane;startSize=30;html=1;` |

For domain-specific shapes (AWS, Azure, GCP, Cisco, Kubernetes, BPMN, P&ID):
use `search_shapes` before generating XML.

**Rigid layout grid (always use this — do not compute positions in prose):**
- Column x = `col_index × 180 + 40`  (col 0 = 40, col 1 = 220, col 2 = 400, …)
- Row y = `row_index × 120 + 40`      (row 0 = 40, row 1 = 160, row 2 = 280, …)
- Node size: rectangles 140×60, diamonds 140×80, circles 60×60

---

## MCP App Server setup

The hosted MCP App Server at `https://mcp.draw.io/mcp` provides two tools:
- `create_diagram` — renders XML as an interactive diagram inline in chat
- `search_shapes` — finds shapes across all draw.io libraries by keyword

**Adding to VS Code:** add as a remote MCP server with URL `https://mcp.draw.io/mcp`.

---

## Common style patterns for EAM / architecture diagrams

Use the standard diagram-patterns for architecture diagrams like archimate.
- Layers: strategic, business, application, technology
- Element types: active structure, behavior, passive structure
- Relationships: composition, aggregation, assignment, realization, etc.
Make the diagrams visually engaging and easy to understand, using the design theme (theme.css) as a reference for colors, fonts, and layout. Avoid overcrowding — split complex diagrams into multiple slides if needed. Make diagram elements look attractive by using bold/italic text, colors, and shapes effectively. Use consistent styling across all diagrams to create a cohesive visual language throughout the presentation.

Use standard diagram patterns for process flows, organizational charts, timelines, and other common structures. For example, use swimlanes for process flows to clearly show responsibilities, use hierarchical layouts for org charts, and use a left-to-right layout for timelines. Always prioritize clarity and readability in the diagrams, ensuring that they effectively communicate the intended message without overwhelming the viewer with too much information at once.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Diagram page renders blank | Missing `id="0"` / `id="1"` root cells | Add both root cells |
| Edges not showing | Self-closing edge cell without mxGeometry child | Add `<mxGeometry relative="1" as="geometry"/>` |
| HTML tags show as literal text | `html=1` missing from style | Add `html=1` to every cell style |
| PPTX shows old diagram | Cached SVG not regenerated | Delete `assets/diagrams/<page-name>.svg` and rebuild |
| Page not found in drawio file | Wrong page name in `#` reference | Check exact `name` attribute on `<diagram>` element |
| Compressed diagram content | draw.io app saved with compression | Use `drawio_svg_renderer.py` directly (handles decompression) |
