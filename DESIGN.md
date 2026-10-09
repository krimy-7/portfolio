---
name: Krishna Nishad
description: One player, two kits. A football-kit portfolio where Home (crimson/white) is brand & social and Away (navy/volt) is the developer side.
colors:
  gold-thread: "#C9A227"
  crest-black: "#14110F"
  kit-white: "#FFFFFF"
  home-crimson: "#C8102E"
  home-deep: "#8A0B20"
  home-accent: "#A00D25"
  home-number-shadow: "#5A0614"
  home-shorts-ink: "#22090E"
  home-shorts-mute: "#6B4A50"
  away-navy: "#0B1F4B"
  away-deep: "#06122F"
  away-volt: "#D7FF3A"
  away-number-shadow: "#7D9A12"
  away-shorts-ink: "#EEF2FA"
  away-shorts-mute: "#9AA8C6"
typography:
  display:
    fontFamily: "Anton, sans-serif"
    fontSize: "clamp(64px, 9.2vw, 146px)"
    fontWeight: 400
    lineHeight: 0.86
    letterSpacing: "0.005em"
  headline:
    fontFamily: "Anton, sans-serif"
    fontSize: "clamp(48px, 6vw, 92px)"
    fontWeight: 400
    lineHeight: 0.9
  numeral:
    fontFamily: "Anton, sans-serif"
    fontSize: "clamp(30px, 3.4vw, 52px)"
    fontWeight: 400
    lineHeight: 1
  title:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "clamp(22px, 2.2vw, 32px)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.02em"
  label:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.12em"
  label-small:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.2em"
  body:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  lede:
    fontFamily: "Barlow, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.55
rounded:
  button: "2px"
  sm: "3px"
  md: "4px"
  patch: "5px"
  crest-patch: "6px"
spacing:
  page-gutter: "clamp(16px, 4.4vw, 64px)"
  section-y: "clamp(72px, 9vw, 128px)"
  hero-stack: "28px"
  fixture-row: "28px"
  patch-gap: "10px"
components:
  button-primary:
    backgroundColor: "{colors.kit-white}"
    textColor: "{colors.home-crimson}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "13px 24px"
    height: "48px"
  button-secondary:
    textColor: "{colors.kit-white}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    padding: "13px 24px"
    height: "48px"
  kit-switch-option:
    typography: "{typography.label}"
    padding: "12px 18px"
    height: "44px"
  kit-switch-option-home-selected:
    backgroundColor: "{colors.kit-white}"
    textColor: "{colors.home-accent}"
  kit-switch-option-away-selected:
    backgroundColor: "{colors.away-volt}"
    textColor: "{colors.away-navy}"
  stitched-patch:
    backgroundColor: "{colors.crest-black}"
    textColor: "{colors.kit-white}"
    typography: "{typography.label}"
    rounded: "{rounded.patch}"
    padding: "10px 14px"
  crest-patch:
    backgroundColor: "{colors.crest-black}"
    textColor: "{colors.kit-white}"
    rounded: "{rounded.crest-patch}"
    padding: "9px 16px"
  flip-button:
    backgroundColor: "{colors.crest-black}"
    textColor: "{colors.kit-white}"
    rounded: "{rounded.sm}"
    padding: "0 22px"
    height: "48px"
  strip-nav-link:
    typography: "{typography.label}"
    padding: "0 18px"
    height: "56px"
  fixture-result:
    typography: "{typography.numeral}"
---

# Design System: Krishna Nishad

## Overview

**Creative North Star: "One Player, Two Kits"**

The page is a club's shirt launch for a single player. The ground is a football-kit colourway with a fine knitted mesh, and everything on it is printed, stitched or badged the way kit is: heavy condensed numerals with a flat drop shadow, caps lettering in a narrow sans, embroidered patches with a dashed gold running stitch, and a shield crest. The player's ID is a holographic rookie card in a penny sleeve.

There are two complete kits and the visitor chooses. HOME (crimson field, white trim) is the brand and social side; AWAY (navy field, volt trim) is the developer side. Gold thread and the crest-black patch are shared by both kits and never change. Switching kit repaints every surface through custom properties, ripples the new kit out from the pressed label, and turns the card a full rotation. The kit choice is identity, not decoration: the content order also changes (Away puts dev fixtures before club career).

