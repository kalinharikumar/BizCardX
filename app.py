import streamlit as st
import easyocr
import cv2
import re
from sqlalchemy import text
import sqlalchemy
import pymysql

st.title(':blue[_BizCardX_]')
st.caption('Business Card scanner')
tab1, tab2 = st.tabs(["Home", "About"])

#Establishing DataBase connection through sqlalchemy-engine
#with cloud server using PlanetScale platform
ssl_args = {'ssl_ca':'/etc/ssl/certs/ca-certificates.crt'}
engine = sqlalchemy.create_engine("mysql+pymysql://5uxix5r7v1ftz5kblzxe:pscale_pw_TIUsd2vFjGgVveKpP1reNw9XUb5D0NraxGEpmvn0vaY@aws.connect.psdb.cloud/kalin",connect_args=ssl_args)
connection=engine.connect()
tables=engine.table_names()

with tab1:
    # col1, col2=st.columns(2)
    st.subheader(':blue[_Upload Card_]')

    uploaded_file = st.file_uploader('Choose image', type=['png', 'jpg'], accept_multiple_files=False,
                                     help='Only .jpg & .png are allowed')
    if uploaded_file != None:
        st.image(uploaded_file)
        #main part
        up=' '
        with open(f'{up}.png', 'wb') as f:
          f.write(uploaded_file.getvalue())
        img = cv2.imread(f'{up}.png')
        reader = easyocr.Reader(['en'])
        l = reader.readtext(img,detail = 0, paragraph = True)
        s=' '.join(l)
        url_s = re.findall(r"[www|WWW|wwW]+[\.|\s]+[a-zA-Z0-9]+[\.|\][a-zA-Z]+", s)
        url = re.sub('[WWW|www|wwW]+ ','www.', url_s[0])
        email_s = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+", s)
        email = email_s[0]
        mob_s = re.findall(r"[6-9]\d{9}|[\+9]\d{12}|[\+91]+\-\d{3}\-\d{4}|[\+1-2]\d{3}\-\d{3}\-\d{4}|[1-2]\d{2}\-\d{3}\-\d{4}",s)
        try:
          if mob_s[1] != None:
            mob=', '.join(mob_s)   
        except:
          mob = mob_s[0]
        ad_s = re.findall(r"[0-9]{1,4}\s[A-za-z]+\s[A-za-z]+[\s|\.|\,]\,\s[A-za-z]+[\|\,|\;]\s[A-za-z]+[\,\s|\,\s|\;\s|\s]+[0-6]{5,7}",s)
        ad = re.findall(r"([0-9]{1,4}\s[A-za-z]+\s[A-za-z]+)[\s|\.|\,]\,\s([A-za-z]+)[\|\,|\;]\s([A-za-z]+)[\,\s|\,\s|\;\s|\s]+([0-6]{5,7})",s)
        area_v = ad[0][0]
        city_v = ad[0][1]
        state_v = ad[0][2]
        pin = ad[0][3]
        l_s=l
        for i in l_s:
          if ad_s[0] in i:
            j=l_s.index(i)
            del(l_s[j])
          elif url_s[0] in i:
            j=l_s.index(i)
            del(l_s[j])
          elif email in i:
            j=l_s.index(i)
            del(l_s[j])
          elif mob in i:
            j=l_s.index(i)
            del(l_s[j])
        x = l_s[0]
        des_s = re.findall(r"[A-Za-z]+[\s|\s\&\s]+[A-Za-z]+$",x)
        des = des_s[0]
        nam_s = x.replace(des,'')
        nam_l = re.findall(r"[A-Za-z]+\s[A-Za-z]+|[A-Za-z]+",nam_s)
        nam = nam_l[0]
        cmp = l_s[-1]

        st.write('Extracted Raw Data:',s)
        st.subheader(':blue[_Check the Details & Save_]')

        with st.form("Details"):
            company_name = st.text_input('Company Name:', value=cmp)
            card_holder_name = st.text_input('Card Holder Name:', value=nam)
            designation = st.text_input('Designation:', value=des)
            mobile_number = st.text_input('Mobile Number:', value=mob)
            email_address = st.text_input('Email Address:', value=email)
            website = st.text_input('Website:', value=url)
            area = st.text_input('Area:', value=area_v)
            city = st.text_input('City:', value=city_v)
            state = st.text_input('State:', value=state_v)
            pincode = st.text_input('Pincode:', value=pin)
            submit_button = st.form_submit_button(label="Save")

        if "load_state" not in st.session_state:
            st.session_state.load_state = False
        if submit_button or st.session_state.load_state:
            st.session_state.load_state = True
            # databade upload
            #Inserting into db
            if tables == []:
              connection.execute(text("CREATE TABLE card_details (id Integer(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,company VARCHAR(20),name VARCHAR(20),designation VARCHAR(20),mobile VARCHAR(30),email VARCHAR(20),website VARCHAR(20),area VARCHAR(20),city VARCHAR(20),state VARCHAR(20),pincode VARCHAR(10),photo MEDIUMBLOB)"))
              query=text("INSERT INTO card_details (company,name,designation,mobile,email,website,area,city,state,pincode,photo) VALUES (:company,:name,:designation,:mobile,:email,:website,:area,:city,:state,:pincode,:photo)")
              connection.execute(query,company=cmp,name=nam,designation=des,mobile=mob,email=email,website=url,area=area,city=city,state=state,pincode=pin,photo=img)
              st.success('Saved to Database', icon="✅")

            if tables != []:
              query=text("INSERT INTO card_details (company,name,designation,mobile,email,website,area,city,state,pincode,photo) VALUES (:company,:name,:designation,:mobile,:email,:website,:area,:city,:state,:pincode,:photo)")
              connection.execute(query,company=cmp,name=nam,designation=des,mobile=mob,email=email,website=url,area=area,city=city,state=state,pincode=pin,photo=img)
              st.success('Saved to Database', icon="✅")
      
#with tab2:
#st.subheader(':blue[_Update details_]')
#search = st.text_input('Enter Card Holder Name')
#if st.button('search'):
#st.write('will be searched')


with tab2:
    st.subheader(':blue[_How to use:_]')
    st.write('1. upload the image from local storage')
    st.write('2. check the details and do corrections if needed')
    st.write('3. finally upload to database by clicking save button')
    st.subheader(':blue[_Packages used:_]')
    st.write('easyocr, streamlit, cv2, regex, sqlalchemy, pymysql')
    st.subheader(':blue[_Demo video:_]')
    st.write('')
    st.subheader(':blue[_GitHub link:_]')
    st.write('https://github.com/kalinharikumar/BizCardX.git')
