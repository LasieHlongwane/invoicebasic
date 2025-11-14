import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
from pdf_generator import generate_pdf  # Keep your existing PDF generator
from normalizer import normalize_columns

# Streamlit app config
st.set_page_config(page_title="LAC Invoice Generator", layout="centered")
st.title("🧾 LAC Invoice Generator (Basic)")
st.caption("Generate professional invoices from your sales data. No emails included.")

# Sidebar settings
st.sidebar.header("Settings")
business_name = st.sidebar.text_input("Business Name", "LAC Invoice Generator")
tax_rate = st.sidebar.number_input("VAT Percentage (%)", 0.0, 100.0, 15.0, step=1.0)

# File uploader
uploaded = st.file_uploader(
    "📂 Upload Sales File (CSV/XLSX)",
    type=["csv", "xlsx"],
    key="invoice_file_upload"
)

if uploaded:
    try:
        # Read the uploaded file
        if uploaded.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)

        # Normalize column names
        df = normalize_columns(df)
        st.success("✅ File uploaded and normalized successfully!")
        st.dataframe(df.head())

        # Check required columns
        required_columns = ["clientname", "amount"]
        missing = [col for col in required_columns if col not in [c.lower() for c in df.columns]]
        if missing:
            st.error(f"❌ Missing columns: {', '.join(missing)}. Please include {required_columns} in your file.")
        else:
            if st.button("🧾 Generate All Invoices"):
                try:
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zipf:
                        for idx, row in df.iterrows():
                            client_name = str(row.get("clientname", f"Client {idx+1}"))
                            reference = str(row.get("referenceno", f"INV-{idx+1}"))
                            amount = float(row.get("amount", 0))

                            tax = amount * (tax_rate / 100)
                            total_with_tax = amount + tax

                            items = [{
                                "description": "Professional Services Rendered",
                                "quantity": 1,
                                "unit_price": amount,
                                "total": total_with_tax
                            }]

                            data = {
                                "business_name": business_name,
                                "client_name": client_name,
                                "reference": reference,
                                "items": items,
                                "tax": tax
                            }

                            buffer = BytesIO()
                            generate_pdf(data, mode="invoice", output_path=buffer)
                            pdf_bytes = buffer.getvalue()

                            filename = f"{reference}_{client_name.replace(' ', '_')}.pdf"
                            zipf.writestr(filename, pdf_bytes)

                    zip_buffer.seek(0)
                    st.success("🎉 All invoices generated successfully!")
                    st.download_button(
                        label="⬇️ Download All Invoices (ZIP)",
                        data=zip_buffer,
                        file_name="All_Invoices.zip",
                        mime="application/zip"
                    )

                except Exception as e:
                    st.error(f"❌ Error generating invoices: {e}")

    except Exception as e:
        st.error(f"❌ Error reading uploaded file: {e}")

else:
    st.info("👆 Upload a CSV or Excel file containing client info to start.")
