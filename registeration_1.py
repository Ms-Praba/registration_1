import streamlit as st
import gspread
from  google.oauth2.service_account import Credentials 
import pandas as pd 

SCOPE=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
@st.cache_resource
def init_connection():
	credentials=Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes=SCOPE)
	clients=gspread.authorize(credentials)
	return clients

connect=init_connection()	
client=connect.open("register1").sheet1

st.title("hyira's fan page")

tab1,tab2=st.tabs(["login","registeration"])

with tab1:
	with st.form("login"):
		username10=st.text_input("enter your username").strip().lower()
		password10=st.text_input("enter password",type="password").strip()
		users=client.get_all_records()
		found=False
		if st.form_submit_button("login"):
			if username10=="admin" and password10=="654321":
				df=pd.DataFrame(users)
				st.dataframe(df)
			else:
				for user in users:
					if str(user["username"])== username10 and str(user["password"]) == password10:
						found=True
						st.success(f"welcome {username10}")
						break
				if not found:
					st.success("wrong username or password")

						




with tab2:
	with st.form("resgisteration"):

		users=client.get_all_records()
		name=st.text_input("enter your name").strip()
		code=st.selectbox("country code",["+233","+234","+44","+1"])
		contact1=st.text_input("enter your contact").strip()
		contact= code+contact1
		email=st.text_input("enter your email").strip()
		gender=st.radio("select gender:",("male","female","not necessary"))
		dob=st.text_input("enter your date of birth").strip()
		username=st.text_input("enter your username").strip().lower()
		password=st.text_input("enter your password",type="password").strip()
		password2=st.text_input("repeat password",type="password").strip()
		if st.form_submit_button("submit"):
			if password != password2:
				st.success("password does not match")
			else:
				client.append_row([name, contact, email,gender,dob, username, password])

				st.success("registeration successful")



