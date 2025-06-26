
import streamlit as st
import sqlite3
import uuid
import time
import os

DATABASE_FILE = "user_data.db"

def activate_app(user_id, code):
    st.write("🔢 الكود المدخل:", code)
    st.write("📁 قاعدة البيانات:", os.path.abspath(DATABASE_FILE))

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    st.write("📥 يتم تنفيذ الاستعلام على الكود...")
    c.execute("SELECT is_used FROM activation_codes WHERE code = ?", (code,))
    code_status = c.fetchone()
    st.write("📊 نتيجة الاستعلام:", code_status)

    if code_status and code_status[0] == 0:
        st.success("✅ الكود صالح وجاهز للاستخدام.")
    elif code_status:
        st.warning("⚠️ الكود مستخدم مسبقًا.")
    else:
        st.error("❌ الكود غير موجود في قاعدة البيانات.")

st.title("تجربة تفعيل الأكواد")
user_id = str(uuid.uuid4())
code_input = st.text_input("أدخل كود التفعيل:")
if st.button("تفعيل"):
    activate_app(user_id, code_input.strip())
