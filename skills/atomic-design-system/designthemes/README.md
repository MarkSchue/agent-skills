# Design Themes Library

A curated reference library housing complete design system specifications for use
with the Atomic Design System. Each subdirectory is a self-contained guide for a
single design system — covering color, typography, spacing, layout, motion, and
iconography — plus ready-to-use `design-config.yaml` files that integrate
directly with the atomic pipeline.

---

## Available Systems

| Directory | System | Version | Status |
|---|---|---|---|
| [`materialdesign3/`](./materialdesign3/) | Google Material Design 3 (Material You) | M3 / 2024 | ✅ Complete |
| [`carbon/`](./carbon/) | IBM Carbon Design System | v11 / 2024 | ✅ Complete |

---

## How to Use

Each design system folder contains:

| File | Purpose |
|---|---|
| `README.md` | System overview, principles, quick reference |
| `design-config.yaml` | Light-theme config — drop into your project |
| `design-config-dark.yaml` | Dark-theme config — drop into your project |
| `design-tokens.yaml` | Complete token definitions (all roles, values) |
| `colors.md` | Color system: roles, palettes, usage rules |
| `typography.md` | Type scale, weights, usage rules |
| `spacing.md` | Spacing scale, layout, grid |
| `motion.md` | Easing, duration, animation principles |
| `icons.md` | Iconography guidelines and icon sets |
| `principles.md` | Design principles and decision rules |

---

## 3-Layer Configuration Model

Every project build involves three configuration layers stacked on top of each other:

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 1 — Design System Canonical Tokens                        │
│  designthemes/<system>/design-tokens.yaml                        │
│  Full token vocabulary. Never edited. Source of truth.          │
└─────────────────────┬──────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│  Layer 2 — Design System Reference Config                        │
│  designthemes/<system>/design-config[dark].yaml                  │
│  Preset baseline. Copy to start a new project.                  │
└─────────────────────┬──────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│  Layer 3 — Project Brand Override                                │
│  <project>/design-config.yaml                                   │
│  Only colors.* and typography.font-family may differ from L2.   │
└─────────────────────┬──────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────────────┐
│  Render Layer — Atoms / Molecules / Templates                    │
│  Design-agnostic. All values come from {{theme.*}} tokens.       │
└──────────────────────────────────────────────────────────────┘
```

### Brand Customization Contract

Customers may customize a design system configuration **without breaking the design system**
by following this contract:

| Config Key | Customer May Change? | Explanation |
|---|---|---|
| `colors.*` | ✅ **Yes** | Replace with brand palette. All semantic tokens (primary, surface, error …) map to brand hex values. |
| `typography.font-family` | ✅ **Yes** | Replace IBM Plex / Roboto with brand font. |
| `canvas.*` | ✅ **Yes** | Adjust output size, margin, gutter for the deliverable format. |
| `borders.*` | ❌ **No** | Owned by the design system. Radius scale encodes the system’s shape language. |
| `spacing.*` | ❌ **No** | Owned by the design system. Spacing scale is grid-derived (8px base). |
| `elevation.*` | ❌ **No** | Owned by the design system. Depth model (shadow vs layer) is a structural principle. |
| `typography.*` (sizes, weights) | ❌ **No** | Type scale encodes hierarchy. Only the font family belongs to the brand. |

> Changing only `colors.*` and `typography.font-family` means every atom, molecule, and template
> will automatically adopt the customer’s brand while remaining fully compliant with the
> chosen design system’s visual language.

### How to Set Up a New Project

```bash
# 1. Choose design system (material or carbon) and copy the reference config
cp .github/agents/atomic-design-system/designthemes/carbon/design-config.yaml \
   <project>/design-config.yaml

# 2. In <project>/design-config.yaml, replace ONLY colors.* and typography.font-family
#    with the customer’s brand values. Leave everything else untouched.

# 3. Build — all atoms and molecules pick up the new tokens automatically
python .github/agents/atomic-design-system/scripts/pptx_builder.py deck.md \
  --design-config design-config.yaml --output output/deck.pptx
```

---

## Adding a New Design System

1. Create a new subdirectory: `designthemes/<system-name>/`
2. Copy the folder structure from an existing system
3. Update `design-tokens.yaml` with the new system's values
4. Generate `design-config.yaml` and `design-config-dark.yaml`
5. Document each design pillar in the subject `.md` files
6. Register the new system in this README's table

---

## Source References

| System | Specification URL |
|---|---|
| Material Design 3 | https://m3.material.io/ |
| Carbon Design System | https://carbondesignsystem.com/ |
