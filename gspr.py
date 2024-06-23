''' Load libraries '''
import streamlit as st
import pandas as pd
import datetime
import numpy as np
import requests as rq
from io import BytesIO


''' Create the Home page '''
def Home():
    st.title("Medical Device Regulation Decision Tool")

    st.markdown("""
                
                Research Title: Design of a Medical Device Regulation Decision Tool 

                Thank you so much for taking the time to participate in this research for a postgraduate student dissertation. This study aims to design a decision tool to correctly filter and select the appropriate regulatory requirements that need to be met by medical devices. After testing this tool, collect user experience to efficiently improve the system application and encourage widespread use in the future.
                
                In more detail, this system briefly analyses the European Union (EU) regulation requirements with relative standards for medical devices from the European Medical Device Nomenclature (EMDN), which according to Annex I: general safety and performance requirements (GSPR) as listed in the Medical Device Regulation (MDR) (2017/745) as well as the In Vitro Diagnostic Medical Devices Regulation (IVDR) (2017/746).
                * **MDR:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **IVDR:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **EMDN:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                User participation in this research study is entirely voluntary and will take around 5 minutes to complete. The survey is anonymous, and the users' answers will only be utilized for the purpose of writing a research report. Any report or publication resulting from this study cannot and will not personally identify the user.
                
                If you have any questions or require more information about this research, please use the following contact email: k23018577@kcl.ac.uk
                """)
    
    st.markdown("""
                            
                研究主題：醫療器材監管決策工具的設計

                非常感謝您抽出寶貴時間參與這項碩士生論文研究。本研究旨在設計一種決策工具，以正確過濾和選擇醫療器材所需滿足的適當監管要求。經過測試後收集使用者體驗，以有效改善應用系統及鼓勵未來廣泛的使用。
                
                該系統根據歐洲醫療器材命名法(EMDN)所提及的醫療器材，簡要分析了歐盟(EU)法規要求的相關標準。而歐盟法規來源於參考醫療器材法規(MDR)(2017/745)、以及體外診斷醫療器材法規(IVDR)(2017/746)中，其中附件一的一般安全和性能要求(GSPR)所列出內容。
                * **醫療器材法規:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **體外診斷醫療器材法規:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **歐洲醫療器材命名法:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                使用者參與本研究完全是自願的，花費時間約3~5分鐘完成。該調查是匿名的，使用戶的回答將僅用於撰寫研究報告為目的。而本研究產生的任何報告或出版物不能也不會識別使用者的個人身分。
                
                如果您對於本研究有任何疑問或需要更多信息，請透過以下電子郵件聯絡：k23018577@kcl.ac.uk
                """)

# # Establishing a Google sheets connection
# url = https://docs.google.com/spreadsheets/d/1f0Scol-OvZT-AioFyd78qFsgmSvkWFTkKw4LMPf2FBI/edit?usp=sharing
# conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# # Fetch existing data
# data = conn.read(spreadsheet=url, worksheet="0")

# Create the GSPR page
def GSPR():
    url = 'https://github.com/yenhua-flora/gspr/raw/main/GSPRproject.xlsx' # Load the excel data
    emdn = rq.get(url).content
    emdn = pd.read_excel(BytesIO(emdn))
    #emdn = pd.read_excel(excel, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN

    st.header("EMDN code")
    st.write("Shown is the European Medical Device Nomenclature (EMDN) structure, which characterizes medical device information into different levels")
    st.dataframe(emdn) # Display the EMDN code data

    emdn_category = st.selectbox("Please select the EMDN code category", list(emdn)) # List the EMDN code category
    grouped_emdn = emdn.groupby(by=[emdn_category], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
    emdn_type = st.selectbox("Please select the EMDN code type", list(grouped_emdn.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 

    if st.button("Search"): # Set up the button
        st.success("Please wait a few minutes; the page turns on medical device: {} information".format(emdn_type))

        st.header("General Safety and Performance Requirements (Annex I)")
        st.write("The {} information shown can be searched, fullscreen, and downloaded as an Excel file for personal records and edits".format(emdn_type))
    
        # Get Chapter I General requirements details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=2) # replace NaN as blank, read the columns from A to C to get English details, and the header is 2nd row of excel
        chapterI_E = chapterI_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_E = chapterI_E.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_E)

        # Get Chapter II Requirements regarding design and manufacture details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=26)
        chapterII_E = chapterII_E.replace("\n", ", ", regex=True) 
        chapterII_E = chapterII_E.iloc[:141] # Selecting all row from header 26 to row 141
        st.dataframe(chapterII_E)

        # Get Chapter III Requirements regarding the information supplied with the device details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=169)
        chapterIII_E = chapterIII_E.replace("\n", ", ", regex=True) 
        chapterIII_E = chapterIII_E.iloc[:265]
        st.dataframe(chapterIII_E)

        # Get Standard details in English
        st.subheader("Standards list")
        standards_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter = False, usecols="K:L", header=2) # replace NaN as blank
        standards_E = standards_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_E = standards_E.iloc[:30]
        st.dataframe(standards_E)

        

        st.header("通用安全和性能要求 (附錄 I)")
        st.write("顯示的資訊結果可以搜尋、全螢幕顯示，也可以下載為Excel檔案，以供個人記錄和編輯")

        # Get Chapter I General requirements details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="F", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="F:H", header=2)  # replace NaN as blank, read the columns from E to G to get Chinese details, and the header is 2nd row of excel
        chapterI_C = chapterI_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_C = chapterI_C.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_C)

        # Get Chapter II Requirements regarding design and manufacture details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="F", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="F:H", header=26)
        chapterII_C = chapterII_C.replace("\n", ", ", regex=True) 
        chapterII_C = chapterII_C.iloc[:141]
        st.dataframe(chapterII_C)

        # Get Chapter III Requirements regarding the information supplied with the device details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="F", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="F:H", header=169)
        chapterIII_C = chapterIII_C.replace("\n", ", ", regex=True) 
        chapterIII_C = chapterIII_C.iloc[:265]
        st.dataframe(chapterIII_C)

        # Get Standard details in Mandarin
        st.subheader("標準清單")
        standards_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter = False, usecols="N:O", header=2) # replace NaN as blank
        standards_C = standards_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_C = standards_C.iloc[:30]
        st.dataframe(standards_C)


        # User requirement data functions
        st.subheader("User Experience Survey 使用者體驗調查")
        with st.form(key="Information form"):
            day = st.text_input("Date 日期", (datetime.date.today()), disabled=True)
            medicaldevice = st.text_input("Searched medical devices 搜尋的醫療器材", (emdn_type), disabled=True)
            background = st.selectbox("Background 背景", ("", "Academics 學術", "Manufacturer 製造商", "Importer 進口商", "Distributor 經銷商", "Others 其他",))
            role = st.selectbox("Role 職位", ("", "Professionals 專業人士", "Professor 教授", "Student 學生", "Manager 經理", "Engineer 工程師", "Officer 專員", "Sales Representative 業務", "Assistant 助理", "Others 其他", "Prefer not to say 不方便提供"))
            clear = st.selectbox("How would you rate the provided device information on this website overall? 請問您對本網站所提供的整體醫材資訊評價如何？", ("","1: Absolutely appropriate and clear 非常適當和明確", "2: Appropriate and clear 適當和明確", "3: Neutral 普通", "4: Inappropriate and unclear 不適當和不明確", "5: Absolutely inappropriate and unclear 非常不適當和不明確"))
            useful = st.selectbox("How would you rate your overall experience with this website on a scale? 請問您對本網站的整體體驗有何評價？", ("","1: Extremely useful 非常有用", "2: Slightly useful 稍微有用", "3: Neither useful nor useless 普通", "4: Slightly useless 稍微沒用", "5: Extremely useless 非常沒用"))
            information = st.text_area("What other information would you like to see on this page? 請問您希望在此頁面上看到哪些其他資訊？")
            feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve? 請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？")
            submission = st.form_submit_button(label="Submit")
            if submission == True:
                userdata = pd.concat([pd.read_excel("UserData.xlsx"), pd.DataFrame.from_records([{
                    "Date": day,
                    "Device": medicaldevice,
                    "Background": background,
                    "Role": role,
                    "How would you rate the provided device information on this website overall?": clear,
                    "How would you rate your overall experience with this website on a scale?": useful,
                    "What other information would you like to see on this page?": information,
                    "Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?": feedback
                    }])])
                userdata.to_excel("Userdata.xlsx", index=False)
                st.success("Successfully submitted. !! Thank you so much for your support !! ")



