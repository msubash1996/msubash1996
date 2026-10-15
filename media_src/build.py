"""Build the profile README visuals: crossfade animated WebP walkthroughs and compressed JPG stills.

usage: python build.py   (writes into ../assets/work/)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'work')
os.makedirs(OUT, exist_ok=True)
H = os.path.expanduser
W, HT = 960, 600
FONT = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf', 17)
BG = (16, 26, 23)


def fit(path):
    """Scale to width W, keep the top 16:10 window; pad short images."""
    im = Image.open(path).convert('RGB')
    h = round(im.height * W / im.width)
    im = im.resize((W, h), Image.LANCZOS)
    if h >= HT:
        return im.crop((0, 0, W, HT))
    canvas = Image.new('RGB', (W, HT), BG)
    canvas.paste(im, (0, (HT - h) // 2))
    return canvas


def caption(im, text):
    if not text:
        return im
    im = im.copy()
    d = ImageDraw.Draw(im, 'RGBA')
    l, t, r, b = d.textbbox((0, 0), text, font=FONT)
    pw, ph = r - l + 28, b - t + 18
    x, y = 16, HT - ph - 16
    d.rounded_rectangle((x, y, x + pw, y + ph), radius=ph // 2, fill=(20, 33, 31, 225), outline=(61, 131, 97, 255), width=2)
    d.text((x + 14 - l, y + 9 - t), text, font=FONT, fill=(236, 244, 240))
    return im


def animate(name, slides, hold=2200, fade_steps=5, fade_ms=70):
    frames, durs = [], []
    imgs = [caption(fit(sl[0]), sl[1]) for sl in slides]
    for i, im in enumerate(imgs):
        frames.append(im)
        own = slides[i][2] if len(slides[i]) > 2 else hold
        durs.append(own)
        if own < 1000:  # typing frames cut straight to the next one
            continue
        nxt = imgs[(i + 1) % len(imgs)]
        for s in range(1, fade_steps + 1):
            frames.append(Image.blend(im, nxt, s / (fade_steps + 1)))
            durs.append(fade_ms)
    dst = os.path.join(OUT, name)
    frames[0].save(dst, save_all=True, append_images=frames[1:], duration=durs, loop=0, quality=78, method=6)
    print(name, len(frames), 'frames', os.path.getsize(dst) // 1024, 'KB')


def still(name, path):
    dst = os.path.join(OUT, name)
    fit(path).save(dst, quality=84, optimize=True, progressive=True)
    print(name, os.path.getsize(dst) // 1024, 'KB')


M = lambda f: os.path.join(HERE, f)
CX = [(M('cx_%02d.png' % i), c, *h) for i, c, *h in [
    (0, 'Free and public: Odoo 16, 17, 18, 19 and 20', 2600),
    (1, 'Upgrade steps and the most-changed models'),
    (3, 'Search any model', 450),
    (5, 'Search any model', 450),
    (6, 'Search any model', 900),
    (8, 'res.partner across five releases'),
    (9, 'Fields removed, with what replaced them'),
    (11, 'Odoo 19 to 20: Community and Enterprise'),
    (12, 'Breaking changes, each with what to do'),
]]
animate('change-explorer.webp', CX, hold=1900)

S = H('~/snm_construction20_work/shots/')
animate('construction-erp.webp', [
    (S + 'sarah_kim_dashboard_portfolio.png', 'Portfolio dashboard'),
    (S + 'sarah_kim_dashboard_project.png', 'Project dashboard'),
    (S + 'sarah_kim_project_cost_control.png', 'Budget and cost control by cost code'),
    (S + 'sarah_kim_pay_application.png', 'Progress billing: pay applications'),
    (S + 'sarah_kim_daily_report.png', 'Daily field reports'),
    (S + 'portal_client_northgate_pay_application.png', 'Client portal'),
])

R = H('~/snm_fr_build/repo/')
D = lambda m, f: R + m + '/static/description/' + f
animate('odoo-apps.webp', [
    (D('snm_studio_upgrade_checker', 'findings.png'), 'Studio Upgrade Checker'),
    (D('snm_view_repair', 'proposal.png'), 'Studio View Repair Assistant'),
    (D('snm_failure_monitor', 'dashboard.png'), 'Automation & Cron Failure Monitor'),
    (D('snm_ai_assistant', 'shot-chat.png'), 'AI Assistant'),
    (D('snm_access_manager', 'dashboard.png'), 'Access Manager'),
    (D('snm_crm_dashboard', 'dashboard.png'), 'CRM Dashboard (free)'),
    (D('snm_financial_reports', 'balance_sheet.png'), 'Financial Reports for Community (free)'),
])

still('ai-workspace.jpg', M('plat_ai.png'))
still('keelhouse.jpg', M('plat_keel.png'))
still('solar-subsidizer.jpg', M('plat_solar.png'))
still('project-gantt.jpg', H('~/snm_apps_build/snm_project_gantt/snm_project_gantt/static/description/gantt_main.png'))