Density is a matchday programme: full-bleed colour bands divided by thick trim rules, tables of fixtures with results on the right, and no floating cards on the field. The one rejected default, confirmed in the direction, is the dark developer portfolio with a particle hero.

**Key Characteristics:**
- Two full colour kits switched by one `data-kit` attribute on `<html>`; gold and crest-black are constant.
- Anton numerals and names with a hard flat drop shadow in the kit's deep tone, like printed shirt lettering.
- Barlow Condensed caps for every label, nav item, date and role; Barlow for reading text.
- Stitched patches: crest-black fill, gold dashed outline inset 5px.
- Sections are full-bleed bands separated by a 6px trim rule; the record lives on a contrasting "shorts" panel.
- A knitted mesh texture on the field, a fainter one on the shorts panel.

## Colors

Two kit colourways over a shared gold thread and crest black; each kit is a field, a deep shade, a trim and a contrasting shorts panel.

### Primary
- **Home Crimson** (home-crimson): the HOME field, the whole page ground, the theme-color, and the card's field colour.
- **Away Navy** (away-navy): the AWAY field and theme-color; also the ink on volt surfaces.

### Secondary
- **Kit White** (kit-white): HOME trim. Strip underline, section rules, the selected kit option, primary button fill, and the HOME shorts panel and card stock.
- **Volt** (away-volt): AWAY trim, used exactly where white is used in HOME: rules, selected option, focus ring, scrollbar, selection, card stock, and accents on the AWAY shorts panel.

### Tertiary
- **Gold Thread** (gold-thread): shared across both kits. Patch stitching, the crest outline and monogram, the card photo frame, the "Now playing:" lead-in and the typing caret. Never a fill for large areas.

### Neutral
- **Crest Black** (crest-black): shared patch fill (crest patch, skill patches, Flip button), crest shield, and the HOME card name plate.
- **Home Deep** (home-deep) / **Away Deep** (away-deep): the strip, the full-time contact band, the footer, and the flat drop shadow under the display name. Away Deep is also the AWAY shorts panel.
- **Home Accent** (home-accent): roles, results and stat labels on the white HOME shorts panel; the text on the selected HOME kit option.
- **Number Shadows** (home-number-shadow, away-number-shadow): the flat offset under the card's "No. 168".
- **Shorts Ink and Mute** (home-shorts-ink, home-shorts-mute, away-shorts-ink, away-shorts-mute): heading/rule ink and secondary text (dates, bullets, descriptions) on the shorts panel.
- On the field, secondary text is white at 88% (HOME) or #EEF2FA at 86% (AWAY); hairline dividers are white at 12-22%; shorts-panel rules are shorts-ink at 14% (HOME) or volt at 18% (AWAY).

### Named Rules
**The Kit Parity Rule.** Every kit token exists in both kits with the same role (`--field --deep --ink --soft --trim --on-trim --shorts --s-ink --s-mute --s-acc --s-rule --stock --plate --plate-ink --num --num-sh`). A new surface uses the role variables, never a kit hex, so it repaints on switch.

**The Shared Thread Rule.** Gold and crest black belong to neither kit. They are the club's embroidery and stay identical on both.

## Typography

**Display Font:** Anton (fallback sans-serif)
**Body Font:** Barlow (fallback system-ui, sans-serif)
**Label Font:** Barlow Condensed, weights 500/600/700

**Character:** Anton is shirt print: names, section titles and results set uppercase, tight, heavy. Barlow Condensed is the kit's technical lettering: caps, tracked wide, short. Barlow is the only face for running prose.

### Hierarchy
- **Display** (Anton 400, clamp(64px, 9.2vw, 146px), 0.86): the hero name, one word per line, with a 5px 5px flat shadow in the kit's deep tone. The contact "Write to me" uses the same voice at clamp(56px, 9vw, 148px).
- **Headline** (Anton 400, clamp(48px, 6vw, 92px), 0.9): section titles named in football terms (Player profile, Club career, Dev fixtures, Academy, Squad attributes).
- **Numeral** (Anton 400, clamp(30px, 3.4vw, 52px), 1): fixture results (+447%, Live, UE5) in the shorts accent.
- **Title** (Barlow Condensed 700, clamp(22px, 2.2vw, 32px), 1.05, uppercase): club and project names in fixture rows.
- **Body** (Barlow 400, 17px, 1.55): reading text, held to 52-62ch inside fixture rows; bio at clamp(19px, 1.6vw, 22px); hero lede at 18px, max 30em.
- **Label** (Barlow Condensed 600, 15px, 0.12em, uppercase): nav, buttons, patches, dates, roles. Small labels (12-15px, 700, 0.16-0.2em) head vitals, attribute groups, contact lines and the footer.

