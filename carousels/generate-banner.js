const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

// LinkedIn banner dimensions: 1584 x 396
const W = 1584, H = 396;

const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background gradient: dark to teal
const grad = ctx.createLinearGradient(0, 0, W, H);
grad.addColorStop(0, '#0a0a0a');
grad.addColorStop(0.4, '#0d1b2a');
grad.addColorStop(0.7, '#065f56');
grad.addColorStop(1, '#0d9488');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, W, H);

// Subtle grid pattern overlay
ctx.strokeStyle = 'rgba(13, 148, 136, 0.08)';
ctx.lineWidth = 1;
for (let x = 0; x < W; x += 40) {
  ctx.beginPath();
  ctx.moveTo(x, 0);
  ctx.lineTo(x, H);
  ctx.stroke();
}
for (let y = 0; y < H; y += 40) {
  ctx.beginPath();
  ctx.moveTo(0, y);
  ctx.lineTo(W, y);
  ctx.stroke();
}

// Fake candlestick chart in background (decorative)
ctx.globalAlpha = 0.15;
const candles = [
  { x: 100, h: 80, body: 40, up: true },
  { x: 140, h: 60, body: 30, up: false },
  { x: 180, h: 90, body: 45, up: true },
  { x: 220, h: 50, body: 25, up: false },
  { x: 260, h: 100, body: 50, up: true },
  { x: 300, h: 70, body: 35, up: true },
  { x: 340, h: 55, body: 28, up: false },
  { x: 380, h: 85, body: 42, up: true },
  { x: 420, h: 45, body: 22, up: false },
  { x: 460, h: 95, body: 48, up: true },
  { x: 500, h: 65, body: 32, up: true },
  { x: 540, h: 75, body: 38, up: false },
  { x: 580, h: 110, body: 55, up: true },
];

candles.forEach(c => {
  const baseY = 280 - (c.up ? c.h : c.h * 0.6);
  // Wick
  ctx.fillStyle = c.up ? '#22c55e' : '#ef4444';
  ctx.fillRect(c.x + 8, baseY, 4, c.h);
  // Body
  ctx.fillRect(c.x, baseY + (c.h - c.body) / 2, 20, c.body);
});
ctx.globalAlpha = 1;

// Main text - left side
ctx.fillStyle = '#ffffff';
ctx.font = 'bold 52px Arial';
ctx.textAlign = 'left';
ctx.fillText('We Build Trading Bots', 680, 120);

ctx.fillStyle = '#fbbf24';
ctx.font = 'bold 52px Arial';
ctx.fillText('That Actually Make Money', 680, 180);

// Stats line
ctx.fillStyle = 'rgba(255,255,255,0.7)';
ctx.font = '24px Arial';
ctx.fillText('135% Avg Returns  |  81% Win Rate  |  500+ Traders  |  MyFXBook Verified', 680, 230);

// CTA
ctx.fillStyle = '#fbbf24';
ctx.font = 'bold 28px Arial';
ctx.fillText('DM "ALGO" for a Free Strategy Consultation', 680, 290);

// Website
ctx.fillStyle = 'rgba(255,255,255,0.5)';
ctx.font = '22px Arial';
ctx.fillText('viprasol.com', 680, 340);

// Decorative line
ctx.fillStyle = '#fbbf24';
ctx.fillRect(680, 245, 500, 3);

// Save
const outPath = path.join(__dirname, '..', 'images', 'linkedin-banner.png');
fs.writeFileSync(outPath, canvas.toBuffer('image/png'));
console.log('Banner saved to:', outPath);
