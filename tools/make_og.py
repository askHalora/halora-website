"""Render the social share images from tools/og.html (needs Node + Playwright and a local server on :8765).
   python -m http.server 8765  (repo root, in another terminal), then: python tools/make_og.py"""
import subprocess, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JS = """
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [h,f] of [['','assets/og.png'],['#ar','assets/og-ar.png']]){const p=await b.newPage({viewport:{width:1200,height:630}});
 await p.goto('http://localhost:8765/tools/og.html'+h);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
 await p.screenshot({path:f});await p.close()}
await b.close()})();"""
subprocess.run(['node', '-e', JS], cwd=ROOT, check=True)
print('og images written')
