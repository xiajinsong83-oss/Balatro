---
title: "Joker Database"
description: "Complete list of all Balatro jokers with rarity tiers, cost, and effect descriptions. Common, Uncommon, Rare, and Legendary jokers."
---

{{ partial "last-updated.html" . }}

Complete list of all jokers in Balatro, sorted by rarity. Jokers are the primary source of scoring bonuses and build-defining effects.

{{ $jokers := .Site.Data.balatro.jokers }}
<div class="tools-grid">
{{ range $jokers }}
  <div class="tool-card">
    <span class="joker-rarity {{ .rarity | lower }}">{{ .rarity }}</span>
    <h3>{{ .name }}</h3>
    <p>{{ .effect }}</p>
    <p><strong>Cost:</strong> ${{ .cost }}</p>
  </div>
{{ end }}
</div>

### Rarity Tiers

- **Common** — Most frequently encountered. Solid early-game picks.
- **Uncommon** — Moderate spawn rate. Build-enabling effects.
- **Rare** — Low spawn rate. High-impact effects that carry a run.
- **Legendary** — Very rare, game-changing synergies and scaling.
