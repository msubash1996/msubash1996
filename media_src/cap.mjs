import { chromium } from '/home/subash/snm-solar-compliance/apps/web/node_modules/playwright-core/index.mjs';
const out = process.argv[2];
const b = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true });
const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
await ctx.addCookies([{ name: 'website_cookies_bar', value: '{"required": true, "optional": false}', domain: 'snmdigitechconsulting.com', path: '/' }]);
const p = await ctx.newPage();
await p.addInitScript(() => { try { localStorage.setItem('snm-theme', 'dark'); localStorage.setItem('snmTheme', 'dark'); } catch (e) {} });
const hideCookie = async () => p.addStyleTag({ content: '#website_cookies_bar,.o_cookies_discrete,.o_cookies_bar_toggle,[class*=cookies]{display:none!important}' }).catch(() => {});
let n = 0; const shot = async () => { await p.screenshot({ path: `${out}/cx_${String(n++).padStart(2, '0')}.png` }); };
await p.goto('https://snmdigitechconsulting.com/odoo-changes', { waitUntil: 'networkidle' }); await hideCookie(); await p.waitForTimeout(800); await shot();
await p.mouse.wheel(0, 520); await p.waitForTimeout(500); await shot();
await p.goto('https://snmdigitechconsulting.com/odoo-changes', { waitUntil: 'networkidle' }); await hideCookie();
const box = p.locator('input[name=q]').first(); await box.click();
for (const ch of 'res.partner') { await box.type(ch); await p.waitForTimeout(60); if ('.p'.includes(ch) || ch === 'r') await shot(); }
await shot();
await Promise.all([p.waitForNavigation(), box.press('Enter')]); await hideCookie(); await p.waitForTimeout(800); await shot();
await p.mouse.wheel(0, 600); await p.waitForTimeout(500); await shot();
await p.mouse.wheel(0, 700); await p.waitForTimeout(500); await shot();
await p.goto('https://snmdigitechconsulting.com/odoo-changes/19-to-20', { waitUntil: 'networkidle' }); await hideCookie(); await p.waitForTimeout(700); await shot();
await p.mouse.wheel(0, 700); await p.waitForTimeout(500); await shot();
for (const [name, url] of [['plat_ai', 'https://aiconnect.snmdigitechconsulting.com'], ['plat_keel', 'https://keelhouse.snmdigitechconsulting.com'], ['plat_solar', 'https://solar.snmdigitechconsulting.com'], ['plat_site', 'https://snmdigitechconsulting.com']]) {
  await p.goto(url, { waitUntil: 'networkidle' }).catch(() => {}); await hideCookie(); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${out}/${name}.png` });
}
console.log('frames', n); await b.close();
