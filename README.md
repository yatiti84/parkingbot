## 目標
1. 在line對話中完成停車場付費機制
2. 串接line message api
3. 減少掃QR code和輸入資料及網頁跳轉的過程

## tech stack
python, flask, line message api
### deploy
on [Render](https://dashboard.render.com/)

## 步驟
1. 設定 line platform
2. line webhook service接收訊息，一定的關鍵字啟動停車場付費工程。
3. 透過call api獲得停車場資訊和交易驗證資訊
4. 確認資訊後透過停車場api獲得linepay付款url
5. 回覆linepay付款url

## future

1. 擴充line menu功能，可一次性設定車號及其他資訊，以便後續重複使用。
2. 回傳付款url可直接開啟linepay付款，減少再次點擊。

### todo
testing

