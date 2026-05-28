# AI 交易助理

> 群益新力軍 Top Trader 競賽 × Claude AI
> 課程作業：AI 工具輔助交易實作

---

## 這個工具在幹嘛

輸入你對市場的觀察（新聞、價位、技術訊號），AI 自動分析並給出：

- 交易方向（做多 / 做空 / 觀望）
- 進場價位、停損、停利
- 建議倉位大小（基於 2% 風險原則）
- 風報比計算
- 競賽風控提醒（帳戶健康狀況）

---

## 快速啟動

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 取得 Claude API Key

前往 [console.anthropic.com](https://console.anthropic.com) 註冊並取得 API Key。

### 3. 啟動工具

```bash
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`。

---

## 使用流程

1. 在左側輸入你的 **Claude API Key**
2. 輸入目前的 **帳戶淨值**（追蹤風控狀態）
3. 選擇 **交易商品**（外匯 / 黃金 / 期貨等）
4. 在文字框輸入 **今日市場觀察**
5. 點擊「取得 AI 交易建議」

---

## 競賽規則摘要

| 項目 | 內容 |
|------|------|
| 初始資金 | USD 100,000 |
| 強制平倉線 | USD 50,000（回撤 50%）|
| 計分方式 | 絕對獲利（結算淨值 − 初始淨值）|
| 槓桿商品 | 外匯、黃金、美股 CFD |
| 期貨商品 | 國內外期貨 |

詳細規則見 [competition_rules_guide.md](competition_rules_guide.md)。

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `app.py` | Streamlit 主程式（AI 交易助理）|
| `requirements.txt` | Python 套件清單 |
| `.env.example` | API Key 設定範例 |
| `competition_rules_guide.md` | 競賽規則完整說明 |
| `detailed_leverage_product_guide.md` | 槓桿商品詳細資訊 |
| `detailed_futures_product_guide.md` | 期貨商品詳細資訊 |

---

## 免責聲明

本工具為課程作業，AI 分析僅供參考，不構成投資建議。交易決策請自行判斷，盈虧自負。
