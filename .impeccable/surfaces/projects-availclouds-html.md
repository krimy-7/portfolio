---
version: 1
slug: "projects-availclouds-html"
primary_target: "projects/availclouds.html"
related_targets: []
---

# Surface: projects/availclouds.html (Availclouds MSP landing page)

Scope: standalone Persuade page for Availclouds LLC's white-label after-hours help desk for US MSPs. Its own world; not the portfolio's kit system (PRODUCT.md marks this page out of the portfolio's design scope).
Audience: owners and service managers of small to mid US MSPs. Job: believe a Kathmandu team can run their nights invisibly and safely. Action: book a 20-minute call (working slot scheduler) or request the two-week paid pilot.
Proof on hand: the mechanism itself (time zones), the morning handoff example, the sample monthly report (both labelled invented), the pilot steps. No testimonials or logos exist; none are invented.
Constraints: no build step, single HTML file, Google Fonts only, works without JS (baked times, email fallback). Demo data still to be replaced before launch: founder names, prices, team size, tool list, phone routing.
Chosen: "Follow the Sun" (IMPECCABLE'S PICK, round e3863f53), with an animated map requested by the owner.

## Assets and provenance
- Logo mark: authored inline SVG (option B of three rendered in .impeccable/mocks/logo-availclouds/, chosen by the owner): a cloud split by the terminator, night blue #1A5FD6-#2A8BF2 left, daylight orange #FF7F2B-#FDB827 right (availclouds.com CTA orange), three star dots, textured on the owner's request ("add some textures in the logo, it's too plain"): the hero's dot-matrix on the night half, a sun glow and three rays on the day half, a pink-orange twilight seam and a soft top light (option 1 of three in textured.png); lockup "Availclouds / AFTER-HOURS DESK". Replaces the owner-supplied raster mark, which was drawn for white grounds (baked black shadow) and read poorly on navy. No raster ships.
- Owner requests after the build: animated map (example-night replay, town lights), hover lens on map dots ("can those little block do some movement? like zoom in"), optimised for a 1366x657 laptop viewport; continuous loop with no replay button (night, 8 AM hold, day fast-forward, next night).
- DESIGN.md at the repo root documents the portfolio, not this page; this brief is this page's design record.

## Direction contract
THESIS: The page is a live map of day and night: when the US is dark, Kathmandu is lit, and that is the product. It refuses the category's headset-agent stock hero and icon-card grid.
OWN-WORLD: Night navy #0B1430 owns the hero, security and booking; pale day-sky #EAF2FA owns the working sections; one lamp amber #FBA41A (the logo's amber; changed from #F2B705 when the owner supplied the logo with "this is our company logo") for the desk, live status and the primary action; dot-matrix land; Red Hat Display 800 headlines, Red Hat Mono only for times and data; hairline hour meridians.
STORY: The visitor sees their own city dark and our desk lit, understands the night shift is our daytime, watches tickets cross to Kathmandu and come back resolved, then reads coverage, scope, handoff, pilot, security and books a slot.
FIRST VIEWPORT: Full-bleed dot map with the real terminator; New York and Kathmandu pins with live clocks; H1 at ~84px over the dark Atlantic, lede, gold "Book a 20-minute call" and the pilot link bottom-left; a readout strip with live status and a "Play last night" control along the bottom edge.
FORM: Dot-matrix world map with live solar terminator, pick card (rank 1 of my grounded list), seed e3863f53. Signature interaction: a time-lapse of one night (6 PM to 8 AM Eastern) where ticket arcs fly from US cities to Kathmandu and return resolved, ending on the morning-handoff tally; live ticket flow while the desk is on shift.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
