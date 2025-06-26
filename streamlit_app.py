import streamlit as st
import sqlite3
import uuid
import time
import os

st.set_page_config(page_title="القوانين اليمنية - نسخة مفعلة", layout="centered")

DATABASE_FILE = "user_data.db"
TRIAL_DURATION = 300  # غير مستخدم حاليًا لكن يمكن تفعيله لاحقًا

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            is_activated INTEGER DEFAULT 0,
            trial_start_time REAL,
            last_activity_time REAL,
            activation_code_used TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS activation_codes (
            code TEXT PRIMARY KEY,
            is_used INTEGER DEFAULT 0,
            used_by_user_id TEXT,
            FOREIGN KEY (used_by_user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_user_id():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (st.session_state.user_id,))
        conn.commit()
        conn.close()
    return st.session_state.user_id

def is_activated(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT is_activated FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] == 1 if result else False

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
        c.execute("UPDATE activation_codes SET is_used = 1, used_by_user_id = ? WHERE code = ?", (user_id, code))
        c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        c.execute("UPDATE users SET is_activated = 1, activation_code_used = ? WHERE user_id = ?", (code, user_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def main():
    st.title("تطبيق القوانين اليمنية - نسخة مفعلة")
    init_db()
    user_id = get_user_id()

    if "activated" not in st.session_state:
        st.session_state.activated = is_activated(user_id)

    if not st.session_state.activated:
        st.warning("⚠️ التطبيق غير مفعل. يرجى إدخال كود التفعيل.")

        code = st.text_input("أدخل كود التفعيل هنا:")
        if st.button("تفعيل التطبيق"):
            if code and activate_app(user_id, code.strip()):
                st.success("✅ تم التفعيل بنجاح!")
                st.session_state.activated = True
                st.rerun()
            else:
                st.error("❌ كود التفعيل غير صحيح أو تم استخدامه مسبقًا.")
    else:
        st.success("✅ التطبيق مفعل! يمكنك استخدام المحتوى الآن.")
        st.markdown("### ✅ هذه نسخة مبسطة من التطبيق المفعّل. يمكنك تطوير المحتوى هنا...")

main()
