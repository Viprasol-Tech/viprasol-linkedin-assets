const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  await page.setViewport({ width: 1080, height: 1080 });
  await page.goto('http://localhost:3456/day1-carousel.html', { waitUntil: 'networkidle0' });

  // Generate PDF with custom page size matching slides
  await page.pdf({
    path: path.join(__dirname, '..', 'images', 'day1-carousel.pdf'),
    width: '1080px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  // Also take screenshots of each slide
  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({
      path: path.join(__dirname, '..', 'images', `day1-slide${i + 1}.png`),
      type: 'png'
    });
    console.log(`Slide ${i + 1} saved`);
  }

  console.log('PDF and images generated successfully!');
  await browser.close();
})();
