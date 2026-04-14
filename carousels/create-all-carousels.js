const pptxgen = require("pptxgenjs");
const path = require("path");

const TEAL = "0D9488";
const DARK = "0A0A0A";
const GOLD = "FBBF24";
const WHITE = "FFFFFF";
const RED = "EF4444";
const GREEN = "22C55E";
const DARK_TEAL = "065F56";
const MUTED = "A0A0A0";

function createPresentation() {
  let pres = new pptxgen();
  pres.defineLayout({ name: "SQUARE", width: 10, height: 10 });
  pres.layout = "SQUARE";
  pres.author = "Viprasol Tech";
  return pres;
}

function addBranding(slide, slideNum, total) {
  slide.addText(slideNum + "/" + total, { x: 9, y: 0.3, w: 0.7, h: 0.4, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
  slide.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });
}

// =============================================
// CAROUSEL 2: "5 Signs You Need a Trading Bot"
// =============================================
function createCarousel2() {
  let pres = createPresentation();
  pres.title = "5 Signs You Need a Trading Bot";

  // Cover
  let s1 = pres.addSlide();
  s1.background = { color: DARK };
  s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 4, fill: { color: TEAL, transparency: 70 } });
  s1.addText([
    { text: "5 Signs\n", options: { color: GOLD, fontSize: 72, bold: true } },
    { text: "You Need a\nTrading Bot", options: { color: WHITE, fontSize: 60, bold: true } }
  ], { x: 0.8, y: 1.5, w: 8.5, h: 5, fontFace: "Arial Black", valign: "middle" });
  s1.addText("Save this post. Swipe →", { x: 0.8, y: 8, w: 5, h: 0.6, color: MUTED, fontSize: 20, fontFace: "Arial" });
  s1.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

  const signs = [
    { num: "01", title: "You Miss Trades While Sleeping", desc: "The best setups happen at 3 AM.\nYour bot doesn't sleep. You do.\nStop losing opportunities.", bg: "0D1B2A" },
    { num: "02", title: "You Move Your Stop Loss", desc: "\"Just this once\" turns into\nevery single time.\nA bot follows rules. Period.", bg: "1A0505" },
    { num: "03", title: "You Close Winners Too Early", desc: "Fear of giving back profits\nmakes you exit at +20 pips\nwhen the move goes +200.", bg: "0D1117" },
    { num: "04", title: "You Revenge Trade After Losses", desc: "Lost $500? Time to make it back NOW.\nThat $500 becomes $2,000 in losses.\nBots don't have ego.", bg: "1A1A00" },
    { num: "05", title: "Your Results Are Inconsistent", desc: "+15% one month, -20% the next.\nSame strategy, different execution.\nAutomation = consistency.", bg: "051A0D" }
  ];

  signs.forEach((s, i) => {
    let slide = pres.addSlide();
    slide.background = { color: s.bg };
    slide.addText(s.num, { x: 0.8, y: 0.8, w: 2, h: 1.5, color: GOLD, fontSize: 80, bold: true, fontFace: "Arial Black", transparency: 30 });
    slide.addText(s.title, { x: 0.8, y: 2.5, w: 8.5, h: 1.5, color: WHITE, fontSize: 40, bold: true, fontFace: "Arial Black" });
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 4.2, w: 3, h: 0.06, fill: { color: GOLD } });
    slide.addText(s.desc, { x: 0.8, y: 4.8, w: 8.5, h: 3, color: MUTED, fontSize: 28, fontFace: "Arial" });
    addBranding(slide, i + 2, 7);
  });

  // CTA slide
  let cta = pres.addSlide();
  cta.background = { color: DARK_TEAL };
  cta.addText("If you said YES\nto any of these...", { x: 0.5, y: 1, w: 9, h: 2, color: WHITE, fontSize: 44, bold: true, fontFace: "Arial Black", align: "center" });
  cta.addText("It's time to automate.", { x: 0.5, y: 3.5, w: 9, h: 1.2, color: GOLD, fontSize: 48, bold: true, fontFace: "Arial Black", align: "center" });
  cta.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.5, y: 5.5, w: 5, h: 1.3, fill: { color: GOLD }, rectRadius: 0.15 });
  cta.addText('DM "ALGO" to Start', { x: 2.5, y: 5.5, w: 5, h: 1.3, color: DARK, fontSize: 32, bold: true, fontFace: "Arial Black", align: "center", valign: "middle" });
  cta.addText("viprasol.com", { x: 2.5, y: 7.5, w: 5, h: 0.7, color: MUTED, fontSize: 22, fontFace: "Arial", align: "center" });
  addBranding(cta, 7, 7);

  return pres;
}

