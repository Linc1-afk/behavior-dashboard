from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import streamlit as st

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔥 DROP ALL TABLES (clean reset)
Base.metadata.drop_all(bind=engine)

# ✅ CREATE TABLES FRESH
Base.metadata.create_all(bind=engine)