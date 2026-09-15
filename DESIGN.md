---
name: MarkMint
description: Calm, Analytical, Premium, Trustworthy, Minimal exam intelligence engine.
colors:
  primary: "#006838"
  accent: "#E6327A"
  light-bg: "#E9E8E1"
  light-fg: "#123327"
  light-card: "#F7F6F2"
  dark-bg: "#0B1110"
  dark-fg: "#F3F0E8"
  dark-card: "#111917"
typography:
  display:
    fontFamily: "Geist, sans-serif"
    fontWeight: "bold"
  body:
    fontFamily: "Geist, sans-serif"
    fontWeight: "normal"
rounded:
  sm: "0.25rem"
  md: "0.375rem"
  lg: "0.5rem"
  xl: "0.75rem"
---

## Overview

MarkMint is a deterministic forecasting engine for SRMIST students. The visual language is calm, analytical, premium, trustworthy, and minimal. It avoids aggressive, "hype" aesthetics (no purple gradients, no pill-shaped buttons) in favor of structured data, clean spacing, and professional typography.

## Colors

The brand relies on an authoritative dark green (\#123327\) foreground on a warm, beige-tinted light background (\#E9E8E1\), shifting to a deep charcoal (\#0B1110\) background in dark mode. 
Primary actions use a stable green (\#006838\), while high-visibility accents (like charts or critical alerts) use magenta (\#E6327A\).

## Typography

The interface uses the \Geist\ and \Geist Mono\ font families. \Geist\ provides clean, highly legible body copy and headings, while \Geist Mono\ is used for precise numbers (GPA outputs, probabilities, credits) to reinforce the analytical nature of the tool.

## Layout

Layouts are structured and grid-based. Information architecture prioritizes scannability, with ample padding around cards and distinct separation between configuration controls and data output.

## Elevation & Depth

The design is mostly flat, using subtle borders (\order-border/50\) and slight background contrast (between \g-background\ and \g-card\) to delineate hierarchy instead of heavy drop shadows.

## Shapes

Corners are softly rounded (\ounded-xl\ for major cards, \ounded-md\ for inputs and buttons). Pill-shaped buttons (\ounded-full\) are strictly prohibited by the brand brief to avoid a bubbly or overly casual feel.

## Components

- **Inputs/Selects**: Structured, full-width or grid-aligned, using \g-background\ on top of \g-card\ for slight inset contrast.
- **Buttons**: Rectangular with medium border radii. Solid background for primary actions, transparent with borders for secondary.
- **Data Cards**: Used heavily for topic predictions and analytics. They feature clear data groupings, mono-spaced metrics, and subtle progress bars.

## Do's and Don'ts

- **Do** use lucide-react or SVG icons for crisp, professional iconography.
- **Do** use semantic Tailwind variables (\g-card\, \	ext-foreground\) so components adapt elegantly to both light and dark modes.
- **Don't** use purple gradients or "AI slop" aesthetics.
- **Don't** use emoji icons.
- **Don't** use em dashes inappropriately.
- **Don't** add fake reviews, metrics, or hallucinated AI chat interfaces.
