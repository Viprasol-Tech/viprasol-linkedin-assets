const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

const W = 1080, H = 1080;
const outDir = path.join(__dirname, '..', 'images');

function drawGradient(ctx, colors, x, y, w, h) {
  const grad = ctx.createLinearGradient(x, y, x + w, y + h);
  colors.forEach((c, i) => grad.addColorStop(i / (colors.length - 1), c));
  ctx.fillStyle = grad;
  ctx.fillRect(x, y, w, h);
}

function drawText(ctx, text, x, y, opts = {}) {
  const { size = 48, color = '#fff', font = 'bold', maxWidth = 900, lineHeight = 1.3, align = 'left' } = opts;
  ctx.fillStyle = color;
  ctx.font = `${font} ${size}px Arial`;
  ctx.textAlign = align;

  const lines = text.split('\n');
  let yPos = y;
  for (const line of lines) {
    const words = line.split(' ');
    let currentLine = '';
    for (const word of words) {
      const testLine = currentLine ? currentLine + ' ' + word : word;
      if (ctx.measureText(testLine).width > maxWidth && currentLine) {
        ctx.fillText(currentLine, x, yPos);
        currentLine = word;
        yPos += size * lineHeight;
      } else {
        currentLine = testLine;
      }
    }
    ctx.fillText(currentLine, x, yPos);
    yPos += size * lineHeight;
  }
  return yPos;
}

function addBranding(ctx, slideNum, total) {
  ctx.fillStyle = '#666';
  ctx.font = '18px Arial';
  ctx.textAlign = 'right';
  ctx.fillText(`${slideNum}/${total}`, W - 50, 40);
  ctx.fillText('Viprasol Tech', W - 50, H - 40);
}

function saveSlide(canvas, name) {
  const buffer = canvas.toBuffer('image/png');
  const filepath = path.join(outDir, name);
  fs.writeFileSync(filepath, buffer);
  console.log('Saved:', name);
}

// ==========================================
// SLIDE SET 1: Day 1 Cover Image (single)
// ==========================================
function createDay1Cover() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  drawGradient(ctx, ['#0d9488', '#065f56', '#0a0a0a'], 0, 0, W, H);

  ctx.fillStyle = '#fff';
  ctx.font = 'bold 68px Arial';
  ctx.fillText('I Lost', 80, 380);
  ctx.fillStyle = '#fbbf24';
  ctx.fillText('$3,000', 280, 380);
  ctx.fillStyle = '#fff';
  ctx.fillText('in Forex.', 80, 460);
  ctx.fillText('Then I Learned', 80, 540);
  ctx.fillText('to', 80, 620);
  ctx.fillStyle = '#fbbf24';
  ctx.fillText('Code.', 170, 620);

  ctx.fillStyle = 'rgba(255,255,255,0.6)';
  ctx.font = '26px Arial';
  ctx.fillText('How algorithmic trading changed everything.', 80, 720);
  ctx.fillText('DM me "ALGO" for a free strategy consultation', 80, 760);

  addBranding(ctx, '', '');
  ctx.fillStyle = '#666';
  ctx.font = '20px Arial';
  ctx.textAlign = 'right';
  ctx.fillText('viprasol.com', W - 50, H - 40);

  saveSlide(canvas, 'day1-cover.png');
}

// ==========================================
// SLIDE SET 2: Stats Image
// ==========================================
function createStatsImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#0d9488';
  ctx.font = 'bold 44px Arial';
  ctx.textAlign = 'left';
  ctx.fillText('Our Verified Results', 80, 100);

  // Draw line
  ctx.fillStyle = '#0d9488';
  ctx.fillRect(80, 120, 300, 3);

  const stats = [
    { num: '135%', label: 'Avg Monthly Return\n(MyFXBook Verified)', x: 60, y: 180 },
    { num: '81%', label: 'Win Rate Across\nLive Accounts', x: 560, y: 180 },
    { num: '44K+', label: 'Pips Gained\nAnd Counting', x: 60, y: 560 },
    { num: '500+', label: 'Traders Trust\nOur Systems', x: 560, y: 560 }
  ];

  stats.forEach(s => {
    // Box
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2;
    ctx.strokeRect(s.x, s.y, 450, 320);
    ctx.fillStyle = 'rgba(251, 191, 36, 0.05)';
    ctx.fillRect(s.x, s.y, 450, 320);

    // Number
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 72px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(s.num, s.x + 225, s.y + 130);

    // Label
    ctx.fillStyle = '#999';
    ctx.font = '22px Arial';
    const lines = s.label.split('\n');
    lines.forEach((l, i) => ctx.fillText(l, s.x + 225, s.y + 200 + i * 30));
  });

  ctx.textAlign = 'left';
  addBranding(ctx, '', '');
  ctx.fillStyle = '#666';
  ctx.font = '24px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('DM "ALGO" for a free strategy consultation | viprasol.com', W/2, H - 40);

  saveSlide(canvas, 'results-stats.png');
}

