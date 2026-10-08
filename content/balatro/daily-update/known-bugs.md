---
title: "Known Bugs"
description: "Community-reported Balatro bugs, crash fixes, and workarounds. Updated daily with the latest patch issues and solutions."
---

{{ partial "last-updated.html" . }}

Aggregated from community player reports. These are community observations, not official developer statements.

{{ $bugs := .Site.Data.balatro.known_bugs }}
{{ range $bugs }}
<div class="bug-item {{ if .workaround }}workaround{{ end }}">
  <h4>{{ .title }}</h4>
  <p><strong>Description:</strong> {{ .description }}</p>
  {{ if .workaround }}<p><strong style="color:var(--gold-bright)">Workaround:</strong> {{ .workaround }}</p>{{ end }}
  <p><em>v{{ .version }} | {{ .platform }} | Severity: {{ .severity }} | {{ .reports }} reports</em></p>
</div>
{{ end }}

### General Troubleshooting

- **PC:** Verify game files through Steam. Update your GPU drivers.
- **Mobile:** Reinstall the game if experiencing frequent crashes.
- **Switch:** Play in docked mode for better performance with many jokers.
