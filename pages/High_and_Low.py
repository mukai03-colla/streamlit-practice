import streamlit as st
import random


#st.success("You Win! ")
#st.error("You Lose ")
#st.info("Draw ")
#st.warning("This is a warning ")


# 初期化
if "base_card" not in st.session_state:
    st.session_state.base_card = random.randint(1, 13)
    st.session_state.next_card = None
    st.session_state.result = ""

st.title("🔼 High and Low Game 🔽")

st.write("High か Low か当ててください。")

# 基準カード表示
st.subheader("基準カード")
st.write(st.session_state.base_card)

# High 選択
if st.button("High"):
    if st.session_state.next_card is None:
        st.session_state.next_card = random.randint(1, 13)
        if st.session_state.next_card > st.session_state.base_card:
            #st.success("You Win!🎉")
            st.session_state.result = "🎉 勝ち！（High 正解）"
        elif st.session_state.next_card < st.session_state.base_card:
            #st.error("You Lose 😢")
            st.session_state.result = "😢 負け…（Lowでした）"
        else:
            #st.info("Draw ")
            st.session_state.result = "引き分け！"

# Low 選択
if st.button("Low"):
    if st.session_state.next_card is None:
        st.session_state.next_card = random.randint(1, 13)
        if st.session_state.next_card < st.session_state.base_card:
            #st.session_state.result = st.success("You Win!🎉")
            st.session_state.result = "🎉 勝ち！（Low 正解）"
        elif st.session_state.next_card > st.session_state.base_card:
            #st.error("You Lose 😢")
            st.session_state.result = "😢 負け…（Highでした）"
        else:
            #st.info("Draw ")
            st.session_state.result = "引き分け！"

# 結果表示
if st.session_state.next_card is not None:
    st.subheader("次のカード")
    st.write(st.session_state.next_card)
    st.subheader("結果")
    st.write(st.session_state.result)

# リセット
if st.button("もう一度遊ぶ"):
    st.session_state.clear()
    st.rerun()