import streamlit as st
import google.generativeai as genai

SYSTEM_PROMPT = """你是「AI 交易助理」，專門協助參加「群益新力軍 Top Trader」競賽的學生做交易決策分析。

【競賽基本規則】
- 初始資金：USD 100,000
- 最大回撤上限：50%（帳戶淨值跌破 USD 50,000 → 強制平倉出局）
- 計分方式：絕對獲利 = 結算淨值 − 初始淨值（需大於 0 才有排名資格）

【你的分析流程】
1. 判斷目前市場環境（多頭 / 空頭 / 盤整）
2. 給出明確交易方向（做多 / 做空 / 觀望）
3. 提供進場價位、停損點、停利目標（具體數字）
4. 計算建議倉位大小（基於帳戶淨值 × 2% 風險原則）
5. 給出 3 個要點的理由說明

【風控原則】
- 單筆最大虧損不超過帳戶淨值 2%
- 帳戶淨值低於 USD 65,000 時自動建議縮小倉位
- 帳戶淨值低於 USD 55,000 時建議停止交易、全力防守

【回覆格式】
請用以下結構化格式回覆：

## 市場判斷
（一句話概述目前市場狀況）

## 交易建議
| 項目 | 內容 |
|------|------|
| 方向 | 做多 / 做空 / 觀望 |
| 進場價位 | XXX |
| 停損 | XXX（風險 USD XXX）|
| 停利 | XXX（報酬 USD XXX）|
| 建議口數 | X 口（佔帳戶風險 X%）|
| 風報比 | 1:X |

## 分析理由
1. （技術面）
2. （基本面 / 消息面）
3. （風控考量）

## 風控提醒
（根據目前帳戶淨值給出具體建議）
"""

PRODUCT_OPTIONS = {
    "外匯保證金": [
        "EUR/USD 歐元/美元（30倍槓桿）",
        "USD/JPY 美元/日圓（30倍槓桿）",
        "GBP/USD 英鎊/美元（30倍槓桿）",
        "AUD/USD 澳幣/美元（20倍槓桿）",
        "USD/CHF 美元/瑞郎（20倍槓桿）",
    ],
    "商品（黃金／原油）": [
        "XAU/USD 黃金（20倍槓桿）",
        "XAG/USD 白銀（10倍槓桿）",
        "XTI/USD 美國輕原油（10倍槓桿）",
        "XBR/USD 布蘭特原油（10倍槓桿）",
    ],
    "海外指數 CFD": [
        "DJ30 道瓊指數（20倍槓桿）",
        "NDAQ100 納斯達克（20倍槓桿）",
        "SPX500 標普500（20倍槓桿）",
        "JPN225 日經225（20倍槓桿）",
    ],
    "海外期貨": [
        "ES 小型S&P500期貨",
        "NQ 小型那斯達克期貨",
        "MES 微型S&P500期貨",
        "MNQ 微型那斯達克期貨",
        "GC 黃金期貨",
        "MGC 微型黃金期貨",
        "CL 輕原油期貨",
        "EC 歐元期貨",
    ],
}


def get_trading_advice(api_key: str, product: str, balance: float, market_input: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
    )

    pnl = balance - 100_000
    pnl_pct = pnl / 100_000 * 100

    user_message = f"""
**交易商品：** {product}
**目前帳戶淨值：** USD {balance:,.0f}
**初始資金：** USD 100,000
**目前損益：** USD {pnl:+,.0f}（{pnl_pct:+.1f}%）

**今日市場觀察：**
{market_input}

請根據以上資訊給出完整的交易分析與建議。
"""

    response = model.generate_content(user_message)
    return response.text


def render_sidebar() -> tuple[str, float]:
    with st.sidebar:
        st.title("⚙️ 設定")

        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="前往 aistudio.google.com 取得你的 API Key",
        )

        st.divider()
        st.subheader("📊 競賽帳戶狀態")

        balance = st.number_input(
            "目前帳戶淨值 (USD)",
            min_value=0,
            max_value=500_000,
            value=100_000,
            step=1_000,
            format="%d",
        )

        pnl = balance - 100_000
        pnl_pct = pnl / 100_000 * 100
        drawdown_pct = max(0.0, -pnl_pct)
        remaining_room = 50.0 - drawdown_pct

        st.metric("損益", f"${pnl:+,.0f}", delta=f"{pnl_pct:+.1f}%")
        st.metric(
            "回撤幅度",
            f"{drawdown_pct:.1f}%",
            delta=f"剩餘空間 {remaining_room:.1f}%",
            delta_color="inverse",
        )

        if balance >= 80_000:
            st.success("🟢 帳戶健康，正常操作")
        elif balance >= 65_000:
            st.warning("🟡 注意：建議縮小倉位")
        elif balance >= 55_000:
            st.error("🔴 警告：接近危險水位！")
        else:
            st.error("⛔ 緊急：立即防守，停止開新倉！")

        st.divider()
        st.caption("競賽強制平倉線：USD 50,000")

    return api_key, balance


def main():
    st.set_page_config(page_title="AI 交易助理", page_icon="📈", layout="wide")

    api_key, balance = render_sidebar()

    st.title("📈 AI 交易助理")
    st.caption("群益新力軍 Top Trader 競賽 × Gemini AI")

    col1, col2 = st.columns([3, 1])

    with col1:
        category = st.selectbox("商品類別", list(PRODUCT_OPTIONS.keys()))
        product = st.selectbox("選擇商品", PRODUCT_OPTIONS[category])

    with col2:
        st.metric("已選商品", product.split()[0])

    st.divider()

    market_input = st.text_area(
        "📝 今日市場觀察",
        placeholder=(
            "請輸入你觀察到的市場資訊，例如：\n\n"
            "• 今日重要消息：Fed 維持利率不變，鮑爾發言偏鴿派\n"
            "• 目前價位：EUR/USD 現價 1.0850\n"
            "• 技術面：站上 20MA，RSI 約 55，近期高點 1.0900\n"
            "• 市場情緒：美元偏弱，歐元需求升溫\n"
            "• 即將公布數據：今晚 21:30 美國非農就業數據"
        ),
        height=220,
    )

    if not api_key:
        st.info("請在左側側邊欄輸入 Gemini API Key 才能使用")

    if st.button("🤖 取得 AI 交易建議", type="primary", use_container_width=True, disabled=not api_key):
        if not market_input.strip():
            st.warning("請先輸入今日市場觀察")
        else:
            with st.spinner("Gemini AI 分析中..."):
                try:
                    advice = get_trading_advice(api_key, product, balance, market_input)
                    st.divider()
                    st.subheader("🎯 AI 分析結果")
                    st.markdown(advice)
                    st.divider()
                    st.caption("⚠️ 以上分析僅供參考，交易決策請自行判斷。AI 不保證獲利。")
                except Exception as e:
                    st.error(f"發生錯誤：{e}")


if __name__ == "__main__":
    main()
