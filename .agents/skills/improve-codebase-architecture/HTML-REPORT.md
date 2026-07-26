# HTML Report Format

The architectural review is a single self-contained HTML file in the OS temp directory. Tailwind and Mermaid come from CDNs. Mermaid handles graph-shaped diagrams; hand-built divs and inline SVG handle editorial visuals.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Candidate card

Each candidate is one `<article>` with a title, recommendation badge, files, before/after diagram, one-sentence problem, one-sentence solution, short wins, and any ADR callout. The diagrams carry the weight; prose is sparse and uses the architecture glossary.

## Diagram patterns

Use Mermaid flowcharts for dependencies and call flow, hand-built boxes and arrows when layout requires it, cross-sections for layered shallowness, mass diagrams for interface versus implementation depth, and call-graph collapse for nested call structures.

## Style guidance

Use generous whitespace, one accent color, red for leakage, and diagrams around 320px tall. The only scripts are the Tailwind CDN and Mermaid ESM import. Keep the report static apart from Mermaid rendering.

## Vocabulary

Use exactly: module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

Do not substitute component, service, unit, API, signature, boundary, layer, or wrapper when one of the glossary terms is intended.
