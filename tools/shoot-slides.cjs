// Screenshot every slide of an HTML deck at 1920x1080. Usage: node tools/shoot-slides.cjs <deck.html> <outdir>
const { chromium } = require('playwright');
const path = require('path');
const [,, file, out] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const url = 'file://' + path.resolve(file);
  await p.goto(url); await p.waitForTimeout(800);
  const n = await p.evaluate(() => document.querySelectorAll('.slide').length);
  for (let k = 1; k <= n; k++) {
    await p.goto(url + '#' + k); await p.reload(); await p.waitForTimeout(1600);
    await p.screenshot({ path: `${out}/s${String(k).padStart(2, '0')}.png` });
  }
  console.log(n); await b.close();
})();