// =============================================
// CAROUSEL 3: "Manual vs Automated Trading"
// =============================================
function createCarousel3() {
  let pres = createPresentation();
  pres.title = "Manual vs Automated Trading";

  let s1 = pres.addSlide();
  s1.background = { color: DARK };
  s1.addText([
    { text: "Manual ", options: { color: RED, fontSize: 56, bold: true } },
    { text: "vs ", options: { color: WHITE, fontSize: 56, bold: true } },
    { text: "Automated\n", options: { color: GREEN, fontSize: 56, bold: true } },
    { text: "Trading", options: { color: WHITE, fontSize: 56, bold: true } }
  ], { x: 0.8, y: 2, w: 8.5, h: 4, fontFace: "Arial Black", valign: "middle" });
  s1.addText("Same strategy. Different results.\nSwipe to compare →", { x: 0.8, y: 7, w: 7, h: 1.2, color: MUTED, fontSize: 22, fontFace: "Arial" });
  s1.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

  const comparisons = [
    { category: "Trade Execution", manual: "Missed 12 entries\n(sleeping/working)", auto: "Caught all 47 signals\n(24/7 operation)", manColor: RED, autoColor: GREEN },
    { category: "Stop Losses", manual: "Moved SL on 5 trades\n(lost more money)", auto: "Executed perfectly\n(every single time)", manColor: RED, autoColor: GREEN },
    { category: "Take Profits", manual: "Closed 3 winners early\n(left money on table)", auto: "Hit TP targets\n(no hesitation)", manColor: RED, autoColor: GREEN },
    { category: "After a Loss", manual: "Skipped 2 trades\n(fear after losing)", auto: "Traded next signal\n(no emotion)", manColor: RED, autoColor: GREEN },
    { category: "Monthly Result", manual: "+3.2%", auto: "+11.4%", manColor: RED, autoColor: GREEN }
  ];

  comparisons.forEach((c, i) => {
    let slide = pres.addSlide();
    slide.background = { color: DARK };
    slide.addText(c.category, { x: 0.5, y: 0.5, w: 9, h: 1, color: GOLD, fontSize: 36, bold: true, fontFace: "Arial Black", align: "center" });

    // Manual side
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2, w: 4.3, h: 6, fill: { color: RED, transparency: 85 } });
    slide.addText("MANUAL", { x: 0.5, y: 2.2, w: 4.3, h: 1, color: RED, fontSize: 28, bold: true, fontFace: "Arial Black", align: "center" });
    slide.addText(c.manual, { x: 0.7, y: 3.5, w: 3.9, h: 3.5, color: WHITE, fontSize: i === 4 ? 64 : 26, fontFace: "Arial", align: "center", valign: "middle" });

    // Auto side
    slide.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 2, w: 4.3, h: 6, fill: { color: GREEN, transparency: 85 } });
    slide.addText("AUTOMATED", { x: 5.2, y: 2.2, w: 4.3, h: 1, color: GREEN, fontSize: 28, bold: true, fontFace: "Arial Black", align: "center" });
    slide.addText(c.auto, { x: 5.4, y: 3.5, w: 3.9, h: 3.5, color: WHITE, fontSize: i === 4 ? 64 : 26, fontFace: "Arial", align: "center", valign: "middle" });

    addBranding(slide, i + 2, 7);
  });

  // CTA
  let cta = pres.addSlide();
  cta.background = { color: DARK_TEAL };
  cta.addText("3.5x Better Results.\nSame Strategy.", { x: 0.5, y: 1.5, w: 9, h: 2.5, color: WHITE, fontSize: 48, bold: true, fontFace: "Arial Black", align: "center" });
  cta.addText("The edge isn't the strategy.\nIt's the execution.", { x: 0.5, y: 4.5, w: 9, h: 1.5, color: GOLD, fontSize: 30, fontFace: "Arial", align: "center" });
  cta.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.5, y: 6.5, w: 5, h: 1.3, fill: { color: GOLD }, rectRadius: 0.15 });
  cta.addText('DM "ALGO" to Automate', { x: 2.5, y: 6.5, w: 5, h: 1.3, color: DARK, fontSize: 30, bold: true, fontFace: "Arial Black", align: "center", valign: "middle" });
  cta.addText("viprasol.com", { x: 2.5, y: 8.3, w: 5, h: 0.7, color: MUTED, fontSize: 22, fontFace: "Arial", align: "center" });
  addBranding(cta, 7, 7);

  return pres;
}

