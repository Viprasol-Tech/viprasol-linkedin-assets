const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.defineLayout({ name: "SQUARE", width: 10, height: 10 });
pres.layout = "SQUARE";
pres.author = "Viprasol Tech";
pres.title = "I Lost $3000 in Forex - Algo Trading Carousel";

// Brand colors (no # prefix)
const TEAL = "0D9488";
const DARK = "0A0A0A";
const GOLD = "FBBF24";
const WHITE = "FFFFFF";
const RED = "EF4444";
const GREEN = "22C55E";
const DARK_TEAL = "065F56";
const MUTED = "A0A0A0";

// ========================
// SLIDE 1: COVER
// ========================
let s1 = pres.addSlide();
s1.background = { color: DARK_TEAL };
// Overlay dark gradient effect using shapes
s1.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: 0, w: 3.5, h: 10, fill: { color: DARK, transparency: 40 } });

s1.addText([
  { text: "I Lost ", options: { color: WHITE, fontSize: 60, bold: true } },
  { text: "$3,000", options: { color: GOLD, fontSize: 60, bold: true } },
  { text: " in Forex.", options: { color: WHITE, fontSize: 60, bold: true, breakLine: true } },
  { text: "Then I Learned", options: { color: WHITE, fontSize: 60, bold: true, breakLine: true } },
  { text: "to ", options: { color: WHITE, fontSize: 60, bold: true } },
  { text: "Code.", options: { color: GOLD, fontSize: 60, bold: true } }
], { x: 0.8, y: 2.5, w: 8.5, h: 4, fontFace: "Arial Black", valign: "middle" });

s1.addText("How algorithmic trading changed everything.\nSwipe to see the full story →", {
  x: 0.8, y: 7, w: 7, h: 1.2, color: MUTED, fontSize: 22, fontFace: "Arial"
});

s1.addText("Viprasol Tech", {
  x: 6.5, y: 9, w: 3, h: 0.6, color: MUTED, fontSize: 16, fontFace: "Arial", align: "right"
});

// ========================
// SLIDE 2: STATS
// ========================
let s2 = pres.addSlide();
s2.background = { color: DARK };

s2.addText("The Brutal Truth About\nManual Trading", {
  x: 0.8, y: 0.5, w: 8.5, h: 1.8, color: TEAL, fontSize: 42, bold: true, fontFace: "Arial Black", valign: "top"
});

// Stat boxes - 2x2 grid
const statData = [
  { num: "90%", label: "of retail traders\nLOSE money", x: 0.5, y: 2.8 },
  { num: "8hrs", label: "average daily\nscreen time", x: 5.2, y: 2.8 },
  { num: "73%", label: "of losses caused by\nEMOTIONAL decisions", x: 0.5, y: 6.2 },
  { num: "$0", label: "what most traders\nmake after 2 years", x: 5.2, y: 6.2 }
];

statData.forEach(s => {
  pres.addSlide; // not needed, just operating on s2
  s2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: s.x, y: s.y, w: 4.3, h: 3, fill: { color: TEAL, transparency: 85 },
    line: { color: TEAL, width: 2 }, rectRadius: 0.2
  });
  s2.addText(s.num, {
    x: s.x, y: s.y + 0.3, w: 4.3, h: 1.5, color: GOLD, fontSize: 56, bold: true,
    fontFace: "Arial Black", align: "center", valign: "middle"
  });
  s2.addText(s.label, {
    x: s.x, y: s.y + 1.8, w: 4.3, h: 1, color: MUTED, fontSize: 18,
    fontFace: "Arial", align: "center", valign: "top"
  });
});

