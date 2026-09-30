# 金融機関コード・支店コード検索

日本銀行「日銀ネット・金融機関等コード一覧」を元データとした、金融機関コード（4桁）・支店コード（3桁）の検索アプリです。
サーバー処理のない静的サイトで、GitHub Pages で公開しています。

- 検索ページ：`index.html`（名称から／コードから／業態・所在地から検索）
- 管理者画面：URL末尾に `#admin` を付ける（更新履歴の確認、動作確認用の一時読込）
- データ：`data.js`（`boj2json.py` で日銀の xlsx から生成）

## 更新方法（管理者）

`docs_update_guide.md` を参照。要点：

```
python3 boj2json.py code1_YYYYMMDD.xlsx --notice "日銀シス第○○号" --by "氏名"
git add data.js && git commit -m "データ更新 YYYY年MM月DD日適用" && git push
```

GitHub の Web 画面から `data.js` を「Upload files」で上書きしても同じです。

## 収録範囲の注意

日銀コード一覧は日銀ネット参加金融機関と日銀当座勘定取引店のみを収録しています。一般の支店・JA・個別の信用組合などは
含まれません。該当がない場合はアプリが各金融機関の公式サイトへのリンクを表示します。
振込・口座登録など重要な手続きでは、必ず各金融機関の公式情報で照合してください。

## 出典

日本銀行 日銀ネット・コード一覧 https://www5.boj.or.jp/bojnet/codenew/mokujinew.htm
