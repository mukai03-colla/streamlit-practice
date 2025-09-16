import streamlit as st

#st.title("Hello, Streamlit!")
#st.write("これは最小構成の Streamlit アプリです。")

#number_1 = st.number_input(
#    "1つ目の数字を入力してください。",
#    min_value=0,
#    max_value=100,
#    value=10,
#    step=1
#)

#number_2 = st.number_input(
#    "2つ目の数字を入力してください。",
#    min_value=0,
#    max_value=100,
#    value=10,
#    step=1
#)

#number_add = number_1 + number_2
#number_multiple = number_1 * number_2

##太文字計算結果
#st.write(f"入力された数値の合計は {number_add} です。")
#st.write(f"入力された数値の積は {number_multiple} です。")

# 初期化
if "count" not in st.session_state:
    st.session_state.count = 0

# 更新
if st.button("カウントアップ"):
    st.session_state.count += 1

# 表示
st.write("カウント:", st.session_state.count)