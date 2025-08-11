import streamlit as st
from db_handler import get_recent_data
import pandas as pd
from io import BytesIO

# Admin password (use env vars in production)
ADMIN_PASSWORD = "######"

st.title("🔒 Admin Panel")
password = st.text_input("Enter admin password:", type="password")

if password == ADMIN_PASSWORD:
    st.success("Access granted.")
    df = get_recent_data(limit=100)
    st.dataframe(df)

    # 👉 Export to CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='user_emissions.csv',
        mime='text/csv'
    )

    # 👉 Export to Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Emissions')
    buffer.seek(0)  # ✅ Critical step
    st.download_button(
        label="📥 Download Excel",
        data=buffer,
        file_name='user_emissions.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

elif password:
    st.error("Incorrect password.")
