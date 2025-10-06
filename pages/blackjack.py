import random
import streamlit as st

# --- 定数 ---
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
          "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}


# --- ヘルパー関数 ---
def new_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def calculate_score(hand):
    score = sum(VALUES[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == "A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


def init_game():
    st.session_state.deck = new_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_draws = []  # ディーラーがスタンドで引いたカードを記録
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.result_detail = ""


# --- 初期化 ---
if "deck" not in st.session_state:
    init_game()

# --- UI ---
st.title("♠ ブラックジャック ♥")

# プレイヤー表示
st.subheader("あなたの手札")
st.write(" ".join(f"{r}{s}" for r, s in st.session_state.player_hand))
player_score = calculate_score(st.session_state.player_hand)
st.write(f"スコア: {player_score}")

# ディーラー表示
st.subheader("ディーラーの手札")
if st.session_state.game_over:
    st.write(" ".join(f"{r}{s}" for r, s in st.session_state.dealer_hand))
    st.write(f"スコア: {calculate_score(st.session_state.dealer_hand)}")
else:
    first = st.session_state.dealer_hand[0]
    st.write(f"{first[0]}{first[1]}  ??")

# --- ボタン ---
col1, col2, col3 = st.columns([1, 1, 1])

# ヒット処理
with col1:
    if st.button("ヒット"):
        if not st.session_state.game_over:
            st.session_state.player_hand.append(st.session_state.deck.pop())
            player_score = calculate_score(st.session_state.player_hand)
            if player_score > 21:
                st.session_state.message = "バースト！あなたの負けです。"
                st.session_state.game_over = True

# スタンド処理
with col2:
    if st.button("スタンド"):
        if not st.session_state.game_over:
            dealer_score = calculate_score(st.session_state.dealer_hand)
            # ディーラーは17以上になるまで引く
            while dealer_score < 17:
                card = st.session_state.deck.pop()
                st.session_state.dealer_hand.append(card)
                st.session_state.dealer_draws.append(card)
                dealer_score = calculate_score(st.session_state.dealer_hand)

            player_score = calculate_score(st.session_state.player_hand)

            # 勝敗判定
            if dealer_score > 21:
                st.session_state.message = "ディーラーがバースト！あなたの勝ちです 🎉"
            elif player_score > dealer_score:
                st.session_state.message = "あなたの勝ち！ 🎉"
            elif player_score < dealer_score:
                st.session_state.message = "ディーラーの勝ち… 😢"
            else:
                st.session_state.message = "引き分け！"

            # 詳細結果メッセージ
            st.session_state.result_detail = (
                f"あなたのスコア: {player_score}　｜　ディーラーのスコア: {dealer_score}"
            )

            st.session_state.game_over = True

# リセット処理
with col3:
    if st.button("リセット"):
        init_game()
        st.experimental_rerun()

# --- 結果表示 ---
st.subheader("結果")
if st.session_state.message:
    st.info(st.session_state.message)
    if st.session_state.result_detail:
        st.write(st.session_state.result_detail)

    # ディーラーの引いたカードも明示
    if st.session_state.dealer_draws:
        st.write("ディーラーが引いたカード:")
        st.write(" ".join(f"{r}{s}" for r, s in st.session_state.dealer_draws))
else:
    st.write("ヒットまたはスタンドを選択してください。")