// =============================================
// CAROUSEL 4: "EA Pricing Breakdown"
// =============================================
function createCarousel4() {
  let pres = createPresentation();
  pres.title = "How Much Does a Custom EA Cost";

  let s1 = pres.addSlide();
  s1.background = { color: DARK };
  s1.addText([
    { text: "How Much Does a\nCustom EA ", options: { color: WHITE, fontSize: 52, bold: true } },
    { text: "Actually Cost?", options: { color: GOLD, fontSize: 52, bold: true } }
  ], { x: 0.8, y: 2, w: 8.5, h: 4, fontFace: "Arial Black", valign: "middle" });
  s1.addText("Transparent pricing. No surprises.\nSwipe →", { x: 0.8, y: 7, w: 7, h: 1, color: MUTED, fontSize: 22, fontFace: "Arial" });
  s1.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

  const tiers = [
    { name: "BASIC", price: "$300-800", features: ["Simple strategy (1-2 indicators)", "Single pair optimization", "Basic risk management", "1-year backtesting", "7 days support"], color: TEAL, bg: "0D1B2A" },
    { name: "STANDARD", price: "$800-2,000", features: ["Complex strategy (multi-condition)", "Multi-pair optimization", "Advanced risk management", "5-year backtesting + Monte Carlo", "30 days support"], color: GOLD, bg: "1A1500" },
    { name: "ADVANCED", price: "$2,000-5,000", features: ["Multi-strategy system", "AI/ML integration", "Dashboard and reporting", "Prop firm compliance", "Ongoing optimization"], color: "A855F7", bg: "150020" }
  ];

  tiers.forEach((t, i) => {
    let slide = pres.addSlide();
    slide.background = { color: t.bg };
    slide.addText(t.name, { x: 0.8, y: 0.8, w: 8.5, h: 1, color: t.color, fontSize: 36, bold: true, fontFace: "Arial Black" });
    slide.addText(t.price, { x: 0.8, y: 2, w: 8.5, h: 1.5, color: GOLD, fontSize: 64, bold: true, fontFace: "Arial Black" });
    slide.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 3.8, w: 4, h: 0.06, fill: { color: t.color } });

    t.features.forEach((f, fi) => {
      slide.addText("✓  " + f, { x: 0.8, y: 4.3 + (fi * 1.1), w: 8.5, h: 0.8, color: WHITE, fontSize: 24, fontFace: "Arial" });
    });
    addBranding(slide, i + 2, 5);
  });

  // ROI slide
  let roi = pres.addSlide();
  roi.background = { color: DARK };
  roi.addText("THE ROI MATH", { x: 0.5, y: 0.5, w: 9, h: 1, color: TEAL, fontSize: 36, bold: true, fontFace: "Arial Black", align: "center" });
  roi.addText("$500 EA", { x: 0.5, y: 2, w: 9, h: 1.2, color: WHITE, fontSize: 48, bold: true, fontFace: "Arial Black", align: "center" });
  roi.addText("+", { x: 0.5, y: 3.2, w: 9, h: 0.8, color: MUTED, fontSize: 36, fontFace: "Arial", align: "center" });
  roi.addText("5%/month on $10K account", { x: 0.5, y: 4, w: 9, h: 1, color: WHITE, fontSize: 30, fontFace: "Arial", align: "center" });
  roi.addText("=", { x: 0.5, y: 5, w: 9, h: 0.8, color: MUTED, fontSize: 36, fontFace: "Arial", align: "center" });
  roi.addText("$500/month profit", { x: 0.5, y: 5.8, w: 9, h: 1.2, color: GOLD, fontSize: 48, bold: true, fontFace: "Arial Black", align: "center" });
  roi.addText("ROI = 1 month", { x: 0.5, y: 7.2, w: 9, h: 1, color: GREEN, fontSize: 36, bold: true, fontFace: "Arial Black", align: "center" });
  roi.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.5, y: 8.5, w: 5, h: 0.8, fill: { color: GOLD }, rectRadius: 0.1 });
  roi.addText('DM "BUILD" for a Quote', { x: 2.5, y: 8.5, w: 5, h: 0.8, color: DARK, fontSize: 22, bold: true, fontFace: "Arial Black", align: "center", valign: "middle" });
  addBranding(roi, 5, 5);

  return pres;
}

