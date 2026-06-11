import streamlit as st
import fitz  # PyMuPDF
import cv2
import numpy as np
import io

# Cấu hình trang web cute hột me
st.set_page_config(page_title="F5 File PDF", page_icon="🌸")

# Giao diện kute =))
st.title("🌸 Trạm Cứu Hộ PDF Mờ Xịt 🌸")
st.write("Cứu vớt mọi thể loại file scan lấm lem, xám xịt trở nên trắng bóc, nét căng chỉ trong một nốt nhạc! ✨💖")

# 1. Khu vực upload file thả thính
uploaded_file = st.file_uploader("📥 Thả nhẹ chiếc file PDF cần làm đẹp vào đây nha ~", type="pdf", accept_multiple_files=False)

# Thuật toán: Xử lý văn bản scan, giữ màu dấu đỏ/chữ ký, làm trắng nền
def process_image_for_sharpness(pixmap_bytes):
    nparr = np.frombuffer(pixmap_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Ép nét chữ
    kernel_sharpening = np.array([[-1, -1, -1], 
                                  [-1,  9, -1], 
                                  [-1, -1, -1]])
    img_sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    
    # Xóa xám nền
    alpha = 1.3  
    beta = 30    
    adjusted = cv2.convertScaleAbs(img_sharpened, alpha=alpha, beta=beta)
    
    # Khử nhiễu nền
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    adjusted[gray > 200] = [255, 255, 255]
    
    # Làm mịn viền
    gaussian_blur = cv2.GaussianBlur(adjusted, (3, 3), 0)
    final_img = cv2.addWeighted(adjusted, 1.5, gaussian_blur, -0.5, 0)
    
    _, img_encoded = cv2.imencode('.png', final_img)
    return img_encoded.tobytes()

# 2. Xử lý sự kiện khi có file
if uploaded_file:
    st.info("Ui cha, nhận được file rùi nè! Đã sẵn sàng làm phép! 🪄")
    
    dpi = st.slider("🎚️ Kéo độ sắc nét (Kéo lên 300 để nét căng đét ráng chịu nha)", min_value=72, max_value=300, value=150, step=10)
    
    if st.button("🪄 Biến hình!!"):
        with st.spinner("Đang múa phép thuật sương sương, đợi xíu nha... ⏳"):
            try:
                # Đọc file PDF
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                output_doc = fitz.open() 
                
                # Biến hình từng trang
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                    
                    processed_bytes = process_image_for_sharpness(pix.tobytes())
                    
                    new_page = output_doc.new_page(width=page.rect.width, height=page.rect.height)
                    new_page.insert_image(new_page.rect, stream=processed_bytes)
                
                # Lưu file
                output_pdf = io.BytesIO()
                output_doc.save(output_pdf)
                output_doc.close()
                doc.close()
                
                # Hiệu ứng thả bóng bay ăn mừng 🎉
                st.balloons()
                st.success("Tadaaa! 🎉 Biến hình thành công xuất sắc luôn!")
                
                # Nút tải file chót vót
                st.download_button(
                    label="💖 Tải chiếc file xịn xò này về máy thuii 💖",
                    data=output_pdf.getvalue(),
                    file_name=f"PDF_NetCang_{dpi}DPI.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Ối, rớt mạng hay gì gòi: {e} 😭")