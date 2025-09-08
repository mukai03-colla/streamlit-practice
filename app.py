import streamlit as st

st.title("Hello, Streamlit!")
st.write("これは最小構成の Streamlit アプリです。")

number_1 = st.number_input(
    "1つ目の数字を入力してください。",
    min_value=0,
    max_value=100,
    value=10,
    step=1
)

number_2 = st.number_input(
    "2つ目の数字を入力してください。",
    min_value=0,
    max_value=100,
    value=10,
    step=1
)

number = number_1 + number_2

st.write(f"入力された数値の合計は {number} です。")