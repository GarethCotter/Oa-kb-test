"""Capture the poster gallery screenshots listed in
corpus-observed/poster-gallery/screenshots/README.md, as reproducible
element-anchored shots at a fixed viewport.

    py scripts/capture-poster-gallery.py            # public shots (no sign-in)
    py scripts/capture-poster-gallery.py --admin    # admin shots (sign in when asked)

Needs: py -m pip install playwright pillow   (uses the installed Chrome; no
browser download).

How auth works
--------------
Admin screens need a signed-in session, and that session **cannot be saved and
replayed**. --admin therefore opens a visible Chrome window on the sign-in page,
waits for you to sign in yourself (this script never touches credentials), and
then takes the screenshots immediately in that same window. Expect to sign in
once per admin capture run.

Why it has to work that way, established 1 Aug 2026 after two failed attempts:

- Playwright's `storage_state` export, taken straight after a real sign-in, held
  only `anon_user_id` and `_dd_s` - no auth token. Admin pages bounced to /auth.
- A full persistent Chrome profile failed the same way, in headless *and*
  headful runs. Inspecting a fresh page on that profile showed `localStorage`
  completely empty, no auth cookie on app.oxfordabstracts.com, and a
  `code_verifier` cookie - i.e. an OAuth/PKCE flow whose access token is held in
  memory by the running page and whose identity-provider session does not
  survive a browser restart in a clean automation profile.

So there is no artefact to save. Same-session capture is the design, not a
workaround.

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

EVENT = 78206
VIRTUAL = 'https://virtual.oxfordabstracts.com/event/%d' % EVENT
APP = 'https://app.oxfordabstracts.com'
ADMIN = APP + '/admin/events/%d/app' % EVENT
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
    """Each shot is independent: one failure reports and the run carries on.

    A sign-in costs the operator fifteen seconds of attention, so a single bad
    selector must never throw away the other four captures.
    """
    for fn in (_shot_decisions_table, _shot_question_picker,
               _shot_question_editor, _shot_program_menu, _shot_access_settings):
        name = fn.__name__.replace('_shot_', '')
        try:
            fn(page)
        except Exception as e:
            print('  FAILED %-38s %s' % (name, str(e).split('\n')[0][:70]))
            try:                                  # salvage: what was on screen
                save_webp(page.screenshot(), 'FAILED-' + name)
            except Exception:
                pass


def _shot_decisions_table(page):
    """The decisions table is far wider than the viewport - the 'In poster
    gallery' column sits off to the right, so scroll it into view first."""
    page.goto(ADMIN + '/decisions', wait_until='networkidle')
    page.wait_for_selector('text=Submission Id', timeout=60000)
    page.wait_for_timeout(2000)
    col = page.locator('text=In poster gallery').first
    col.wait_for(timeout=30000)
    col.scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    shoot(page, 'decisions-table-in-poster-gallery-column')


def _shot_question_picker(page):
    page.goto(ADMIN + '/edit-submission-form', wait_until='networkidle')
    page.wait_for_selector('text=Submission form', timeout=60000)
    page.get_by_role('button', name='Question').first.click()
    page.wait_for_selector('text=Poster questions', timeout=30000)
    page.wait_for_timeout(800)
    shoot(page, 'question-picker-poster-group-after')


def _shot_question_editor(page):
    page.get_by_role('button', name='Back to form').first.click()
    page.wait_for_timeout(1500)
    page.get_by_text('Please upload a 1 page pdf file').first.click()
    page.wait_for_selector('text=Poster gallery upload', timeout=30000)
    page.locator('text=Question settings').first.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    shoot(page, 'poster-upload-question-defaults')


def _shot_program_menu(page):
    page.goto(ADMIN + '/program-builder', wait_until='networkidle')
    page.wait_for_timeout(3000)
    page.get_by_text('DISPLAY', exact=True).first.click()
    page.get_by_text('Program menu', exact=True).first.click()
    page.wait_for_selector('text=This panel controls', timeout=30000)
    page.wait_for_timeout(800)
    shoot(page, 'program-menu-poster-gallery-enabled')


def _shot_access_settings(page):
    page.goto(ADMIN + '/program-builder/access-code', wait_until='networkidle')
    page.wait_for_selector('text=Show submission contents', timeout=30000)
    page.wait_for_timeout(800)
    shoot(page, 'program-access-settings')


# ------------------------------------------------------------- sign-in ----

def signed_out(page):
    """True if this page is the sign-in screen."""
    if '/auth' in page.url:
        return True
    try:
        return 'Sign in to Oxford Abstracts' in page.inner_text('body')
    except Exception:
        return True                                # mid-navigation; assume not yet


def wait_for_sign_in(page, minutes=10):
    """Park on the sign-in page until the user is genuinely through.

    The script never types credentials. Detection is by PROBE, not by URL:
    the app briefly shows an /events URL while bouncing through auth, and an
    earlier version of this function matched that transient and charged ahead
    into five failed captures. So: wait for the sign-in screen to go away and
    stay away, then prove it by loading the real target and checking we are
    not bounced back.
    """
    page.goto(APP, wait_until='networkidle')
    print('\nA Chrome window is open. Sign in there - capture starts by itself.')
    print('(waiting up to %d minutes)' % minutes)

    deadline = minutes * 30                        # 2-second polls
    stable = 0
    for _ in range(deadline):
        page.wait_for_timeout(2000)
        if signed_out(page):
            stable = 0
            continue
        stable += 1
        if stable < 3:                             # hold for ~6s before probing
            continue

        # probe: load a page that genuinely requires auth
        try:
            page.goto(ADMIN + '/decisions', wait_until='networkidle')
            page.wait_for_timeout(2500)
        except Exception:
            stable = 0
            continue
        if signed_out(page):
            print('  ...still signing in, waiting')
            page.goto(APP, wait_until='networkidle')
            stable = 0
            continue
        print('signed in and verified on an admin page, capturing...\n')
        return True

    print('Timed out after %d minutes without a verified sign-in.' % minutes)
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    admin = '--admin' in sys.argv

    with sync_playwright() as p:
        if admin:
            # headful: the user has to sign in, and capture happens in the very
            # same session because the token cannot be persisted (see above)
            browser = p.chromium.launch(channel='chrome', headless=False)
            ctx = browser.new_context(viewport=VIEWPORT)
            page = ctx.new_page()
            if not wait_for_sign_in(page):
                browser.close()
                return 1
            print('admin shots:')
            admin_shots(page)
        else:
            browser = p.chromium.launch(channel='chrome', headless=True)
            ctx = browser.new_context(viewport=VIEWPORT)
            page = ctx.new_page()
            print('public shots:')
            public_shots(page)
        browser.close()
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
