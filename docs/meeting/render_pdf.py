# HTML -> PDF (Chromium via Playwright). 글꼴: koreanize-matplotlib의 NanumGothic TTF에서 TSI* 표를 지운 것을 같은 폴더의 fonts/에 두고 실행.
# 사용: python3 render_pdf.py <html> <pdf>
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
src = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
foot = ('<div style="width:100%;font-size:7.5pt;color:#7a8592;padding:0 16mm;display:flex;justify-content:space-between;'
        'font-family:sans-serif"><span>영국 계통용 배터리와 시장 규칙 · 연구 진행 보고 2026-10-13</span>'
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg = b.new_page()
    pg.goto(src.as_uri()); pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready")
    pg.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<div></div>", footer_template=foot,
           margin={"top": "17mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
    b.close()
print("ok", out)
