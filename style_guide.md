# PulseIQ Dashboard Style Guide

## 1. Purpose
This style guide defines the visual standards for PulseIQ workforce analytics dashboards. It ensures consistency, readability, and accessibility across all charts and dashboard pages.

## 2. Colour Palette

The dashboard uses a colour-blind-friendly palette inspired by the Okabe–Ito colour scheme.

| Purpose | Colour | Hex Code |
|---|---|---|
| Primary data | Blue | #0072B2 |
| Secondary data | Orange | #E69F00 |
| Positive indicators | Bluish Green | #009E73 |
| Additional categories | Reddish Purple | #CC79A7 |
| Main text | Dark Grey | #333333 |
| Dashboard background | Light Grey | #F3F5F7 |
| Chart background | White | #FFFFFF |

Accessibility rules:
- Do not use colour alone to communicate meaning.
- Use labels, legends, and clear chart titles.
- Maintain sufficient contrast between text and background.
- Apply colours consistently across all dashboards.

## 3. Typography

- Dashboard title: Arial, bold, 24–28 px.
- Section headings: Arial, bold, 18–20 px.
- Chart titles: Arial, bold, 16–18 px.
- Chart labels: Arial, regular, 12–14 px.
- KPI values: Arial, bold, 24–32 px.

Use a consistent font throughout the dashboard. Avoid decorative fonts and overcrowded labels.

## 4. Chart Title and Takeaway Rules

Every chart must include:
1. A clear, descriptive title.
2. A one-line takeaway explaining the main insight.

Examples:

- **Employee Count by Department**  
  Takeaway: Shows how employees are distributed across departments.

- **Headcount Trend**  
  Takeaway: Highlights workforce growth or decline over time.

- **Workforce by Role**  
  Takeaway: Compares employee distribution across job roles.

- **Joiners vs Leavers**  
  Takeaway: Compares employee additions with departures over time.

Avoid vague titles such as "Chart 1" or "Data Analysis".

## 5. Number Formats

| Metric | Format | Example |
|---|---|---|
| Employee count | Whole number with thousands separator | 1,606 |
| Department count | Whole number | 12 |
| Percentage | One decimal place | 12.5% |
| Average tenure | One decimal place with unit | 3.4 years |
| Payroll cost | Indian currency format | ₹12,50,000 |
| Monthly trend | Month and year | Jan 2026 |

Use consistent number formats throughout the dashboard. Use actual database results rather than illustrative values.

## 6. Dashboard Layout

- Place the dashboard title and reporting period in the header.
- Display four key performance indicators (KPIs) at the top.
- Arrange charts below the KPI row in a clean, aligned grid.
- Place dashboard filters in a side panel where supported.
- Keep chart spacing, titles, and backgrounds consistent.
- On smaller screens, stack charts vertically and keep filters easy to access.

## 7. Design Review Checklist

- [ ] The most important KPI appears first.
- [ ] Titles and labels are readable on a laptop.
- [ ] Charts remain understandable on a mobile screen.
- [ ] The colour palette is colour-blind friendly.
- [ ] Text and background have sufficient contrast.
- [ ] Every chart has a title and a one-line takeaway.
- [ ] Number formats are consistent.
- [ ] Illustrative values have been replaced with verified data.

## 8. Review and Improvements

The layout prioritises total employee headcount, followed by other workforce KPIs. The colour palette uses distinct hues to reduce dependence on red-versus-green distinctions. Consistent typography and number formatting improve readability. A responsive, single-column chart arrangement is recommended for mobile screens.

Final validation must be performed in Apache Superset on both laptop and mobile-sized screens before publishing.