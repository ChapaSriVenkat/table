import streamlit as st
import mysql.connector
import pandas as pd
from Jwt_tokens import generate_token, decode_token
import logging

logging.basicConfig(filename='backend.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect():
    logging.info("Connecting to the MySQL database.")
    return mysql.connector.connect(
        host="34.200.59.62",
        user="root",
        password="Srii@773",
        database="login"
    )

def create_table():
    logging.info("Creating table if it doesn't exist.")
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
    logging.info("Table checked/created successfully.")

def add_user(username, email, password):
    logging.info(f"Attempting to add user: {username}")
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        logging.info(f"User {username} added successfully.")
        return True
    except mysql.connector.errors.IntegrityError as e:
        logging.error(f"Failed to add user {username}: {str(e)}")
        return False
    finally:
        conn.close()

def fetch_user(username):
    logging.info(f"Fetching user: {username}")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        logging.info(f"User found: {username}")
    else:
        logging.warning(f"User not found: {username}")
    return user

def fetch_all_users():
    logging.info("Fetching all users.")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    logging.info(f"Total users fetched: {len(users)}")
    return users

st.title("User Management Panel")


if st.button("Create Table"):
    create_table()
    st.success("Table created.")

st.subheader("Add a New User")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Add user"):
    if username and email and password:
        if add_user(username.strip(), email.strip(), password.strip()):
            st.success(f"User '{username}' added.")
        else:
            st.error("Username or Email already exists.")
    else:
        st.warning("Please fill in all fields.")

st.subheader("Login to Get JWT Token")
login_username = st.text_input("Login Username")
login_password = st.text_input("Login Password", type="password")

if st.button("Login"):
    user = fetch_user(login_username.strip())
    if user and user[3] == login_password:
        token = generate_token(login_username.strip())
        logging.info(f"JWT token generated for user: {login_username}")
        st.success("Login successful ")
        st.code(token, language='text')
    else:
        logging.warning(f"Login failed for user: {login_username}")
        st.error("Invalid username or password ")

st.subheader("Feature a User")
search_name = st.text_input("Enter username to search")
if st.button("Feature user"):
    user = fetch_user(search_name.strip())
    if user:
        st.info(f"**ID:** {user[0]}\n\n**Username:** {user[1]}\n\n**Email:** {user[2]}\n\n**Password:** {user[3]}")
    else:
        st.error("User not found.")

if st.button("Show users"):
    data = fetch_all_users()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Password"])
        st.dataframe(df[["Name", "Email", "Password"]], use_container_width=True)
    else:
        st.info("No users found.")

st.subheader("Decode a JWT Token")
input_token = st.text_area("Paste JWT Token")

if st.button("Decode Token"):
    result = decode_token(input_token.strip())
    st.json(result)
