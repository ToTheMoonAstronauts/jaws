const {chromium}=require('playwright');const path=require('path');
const W=path.resolve(__dirname,'../../website/images');
const J=[
 ['og-home-en','Hard gum<b>for a stronger jaw</b>','Two hardness levels · sugar-free · vegan','hero-01.webp'],
 ['og-home-lt','Kieta guma<b>stipresniam žandikauliui</b>','Du kietumo lygiai · be cukraus · veganiška','hero-01.webp'],
 ['og-home-de','Harter Kaugummi<b>für einen stärkeren Kiefer</b>','Zwei Härtegrade · zuckerfrei · vegan','hero-01.webp',0,70],
 ['og-gums-en','Hard &amp; Ultra<b>Hard gum</b>','4 flavours · 40 pieces per pack','products/bundle-hard.webp',1],
 ['og-gums-lt','Kieta ir<b>ypač kieta guma</b>','4 skoniai · 40 vnt. pakuotėje','products/bundle-hard.webp',1],
  ['og-gums-de','Hard &amp; Ultra<b>Hard Gum</b>','4 Geschmäcker · 40 Stück pro Packung','products/bundle-hard.webp',1],
  ['og-energy-en','Hard gum<b>+ caffeine</b>','40 mg caffeine per piece · mint','products/trio-caffeine-mint.webp',1],
  ['og-energy-lt','Kieta guma<b>+ kofeinas</b>','40 mg kofeino gabalėlyje · mėtų','products/trio-caffeine-mint.webp',1],
  ['og-energy-de','Hard Gum<b>+ Koffein</b>','40 mg Koffein pro Stück · Minze','products/trio-caffeine-mint.webp',1],
];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
for(const [n,h,s,img,pp,fs] of J.filter(j=>!process.argv[2]||j[0].includes(process.argv[2]))){const u='file://'+path.resolve(__dirname,'og.html')+'?'+new URLSearchParams({h,s,img:'file://'+W+'/'+img,p:pp?'1':'',fs:fs||''});
await p.goto(u);await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:path.join(W,n+'.png')});console.log(n);}await b.close();})();
