import random
import streamlit as st

# トランプのデッキ作成
suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
          "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

def calculate_score(hand):
    score = sum(values[card[0]] for card in hand)
    # A を 1 として調整
    aces = sum(1 for card in hand if card[0] == "A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# 初期化
if "deck" not in st.session_state:
    st.session_state.deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(st.session_state.deck)
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    st.session_state.message = ""

st.title("♠ ブラックジャック ♥")

# プレイヤーとディーラーの表示
st.subheader("あなたの手札")
st.write([f"{r}{s}" for r, s in st.session_state.player_hand])
st.write("スコア:", calculate_score(st.session_state.player_hand))

st.subheader("ディーラーの手札")
if st.session_state.game_over:
    st.write([f"{r}{s}" for r, s in st.session_state.dealer_hand])
    st.write("スコア:", calculate_score(st.session_state.dealer_hand))
else:
    st.write([f"{st.session_state.dealer_hand[0][0]}{st.session_state.dealer_hand[0][1]}", "??"])

# ヒット処理
if st.button("ヒット"):
    if not st.session_state.game_over:
        st.session_state.player_hand.append(st.session_state.deck.pop())
        if calculate_score(st.session_state.player_hand) > 21:
            st.session_state.message = "バースト！ あなたの負けです。"
            st.session_state.game_over = True

# スタンド処理
if st.button("スタンド"):
    if not st.session_state.game_over:
        # ディーラーは17以上になるまでヒット
        while calculate_score(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(st.session_state.deck.pop())
        player_score = calculate_score(st.session_state.player_hand)
        dealer_score = calculate_score(st.session_state.dealer_hand)
        if dealer_score > 21 or player_score > dealer_score:
            st.session_state.message = "あなたの勝ち！ 🎉"
        elif player_score < dealer_score:
            st.session_state.message = "ディーラーの勝ち… 😢"
        else:
            st.session_state.message = "引き分け！"
        st.session_state.game_over = True

# メッセージ表示
st.subheader("結果")
st.write(st.session_state.message)

# リセット
if st.button("リセット"):
    st.session_state.clear()
    st.experimental_rerun()