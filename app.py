import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
import io
from reportlab.platypus import Image
from PIL import Image as PILImage

def create_pdf(name, job_title, email, phone, linkedIn, portfolio, profile_img, summary, qualification, skills, experience, experience_details):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Background Color for Header
    c.setFillColor(HexColor("#808000"))  # 
    c.rect(0, 700, 600, 70, fill=True, stroke=False)
    
    # Profile Image
    if profile_img:
        image = PILImage.open(profile_img)
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img = Image(img_buffer, width=60, height=60)
        img.drawOn(c, 60, 710)  # Adjusted position for alignment
    
    # Name & Job Title in White
    c.setFillColor('white')
    c.setFont("Helvetica-Bold", 26)
    c.drawString(160, 740, name)
    c.setFont("Helvetica", 16)
    c.drawString(160, 720, job_title)
    
    # Colored Line
    c.setStrokeColor(HexColor("#808000"))  # Blue color
    c.setLineWidth(2)
    c.line(50, 690, 550, 690)
    
    # Contact Details
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 660, "Contact Information")
    c.setFont("Helvetica", 11)
    c.drawString(50, 640, f"📧 Email: {email}")
    c.drawString(50, 620, f"📞 Phone: {phone}")
    c.drawString(50, 600, f"🔗 LinkedIn: {linkedIn}")
    c.drawString(50, 580, f"🌐 Portfolio: {portfolio}")
    
    # Summary Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 550, "Summary")
    c.setFont("Helvetica", 10)
    text = c.beginText(50, 530)
    for line in summary.split("\n"):
        text.textLine(line)
    c.drawText(text)
    
    # Qualification
    y_position = 490 if summary else 530
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Qualification")
    c.setFont("Helvetica", 11)
    c.drawString(50, y_position - 20, f"🎓 {qualification}")
    
    # Skills
    y_position -= 60
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Skills")
    c.setFont("Helvetica", 11)
    skill_list = skills.split(",")
    c.drawString(50, y_position - 20, " • " + " | ".join([s.strip() for s in skill_list]))
    
    # Experience
    y_position -= 60
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Experience")
    c.setFont("Helvetica", 11)
    c.drawString(50, y_position - 20, f"👔 {experience} years")
    
    y_position -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Experience Details")
    c.setFont("Helvetica", 10)
    exp_text = c.beginText(50, y_position - 20)
    for line in experience_details.split("\n"):
        exp_text.textLine(line)
    c.drawText(exp_text)
    
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("💼 Live Preview Resume Builder")

name = st.text_input("Enter your name:")
job_title = st.text_input("Job Title:")
email= st.text_input("Email")
phone= st.text_input("Phone No.")
linkedIn= st.text_input("LinkedIn")
portfolio= st.text_input("Portfolio URL")
profile_img = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])
summary = st.text_area("Summary:")
qualification = st.selectbox(
    "Select your highest qualification:",
    ["High School", "Diploma", "Bachelor's", "Master's", "PhD"]
)
skills = st.text_area("Skills (comma separated):")
experience = st.number_input("Enter your experience (in years):", min_value=0, max_value=50, step=1)
experience_details = st.text_area("Describe your work experience:")

# Live Preview
st.subheader("Live Preview")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### {name if name else 'Your Name'}")
    st.markdown(f"**{job_title if job_title else 'Your Job Title'}**")
with col2:
    if profile_img:
        st.image(profile_img, width=70)

st.markdown(f" 📧 **Email:** {email if email else 'Your Email...'}_")
st.markdown(f" 📞 **Phone No:** {phone if phone else 'Your Phone No...'}_")
st.markdown(f" 🔗 **LinkedIn:** {linkedIn if linkedIn else 'Your LinkedIn URL...'}_")
st.markdown(f" 🌐 **Portfolio:** {portfolio if portfolio else 'Your Portfolio URL...'}_")
st.markdown(f"### 📝 {'Summary'}")
st.write(f"_{summary if summary else 'Your summary will appear here...'}_")
st.markdown(f" ### 🎓 {'Qualification'}")
st.markdown(f" {qualification if qualification else 'Not Provided'}")
st.markdown(f"### {'Skills'}")
if skills:
    skill_list = skills.split(",")
    st.markdown("**Skills:** " + ", ".join([f"`{s.strip()}`" for s in skill_list]))
st.markdown(f" ### 👔 {'Experience'}")
st.markdown(f"👔 **Experience:** {experience if experience else 'Not Provided'} years")
st.markdown(f"📝 **Summary:** {experience_details if experience_details else 'No details provided'}")

if st.button("Generate PDF"):
    pdf_data = create_pdf(name, job_title, email, phone, linkedIn, portfolio, profile_img, summary, qualification, skills, experience, experience_details)
    st.download_button(label="📥 Download PDF", data=pdf_data, file_name="resume.pdf", mime="application/pdf")
