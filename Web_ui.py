import streamlit as st
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="34.200.59.62",
        user="root",
        password="Srii@773",
        database="login"
    )

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False
    finally:
        conn.close()

def fetch_user(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def fetch_all_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

st.title(" User Management Panel")

if st.button("1. Create Table"):
    create_table()
    st.success(" Table created (if not exists).")

st.subheader("2. Add a New User")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Add user"):
    if username and email and password:
        if add_user(username.strip(), email.strip(), password.strip()):
            st.success(f" User '{username}' added.")
        else:
            st.error(" Username or Email already exists.")
    else:
        st.warning(" Please fill in all fields.")

st.subheader("3. Feature a User")
search_name = st.text_input("Enter username to search")
if st.button("Feature user"):
    user = fetch_user(search_name.strip())
    if user:
        st.info(f"**ID:** {user[0]}\n\n**Username:** {user[1]}\n\n**Email:** {user[2]}\n\n**Password:** {user[3]}")
    else:
        st.error(" User not found.")

if st.button("4. Show users"):
    data = fetch_all_users()
    if data:
        import pandas as pd
        df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Password"])
        st.dataframe(df[["Name", "Email", "Password"]], use_container_width=True)
    else:
        st.info(" No users found.")