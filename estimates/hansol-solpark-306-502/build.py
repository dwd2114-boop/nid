"""한솔솔파크 306동 502호 상세견적서 생성기.

python3 build.py  ->  index.html 생성 후 같은 폴더에 PDF 출력 (Playwright/Chromium).
금액은 품목 데이터에서 계산하며, 섹션 합계·총액이 기준 금액과 다르면 중단한다.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_NAME = "상세견적서_한솔솔파크 306동 502호_261109_수정.pdf"

SITE = "한솔솔파크 306동 502호 귀하"
DATE = "2026년 11월 9일"
PERIOD = "총 20일 예상"
EXPECTED_SUPPLY = 35_042_000  # 총 공급가액 (변동 없음)

SANGKOM = ("쌍곰 퍼펙트라인 소포장 내장줄눈 / 방수·항균 타일줄눈",
           ["sangkom_perfectline.jpg"], "쌍곰 퍼펙트라인 내장줄눈")

# 품목: (품명, 규격, 수량, 단위, 단가, 구분 m=자재 l=노무 e=경비, 사진[], 사진설명|None)
# 사진설명 None 이면 규격의 ' / ' 앞부분을 사용
SECTIONS = [
    ("철거", 111_000, [
        ("철거 인건비", "철거공 3인 × 2일 / 화장대·부엌장·아일랜드·걸레받이·기존등·강화마루·욕실 2곳·욕조", 6, "인·일", 250_000, "l", ["o10.jpg", "o11.jpg", "o12.jpg", "o13.jpg"], None),
        ("폐기물 처리", "1톤 차량 반출·처리 (강화마루·욕실 타일 포함)", 3, "대", 250_000, "e", ["o14.jpg"], None),
        ("식대", "철거 6인·일", 6, "인·일", 15_000, "e", [], None),
    ]),
    ("목공 (천장 평탄화·아트월·걸레받이)", 14_600, [
        ("석고보드", "KCC 일반 석고보드 9.5T 900×1800 / 거실 천장 평탄화 + 아트월 덧방", 24, "장", 4_300, "m", ["o15.jpg"], None),
        ("각재", "다루끼 30×30×3600 / 천장 레벨 작업", 4, "단", 30_000, "m", ["o16.jpg"], None),
        ("걸레받이", "4전 걸레받이 (40mm) 화이트 2.4m / 약 100m", 42, "본", 4_600, "m", ["o17.jpg"], None),
        ("목공 부자재", "피스·타카핀·본드", 1, "식", 60_000, "m", ["o18.jpg"], None),
        ("목수 인건비", "목수 2인 × 1.5일 / 천장 평탄화·아트월·걸레받이", 3, "인·일", 320_000, "l", [], None),
        ("목공 조공", "조공 1인 × 1일", 1, "인·일", 200_000, "l", [], None),
        ("식대", "목공 4인·일", 4, "인·일", 15_000, "e", [], None),
    ]),
    ("도배", 2_550, [
        ("실크 벽지", "신한벽지 실크 15130-1 화이트 / 공급 33평", 15, "롤", 43_830, "m", ["o19.jpg"], None),
        ("도배 부자재", "초배지·부직포·풀", 1, "식", 150_000, "m", ["o20.jpg"], None),
        ("도배 인건비", "도배사 3인 × 2일", 6, "인·일", 290_000, "l", [], None),
        ("식대", "도배 6인·일", 6, "인·일", 15_000, "e", [], None),
    ]),
    ("장판", 880_000, [
        ("장판", "LX 엑스컴포트 5.0 크리마마필 그레이 XCF4482 (600×600 타일형) / 약 21평 + 로스", 23, "평", 70_000, "m", ["o21.jpg"], "LX 엑스컴포트 5.0 크리마마필 그레이 XCF4482 (600×600 타일형)"),
        # 기존 '장판 부자재(양면테이프·이음 용접) 60,000' 항목 삭제 → 장판 시공비에 포함 (260,000 → 290,000 × 2)
        ("장판 인건비", "장판 기사 2인 × 1일 / 바닥 양면테이프 시공 포함", 2, "인·일", 290_000, "l", [], None),
        ("식대", "장판 2인·일", 2, "인·일", 15_000, "e", [], None),
    ]),
    ("전기·조명", 290_000, [
        ("다운라이트", "장수램프 LED 확산형 3인치 10W / 주광색", 30, "개", 7_000, "m", ["o25.jpg"], None),
        ("실링팬", "로슬러 프라임 초슬림 실링팬 화이트 / 거실 외 1곳", 2, "개", 325_000, "m", ["o26.jpg"], None),
        ("인덕션 전용 회로", "20A 차단기 + 4sq 전선 / 분전반에서 단독 배선", 1, "식", 70_000, "m", ["o27.jpg"], None),
        ("전기 부자재", "전선·매입박스·커넥터", 1, "식", 120_000, "m", ["o28.jpg"], None),
        ("전기 인건비", "전기 기사 2인 × 2일 / 타공·배선·실링팬·인덕션 회로", 4, "인·일", 300_000, "l", [], None),
        ("식대", "전기 4인·일", 4, "인·일", 15_000, "e", [], None),
    ]),
    ("주방", 285_000, [
        ("씽크대 상·하부장", "MJ씽크대 주문제작 / PET 무광 화이트 / 인덕션·매립후드(900)·사각볼·폭포수전 포함", 1, "식", 1_800_000, "m", ["o29.jpg"], None),
        ("씽크대 상판", "LX 하이막스 소프트 그레이 (G184) / 주방 벽타일 8021과 같은 톤", 1, "식", 750_000, "m", ["o30.jpg"], None),
        ("L자 아일랜드 수납장", "MJ씽크대 주문제작 / PET 무광 화이트 (기존 철거 후 신규)", 1, "식", 2_800_000, "m", ["o31.jpg"], None),
        ("냉장고장", "MJ씽크대 주문제작 상부장 / PET 무광 화이트", 1, "식", 200_000, "m", ["o32.jpg"], None),
        ("씽크대 벽타일", "8021 밝은 그레이 포세린 800×800 / 약 4㎡ (1박스 2매·1.28㎡)", 4, "박스", 40_000, "m", ["o33.jpg"], None),
        ("탄성줄눈", SANGKOM[0], 2, "포", 25_000, "m", SANGKOM[1], SANGKOM[2]),
        ("가구 설치 인건비", "MJ씽크대 설치팀 2인 × 2일 / 씽크대·아일랜드·냉장고장", 4, "인·일", 280_000, "l", [], None),
        ("주방 타일 인건비", "타일 기공 1인 × 1일", 1, "인·일", 330_000, "l", [], None),
        ("식대", "주방 5인·일", 5, "인·일", 15_000, "e", [], None),
    ]),
    ("욕실 2곳 (철거 후 방수·타일·도기 신규)", 322_000, [
        ("방수제", "아덱스 WPM003 1액형 탄성 도막방수 16kg", 2, "통", 130_000, "m", ["o36.jpg"], None),
        ("안방 욕실 벽타일", "3371 밝은 그레이 300×600 / 약 17㎡", 12, "박스", 20_000, "m", ["o39.jpg"], None),
        ("안방 욕실 바닥타일", "30411 그레이 300×300 / 약 3㎡", 3, "박스", 15_000, "m", ["o40.jpg"], None),
        ("거실 욕실 벽타일", "3376 밝은 그레이 300×600 / 약 17㎡", 12, "박스", 20_000, "m", ["o41.jpg"], None),
        ("거실 욕실 바닥타일", "30416 그레이 300×300 / 약 3㎡", 3, "박스", 15_000, "m", ["o42.jpg"], None),
        ("탄성줄눈", SANGKOM[0], 10, "포", 25_000, "m", SANGKOM[1], SANGKOM[2]),
        ("시멘트·모래", "바닥 구배·미장", 1, "식", 120_000, "m", ["o43.jpg"], None),
        ("실리콘", "다우실란트 바이오 707 (욕실용)", 2, "식", 60_000, "m", ["o44.jpg"], None),
        ("코너비드·재료분리대", "알루미늄 ㄴ자", 1, "식", 60_000, "m", ["corner_bead_al.svg"], "알루미늄 ㄴ자 (참고 이미지)"),
        ("양변기", "아수아 AST-273", 2, "개", 130_000, "m", ["o46.jpg"], None),
        ("세면대", "아수아 반다리 세면대 ASL-501", 2, "개", 150_000, "m", ["o47.jpg"], None),
        ("세면대 수전", "비고(VIGO) VG1001 무광 니켈 원홀", 2, "개", 55_000, "m", ["o48.jpg"], None),
        ("샤워 수전", "비고(VIGO) VG-1006SS 무광 스텐 / 슬라이드바 샤워세트", 2, "개", 58_500, "m", ["shower_vigo.jpg"], "비고(VIGO) 무광 스텐"),
        ("천장재", "SMC 평형천장 무광 300×600 / 1박스 + 몰딩", 2, "식", 180_000, "m", ["o50.jpg"], None),
        ("욕실장", "슬라이드장 댐퍼형 / 폭 1400·1500", 2, "개", 288_000, "m", ["o51.jpg"], None),
        ("욕실 액세서리", "비고(VIGO) 무광 니켈 / 코너선반·수건걸이·휴지걸이", 2, "식", 130_000, "m", ["towel_bar.jpg"], "수건걸이"),
        ("방수 인건비", "방수 기공 1인 × 1일 (2곳)", 1, "인·일", 300_000, "l", [], None),
        ("타일 인건비", "타일 기공 2인 × 2.5일", 5, "인·일", 330_000, "l", [], None),
        ("타일 조공", "조공 1인 × 3일", 3, "인·일", 200_000, "l", [], None),
        ("설비 인건비", "설비 기사 1인 × 2일 / 도기·수전·천장재·욕실장", 2, "인·일", 300_000, "l", [], None),
        ("식대", "욕실 11인·일", 11, "인·일", 15_000, "e", [], None),
    ]),
    ("문 교체·필름", 181_300, [
        ("ABS 도어", "우딘 ABS 도어 화이트 / 문짝 교체, 경첩·레버 손잡이 포함 (추정)", 5, "짝", 120_000, "m", ["o55.jpg"], None),
        ("문틀 필름 (문 교체분)", "우딘 인테리어필름 WS034 파스텔중백색 / 문틀 5곳", 25, "m", 9_900, "m", ["o56.jpg"], None),
        ("문·문틀 필름", "우딘 인테리어필름 WS034 파스텔중백색 / 2곳", 10, "m", 9_900, "m", ["o56.jpg"], None),
        ("신발장 필름", "우딘 인테리어필름 WS034 파스텔중백색", 8, "m", 9_900, "m", ["o56.jpg"], None),
        ("장롱 필름", "우딘 인테리어필름 WS034 파스텔중백색 / 기존 장롱", 15, "m", 9_900, "m", ["o56.jpg"], None),
        ("필름 부자재", "프라이머·퍼티", 1, "식", 60_000, "m", ["o57.jpg"], None),
        ("방문 레버 손잡이", "레버형 손잡이 무광 / 7개", 7, "개", 15_000, "m", ["o58.jpg"], None),
        ("경첩", "스텐 경첩 / 문당 2개", 14, "개", 3_000, "m", ["o59.jpg"], None),
        ("도어 설치 인건비", "목수 1인 × 1.5일 / 문 교체·손잡이·경첩", 1.5, "인·일", 320_000, "l", [], None),
        ("필름 인건비", "필름 기사 2인 × 1.5일", 3, "인·일", 260_000, "l", [], None),
        ("식대", "문·필름 4.5인·일", 4.5, "인·일", 15_000, "e", [], None),
    ]),
    ("화장대·장롱", 190_000, [
        ("화장대", "MJ씽크대 주문제작 실속형 / 거울·하부장·조명", 1, "식", 550_000, "m", ["o60.jpg"], None),
        ("양문형 장롱", "MJ씽크대 주문제작 약 3.7m / 화장대와 이어서 총 4730", 1, "식", 1_200_000, "m", ["o31.jpg"], None),
        ("가구 설치 인건비", "MJ씽크대 설치팀 2인 × 1일", 2, "인·일", 280_000, "l", [], None),
        ("식대", "가구 2인·일", 2, "인·일", 15_000, "e", [], None),
    ]),
    ("현관", 235_000, [
        ("현관 타일", "66551 그레이 계열 화이트 600×600 포세린 / 약 2㎡", 2, "박스", 30_800, "m", ["o61.jpg"], None),
        ("탄성줄눈", SANGKOM[0], 1, "포", 25_000, "m", SANGKOM[1], SANGKOM[2]),
        ("현관 타일 인건비", "타일 기공 0.5일 / 주방 타일과 같은 날 (서비스 단가)", 1, "식", 63_400, "l", [], None),
        ("현관 중문", "케이도어 3연동 슬라이딩 (일반) / 화이트 프레임 · 모루유리", 1, "세트", 800_000, "m", ["o64.jpg"], None),
        ("중문 설치", "케이도어 설치팀 2인 × 0.5일", 1, "인·일", 250_000, "l", [], None),
        ("식대", "현관 1인·일", 1, "인·일", 15_000, "e", [], None),
    ]),
    ("샤시 문 손잡이", 185_000, [
        ("샤시 손잡이", "시스템창호용 핸들 화이트 / 약 10개 (추정)", 10, "개", 35_000, "m", ["o65.jpg"], None),
        ("설치 인건비", "설비 기사 1인 × 1일", 1, "인·일", 250_000, "l", [], None),
        ("식대", "1인·일", 1, "인·일", 15_000, "e", [], None),
    ]),
    ("기타", 8_200, [
        ("엘리베이터 사용료", "관리사무소 납부", 1, "식", 150_000, "e", ["o66.jpg"], None),
        ("엘리베이터 보양재", "보양재 5p / 엘리베이터·복도", 1, "세트", 34_300, "m", ["o67.jpg"], None),
        ("보양 작업", "조공 0.5일", 0.5, "인·일", 200_000, "l", [], None),
        ("식대", "0.5인·일", 0.5, "인·일", 15_000, "e", [], None),
    ]),
]

# 섹션 금액은 원본 견적과 동일해야 함 (금액 변동 없음)
EXPECTED_SECTION_TOTALS = [2_451_000, 1_711_000, 2_640_000, 3_100_000, 2_600_000, 7_570_000,
                           7_000_000, 2_890_000, 2_530_000, 1_450_000, 800_000, 300_000]

NOTES = [
    ("hl", None),  # 부가세 포함 문구 (계산값)
    ("", "※ 별도: 휴젠트 노바 2개 800,000원 (부가세 없음) → 총 결제 금액 {pay}원"),
    ("", "위 견적금액은 부가세 별도 금액이며 공사일정은 총20일 예상됩니다."),
    ("", "계약금 10% 입금 시 공사일정 확정 / 착공 시 40% · 공사진행 10일 후 30% · 완공 후 20% 지불해 주시면 됩니다."),
    ("", "사진은 선택하신 모델(또는 동급 참고) 이미지이며, 색상·패턴은 현장 샘플로 최종 확정합니다. 자재 단가는 2026년 11월 온라인 최저가 기준입니다."),
    ("", "공사진행후 추가된 작업은 최종잔금에 포함하여 지불해주시면 됩니다."),
    ("", "A/S는 1년 무상으로 진행되며, 시공자 책임일 경우 2년간 무상으로 진행됩니다."),
    ("", "기업 01020282114 이대수"),
]


def won(n):
    return f"{int(round(n)):,}"


def qty(q):
    return str(int(q)) if float(q).is_integer() else str(q)


def esc(s):
    return html.escape(s, quote=True)


def build():
    body = []
    no = 0
    tot = {"m": 0, "l": 0, "e": 0}
    mgmt_total = 0
    for si, (title, mgmt, items) in enumerate(SECTIONS):
        sec = {"m": 0, "l": 0, "e": 0}
        rows = []
        for name, spec, q, unit, price, kind, imgs, cap in items:
            no += 1
            amt = round(q * price)
            sec[kind] += amt
            cells = {k: (won(amt) if k == kind else "") for k in "mle"}
            photo = ""
            if imgs:
                caption = cap if cap else spec.split(" / ")[0]
                cls = "ph multi" if len(imgs) > 1 else "ph"
                pics = "".join(f'<img src="img/{esc(i)}" alt="">' for i in imgs)
                photo = f'<div class="{cls}"><div class="pics">{pics}</div><div class="cap">{esc(caption)}</div></div>'
            rows.append(
                f'<tr class="{"tall" if imgs else ""}"><td class="c">{no}</td><td>{esc(name)}</td>'
                f'<td class="spec">{esc(spec)}</td><td class="c">{qty(q)}</td><td class="c">{esc(unit)}</td>'
                f'<td class="r">{won(price)}</td><td class="r">{cells["m"]}</td><td class="r">{cells["l"]}</td>'
                f'<td class="r">{cells["e"]}</td><td class="r b">{won(amt)}</td><td class="photo">{photo}</td></tr>')
        rows.append(f'<tr><td></td><td colspan="2">일반관리비·이윤</td><td></td><td></td><td></td><td></td><td></td><td></td>'
                    f'<td class="r b">{won(mgmt)}</td><td></td></tr>')
        sec_total = sec["m"] + sec["l"] + sec["e"] + mgmt
        if sec_total != EXPECTED_SECTION_TOTALS[si]:
            sys.exit(f"섹션 금액 불일치: {title} {sec_total:,} != {EXPECTED_SECTION_TOTALS[si]:,}")
        body.append(f'<tr class="sec"><td colspan="6">{esc(title)}</td><td class="r">{won(sec["m"])}</td>'
                    f'<td class="r">{won(sec["l"])}</td><td class="r">{won(sec["e"])}</td><td class="r">{won(sec_total)}</td><td></td></tr>')
        body.extend(rows)
        for k in tot:
            tot[k] += sec[k]
        mgmt_total += mgmt

    direct = tot["m"] + tot["l"] + tot["e"]
    supply = direct + mgmt_total
    if supply != EXPECTED_SUPPLY:
        sys.exit(f"총 공급가액 불일치: {supply:,} != {EXPECTED_SUPPLY:,}")
    vat = round(supply * 0.1)
    incl = supply + vat
    rate = mgmt_total / direct * 100

    body.append(f'<tr class="sum"><td colspan="6" class="c">직접공사비 소계</td><td class="r">{won(tot["m"])}</td>'
                f'<td class="r">{won(tot["l"])}</td><td class="r">{won(tot["e"])}</td><td class="r">{won(direct)}</td><td></td></tr>')
    body.append(f'<tr class="sum"><td colspan="9" class="c">일반관리비·기업이윤 (직접공사비의 {rate:.1f}%)</td>'
                f'<td class="r">{won(mgmt_total)}</td><td></td></tr>')
    body.append(f'<tr class="grand"><td colspan="9" class="c">총 공급가액</td><td class="r">{won(supply)}</td><td></td></tr>')

    notes = []
    for cls, text in NOTES:
        if cls == "hl":
            text = f"※ 부가세 포함 금액 {won(incl)}원 (공급가액 {won(supply)}원 + 부가세 {won(vat)}원)"
        text = text.format(pay=won(incl + 800_000))
        notes.append(f'<li class="{cls}">{esc(text)}</li>')

    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        tpl = f.read()
    out = (tpl.replace("{{SITE}}", esc(SITE)).replace("{{DATE}}", esc(DATE)).replace("{{PERIOD}}", esc(PERIOD))
           .replace("{{MAT}}", won(tot["m"])).replace("{{LAB}}", won(tot["l"])).replace("{{EXP}}", won(tot["e"]))
           .replace("{{MGMT}}", won(mgmt_total)).replace("{{VAT}}", won(vat)).replace("{{INCL}}", won(incl))
           .replace("{{SUPPLY}}", won(supply)).replace("{{ROWS}}", "\n".join(body)).replace("{{NOTES}}", "\n".join(notes)))
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"자재비 {won(tot['m'])} / 노무비 {won(tot['l'])} / 경비 {won(tot['e'])} / 관리비 {won(mgmt_total)} "
          f"/ 공급가액 {won(supply)} / 부가세 {won(vat)} / 합계 {won(incl)} / 품목 {no}개")


def pdf():
    import subprocess
    js = """
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(1);
  const b = await chromium.launch();
  const pg = await b.newPage();
  await pg.goto('file://' + src, { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  // 섹션 제목 행이 페이지 맨 아래에 혼자 남지 않도록 다음 페이지로 넘김
  await pg.emulateMedia({ media: 'print' });
  await pg.evaluate(() => {
    const pageH = (297 - 24) / 25.4 * 96 - 6;
    const tbl = document.querySelector('table.est');
    const theadH = tbl.tHead.getBoundingClientRect().height;
    const rows = [...tbl.tBodies[0].rows];
    let y = tbl.getBoundingClientRect().top + window.scrollY + theadH;
    rows.forEach((tr, i) => {
      const h = tr.getBoundingClientRect().height;
      const need = tr.classList.contains('sec') && rows[i + 1] ? h + rows[i + 1].getBoundingClientRect().height : h;
      if (y + need > pageH) {
        if (tr.classList.contains('sec')) tr.style.breakBefore = 'page';
        y = theadH + h;
      } else y += h;
    });
  });
  await pg.pdf({ path: out, format: 'A4', printBackground: true,
                 margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  await b.close();
})();
"""
    subprocess.run(["node", "-e", js, os.path.join(HERE, "index.html"), os.path.join(HERE, PDF_NAME)], check=True)


if __name__ == "__main__":
    build()
    if "--no-pdf" not in sys.argv:
        pdf()