// ==========================================
// SLIDE SET 3: Manual vs Auto
// ==========================================
function createComparisonImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#fff';
  ctx.font = 'bold 40px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('Same Strategy. Different Results.', W/2, 80);

  // Manual side (red)
  ctx.fillStyle = 'rgba(239, 68, 68, 0.1)';
  ctx.fillRect(30, 120, 500, 850);
  ctx.fillStyle = '#ef4444';
  ctx.font = 'bold 32px Arial';
  ctx.fillText('MANUAL', 280, 180);

  const manualItems = ['+3.2%/month', 'Missed 12 trades', 'Moved stop loss 5x', 'Closed winners early', 'Skipped trades from fear'];
  ctx.font = '24px Arial';
  ctx.fillStyle = '#fff';
  manualItems.forEach((item, i) => {
    ctx.fillStyle = '#ef4444';
    ctx.fillText('✗', 120, 260 + i * 120);
    ctx.fillStyle = 'rgba(255,255,255,0.8)';
    ctx.fillText(item, 280, 260 + i * 120);
  });

  // Auto side (green)
  ctx.fillStyle = 'rgba(34, 197, 94, 0.1)';
  ctx.fillRect(550, 120, 500, 850);
  ctx.fillStyle = '#22c55e';
  ctx.font = 'bold 32px Arial';
  ctx.fillText('AUTOMATED', 800, 180);

  const autoItems = ['+11.4%/month', 'Caught all 47 signals', 'SL executed perfectly', 'Hit all TP targets', 'Traded every signal'];
  ctx.font = '24px Arial';
  autoItems.forEach((item, i) => {
    ctx.fillStyle = '#22c55e';
    ctx.fillText('✓', 640, 260 + i * 120);
    ctx.fillStyle = 'rgba(255,255,255,0.8)';
    ctx.fillText(item, 800, 260 + i * 120);
  });

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 24px Arial';
  ctx.fillText('3.5x better results. Same strategy.', W/2, H - 30);

  saveSlide(canvas, 'manual-vs-auto.png');
}

// ==========================================
// SLIDE SET 4: 5 Signs You Need a Bot
// ==========================================
function create5SignsImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  drawGradient(ctx, ['#0a0a0a', '#0d1b2a'], 0, 0, W, H);

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 48px Arial';
  ctx.textAlign = 'left';
  ctx.fillText('5 Signs You Need', 80, 100);
  ctx.fillText('a Trading Bot', 80, 160);

  ctx.fillStyle = '#fbbf24';
  ctx.fillRect(80, 185, 200, 4);

  const signs = [
    'You miss trades while sleeping',
    'You move your stop loss "just once"',
    'You close winners too early',
    'You revenge trade after losses',
    'Your results are inconsistent'
  ];

  signs.forEach((s, i) => {
    const y = 260 + i * 140;
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 56px Arial';
    ctx.globalAlpha = 0.3;
    ctx.fillText(`0${i+1}`, 80, y + 10);
    ctx.globalAlpha = 1;

    ctx.fillStyle = '#fff';
    ctx.font = '28px Arial';
    ctx.fillText(s, 200, y);

    if (i < 4) {
      ctx.fillStyle = 'rgba(255,255,255,0.1)';
      ctx.fillRect(80, y + 50, 920, 1);
    }
  });

  ctx.fillStyle = '#0d9488';
  ctx.font = 'bold 24px Arial';
  ctx.fillText('If you said YES to any → DM "ALGO"', 80, H - 50);
  ctx.fillStyle = '#666';
  ctx.font = '18px Arial';
  ctx.textAlign = 'right';
  ctx.fillText('viprasol.com', W - 50, H - 50);

  saveSlide(canvas, '5-signs-trading-bot.png');
}

