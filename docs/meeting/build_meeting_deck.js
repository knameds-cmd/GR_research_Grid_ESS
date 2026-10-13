// Research meeting deck: 3 slides, white background, Times New Roman, English.
// Build: npm install pptxgenjs, then NODE_PATH=./node_modules node build_meeting_deck.js out.pptx (apply_theme.js comes from the pptx skill).
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(
  "/root/.claude/skills/synced/b2a054f3-edc9-4060-a65f-8749b77dfff4_163eb27a-e6ef-4b9e-9dae-85af8bd8acd2/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";
const THEME = {
  name: "Research Meeting",
  headFontFace: "Times New Roman",
  bodyFontFace: "Times New Roman",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "262626", lt2: "F2F2F2",
    accent1: "1F3864", accent2: "595959", accent3: "7F7F7F", accent4: "A6A6A6",
    accent5: "BFBFBF", accent6: "D9D9D9", hlink: "1F3864", folHlink: "595959",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "GB grid-scale batteries and market rules: research meeting";
const C = pres.SchemeColor;
const FONT = "Times New Roman";
const X = 0.6, W = 12.13;

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X, y: 0.35, w: W, h: 0.8, fontSize: 30,
      bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.25, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: "7F7F7F", fontFace: FONT, align: "right" },
});

const border = () => ({ type: "solid", pt: 0.75, color: "A6A6A6" });
const cell = (text, o = {}) => ({ text, options: { fontFace: FONT, fontSize: 16, color: C.text1, valign: "top",
  margin: [0.06, 0.08, 0.06, 0.08], border: [border(), border(), border(), border()], ...o } });
const head = (text, o = {}) => cell(text, { bold: true, fill: { color: C.background2 }, valign: "middle", ...o });
const label = (text, o = {}) => cell(text, { bold: true, ...o });

pres.addSection({ title: "Research meeting" });

// 1. Research topic and objectives
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Research meeting" });
  s.addText("Research Topic and Objectives", { placeholder: "title" });
  const rows = [
    [label("Topic", { fill: { color: C.background2 } }),
     cell("Which GB market product rules made grid-scale batteries profitable, and how much does each rule change revenue and operation?",
       { colspan: 2, italic: true, fill: { color: C.background2 } })],
    [head("Question"), head("What we want to find out"), head("Method")],
    [label("RQ1  Revenue evolution"),
     cell("How the battery revenue mix changed from 2020 to 2026, and which rule changes defined each phase"),
     cell("Revenue-stack decomposition from public data; rule timeline")],
    [label("RQ2  Rule attribution"),
     cell("How much each rule (fast frequency response, EAC co-optimisation, SoE rule, reserve products, BM access) contributes to revenue, and whether this differs between phases"),
     cell("Rule on/off counterfactuals in an optimisation model; Shapley decomposition")],
    [label("RQ3  Operating strategy"),
     cell("How optimal bidding and operation (service allocation, cycling, state of energy) change when rules change"),
     cell("Perfect-foresight vs rolling-horizon MILP")],
    [label("Benchmark  Realised revenue"),
     cell("How far actual battery revenue falls below the model upper bound"),
     cell("Unit-level revenue rebuilt from public EAC, BM and wholesale data")],
  ];
  s.addTable(rows, { x: X, y: 1.45, w: W, colW: [2.75, 5.38, 4.0], objectName: "Research topic table" });
}

// 2. GB market phases
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Research meeting" });
  s.addText("GB Market Phases", { placeholder: "title" });
  const rows = [
    [head("Phase"), head("Period"), head("Key rule changes"), head("Battery revenue")],
    [label("1  Contracted Entry"), cell("2016 – Sep 2020"),
     cell("Enhanced Frequency Response tender (2016, 4-year contracts); Firm Frequency Response; Capacity Market"),
     cell("First commercial batteries on fixed-term contracts")],
    [label("2  Scarcity Boom"), cell("Oct 2020 – 2022"),
     cell("Dynamic Containment launched (price cap £17/MW/h); DC\u00A0+\u00A0BM stacking allowed (2021); DM and DR (2022)"),
     cell("Frequency response ≈\u00A090% of revenue")],
    [label("3  Saturation and EAC"), cell("2023 – 2024"),
     cell("DC prices fall by over 90%; EAC co-optimised auction (Nov 2023); Balancing Reserve and 30-min rule (Mar 2024); SoE rules (2024); Quick Reserve (Dec 2024)"),
     cell("Shift to wholesale + BM; ≈\u00A0£50k/MW/yr in 2024")],
    [label("4  Merchant and Dispatch Reform"), cell("2025 – present"),
     cell("Quick Reserve open to non-BM units (Sep 2025); BR moves into EAC (Oct 2025); Slow Reserve (Mar\u00A02026); GC0166 BM parameters"),
     cell("Wholesale + BM ≈\u00A060%, ancillary ≈\u00A01/3, Capacity Market ≈\u00A010%")],
  ];
  s.addTable(rows, { x: X, y: 1.45, w: W, colW: [2.75, 1.75, 4.88, 2.75], objectName: "Market phases table" });
  s.addText("The model compares pre-EAC (2021 – Oct 2023) and post-EAC (Nov 2023 onwards) conditions with the same engine.",
    { x: X, y: 5.9, w: W, h: 0.4, fontSize: 16, color: C.text1, margin: 0, isTextBox: true, objectName: "Analysis note" });
  s.addText("Revenue shares: Modo GB index, indicative.",
    { x: X, y: 6.4, w: W, h: 0.3, fontSize: 11, color: C.accent3, margin: 0, isTextBox: true, objectName: "Source note" });
}

// 3. Modelling approach and rationale
{
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Research meeting" });
  s.addText("Modelling Approach and Rationale", { placeholder: "title" });
  const rows = [
    [head("Modelling choice"), head("Rationale")],
    [label("Perfect-foresight MILP (first layer)"),
     cell("Gives the revenue upper bound; losses from imperfect information (rolling horizon) and BM non-acceptance are measured against it")],
    [label("Price-taking battery, 50 MW / 2 h"),
     cell("A single unit barely moves prices; 2 h is the dominant new-build duration (1 h and 4 h as scenarios)")],
    [label("30-min periods; DC/DM/DR fixed per 4-h EFA block"),
     cell("Matches GB settlement and the auction product definitions")],
    [label("Wholesale price: Elexon MID"),
     cell("Free and public; also used by the closest Q1 study (Gale et al. 2026), so results are comparable")],
    [label("Revenue: wholesale + EAC services"),
     cell("DC/DM/DR and BR/QR/SR can be stacked with trading in the same period; BM and Capacity Market are added as later layers")],
    [label("Headroom and energy constraints"),
     cell("Services must be deliverable: power margin around the baseline, energy for the contracted duration (2024 SoE rule), energy drawn by frequency response")],
    [label("Charge/discharge binaries"),
     cell("Prevent simultaneous charging and discharging at negative prices")],
    [label("Rule switches + Shapley decomposition"),
     cell("Attribute revenue to each rule; Shapley averages over all orderings because rules interact")],
  ];
  s.addTable(rows, { x: X, y: 1.45, w: W, colW: [4.3, 7.83], objectName: "Modelling table" });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