// =============================================
// CAROUSEL 5: "Risk Management Rules"
// =============================================
function createCarousel5() {
  let pres = createPresentation();
  pres.title = "8 Risk Management Rules We Code Into Every EA";

  let s1 = pres.addSlide();
  s1.background = { color: DARK };
  s1.addText([
    { text: "8 Risk Rules\n", options: { color: GOLD, fontSize: 60, bold: true } },
    { text: "We Code Into\nEvery EA", options: { color: WHITE, fontSize: 52, bold: true } }
  ], { x: 0.8, y: 2, w: 8.5, h: 5, fontFace: "Arial Black", valign: "middle" });
  s1.addText("This is what separates pro EAs from gambling bots.\nSwipe →", { x: 0.8, y: 7.5, w: 8, h: 1, color: MUTED, fontSize: 20, fontFace: "Arial" });
  s1.addText("Viprasol Tech", { x: 6.5, y: 9.2, w: 3, h: 0.5, color: MUTED, fontSize: 14, fontFace: "Arial", align: "right" });

  const rules = [
    { num: "1", rule: "Max 2% Risk Per Trade", desc: "Never risk more than 2% of your account on a single trade. Adjustable based on your comfort." },
    { num: "2", rule: "Max 3 Simultaneous Positions", desc: "Prevents overexposure. No matter how good the signals look." },
    { num: "3", rule: "Daily Loss Limit: -5%", desc: "EA stops trading for the day if losses hit 5%. Protects against bad market days." },
    { num: "4", rule: "Weekly Loss Limit: -10%", desc: "EA pauses until Monday if weekly drawdown exceeds 10%." },
    { num: "5", rule: "News Filter", desc: "Stops trading 30 min before and after major economic events. Avoids volatility spikes." },
    { num: "6", rule: "Spread Filter", desc: "Skips trades if spread is abnormally high. No trading during illiquid hours." },
    { num: "7", rule: "Trailing Stop Loss", desc: "Locks in profits as trade moves in your favor. Never gives back big wins." },
    { num: "8", rule: "Break-Even Protection", desc: "Moves stop loss to entry after X pips of profit. Eliminates risk on winning trades." }
  ];

  // 2 rules per slide = 4 slides
  for (let i = 0; i < 4; i++) {
    let slide = pres.addSlide();
    slide.background = { color: DARK };

    for (let j = 0; j < 2; j++) {
      let r = rules[i * 2 + j];
      let yBase = j === 0 ? 0.5 : 5.2;

      slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: yBase, w: 9, h: 4.3, fill: { color: TEAL, transparency: 90 }, line: { color: TEAL, width: 1 } });
      slide.addText(r.num, { x: 0.8, y: yBase + 0.3, w: 1.5, h: 1.5, color: GOLD, fontSize: 56, bold: true, fontFace: "Arial Black", transparency: 40 });
      slide.addText(r.rule, { x: 2.5, y: yBase + 0.3, w: 6.5, h: 1.2, color: WHITE, fontSize: 30, bold: true, fontFace: "Arial Black" });
      slide.addText(r.desc, { x: 2.5, y: yBase + 1.8, w: 6.5, h: 2, color: MUTED, fontSize: 22, fontFace: "Arial" });
    }
    addBranding(slide, i + 2, 6);
  }

  // CTA
  let cta = pres.addSlide();
  cta.background = { color: DARK_TEAL };
  cta.addText("If your current bot\ndoesn't have these...", { x: 0.5, y: 1.5, w: 9, h: 2, color: WHITE, fontSize: 44, bold: true, fontFace: "Arial Black", align: "center" });
  cta.addText("It's a ticking time bomb.", { x: 0.5, y: 4, w: 9, h: 1.2, color: GOLD, fontSize: 40, bold: true, fontFace: "Arial Black", align: "center" });
  cta.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2, y: 6, w: 6, h: 1.3, fill: { color: GOLD }, rectRadius: 0.15 });
  cta.addText('DM "SAFE" for a Risk Audit', { x: 2, y: 6, w: 6, h: 1.3, color: DARK, fontSize: 28, bold: true, fontFace: "Arial Black", align: "center", valign: "middle" });
  cta.addText("viprasol.com", { x: 2.5, y: 8, w: 5, h: 0.7, color: MUTED, fontSize: 22, fontFace: "Arial", align: "center" });
  addBranding(cta, 6, 6);

  return pres;
}

// Generate all carousels
async function generateAll() {
  const outDir = path.join(__dirname, "..", "images");

  const carousels = [
    { fn: createCarousel2, name: "day2-5signs-carousel.pptx" },
    { fn: createCarousel3, name: "day3-manual-vs-auto-carousel.pptx" },
    { fn: createCarousel4, name: "day16-ea-pricing-carousel.pptx" },
    { fn: createCarousel5, name: "day13-risk-management-carousel.pptx" }
  ];

  for (const c of carousels) {
    const pres = c.fn();
    const outPath = path.join(outDir, c.name);
    await pres.writeFile({ fileName: outPath });
    console.log("Created: " + c.name);
  }

  console.log("\nAll carousels generated!");
}

generateAll().catch(console.error);
