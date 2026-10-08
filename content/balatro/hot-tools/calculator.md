---
title: "Score Calculator"
description: "Free Balatro score calculator. Compute expected hand scores with poker hand rankings, joker multipliers, and retrigger effects."
---

{{ partial "last-updated.html" . }}

Enter your hand details to estimate your final score. Formula: (Base Chips + Card Chips) × (Base Mult + Joker Mult) × Retriggers.

{{< balatro-calculator >}}

{{< ad >}}

### How Scoring Works

Balatro scoring follows a simple but deep formula. Every poker hand has base Chips and Mult values. Your played cards add chips, your jokers add Mult, and retriggers multiply the entire result.

- **Chips**: Base value of the hand + chips from individual cards.
- **Mult**: Base multiplier of the poker hand + Mult from jokers and cards.
- **Retriggers**: Cards that score multiple times multiply the entire hand score.