s2.addText("2/6", { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
s2.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

// ========================
// SLIDE 3: PROBLEMS
// ========================
let s3 = pres.addSlide();
s3.background = { color: "1A0505" };

s3.addText("Why Manual Traders Fail", {
  x: 0.8, y: 0.6, w: 8.5, h: 1.2, color: RED, fontSize: 44, bold: true, fontFace: "Arial Black"
});

const problems = [
  "Fear closes winning trades too early",
  "Greed moves stop losses (then you lose more)",
  "You miss trades while sleeping or working",
  "Revenge trading after a loss destroys accounts",
  "Inconsistent execution kills even good strategies"
];

problems.forEach((p, i) => {
  let yPos = 2.3 + (i * 1.4);
  s3.addText("X", {
    x: 0.8, y: yPos, w: 0.8, h: 0.8, color: RED, fontSize: 32, bold: true,
    fontFace: "Arial Black", align: "center", valign: "middle"
  });
  s3.addText(p, {
    x: 1.8, y: yPos, w: 7.5, h: 0.8, color: WHITE, fontSize: 24,
    fontFace: "Arial", valign: "middle"
  });
  if (i < problems.length - 1) {
    s3.addShape(pres.shapes.LINE, {
      x: 0.8, y: yPos + 1.1, w: 8.5, h: 0, line: { color: WHITE, width: 0.5, transparency: 85 }
    });
  }
});

s3.addText("3/6", { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
s3.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

// ========================
// SLIDE 4: SOLUTION
// ========================
let s4 = pres.addSlide();
s4.background = { color: "051A0D" };

s4.addText("The Algo Trading Advantage", {
  x: 0.8, y: 0.6, w: 8.5, h: 1.2, color: GREEN, fontSize: 44, bold: true, fontFace: "Arial Black"
});

const solutions = [
  "Trades 24/7 — never misses an entry",
  "Zero emotions — executes perfectly every time",
  "Backtested across 5+ years of data",
  "Risk management hardcoded (can't be overridden)",
  "Consistent execution = consistent results"
];

solutions.forEach((s, i) => {
  let yPos = 2.3 + (i * 1.4);
  s4.addText("✓", {
    x: 0.8, y: yPos, w: 0.8, h: 0.8, color: GREEN, fontSize: 36, bold: true,
    fontFace: "Arial", align: "center", valign: "middle"
  });
  s4.addText(s, {
    x: 1.8, y: yPos, w: 7.5, h: 0.8, color: WHITE, fontSize: 24,
    fontFace: "Arial", valign: "middle"
  });
  if (i < solutions.length - 1) {
    s4.addShape(pres.shapes.LINE, {
      x: 0.8, y: yPos + 1.1, w: 8.5, h: 0, line: { color: WHITE, width: 0.5, transparency: 85 }
    });
  }
});

s4.addText("4/6", { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
s4.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

// ========================
// SLIDE 5: RESULTS
// ========================
let s5 = pres.addSlide();
s5.background = { color: DARK };

s5.addText("Our Verified Results", {
  x: 0.8, y: 0.5, w: 8.5, h: 1.2, color: GOLD, fontSize: 44, bold: true, fontFace: "Arial Black"
});

const results = [
  { num: "135%", label: "Average Monthly Return\n(MyFXBook Verified)", x: 0.5, y: 2.2 },
  { num: "81%", label: "Win Rate Across\nLive Accounts", x: 5.2, y: 2.2 },
  { num: "44K+", label: "Pips Gained\nAnd Counting", x: 0.5, y: 5.8 },
  { num: "500+", label: "Traders Trust\nOur Systems", x: 5.2, y: 5.8 }
];

results.forEach(r => {
  s5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: r.x, y: r.y, w: 4.3, h: 3.2, fill: { color: GOLD, transparency: 88 },
    line: { color: GOLD, width: 2 }, rectRadius: 0.2
  });
  s5.addText(r.num, {
    x: r.x, y: r.y + 0.3, w: 4.3, h: 1.5, color: GOLD, fontSize: 64, bold: true,
    fontFace: "Arial Black", align: "center", valign: "middle"
  });
  s5.addText(r.label, {
    x: r.x, y: r.y + 2, w: 4.3, h: 1, color: MUTED, fontSize: 17,
    fontFace: "Arial", align: "center", valign: "top"
  });
});

s5.addText("5/6", { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
s5.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

// ========================
// SLIDE 6: CTA
// ========================
let s6 = pres.addSlide();
s6.background = { color: DARK_TEAL };

s6.addText("Ready to Stop\nTrading Manually?", {
  x: 0.5, y: 1.5, w: 9, h: 2.5, color: WHITE, fontSize: 52, bold: true,
  fontFace: "Arial Black", align: "center", valign: "middle"
});

// Gold CTA button
s6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 2.5, y: 4.5, w: 5, h: 1.3, fill: { color: GOLD }, rectRadius: 0.15
});
s6.addText('DM me "ALGO"', {
  x: 2.5, y: 4.5, w: 5, h: 1.3, color: DARK, fontSize: 36, bold: true,
  fontFace: "Arial Black", align: "center", valign: "middle"
});

s6.addText("Free Strategy Consultation\nCustom EA Development\nVerified Results", {
  x: 1.5, y: 6.2, w: 7, h: 1.8, color: WHITE, fontSize: 22,
  fontFace: "Arial", align: "center", valign: "middle", transparency: 20
});

s6.addText("viprasol.com", {
  x: 2.5, y: 8.3, w: 5, h: 0.7, color: MUTED, fontSize: 24,
  fontFace: "Arial", align: "center"
});

s6.addText("6/6", { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
s6.addText("Viprasol Tech", { x: 3.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 16, fontFace: "Arial", align: "center" });

// Save
const outPath = "C:/Users/viprasol/Downloads/Telegram Desktop/linkedin/images/day1-carousel.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("Carousel saved to: " + outPath);
}).catch(err => {
  console.error("Error:", err);
});
