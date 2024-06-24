''' Load libraries '''
import pandas
import streamlit as st
import datetime
import requests
from io import BytesIO


# Create the Home page
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




# Create the GSPR page in English
def EMDNen():
    st.header("EMDN code")
    st.write("Shown is the European Medical Device Nomenclature (EMDN) structure, which characterizes medical device information into different levels")
    
    excel = pandas.ExcelFile('https://github.com/flora8/gspr/raw/main/GSPRen.xlsx')
    emdn = pandas.read_excel(excel, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN

    st.dataframe(emdn) # Display the EMDN code data

    emdn_category = st.selectbox("Please select the EMDN code category", list(emdn)) # List the EMDN code category
    grouped_emdn = emdn.groupby(by=[emdn_category], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
    emdn_type = st.selectbox("Please select the EMDN code type", list(grouped_emdn.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 

    if st.button("Search"): # Set up the button
        st.success("Please wait a few minutes; the page turns on medical device: {} information".format(emdn_type))
        GSPRen(excel, emdn_type)
        SURVEYen(emdn_type)


def GSPRen(excel, emdn_type):
    st.header("General Safety and Performance Requirements (Annex I)")
    st.write("The {} information shown can be searched, fullscreen, and downloaded as an Excel file for personal records and edits".format(emdn_type))

    # Set up different tabs
    ChapterI, ChapterII, ChapterIII, Standards = st.tabs(["Chapter I", "Chapter II", "Chapter III", "Standards"])


    with ChapterI: # Get Chapter I General requirements details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=2) # replace NaN as blank, read the columns from A to C to get English details, and the header is 2nd row of excel
        chapterI_E = chapterI_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_E = chapterI_E.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_E)

    with ChapterII: # Get Chapter II Requirements regarding design and manufacture details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=26)
        chapterII_E = chapterII_E.replace("\n", ", ", regex=True) 
        chapterII_E = chapterII_E.iloc[:141] # Selecting all row from header 26 to row 141
        st.dataframe(chapterII_E)

    with ChapterIII: # Get Chapter III Requirements regarding the information supplied with the device details in English
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=169)
        chapterIII_E = chapterIII_E.replace("\n", ", ", regex=True) 
        chapterIII_E = chapterIII_E.iloc[:265]
        st.dataframe(chapterIII_E)

    with Standards: # Get Standard details in English
        st.subheader("Standards List")
        standards_E = pd.read_excel(excel, sheet_name=emdn_type, na_filter = False, usecols="K:L", header=2) # replace NaN as blank
        standards_E = standards_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_E = standards_E.iloc[:30]
        st.dataframe(standards_E)


def SURVEYen(emdn_type):
    # User requirement data functions
    st.subheader("User Experience Survey")

    with st.form(key="Information form"):
        day = st.text_input("Date ", (datetime.date.today()), disabled=True)
        medicaldevice = st.text_input("Searched medical devices", (emdn_type), disabled=True)
        background = st.selectbox("Background", ("", "Academics", "Manufacturer", "Importer", "Distributor", "Others",))
        role = st.selectbox("Role", ("", "Professionals", "Professor", "Student", "Manager", "Engineer", "Officer", "Sales Representative", "Assistant", "Others", "Prefer not to say"))
        clear = st.selectbox("How would you rate the provided device information on this website overall?", ("","1: Absolutely appropriate and clear", "2: Appropriate and clear", "3: Neutral", "4: Inappropriate and unclear", "5: Absolutely inappropriate and unclear"))
        useful = st.selectbox("How would you rate your overall experience with this website on a scale?", ("","1: Extremely useful", "2: Slightly useful", "3: Neither useful nor useless", "4: Slightly useless", "5: Extremely useless"))
        information = st.text_area("What other information would you like to see on this page?")
        feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?")
        submission = st.form_submit_button(label="Submit")
        if submission == True:
            userdata = pd.concat([pd.read_excel("SurveyEn.xlsx", sheet_name="DataEn"), pd.DataFrame.from_records([{
                "Date": day,
                "Device": medicaldevice,
                "Background": background,
                "Role": role,
                "How would you rate the provided device information on this website overall?": clear,
                "How would you rate your overall experience with this website on a scale?": useful,
                "What other information would you like to see on this page?": information,
                "Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?": feedback
                }])])
            userdata.to_excel("SurveyEn.xlsx", sheet_name="DataEn", index=False)
            st.success("Successfully submitted. !! Thank you so much for your support !! ")





# Create the GSPR page in Ｍandarin
def GSPRcn():
    excel = pd.ExcelFile('GSPRcn.xlsx') # Load the excel data
    emdn = pd.read_excel(excel, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN

    st.header("EMDN 代碼")
    st.write("表格所示為歐洲醫療器材命名法(EMDN)結構，該結構將醫療器材劃分為不同種類")
    st.dataframe(emdn) # Display the EMDN code data

    emdn_category = st.selectbox("請選擇 EMDN 代碼類別", list(emdn)) # List the EMDN code category
    grouped_emdn = emdn.groupby(by=[emdn_category], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
    emdn_type = st.selectbox("請選擇 EMDN 代碼類型", list(grouped_emdn.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 

    if st.button("搜尋"): # Set up the button
        st.success("請稍等幾分鐘；頁面將開啟: {}的醫療器材資訊".format(emdn_type))

        # Set up different tabs
        #一般安全和性能要求, 標準清單, 使用者體驗調查 = st.tabs(["一般安全和性能要求", "標準清單", "使用者體驗調查"])

        #with 一般安全和性能要求:
        st.header("一般安全和性能要求 (附錄 I)")
        st.write("顯示的資訊結果可以搜尋、全螢幕顯示，也可以下載為Excel檔案，以供個人記錄和編輯")

        # Get Chapter I General requirements details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=2)  # replace NaN as blank, read the columns from E to G to get Chinese details, and the header is 2nd row of excel
        chapterI_C = chapterI_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_C = chapterI_C.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_C)

        # Get Chapter II Requirements regarding design and manufacture details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=26)
        chapterII_C = chapterII_C.replace("\n", ", ", regex=True) 
        chapterII_C = chapterII_C.iloc[:141]
        st.dataframe(chapterII_C)

        # Get Chapter III Requirements regarding the information supplied with the device details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel, sheet_name=emdn_type, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter=False, usecols="A:C", header=169)
        chapterIII_C = chapterIII_C.replace("\n", ", ", regex=True) 
        chapterIII_C = chapterIII_C.iloc[:265]
        st.dataframe(chapterIII_C)


        #with 標準清單:
        # Get Standard details in Mandarin
        st.subheader("標準清單")
        standards_C = pd.read_excel(excel, sheet_name=emdn_type, na_filter = False, usecols="K:L", header=2) # replace NaN as blank
        standards_C = standards_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_C = standards_C.iloc[:30]
        st.dataframe(standards_C)


        #with 使用者體驗調查:
        # User requirement data functions
        conn = sqlite3.connect('data.db', check_same_thread=False)
        cur = conn.cursor()

        st.subheader("使用者體驗調查")
        survey = st.form("資料表單")
        day = survey.text_input("日期", (datetime.date.today()), disabled=True)
        medicaldevice = survey.text_input("醫療器材", (emdn_type), disabled=True)
        background = survey.selectbox("請問您的背景", ("", "學術", "製造商", "進口商", "經銷商", "其他",))
        role = survey.selectbox("請問您目前的職位", ("", "專業人士", "教授", "學生", "經理", "工程師", "專員", "業務", "助理", "其他", "不方便提供"))
        submission = survey.form_submit_button(label="提交")
        

        if submission == True:
            userdata = pd.concat([pd.read_excel("SurveyCn.xlsx"), pd.DataFrame.from_records([{
                "日期": day,
                "醫療器材": medicaldevice,
                "背景": background,
                "職位": role,
                }])])
            userdata.to_excel("SurveyCn.xlsx", index=False)
            st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")








            # st.subheader("使用者體驗調查")

            # with st.form(key="資料表單"):
            #     day = st.text_input("日期", (datetime.date.today()), disabled=True)
            #     medicaldevice = st.text_input("醫療器材", (emdn_type), disabled=True)
            #     background = st.selectbox("請問您的背景", ("", "學術", "製造商", "進口商", "經銷商", "其他",))
            #     role = st.selectbox("請問您目前的職位", ("", "專業人士", "教授", "學生", "經理", "工程師", "專員", "業務", "助理", "其他", "不方便提供"))
            #     clear = st.selectbox("請問您對本網站所提供的整體醫材資訊評價如何？", ("","1: 非常適當和明確", "2: 適當和明確", "3: 普通", "4: 不適當和不明確", "5: 非常不適當和不明確"))
            #     useful = st.selectbox("請問您對本網站的整體體驗有何評價？", ("","1: 非常有用", "2: 稍微有用", "3: 普通", "4: 稍微沒用", "5: 非常沒用"))
            #     information = st.text_area("請問您希望在此頁面上看到哪些其他資訊？")
            #     feedback = st.text_area("請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？")
            #     submission = st.form_submit_button(label="提交")
            #     if submission == True:
            #         userdata = pd.concat([pd.read_excel("SurveyCn.xlsx"), pd.DataFrame.from_records([{
            #             "日期": day,
            #             "醫療器材": medicaldevice,
            #             "背景": background,
            #             "職位": role,
            #             "請問您對本網站所提供的整體醫材資訊評價如何？": clear,
            #             "請問您對本網站的整體體驗有何評價？": useful,
            #             "請問您希望在此頁面上看到哪些其他資訊？": information,
            #             "請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？": feedback
            #             }])])
            #         userdata.to_excel("SurveyCn.xlsx", index=False)
            #         st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")
    



# # Create the sidebar for choosing the specific page
options = st.sidebar.radio("Pages", options=["Home", "GSPR (EN)", "GSPR (CN)"])

if options == "Home":
    Home()
elif options == "GSPR (EN)":
    EMDNen()
elif options == "GSPR (CN)":
    GSPRcn()
