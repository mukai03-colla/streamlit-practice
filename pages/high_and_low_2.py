import streamlit as st
import random
import json
import os
import pandas as pd

# --- 設定 ---
DATA_DIR = "sample_data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
MAX_ROUNDS = 3
BET = 10

# --- JSONの読み書き ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- 初期化 ---
if "chips" not in st.session_state:
    st.session_state.chips = 100
    st.session_state.deck = list(range(1, 14))
    st.session_state.rounds = load_history()
    st.session_state.base_card = None
    st.session_state.result_card = None
    st.session_state.outcome = ""

st.title("🎲 High & Low ゲーム")
st.write("High か Low を選んでチップを賭けよう！（全3ラウンド）")

# --- 勝敗判定処理 ---
def play_round(choice: str):
    if not st.session_state.deck:
        return

    st.session_state.player_choice = choice
    st.session_state.result_card = random.choice(st.session_state.deck)
    st.session_state.deck.remove(st.session_state.result_card)

    base = st.session_state.base_card
    result = st.session_state.result_card

    if base is not None and result is not None:
        if choice == "High":
            if result > base:
                st.session_state.outcome = "win"
                st.session_state.chips += BET
            elif result < base:
                st.session_state.outcome = "lose"
                st.session_state.chips -= BET
            else:
                st.session_state.outcome = "draw"
        elif choice == "Low":
            if result < base:
                st.session_state.outcome = "win"
                st.session_state.chips += BET
            elif result > base:
                st.session_state.outcome = "lose"
                st.session_state.chips -= BET
            else:
                st.session_state.outcome = "draw"

        record = {
            "round": len(st.session_state.rounds) + 1,
            "base_card": base,
            "choice": choice,
            "result_card": result,
            "outcome": st.session_state.outcome,
            "chips_after": st.session_state.chips
        }
        st.session_state.rounds.append(record)
        save_history(st.session_state.rounds)

# --- 基準カードを引く ---
if st.session_state.base_card is None and st.session_state.deck and len(st.session_state.rounds) < MAX_ROUNDS:
    st.session_state.base_card = random.choice(st.session_state.deck)
    st.session_state.deck.remove(st.session_state.base_card)

if len(st.session_state.rounds) < MAX_ROUNDS:
    st.subheader("あなたのカード")
    st.write(st.session_state.base_card)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("High") and st.session_state.result_card is None:
            play_round("High")
    with col2:
        if st.button("Low") and st.session_state.result_card is None:
            play_round("Low")

    if st.session_state.result_card is not None:
        st.subheader("結果")
        st.write(f"引かれたカード: {st.session_state.result_card}")
        st.write(f"判定: {st.session_state.outcome}")
        st.write(f"所持チップ: {st.session_state.chips}")
        st.write(f"残りのカード: {st.session_state.deck}")

        if len(st.session_state.rounds) < MAX_ROUNDS:
            if st.button("次のラウンド"):
                st.session_state.base_card = None
                st.session_state.result_card = None
                st.session_state.outcome = ""
                st.rerun()
else:
    st.subheader("🎉 ゲーム終了！")
    st.write(f"最終チップ: {st.session_state.chips}")

# --- リセット ---
if st.button("リセット"):
    st.session_state.clear()
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.rerun()

# --- 履歴 ---
if st.session_state.rounds:
    st.subheader("プレイ履歴（最大3回）")
    df = pd.DataFrame(st.session_state.rounds)
    st.table(df)
