def app(st, current_dir, Image):
    # _______________________ directory of needed files __________
    resume_file = current_dir / "Resume" / "MyResume.pdf"
    profile_pic = current_dir / "Photos" / "profile-pic.png"
    Linkedin_pic = current_dir / "Photos" / "linkedin.png"
    Github_pic = current_dir / "Photos" / "github.png"
    Gmail_pic = current_dir / "Photos" / "gmail.png"


    # ___________________________ Picture ans summary  __________________
    c1,c2 = st.columns([1,2])
    profile_pic = Image.open(profile_pic)
    c1.image(profile_pic)
    with c2:
        st.header('About Me')
        st.markdown("My name is **Alexander Agbu**, I am a Data Science Master's student at University of Salford with a focused interest in the field of machine learning and data science. Eager to elevate my skills through hands-on, cutting-edge projects.  I am ready to apply my knowledge to real-world challenges, contributing to the forefront of technology and innovation.")
        st.caption('March 2024')
# TODO: Myresume.pdf 
        with open(resume_file, "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(
            label=" 📄 Download Resume",
            data=PDFbyte,
            file_name='Alexander_Agbu_Resume',
            mime="application/octet-stream",
        )
            
    st.write('#')
    # ___________________________ Links __________________
    _,sup = st.columns([1,2])
    Linkedin_pic = Image.open(Linkedin_pic)
    Github_pic = Image.open(Github_pic)
    Gmail_pic = Image.open(Gmail_pic)
    with sup:
        sub = st.columns(3)
        sub[0].image(Linkedin_pic, width= 50)
        LinkedIn = sub[0].link_button('LinkedIn', 'https://www.linkedin.com/in/alexanderagbu/')
        sub[1].image(Github_pic, width= 50)
        GitHub = sub[1].link_button('GitHub', 'https://github.com/Mrahlex')
        sub[2].image(Gmail_pic, width= 50)
        Gmail = sub[2].link_button('Gmail', 'mailto: agbualexuche@gmail.com')
