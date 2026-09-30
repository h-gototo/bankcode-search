#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日銀ネット・金融機関等コード一覧（xlsx）→ アプリ用 data.js 変換スクリプト

使い方（管理者）:
  python3 boj2json.py code1_YYYYMMDD.xlsx --notice "日銀シス第111号" --by "総務 山田"
  → 同じフォルダに data.js を生成（既存 data.js があれば更新履歴を引き継ぐ）

オプション:
  --notice  日銀「コード改正情報」の通知番号（任意）
  --by      更新者名（任意）
  --out     出力ファイル名（既定: data.js）
"""
import sys, json, re, argparse, datetime, os
import openpyxl

ap = argparse.ArgumentParser()
ap.add_argument('xlsx')
ap.add_argument('--notice', default='')
ap.add_argument('--by', default='')
ap.add_argument('--out', default='data.js')
a = ap.parse_args()

wb = openpyxl.load_workbook(a.xlsx, read_only=True)
ws = [s for s in wb.worksheets if '現在' in s.title][0]
asof = re.sub(r'[^0-9年月日]', '', ws.title)

insts, cur = [], None
for i, r in enumerate(ws.iter_rows(values_only=True)):
    if i < 2 or r[3] is None:
        continue
    cat, iname, sname, icode, scode = r[0], r[1], r[2], r[3], r[4]
    if iname and scode is None:                       # 金融機関行
        cur = {"c": f"{int(icode):04d}", "n": str(iname).strip(), "t": (cat or '').strip(),
               "bic": r[6] == '○', "b": []}
        insts.append(cur)
    elif scode is not None and cur:                   # 店舗行
        cur["b"].append({"c": f"{int(scode):03d}", "n": str(sname or '').strip(),
                         "on": r[5] == '○', "bic": r[6] == '○',
                         "tz": (str(r[7]).strip() if r[7] else '')})

# 既存 data.js の履歴を引き継ぐ
history = []
if os.path.exists(a.out):
    try:
        old = json.loads(re.sub(r'^\s*const\s+BANK_DATA\s*=\s*', '', open(a.out, encoding='utf-8').read()).rstrip().rstrip(';'))
        history = old.get('history', [])
    except Exception as e:
        print(f'注意: 既存 {a.out} の履歴を読めませんでした（{e}）。新規履歴として作成します。', file=sys.stderr)

today = datetime.date.today().strftime('%Y年%m月%d日')
entry = {"asof": asof, "notice": a.notice, "by": a.by, "updated": today, "file": os.path.basename(a.xlsx),
         "inst": len(insts), "branch": sum(len(x['b']) for x in insts)}
history = [entry] + [h for h in history if h.get('file') != entry['file']]

out = {"source": "日本銀行金融ネットワークシステム・金融機関等コード一覧（当座勘定取引関係事務）",
       "url": "https://www5.boj.or.jp/bojnet/codenew/mokujinew.htm",
       "asof": asof, "notice": a.notice, "by": a.by, "updated": today, "file": os.path.basename(a.xlsx),
       "history": history[:20], "data": insts}
with open(a.out, 'w', encoding='utf-8') as f:
    f.write("const BANK_DATA = " + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ";\n")
print(f"{a.out} を生成しました: 適用日 {asof} / 金融機関 {len(insts)} 件 / 店舗 {entry['branch']} 件")