### Named Rules
**The Block Heading Rule.** The name (h1) and every section h2 are drawn as 5×7 extruded cubes, not set in Anton. The script builds an inline SVG per word from the heading's own text (kept visually hidden for screen readers and search; without JS the Anton text shows). Cubes fill 90% of a cell with a 0.26-cell down-right extrusion; faces take `currentColor`, the side faces mix it with the ground (`--deep` on the field, `--field` on the Home shorts panel, black on the contact band). Width is set in em, so a heading keeps its Anton size, and it is capped at 100% of its column. The name's first letter is gold. Cubes snap in left to right (18ms per column, 0.55s ease-out) when a heading enters view; there's no motion under reduced motion.

**The Printed Number Rule.** Anton carries names, titles and results only, always uppercase. Its flat shadow is offset down-right with zero blur in the kit's deep tone (or black at 35% on the deep band).

**The Caps Label Rule.** Anything that is a label, not a sentence, is Barlow Condensed uppercase with at least 0.06em tracking. Sentences are never set in caps.

## Layout

Full-bleed horizontal bands, each with the shared page gutter (clamp(16px, 4.4vw, 64px)) and section padding of clamp(72px, 9vw, 128px). Bands are separated by a 6px trim rule. Order: matchday strip (56px), hero, Player profile on the field, the record on the shorts panel, Academy + Squad attributes on the field, the full-time contact band on the deep tone, footer.

The hero is a 46/54 two-column grid at min(100svh - 56px, 940px): copy left in a 28px-gap stack, card right. Fixture rows are a three-column grid: date (170px), body, result (210px, right-aligned); dev fixtures put a 16:9 thumbnail in the first column. Patches wrap with a 10px gap. Attributes use auto-fit columns with a 280px minimum.

At 1100px and below the strip drops its location and narrows its links. At 900px and below everything collapses to one column: the strip nav becomes a 3-column grid of 46px cells, the kit switch stretches full width, the card stage is min(140vw, 640px), fixture results go left-aligned at 34px with their caption inline, and the contact crest moves above the heading.

## Elevation & Depth

The field is flat colour with a knitted mesh texture; depth comes from print and stitching, not floating surfaces. Shadows come in two kinds: flat zero-blur offsets that read as printed lettering, and soft blurred shadows under the only real objects (the card, the crest, the crest patch).

### Shadow Vocabulary
- **Print shadow** (`text-shadow: 5px 5px 0 var(--deep)`): the hero name. Numerals on the card use `3px 3px 0 var(--num-sh)`; the contact heading uses `6px 6px 0 rgba(0,0,0,.35)`.
- **Card lift** (`box-shadow: 14px 18px 32px rgba(0,0,0,.32)`): the DOM rookie card faces. The WebGL card casts a radial soft shadow plane instead.
- **Patch lift** (`box-shadow: 0 3px 6px rgba(0,0,0,.25)`): the "Now playing" crest patch only.
- **Crest drop** (`filter: drop-shadow(10px 14px 18px rgba(0,0,0,.35))`): the large rotated crest in the contact band.

### Named Rules
**The Print, Not Plastic Rule.** A hard offset shadow belongs to lettering (Anton text), because that is how kit is printed. Boxes on the field do not float.

## Shapes

Kit edges are nearly square: 2px on buttons, 3px on the Flip button, thumbnails and swatches, 4px on the kit switch and certificate, 5-6px on patches. The card is the only rounded object (4.5% / 3.2% corners). Borders are 2-3px solid in ink or trim; section dividers are 6px trim rules; table rules are 1px shorts-rule. The crest is a pointed shield with a dashed inner stitch at 80% scale. The card name plate is skewed -3deg, like a printed band.

## Components

