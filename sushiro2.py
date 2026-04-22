#!/usr/bin/env python
# coding: utf-8
# In[1]:

import streamlit as st

st.set_page_config(page_title="🍣 Sushiro Calculator", layout="centered")

st.title("🍣 Sushiro Price Calculator")

# =========================
# Default ค่าเริ่มต้น
# =========================
defaults = {
    "price_red": 40,
    "price_silver": 60,
    "price_gold": 80,
    "price_black": 120,
    "red_qty": 0,
    "silver_qty": 0,
    "gold_qty": 0,
    "black_qty": 0,
}

# =========================
# Init session
# =========================
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "extras" not in st.session_state:
    st.session_state.extras = []

# =========================
# Reset
# =========================
def reset_all():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state.extras = []

# =========================
# 🔥 Sidebar (Settings)
# =========================
with st.sidebar:
    st.title("⚙️ Settings")

    st.subheader("💰 ราคาต่อจาน")
    st.number_input("🔴 แดง", key="price_red")
    st.number_input("⚪ เงิน", key="price_silver")
    st.number_input("🟡 ทอง", key="price_gold")
    st.number_input("⚫ ดำ", key="price_black")

    st.markdown("---")

    st.subheader("🧾 ค่าใช้จ่ายเพิ่มเติม")
    vat_percent = st.slider("VAT (%)", 0, 10, 7)
    service_percent = st.slider("Service (%)", 0, 15, 0)

    st.markdown("---")
    st.button("🔄 รีเซ็ตทั้งหมด", on_click=reset_all)

# =========================
# จำนวนจาน
# =========================
st.subheader("🍽️ จำนวนจาน")

c1, c2 = st.columns(2)

with c1:
    st.number_input("🔴 แดง (จาน)", key="red_qty", min_value=0)
    st.number_input("⚪ เงิน (จาน)", key="silver_qty", min_value=0)

with c2:
    st.number_input("🟡 ทอง (จาน)", key="gold_qty", min_value=0)
    st.number_input("⚫ ดำ (จาน)", key="black_qty", min_value=0)

# =========================
# คำนวณจาน
# =========================
red_total = st.session_state.red_qty * st.session_state.price_red
silver_total = st.session_state.silver_qty * st.session_state.price_silver
gold_total = st.session_state.gold_qty * st.session_state.price_gold
black_total = st.session_state.black_qty * st.session_state.price_black

# =========================
# เมนูอื่นๆ
# =========================
st.subheader("🍟 เมนูอื่นๆ / เพิ่มเอง")

def add_item():
    st.session_state.extras.append({
        "name": "",
        "price": 0,
        "qty": 1
    })

st.button("➕ เพิ่มเมนู", on_click=add_item)

extra_total = 0

for i, item in enumerate(st.session_state.extras):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

    with col1:
        item["name"] = st.text_input("ชื่อเมนู", value=item["name"], key=f"name_{i}")
    with col2:
        item["price"] = st.number_input("ราคา", value=item["price"], key=f"price_{i}")
    with col3:
        item["qty"] = st.number_input("จำนวน", value=item["qty"], min_value=1, key=f"qty_{i}")
    with col4:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.extras.pop(i)
            st.rerun()

    extra_total += item["price"] * item["qty"]

# =========================
# รวมทั้งหมด
# =========================
subtotal = (
    red_total
    + silver_total
    + gold_total
    + black_total
    + extra_total
)

vat = subtotal * (vat_percent / 100)
service = subtotal * (service_percent / 100)
total = subtotal + vat + service

# =========================
# แสดงผล
# =========================
st.subheader("📊 สรุปบิล")

st.write(f"🔴 แดง: {red_total:.2f} บาท")
st.write(f"⚪ เงิน: {silver_total:.2f} บาท")
st.write(f"🟡 ทอง: {gold_total:.2f} บาท")
st.write(f"⚫ ดำ: {black_total:.2f} บาท")

st.write(f"🍟 เมนูอื่นๆ: {extra_total:.2f} บาท")

if st.session_state.extras:
    st.markdown("### 📋 รายการเพิ่มเติม")
    for item in st.session_state.extras:
        if item["name"]:
            st.write(f"- {item['name']} x {item['qty']} = {item['price'] * item['qty']} บาท")

st.markdown("---")
st.write(f"Subtotal: {subtotal:.2f} บาท")
st.write(f"VAT: {vat:.2f} บาท")
st.write(f"Service: {service:.2f} บาท")

st.markdown(f"## 💰 Total: {total:.2f} บาท")

# =========================
# 🔔 ข้อความกลางจอ
# =========================
st.markdown("---")

def show_center_text(text, color):
    st.markdown(
        f"""
        <h2 style='text-align: center; font-weight: bold; color: {color};'>
            {text}
        </h2>
        """,
        unsafe_allow_html=True
    )

if total <= 0:
    show_center_text("ยังไม่กินอะไรเลยนะ 🤨", "#aaaaaa")
elif total <= 99:
    show_center_text("อิ่มหรอ? 😅", "#00cc66")
elif total <= 199:
    show_center_text("ตามสั่งจานละ 40 บาทก็อิ่มนะ 🍛", "#3399ff")
elif total <= 399:
    show_center_text("ยังได้อีก อย่าไปยอม!!!🔥", "#3399ff")
elif total <= 499:
    show_center_text("บุฟเฟ่ต์หน่อยไหม 😏", "#ff9933")
else:
    show_center_text("จยย นะ พรุ่งนี้สงสัยคงได้กินมาม่า 🥲", "#ff3333")

# In[]: