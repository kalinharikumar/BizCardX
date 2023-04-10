# BizCardX: Extracting Business Card Data with OCR
## Statement:
To develop a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The extracted information should then be displayed in the application's graphical user interface (GUI). In addition, the application should allow users to save the extracted information into a database along with the uploaded business card image. The database should be able to store multiple entries, each with its own business card image and extracted information.
## Packages used:
easyocr, streamlit, cv2, regex, sqlalchemy, pymysql
## workflow:
- Installing the required packages.
- Using Streamlit creating made UI with header, subheader, tabs, writebox, forms etc.
- Establishing DataBase connection through sqlalchemy-engine and engine.connecter.execute(text()) were used to write queries.
- Made upload button where only img file are allowded to select.
- streamlite loads img file to object so it is made again as file for further cv2 reading.
- Easy-ocr execution is made and raw text is extracted from image.
- using regex deeply i've made out every pattern for identification.
- company,name,designation,mobile,email,website,area,city,state,pincode all are extreacted individually using re, loops and conditions.
- finally extracted data is displaced using a form where user is allowed to edit the extracted details.
- submit button in form is uded to asign edited data to their varialble names and each column is assigned for each variable in the table
- additionally card image as object is uploaded to DB with the other details.
## Demo:
Demo video is uploaded in my linkedin page with code explanation please check it out:
