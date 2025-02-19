import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io
from reportlab.platypus import Image
from PIL import Image as PILImage

def create_pdf(name, job_title, email, phone, linkedIn, portfolio, profile_img, summary, qualification, skills, experience, experience_details):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Set starting positions
    y = 680
    img_x = 100
    img_y = y - 20  # Align image and name on same level

    # Profile Image
    if profile_img:
        image = PILImage.open(profile_img)
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img = Image(img_buffer, width=80, height=80)
        img.drawOn(c, img_x, img_y)  # Draw image on left side

    # Name and Job Title beside image
    text_x = img_x + 100
    c.setFont("Helvetica-Bold", 14)
    c.drawString(text_x, y + 10, name)
    c.setFont("Helvetica", 12)
    c.drawString(text_x, y - 10, job_title)

    # Colored Line
    c.setStrokeColor(HexColor("#3498db"))  # Blue color
    c.setLineWidth(2)
    c.line(80, y - 40, 530, y - 40)  # Draw a horizontal line

    y -= 60  # Move down after line

    # Add remaining content
    c.drawString(100, y, f"Email: {email}"); y -= 20
    c.drawString(100, y, f"Phone: {phone}"); y -= 20
    c.drawString(100, y, f"LinkedIn: {linkedIn}"); y -= 20
    c.drawString(100, y, f"Portfolio: {portfolio}"); y -= 40

    

    # Summary
    c.drawString(100, y, "Summary:"); y -= 20
    text = c.beginText(100, y)
    text.setFont("Helvetica", 10)
    for line in summary.split("\n"):
        text.textLine(line)
        y -= 12
    c.drawText(text)
    y -= 20

    # Qualification
    c.drawString(100, y, f"Qualification: {qualification}"); y -= 40

    # Skills
    c.drawString(100, y, "Skills:"); y -= 20
    skill_list = skills.split(",")
    skill_text = ", ".join(skill_list)
    c.drawString(100, y, skill_text); y -= 40

    # Experience
    c.drawString(100, y, f"Experience: {experience} years"); y -= 20
    c.drawString(100, y, "Experience Details:"); y -= 20
    exp_text = c.beginText(100, y)
    exp_text.setFont("Helvetica", 10)
    for line in experience_details.split("\n"):
        exp_text.textLine(line)
        y -= 12
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

st.write(f"_{email if email else 'Your Email...'}_")
st.write(f"_{phone if phone else 'Your Phone No...'}_")
st.write(f"_{linkedIn if linkedIn else 'Your LinkedIn URL...'}_")
st.write(f"_{portfolio if portfolio else 'Your Portfolio URL...'}_")
st.write(f"_{summary if summary else 'Your summary will appear here...'}_")
st.markdown(f"🎓 **Qualification:** {qualification if qualification else 'Not Provided'}")

if skills:
    skill_list = skills.split(",")
    st.markdown("**Skills:** " + ", ".join([f"`{s.strip()}`" for s in skill_list]))

st.markdown(f"👔 **Experience:** {experience if experience else 'Not Provided'} years")
st.markdown(f"📝 **Summary:** {experience_details if experience_details else 'No details provided'}")

# Generate PDF Button
if st.button("Generate PDF"):
    pdf_data = create_pdf(name, job_title, email, phone, linkedIn, portfolio, profile_img, summary, qualification, skills, experience, experience_details)
    st.download_button(label="📥 Download PDF", data=pdf_data, file_name="resume.pdf", mime="application/pdf")
