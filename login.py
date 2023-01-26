import pickle
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth

names=["ratan tata","bill gates","abhishek","divyanshu","ambuj","joshi","rana","sindhwal"]
usernames=['ratan','bill','abhishek','divyanshu','ambuj','joshi','rana','sindhwal']
passwords=['abc','abc','abc','abc','abc','abc','abc','abc']

hashed_passwords=stauth.Hasher(passwords).generate()

file_path=Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)