"""Capture the poster gallery screenshots listed in
corpus-observed/poster-gallery/screenshots/README.md, as reproducible
element-anchored shots at a fixed viewport.

    py scripts/capture-poster-gallery.py            # public shots (no sign-in)
    py scripts/capture-poster-gallery.py --login    # one-time: sign in, save session
    py scripts/capture-poster-gallery.py --admin    # admin shots (needs the session)

Needs: py -m pip install playwright pillow   (uses the installed Chrome; no
browser download).

How auth works
--------------
Admin screens need Gareth's session. --login opens a visible window on the
sign-in page; **you sign in yourself** (this script never touches credentials),
press Enter in the terminal when the dashboard is up, and the session is saved to

    %USERPROFILE%\\.oa-capture-state.json

OUTSIDE the repo, deliberately: that file holds live session cookies and must
never be committed. Admin runs then reuse it headlessly until it expires.

Conventions
-----------
- Viewport fixed at 1440x900 so every capture is comparable run to run.
- Shots are cropped by ELEMENT SELECTOR, not pixel coordinates, so a re-run
  after a UI change photographs the new state of the same control.
- Output is WebP quality 85 into corpus-observed/poster-gallery/screenshots/,
  named by state per the exploration brief.
- The conference platform shows a timezone dialog on first load of a fresh
  profile; dismiss() handles it once per context.

Not capturable without changing the demo event (left out on purpose):
- question-picker-poster-group-before: needs all three poster questions deleted.
- poster-upload-invalid-file-type-error / file-too-large-error: need a scripted
  wrong upload on the submission form; do these during the next exploration run.
"""

import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'corpus-observed', 'poster-gallery', 'screenshots')
STATE = os.path.join(os.path.expanduser('~'), '.oa-capture-state.json')

EVENT = 78206
VIRTUAL = 'https://virtual.oxfordabstracts.com/event/%d' % EVENT
ADMIN = 'https://app.oxfordabstracts.com/admin/events/%d/app' % EVENT
VIEWPORT = {'width': 1440, 'height': 900}


def save_webp(png_bytes, name):
    import io
    img = Image.open(io.BytesIO(png_bytes))
    path = os.path.join(OUT, name + '.webp')
    img.save(path, 'WEBP', quality=85)
    print('  %-46s %dx%d  %5.1f KB' % (name + '.webp', img.width, img.height,
                                       os.path.getsize(path) / 1024))


def dismiss_timezone(page):
    save = page.get_by_role('button', name='Save')
    try:
        save.wait_for(timeout=5000)
        save.click()
        page.wait_for_load_state('networkidle')
    except Exception:
        pass                                     # dialog not shown - fine


def shoot(page, name, locator=None):
    if locator is not None:
        save_webp(locator.screenshot(), name)
    else:
        save_webp(page.screenshot(), name)


# ---------------------------------------------------------------- public ----

def public_shots(page):
    # grid, populated
    page.goto(VIRTUAL + '/poster-gallery/grid', wait_until='networkidle')
    dismiss_timezone(page)
    page.wait_for_selector('text=Showing', timeout=20000)
    shoot(page, 'gallery-grid-populated')

    # list view (the bare /poster-gallery path)
    page.goto(VIRTUAL + '/poster-gallery', wait_until='networkidle')
    page.wait_for_selector('text=Showing', timeout=20000)
    shoot(page, 'gallery-list-view')

    # empty state with Clear filters (via a search that matches nothing).
    # Wait for the outcome text, not the Clear filters chip - the chip appears
    # while the debounced search is still running and the old results are
    # still on screen.
    box = page.get_by_placeholder('Search posters')
    box.fill('zzzz')
    page.wait_for_selector('text=Showing 0 results', timeout=20000)
    shoot(page, 'gallery-empty-clear-filters')
    box.fill('')

    # poster detail panel (known issue: the PDF viewer shows a spinner - that
    # is the app's current behaviour, so it is what gets photographed)
    page.goto(VIRTUAL + '/poster-gallery?current=1', wait_until='networkidle')
    page.wait_for_selector('text=Authors', timeout=20000)
    page.wait_for_timeout(1500)
    dlg = page.locator('[role=dialog]')
    shoot(page, 'gallery-poster-detail', dlg.first if dlg.count() else None)


# ----------------------------------------------------------------- admin ----

def admin_shots(page):
    # decisions table with the In poster gallery column
    page.goto(ADMIN + '/decisions', wait_until='networkidle')
    page.wait_for_selector('text=In poster gallery', timeout=30000)
    shoot(page, 'decisions-table-in-poster-gallery-column')

    # question picker, with the poster upload question already existing
    page.goto(ADMIN + '/edit-submission-form', wait_until='networkidle')
    page.get_by_role('button', name='Question').click()
    page.wait_for_selector('text=Poster questions', timeout=15000)
    shoot(page, 'question-picker-poster-group-after')

    # the poster upload question's editor (settings block)
    page.get_by_role('button', name='Back to form').click()
    page.get_by_text('Please upload a 1 page pdf file').click()
    page.wait_for_selector('text=Poster gallery upload', timeout=15000)
    shoot(page, 'poster-upload-question-defaults')

    # program menu panel
    page.goto(ADMIN + '/program-builder', wait_until='networkidle')
    page.get_by_text('DISPLAY', exact=False).click()
    page.get_by_text('Program menu').click()
    page.wait_for_selector('text=This panel controls', timeout=15000)
    dlg = page.locator('text=Program menu').locator(
        'xpath=ancestor::div[contains(@class,"dialog") or @role="dialog"][1]')
    shoot(page, 'program-menu-poster-gallery-enabled',
          dlg.first if dlg.count() else None)

    # program access settings
    page.goto(ADMIN + '/program-builder/access-code', wait_until='networkidle')
    page.wait_for_selector('text=Show submission contents', timeout=15000)
    shoot(page, 'program-access-settings')


# ----------------------------------------------------------------- login ----

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=False)
        ctx = browser.new_context(viewport=VIEWPORT)
        page = ctx.new_page()
        page.goto('https://app.oxfordabstracts.com')
        print('\nA Chrome window is open. Sign in there yourself.')
        input('When you can see the Oxford Abstracts dashboard, press Enter here... ')
        ctx.storage_state(path=STATE)
        browser.close()
    print('Session saved to %s (never commit this file).' % STATE)


def main():
    os.makedirs(OUT, exist_ok=True)
    if '--login' in sys.argv:
        return login()

    admin = '--admin' in sys.argv
    if admin and not os.path.exists(STATE):
        print('No saved session at %s' % STATE)
        print('Run:  py scripts/capture-poster-gallery.py --login')
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=True)
        ctx = browser.new_context(viewport=VIEWPORT,
                                  storage_state=STATE if admin else None)
        page = ctx.new_page()
        if admin:
            print('admin shots:')
            admin_shots(page)
        else:
            print('public shots:')
            public_shots(page)
        browser.close()
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
