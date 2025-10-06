import random
import streamlit as st

# --- 定数 ---
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
          "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}


# --- ヘルパー関数 ---
def new_deck():
    """フルデッキを返す（(rank, suit) タプルのリスト）。"""
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def ensure_deck_has_cards():
    """デッキが空になったときに、現在の手札を除いた新しいデッキを作り直す処理。
       （手札と重複するカードを再投入しないようにする）"""
    if "deck" not in st.session_state or len(st.session_state.deck) == 0:
        deck = new_deck()
        # 既に配られているカードは新デッキから削除する
        for card in st.session_state.get("player_hand", []) + st.session_state.get("dealer_hand", []):
            if card in deck:
                deck.remove(card)
        random.shuffle(deck)
        st.session_state.deck = deck


def draw_card():
    """デッキから1枚引いて返す。デッキ不足時は再作成する。"""
    ensure_deck_has_cards()
    return st.session_state.deck.pop()


def calculate_score(hand):
    """手札（[(rank,suit), ...]）の得点を計算（Aの11/1の調整を行う）。"""
    score = sum(VALUES[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == "A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


def init_game():
    """新しいゲームを初期化（デッキ生成、配牌、ブラックジャック判定まで）。"""
    st.session_state.deck = new_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    st.session_state.message = ""
    # 自然ブラックジャックの判定
    p_blackjack = calculate_score(st.session_state.player_hand) == 21 and len(st.session_state.player_hand) == 2
    d_blackjack = calculate_score(st.session_state.dealer_hand) == 21 and len(st.session_state.dealer_hand) == 2
    if p_blackjack or d_blackjack:
        st.session_state.game_over = True
        if p_blackjack and d_blackjack:
            st.session_state.message = "両者ブラックジャック！引き分けです。"
        elif p_blackjack:
            st.session_state.message = "あなたはブラックジャック！おめでとう、あなたの勝ちです。"
        else:
            st.session_state.message = "ディーラーがブラックジャック。あなたの負けです。"


# --- 初期化（最初の一回のみ）---
if "initialized" not in st.session_state:
    init_game()
    st.session_state.initialized = True

# --- UI ---
st.title("♠ ブラックジャック ♥")

st.subheader("あなたの手札")
st.write(" ".join(f"{r}{s}" for r, s in st.session_state.player_hand))
st.write("スコア:", calculate_score(st.session_state.player_hand))

st.subheader("ディーラーの手札")
if st.session_state.game_over:
    # 終了時は両方見せる
    st.write(" ".join(f"{r}{s}" for r, s in st.session_state.dealer_hand))
    st.write("スコア:", calculate_score(st.session_state.dealer_hand))
else:
    # 1枚だけ見せる
    first = st.session_state.dealer_hand[0]
    st.write(f"{first[0]}{first[1]}  ??")

st.subheader("操作")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("ヒット", key="hit"):
        if not st.session_state.game_over:
            st.session_state.player_hand.append(draw_card())
            player_score = calculate_score(st.session_state.player_hand)
            if player_score > 21:
                st.session_state.message = "バースト！ あなたの負けです。"
                st.session_state.game_over = True
            elif player_score == 21:
                # 自動的にスタンド相当の処理（プレイヤーが21を作った場合）
                # すぐにディーラー手番へ
                while calculate_score(st.session_state.dealer_hand) < 17:
                    st.session_state.dealer_hand.append(draw_card())
                dealer_score = calculate_score(st.session_state.dealer_hand)
                if dealer_score > 21 or player_score > dealer_score:
                    st.session_state.message = "あなたの勝ち！ 🎉"
                elif player_score < dealer_score:
                    st.session_state.message = "ディーラーの勝ち… 😢"
                else:
                    st.session_state.message = "引き分け！"
                st.session_state.game_over = True

with col2:
    if st.button("スタンド", key="stand"):
        if not st.session_state.game_over:
            # ディーラーは17以上になるまでヒット（ソフト17の扱いはここでは">=17で止める"）
            while calculate_score(st.session_state.dealer_hand) < 17:
                st.session_state.dealer_hand.append(draw_card())
            player_score = calculate_score(st.session_state.player_hand)
            dealer_score = calculate_score(st.session_state.dealer_hand)
            if dealer_score > 21:
                st.session_state.message = "ディーラーがバースト！ あなたの勝ちです。"
            elif player_score > dealer_score:
                st.session_state.message = "あなたの勝ち！ 🎉"
            elif player_score < dealer_score:
                st.session_state.message = "ディーラーの勝ち… 😢"
            else:
                st.session_state.message = "引き分け！"
            st.session_state.game_over = True

with col3:
    if st.button("リセット", key="reset"):
        # session_state を完全に clear すると initial flag も消えるため、
        # init_game() を呼んで必要なキーだけ上書きする方が安全。
        init_game()

st.subheader("結果")
if st.session_state.message:
    st.info(st.session_state.message)
else:
    if st.session_state.game_over:
        st.info("ゲーム終了。リセットして新しいゲームを始めてください。")
    else:
        st.write("ゲーム中です。ヒットかスタンドを選んでください。")