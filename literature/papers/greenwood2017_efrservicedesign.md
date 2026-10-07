---
id: greenwood2017_efrservicedesign
title: "Frequency response services designed for energy storage"
authors: ["Greenwood, D.M.", "Lim, K.Y.", "Patsios, C.", "Lyons, P.F.", "Lim, Y.S.", "Taylor, P.C."]
year: 2017
journal: "Applied Energy"
volume_issue_pages: "203:115-127"
doi: "10.1016/j.apenergy.2017.06.046"
quartile: "Q1 (SJR 2017, Energy Engineering and Power Technology)"
quartile_basis: "pub-year; rule=pass; checked in this entry"
group: "Phil Taylor group, Newcastle University (with Universiti Tunku Abdul Rahman, Malaysia)"
lineage: "Taylor (Newcastle, later Bristol) senior author; Greenwood, Patsios, Lyons = Newcastle researchers in Taylor's group (EPSRC EP/K002252/1). Advisor-student ties not verified."
streams: [S6_ancillary_products]
market_context: "GB Enhanced Frequency Response (EFR, 2016 tender) and existing GB frequency response services"
method_class: "real-time simulation + power-hardware-in-the-loop + statistical analysis (no optimisation)"
evidence_read: "abstract (Bath/Bristol research portals) + conference slides by first author; full text CC-BY but publisher/eprints PDFs blocked to fetcher"
oa_link: "https://eprints.ncl.ac.uk/238873"
---

## 1. Research question
How should frequency response services be specified so that energy storage can deliver them, and how can storage design/operational requirements (energy, SoC behaviour) under a given service specification be quantified? (from abstract)

## 2. Setting & assumptions
- GB transmission system; service framework = existing GB services and the newly tendered EFR (1 s full delivery, wide/narrow deadband variants).
- Storage modelled in a real-time network simulator and tested with power hardware in the loop (PHIL).
- High-resolution measured GB frequency data drive the analysis (exact period/resolution not verified).

## 3. Constraints that drove the model choice
Service compliance is defined on second-scale trajectories (envelope, response time), so the authors use real-time simulation + PHIL rather than an optimisation model; statistical techniques are needed to translate frequency distributions into storage energy/SoC requirements.

## 4. Model
- Real-time network simulation of the GB system with an ESS following a service droop/envelope.
- PHIL test of a physical storage unit.
- Novel statistical techniques to derive ESS design (energy capacity) and operational requirements from the service specification and frequency data.
- Illustrative new service design proposed.

## 5. Data & processing
High-resolution GB transmission-system frequency data (source National Grid; period not verified). Slides report ESS response within 80 ms and frequency-nadir improvement vs EFR MW procured (0–500 MW).

## 6. Justification
Laboratory PHIL validation of storage response; statistical quantification on measured frequency (from abstract).

## 7. Key results
- Methods to assess ESS performance within existing service frameworks and to design new services "to take advantage of the capabilities of ESS" (from abstract).
- First-author slides: storage responds within ~80 ms; more EFR MW reduces frequency nadir (49.3–49.7 Hz range in plotted cases).
- Numerical SoC/energy-requirement results not verified (full text not read).

## 8. Limitations (stated + your critical reading)
- No economics (revenue, degradation) — engineering service-design focus.
- EFR was a one-off 2016 tender (201 MW, 4-year contracts) later replaced by Dynamic Containment; results are specification-specific.

## 9. Relevance to my study
Key GB reference arguing that the product specification itself (deadband, envelope, SoC-management allowance) should be designed around storage; supports treating product rules as explanatory variables of battery operation.

## 10. Lineage links
- Builds on: National Grid EFR specification (2016).
- Built upon by (notable): gundogdu2018_efrtriad; lee2019_closedloopgb; cao2024_dcvsefr; Vorobev, Greenwood et al., "Deadbands, droop and inertia impact on power system frequency distribution" (IEEE TPWRS 2019, not archived).

## 11. Verification log
- OpenAlex works/doi:10.1016/j.apenergy.2017.06.046: title, year, 203:115-127, authors/affiliations (Newcastle; UTAR Malaysia). Bath portal: abstract verbatim, CC BY 4.0.
- SJR sid 28801: Applied Energy Q1 2017.
- Full text not read (ScienceDirect and eprints.ncl.ac.uk PDF blocked by robots). Slides: cesi.meeting-mojo.com/uploads/3343/cesi_david-greenwood.pdf.
