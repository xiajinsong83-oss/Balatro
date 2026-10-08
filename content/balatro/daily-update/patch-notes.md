---
title: "Patch Notes"
description: "Latest Balatro patch notes and changelog. Bug fixes, balance changes, and new features from every update."
---

{{ partial "last-updated.html" . }}

Official patch summaries for Balatro. Updated with every new release.

{{ $patches := .Site.Data.balatro.patch_notes }}
{{ range $patches }}
<div class="bug-item">
  <h4>{{ .title }} <span style="color:var(--text-dim);font-weight:400;font-size:0.85rem">v{{ .version }}</span></h4>
  <ul>
    {{ range .changes }}<li>{{ . }}</li>{{ end }}
  </ul>
  <p><em>Released: {{ .release_date }}</em></p>
</div>
{{ end }}