### Buttons
Tactile shirt-print buttons in condensed caps.
- **Shape:** squared (2px), 2px solid ink border, min-height 48px, padding 13px 24px.
- **Primary:** ink fill with field-coloured text (white on crimson in HOME, white on navy in AWAY), trailing arrow icon.
- **Secondary:** transparent with an ink border and ink text.
- **Hover / Focus:** lifts translate(-1px,-1px) over 0.2s cubic-bezier(.2,.8,.2,1). Focus is the global 3px trim outline at 3px offset.

### Kit switch
A real radio fieldset ("Choose the kit") shown only when JS runs. Two labels in a 2px trim frame with a 4px radius, each with a diagonal two-colour swatch (22px, 3px radius) and "Home · Brand & Social" / "Away · Developer". The checked label fills with trim and takes the on-trim colour; keyboard focus draws a gold 3px outline inset 5px.
- **Mechanism:** `setKit()` writes `data-kit` on `<html>`, updates `meta[name=theme-color]`, persists to `localStorage("kit")`, and accepts `?kit=` on load. When triggered from the switch and motion is allowed, `document.startViewTransition` reveals the new kit with a circular clip-path growing from the pressed label (560ms, cubic-bezier(.3,.7,.2,1)). It then dispatches a `kitchange` event; the card does a full turn and repaints when edge-on. Elements marked `.h-only` / `.a-only` show per kit.

### Stitched patches (chips)
- **Style:** crest-black fill, white Barlow Condensed caps, 5px radius, 1.5px dashed gold outline inset 5px. 15px in Interests, 14px in Squad attributes.
- **Crest patch:** the same stitch at 6px radius with the patch lift; holds "Now playing:" in gold and the typed role with a blinking gold caret.

### Navigation (matchday strip)
A deep-tone bar, 56px, with a 3px trim underline. Left: the crest and "KN·168" in Anton. Links are Barlow Condensed 600 caps at 15px, 0.12em, separated by hairlines, hover at white 10%. Location sits at the far right. Under 900px it becomes a 3×2 grid of centred cells.

### Fixture rows
The career and projects as a results table on the shorts panel. Header: Anton title with a small right-aligned column caption ("Result", "Stack") over a 3px ink rule. Each row: date in muted condensed caps, club or project title, role in shorts accent, dash-bulleted duties (8×2px accent bars), and an Anton result with a small caption. Dev rows lead with a 16:9 thumbnail in a 3px ink frame that scales to 1.04 on hover.

### Rookie card (signature)
A 5:7 trading card. Front: kit stock, gold-framed natural-colour photo with holo foil on the backdrop only, crest, "RC" rookie shield, skewed name plate, "Brand × Dev" band and "No. 168" with a print shadow. Back: a stat sheet on the shorts colour with a band header, four stat boxes, a pro career record and a highlight. The WebGL version (Three.js) adds thin-film foil keyed to the reflection vector, a translucent penny sleeve, spring tilt toward the pointer, idle float and flip. The DOM card is the first paint and the no-WebGL fallback (CSS 3D flip, 0.8s). The Flip button below is a crest-black stitched patch with a turn icon. Rendering pauses off-screen and in hidden tabs, and reduced motion removes idle and spring animation.

### Crest
The KN shield: crest-black fill, 5px gold edge, dashed gold inner stitch, a white peak line with a gold arrow, "KN" in Anton gold. Used in the strip, on the card, and large in the contact band at -6deg.

## Do's and Don'ts

### Do:
- **Do** colour every new surface through kit role variables (`--field`, `--deep`, `--trim`, `--on-trim`, `--shorts`, `--s-*`) so it works in both kits.
- **Do** keep gold (#C9A227) and crest black (#14110F) for stitching, crests and patches in both kits.
- **Do** set names, titles and results in uppercase Anton with a zero-blur offset shadow in the kit's deep tone.
- **Do** set labels, dates, roles and nav in Barlow Condensed caps tracked 0.06-0.2em.
- **Do** separate sections with full-bleed bands and a 6px trim rule; put records and tables on the shorts panel.
- **Do** keep the global focus ring as a 3px trim outline at 3px offset, and give every motion a reduced-motion path.

### Don't:
- **Don't** hard-code a kit hex on a component; it will break the other kit.
- **Don't** turn the page into a dark developer portfolio with a particle hero.
- **Don't** float rounded cards on the field; the rookie card is the only card-shaped object.
- **Don't** set sentences in Anton or in caps.