// ==========================================
// SLIDE SET 5: Risk Management
// ==========================================
function createRiskImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 40px Arial';
  ctx.textAlign = 'left';
  ctx.fillText('8 Risk Rules We Code', 80, 80);
  ctx.fillText('Into Every EA', 80, 130);

  const rules = [
    'Max 2% risk per trade',
    'Max 3 simultaneous positions',
    'Daily loss limit: -5%',
    'Weekly loss limit: -10%',
    'News event filter (auto-pause)',
    'Spread filter (skip bad conditions)',
    'Trailing stop loss',
    'Break-even protection'
  ];

  rules.forEach((r, i) => {
    const y = 200 + i * 95;
    ctx.fillStyle = '#0d9488';
    ctx.font = 'bold 28px Arial';
    ctx.fillText(`${i+1}.`, 80, y);
    ctx.fillStyle = '#fff';
    ctx.font = '26px Arial';
    ctx.fillText(r, 130, y);

    if (i < 7) {
      ctx.fillStyle = 'rgba(13, 148, 136, 0.2)';
      ctx.fillRect(80, y + 35, 920, 1);
    }
  });

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 22px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('If your bot doesn\'t have these — it\'s a ticking time bomb.', W/2, H - 40);

  saveSlide(canvas, 'risk-management-rules.png');
}

// ==========================================
// SLIDE SET 6: EA Pricing
// ==========================================
function createPricingImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = '#fff';
  ctx.font = 'bold 44px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('Custom EA Pricing', W/2, 80);

  const tiers = [
    { name: 'BASIC', price: '$300-800', color: '#0d9488', features: ['Simple strategy', '1 pair', 'Basic risk mgmt'] },
    { name: 'STANDARD', price: '$800-2K', color: '#fbbf24', features: ['Complex strategy', 'Multi-pair', 'Advanced risk mgmt'] },
    { name: 'ADVANCED', price: '$2K-5K', color: '#a855f7', features: ['Multi-strategy + AI', 'Dashboard', 'Ongoing optimization'] }
  ];

  tiers.forEach((t, i) => {
    const x = 30 + i * 350;

    ctx.fillStyle = t.color;
    ctx.globalAlpha = 0.1;
    ctx.fillRect(x, 130, 330, 700);
    ctx.globalAlpha = 1;

    ctx.strokeStyle = t.color;
    ctx.lineWidth = 2;
    ctx.strokeRect(x, 130, 330, 700);

    ctx.fillStyle = t.color;
    ctx.font = 'bold 28px Arial';
    ctx.fillText(t.name, x + 165, 200);

    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 48px Arial';
    ctx.fillText(t.price, x + 165, 300);

    ctx.fillStyle = '#fff';
    ctx.font = '22px Arial';
    t.features.forEach((f, fi) => {
      ctx.fillText('✓ ' + f, x + 165, 400 + fi * 60);
    });
  });

  ctx.fillStyle = '#22c55e';
  ctx.font = 'bold 26px Arial';
  ctx.fillText('ROI = 1 month on a $10K account', W/2, H - 70);
  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 22px Arial';
  ctx.fillText('DM "BUILD" for a quote | viprasol.com', W/2, H - 30);

  saveSlide(canvas, 'ea-pricing.png');
}

// ==========================================
// SLIDE SET 7: CTA Image
// ==========================================
function createCTAImage() {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  drawGradient(ctx, ['#0d9488', '#065f56'], 0, 0, W, H);

  ctx.fillStyle = '#fff';
  ctx.font = 'bold 56px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('Ready to Stop', W/2, 300);
  ctx.fillText('Trading Manually?', W/2, 370);

  // Gold button
  const bx = W/2 - 200, by = 450, bw = 400, bh = 80;
  ctx.fillStyle = '#fbbf24';
  ctx.beginPath();
  ctx.roundRect(bx, by, bw, bh, 15);
  ctx.fill();

  ctx.fillStyle = '#0a0a0a';
  ctx.font = 'bold 36px Arial';
  ctx.fillText('DM "ALGO"', W/2, by + 52);

  ctx.fillStyle = 'rgba(255,255,255,0.8)';
  ctx.font = '26px Arial';
  ctx.fillText('Free Strategy Consultation', W/2, 620);
  ctx.fillText('Custom EA Development', W/2, 660);
  ctx.fillText('Verified Results', W/2, 700);

  ctx.fillStyle = 'rgba(255,255,255,0.5)';
  ctx.font = '28px Arial';
  ctx.fillText('viprasol.com', W/2, 800);

  ctx.fillStyle = 'rgba(255,255,255,0.4)';
  ctx.font = '20px Arial';
  ctx.fillText('Viprasol Tech', W/2, H - 40);

  saveSlide(canvas, 'cta-algo.png');
}

// Generate all
createDay1Cover();
createStatsImage();
createComparisonImage();
create5SignsImage();
createRiskImage();
createPricingImage();
createCTAImage();
console.log('\nAll PNG images generated!');