# # Create the sidebar for choosing the specific page
options = st.sidebar.radio("Pages", options=["Home", "GSPR"])

if options == "Home":
    Home()
elif options == "GSPR":
    GSPR()


















# # User requirement data functions
# def form():
#     st.subheader("User Experience Survey")

#     with st.form(key="Information form"):
#         day = st.text_input("Date", (datetime.date.today()), disabled=True)
#         device = st.text_input("Searched devices", (emdn_type), disabled=True)
#         background = st.selectbox("Background", ("","Academics","Manufacturer","Importer","Distributor","Others",))
#         role = st.selectbox("Role", ("","Professionals","Professor","Student","Manager","Engineer","Officer","Sales Representative","Assistant","Others"))
#         clear = st.selectbox("How would you rate the provided device information on this website overall?", ("","1: Absolutely appropriate and clear", "2: Appropriate and clear", "3: Neutral", "4: Inappropriate and unclear", "5: Absolutely inappropriate and unclear"))
#         useful = st.selectbox("How would you rate your overall experience with this website on a scale?", ("","1: Extremely useful", "2: Slightly useful", "3: Neither useful nor useless", "4: Slightly useless", "5: Extremely useless"))
#         information = st.text_area("What other information would you like to see on this page?")
#         feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?")
#         submission = st.form_submit_button(label="Submit")
#         if submission == True:
#             userdata = pd.concat([pd.read_excel("UserData.xlsx"), pd.DataFrame.from_records([{
#                 "Date": day,
#                 "Device": device,
#                 "Background": background,
#                 "Role": role,
#                 "How would you rate the provided device information on this website overall?": clear,
#                 "How would you rate your overall experience with this website on a scale?": useful,
#                 "What other information would you like to see on this page?": information,
#                 "Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?": feedback
#                 }])])
#             userdata.to_excel("UserData.xlsx", index=False)
#             st.success("Successfully submitted. !! Thank you so much for your support !! ")

# form()










# # User requirement data functions
# conn = sqlite3.connect('data.db', check_same_thread=False)
# cur = conn.cursor()

# def form():
#     st.subheader("User Experience Survey")
#     # today = datetime.date.today()
#     with st.form(key="Information form"):
#         day = st.text_input("Date", (datetime.date.today()), disabled=True)
#         device = st.text_input("Searched devices", (emdn_type), disabled=True)
#         gender = st.selectbox("Sex", ("","male","female","prefer not to say"))
#         background = st.selectbox("Background", ("","Academics","Manufacturer","Importer","Distributor","Others",))
#         role = st.selectbox("Role", ("","Professionals","Professor","Student","Manager","Engineer","Officer","Assistant","Others"))
#         useful = st.selectbox("Do you think this system is useful?", ("","1: Strongly Agree", "2: Agree", "3: Neither Agree or Disagree", "4: Disagree", "5: Strongly Disagree"))
#         feedback = st.text_area("Please provide any feedback or suggestions to support us in improving the system performance.")
#         submission = st.form_submit_button(label="Submit")
#         if submission == True:
#             addData(day, device, gender,background,role, useful,feedback) 

# # The answers from users will be updated to the SQL database for analysis
# def addData(a,b,c,d,e,f,g):
#     cur.execute("""CREATE TABLE user_information(Date integer, Device text, Gender text, Background text, Role text, Useful text, Feedback text);""")
#     cur.execute("INSERT INTO user_information VALUES(?,?,?,?,?,?,?)", (a,b,c,d,e,f,g))
#     conn.commit()
#     conn.close()
#     st.success("Successfully submitted")

# form()
