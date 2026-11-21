const { chromium } = require('playwright');
const fs=require('fs');
const P={
 phone:'<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
 nav:'<path d="M12 2.8 19.5 20.5 12 16.6 4.5 20.5Z"/>',
 spark:'<path d="M12 3c.6 4.6 2.4 6.4 7 7-4.6.6-6.4 2.4-7 7-.6-4.6-2.4-6.4-7-7 4.6-.6 6.4-2.4 7-7Z"/><path d="M19 15.5c.25 1.7.8 2.25 2.5 2.5-1.7.25-2.25.8-2.5 2.5-.25-1.7-.8-2.25-2.5-2.5 1.7-.25 2.25-.8 2.5-2.5Z"/>',
 userplus:'<circle cx="9.5" cy="8" r="3.8"/><path d="M2.8 20.5c.6-3.7 3.3-5.8 6.7-5.8s6.1 2.1 6.7 5.8"/><path d="M19 8v6M16 11h6"/>',
 flag:'<path d="M5 21.5V3.5"/><path d="M5 4.5c4.5-2.4 7.5 2.4 13 0v9c-5.5 2.4-8.5-2.4-13 0"/>',
 home:'<path d="M3.5 10.5 12 3.5l8.5 7V20.5h-17Z"/><path d="M12 17.6c-2.7-1.8-3.6-3-3.6-4.3 0-1.1.9-1.9 1.9-1.9.7 0 1.3.4 1.7 1 .4-.6 1-1 1.7-1 1 0 1.9.8 1.9 1.9 0 1.3-.9 2.5-3.6 4.3Z"/>',
 grid:'<rect x="2.5" y="5.5" width="19" height="13" rx="1.5"/><path d="M7.25 5.5v13M12 5.5v13M16.75 5.5v13M2.5 12h19"/>',
 check:'<circle cx="12" cy="12" r="9"/><path d="m7.8 12.3 2.8 2.8 5.6-5.8"/>',
 chat:'<path d="M4 4.5h16a1.5 1.5 0 0 1 1.5 1.5v9.5A1.5 1.5 0 0 1 20 17h-9l-5 4v-4H4a1.5 1.5 0 0 1-1.5-1.5V6A1.5 1.5 0 0 1 4 4.5Z"/><path d="M12 7.3c.3 1.9 1 2.6 2.9 2.9-1.9.3-2.6 1-2.9 2.9-.3-1.9-1-2.6-2.9-2.9 1.9-.3 2.6-1 2.9-2.9Z"/>',
 hammer:'<rect x="3.5" y="12.5" width="8" height="8" rx="1.2"/><rect x="12.5" y="12.5" width="8" height="8" rx="1.2"/><rect x="8" y="3.5" width="8" height="8" rx="1.2"/>',
 easel:'<rect x="2.5" y="3.5" width="19" height="12" rx="1.5"/><path d="M12 15.5v3M7.5 21.5l4.5-3 4.5 3M7 11l3-3 2.5 2.5L17 7"/>',
 summary:'<path d="M10 6.5h10M10 12h10M10 17.5h10"/><path d="m3.8 6.4 1.4 1.4 2.4-2.6M3.8 11.9l1.4 1.4 2.4-2.6M3.8 17.4l1.4 1.4 2.4-2.6"/>',
 smile:'<circle cx="12" cy="12" r="9.5"/><path d="M7.8 14.2c1.1 1.8 2.5 2.7 4.2 2.7s3.1-.9 4.2-2.7"/><path d="M9 9.2v1.3M15 9.2v1.3"/>',
 pen:'<path d="M15.5 3.5 20.5 8.5 9 20H4v-5Z"/><path d="M13 6l5 5"/><path d="M13 21.5h8"/>',
};
(async()=>{const b=await chromium.launch();const pg=await b.newPage({deviceScaleFactor:1});
for(const [col,c] of [['light','#B4431F'],['dark','#F0703A'],['ink','#1E130F']]) for(const [n,d] of Object.entries(P)){
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="256" height="256" fill="none" stroke="${c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
 fs.writeFileSync(`${n}-${col}.svg`,svg);
 await pg.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
 await pg.locator('svg').screenshot({path:`${n}-${col}.png`,omitBackground:true});}
await b.close();})();
