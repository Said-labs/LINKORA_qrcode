import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import base64
import cv2
import numpy as np

st.set_page_config(page_title="LINKORA", page_icon="qrcodeyyy.png")
st.title("✨ QR CODE GENERATOR ✨")


qr_data = st.text_input("Enter your link to generate code", key="qr_input")


st.subheader("⚙️ Customize QR")
qr_color = st.color_picker("Pick QR color", "#000000")
bg_color = st.color_picker("Pick background color", "#FFFFFF")
add_logo = st.checkbox("Add logo in center")


if st.button("Generate QR Code"):
    if qr_data:
        
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

        
        if add_logo:
            logo = Image.open("qrcodeyyy.png")  
            logo = logo.resize((60, 60))
            pos = ((img.size[0] - logo.size[0]) // 2,
                   (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos)

        
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        
        st.markdown(
            """
            <style>
            img {
                animation: fadeIn 2s;
            }
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.image(byte_im, caption="Your QR Code")

        b64 = base64.b64encode(byte_im).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="qrcode.png">📥 Download QR Code</a>'
        st.markdown(href, unsafe_allow_html=True)

    
        st.balloons()
    else:
        st.warning("⚠️ Please enter data")


st.subheader("🔍 Scan QR from Image")
uploaded_file = st.file_uploader("Upload QR image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded QR")

    
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(cv_img)

    if data:
        st.success(f"✅ QR Content: {data}")
        st.markdown(f"[🔗 Open Link]({data})")
    else:
        st.error("❌ Tidak ada data QR yang terbaca.")
