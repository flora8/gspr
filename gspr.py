import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import openpyxl
import pip
from streamlit_gsheets import GSheetsConnection
from google.oauth2.service_account import Credentials
import gspread




#---------------------------------#
# Hide menu in Streamlit apps
hide = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)




# #---------------------------------#
# Count page views
# def Pageviews():
#     sum = 0
#     for i in range(10000):
#         sum = sum+i
#     return [sum] # convert the integers to list type
# pageviews = Pageviews()
# pageviews.append('dummy')

# try:
#     st.sidebar.markdown('Page viewed: {} times'.format(len(pageviews)))
# except ValueError:
#     st.sidebar.markdown('Page viewed: {} times'.format(1))




#---------------------------------#
# Create the Home page
def Home():
    st.title("Medical Device Regulation Decision Tool :stethoscope: ")

    st.markdown("""
                
                Research Title: Design of a Medical Device Regulation Decision Tool

                Thank you so much for taking the time to participate in this research for a postgraduate student dissertation. This study aims to design a decision tool to correctly filter and select the appropriate regulatory requirements that need to be met by medical devices. After testing this tool, collect user experience to efficiently analyse search results and improve the system application for encouraging widespread use in the future.

                In more detail, this system briefly analyses the European Union (EU) regulation requirements with relative standards for medical devices from the European Medical Device Nomenclature (EMDN), which according to Annex I: general safety and performance requirements (GSPR) as listed in the Medical Device Regulation (MDR) (2017/745) as well as the In Vitro Diagnostic Medical Devices Regulation (IVDR) (2017/746).
                * **MDR:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **IVDR:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **EMDN:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                User participation in this research study is entirely voluntary and will take around 5 minutes to complete. The survey is anonymous, and the users' answers will only be utilized for the purpose of writing a research report. Any report or publication resulting from this study cannot and will not personally identify the user.
                
                Please be aware that all information this system provides is for reference only, as regulations are updated frequently and the database may delay follow-up. If you have any questions or require more information about this research, please use the following contact email: k23018577@kcl.ac.uk
                """)
    
    st.markdown("""
                            
                研究主題：醫療器材監管決策工具的設計

                非常感謝您抽出寶貴時間參與這項碩士生論文研究。本研究旨在設計一種決策工具，以正確過濾和選擇醫療器材所需滿足的適當監管要求。經過測試後收集使用者體驗，以有效分析搜尋結果並改善應用系統進一步促進未來廣泛的使用。

                該系統根據歐洲醫療器材命名法(EMDN)所提及的醫療器材，簡要分析了歐盟(EU)法規要求的相關標準。而歐盟法規來源於參考醫療器材法規(MDR)(2017/745)、以及體外診斷醫療器材法規(IVDR)(2017/746)中，其中附件一的一般安全和性能要求(GSPR)所列出內容。
                * **醫療器材法規:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **體外診斷醫療器材法規:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **歐洲醫療器材命名法:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                使用者參與本研究完全是自願的，花費時間約3~5分鐘完成。該調查是匿名的，使用戶的回答將僅用於撰寫研究報告為目的。而本研究產生的任何報告或出版物不能也不會識別使用者的個人身分。
                
                請注意，本系統提供的所有資訊僅供參考，因法規日益更新而資料庫可能延遲跟進。如果您對於本研究有任何疑問或需要更多信息，請透過以下電子郵件聯絡：k23018577@kcl.ac.uk
                """)




#---------------------------------#
# Load excel data
excel_E = pd.ExcelFile('GSPRen.xlsx') # Load the excel data in English
emdn_E = pd.read_excel(excel_E, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN
emdn_E_all = emdn_E.iloc[:27] # Selecting all row from header 2 to row 27
emdn_E_part = emdn_E.iloc[32:] # Selecting all row from 32 to all row

excel_C = pd.ExcelFile('GSPRcn.xlsx') # Load the excel data in Mandarin
emdn_C = pd.read_excel(excel_C, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN
emdn_C_all = emdn_C.iloc[:27] # Selecting all row from header 2 to row 27
emdn_C_part = emdn_C.iloc[32:] # Selecting all row from 32 to all row


def EMDN(): # Create the EMDN page
    st.header(" :star2:  General Safety and Performance Requirements 一般安全和性能要求")
    st.markdown("""
                Thank you so much for testing the system function. The table below shows each EMDN code category and type corresponds with specific medical device data. Please select English or Mandarin to offer the EMDN code you would like to search for; then, the system will load the related information immediately. 
                
                非常感謝您測試本系統的功能。下表顯示了每個 EMDN 代碼類別和類型對應特定的醫療器材資料。請選擇英文或中文給予預計搜尋之 EMDN 代碼；然後，系統會立即載入相關資訊供您參考。
                """)

    st.image('image_flowchart.png') # The flowchart introduces how to operate this website
    
    col1, col2 = st.tabs(["EMDN code","EMDN 代碼"])

    with col1:  # Create the EMDN page in English
        st.header("EMDN code")
        st.write("""Shown is the European Medical Device Nomenclature (EMDN) structure, which characterizes medical device information into different levels""")
        st.dataframe(emdn_E_all) # Display the all EMDN code strature

        st.write("""Due to project time limitations, only a few medical devices of the EMDN code are available to search on the application""")
        category_E = st.selectbox("Please select the EMDN code category", list(emdn_E_part)) # List the EMDN code category, and user can only search a few medical device
        group_E = emdn_E_part.groupby(by=[category_E], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_E = st.selectbox("Please select the EMDN code type", list(group_E.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 
        
        if st.button("Search"): # Set up the button
            try:
                st.success("Please wait a few minutes; the page turns on medical device: {} information".format(type_E))
                type_E = type_E.split()[0]  # Split the string of EMDN type into a list and return the first element, which has the same name as the Excel worksheet
                GSPR_E(type_E) # The EMDN type will retun to the GSPR_E function
            except:
                st.error('The medical device information is unavailable for search; please select another EMDN code type', icon="🚨")
            

    with col2:  # Create the EMDN page in Mandarin
        st.header("EMDN 代碼")
        st.write("""表格所示為歐洲醫療器材命名法(EMDN)結構，該結構將醫療器材劃分為不同種類""")
        st.dataframe(emdn_C_all) # Display the EMDN code data in Mandarin

        st.write("""由於專案時間限制，目前該應用程式只能搜尋少數 EMDN 代碼的醫療器材資訊""")
        category_C = st.selectbox("請選擇 EMDN 代碼類別", list(emdn_C_part)) # List the EMDN code category
        group_C = emdn_C_part.groupby(by=[category_C], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_C = st.selectbox("請選擇 EMDN 代碼類型", list(group_C.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 
        
        if st.button("搜尋"): # Set up the button
            try:
                st.success("請稍等幾分鐘；頁面將開啟: {}的醫療器材資訊".format(type_C))
                type_C = type_C.split()[0]  # Split the string of EMDN type into a list and return the first element, which has the same name as the Excel worksheet
                GSPR_C(type_C)
            except:
                st.error('該醫療器材資訊目前無法檢索；請選擇其他 EMDN 代碼類型', icon="🚨")



def GSPR_E(type_E):  # Create the GSPR page in English
    st.write("The {} information shown can be searched, fullscreen, and downloaded as an Microsoft Excel file for personal records and edits".format(type_E))
    
    # Set up different tabs
    ChapterI, ChapterII, ChapterIII, Standards, Example = st.tabs(["Chapter I", "Chapter II", "Chapter III", "Standards", "Example"])

    with ChapterI: # Get Chapter I General requirements details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=2) # replace NaN as blank, read the columns from A to C to get English details, and the header is 2nd row of excel
        chapterI_E = chapterI_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_E = chapterI_E.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_E)

    with ChapterII: # Get Chapter II Requirements regarding design and manufacture details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=26)
        chapterII_E = chapterII_E.replace("\n", ", ", regex=True) 
        chapterII_E = chapterII_E.iloc[:141] # Selecting all row from header 26 to row 141
        st.dataframe(chapterII_E)

    with ChapterIII: # Get Chapter III Requirements regarding the information supplied with the device details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=169)
        chapterIII_E = chapterIII_E.replace("\n", ", ", regex=True) 
        chapterIII_E = chapterIII_E.iloc[:265]
        st.dataframe(chapterIII_E)

    with Standards: # Get Standard details in English
        st.subheader("Standards list")
        st.markdown("""
                    * **ISO:** [International Organization for Standardization](https://www.iso.org/home.html)

                    * **IEC:** [International Electrotechnical Commission](https://www.iec.ch/homepage)
                    
                    * **IMDRF:** [International Medical Device Regulators Forum](https://www.imdrf.org/)

                    * **CEN and CENELEC:** [European Committee for Standardisation and European Committee for Electrotechnical Standardisation](https://www.cencenelec.eu/)
                    """)
        standards_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_E = standards_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_E = standards_E.iloc[:30]
        st.dataframe(standards_E)

    with Example:
        st.subheader("Example template")
        st.markdown("""
                    * **MDCG 2021-08:** [Checklist of general safety and performance requirements, Standards, common specifications and scientific advice](https://ec.europa.eu/health/sites/default/files/md_sector/docs/mdcg_2021-8_annex6.docx)
                    1. Please click the link to download the template.
                    2. Please confirm the applied medical device(s) comply with :rainbow[EU MDR] or :rainbow[EU IVDR].
                    3. Please change the general safety and performance requirements (GSPR) information if the device(s) follow IVDR since the template uses MDR content. 
                    4. Please review the device(s) information in the chapter I, II, and III tabs to support you complete the form appropriately. 
                    """)
        st.image('imageA.jpg', caption='A. Standards, common specifications, scientific advice')
        st.image('imageB_example.png', caption='Example: B. Matrix of General safety and performance requirements')
        st.image('imageB_description.png', caption='Description: B. Matrix of General safety and performance requirements')


def GSPR_C(type_C):  # Create the GSPR page in Mandarin
    st.write("顯示的 {} 資訊結果可以搜尋、全螢幕顯示，也可以下載為Microsoft Excel檔案，以供個人後續記錄和編輯".format(type_C))
    
    #Set up different tabs
    第一章, 第二章, 第三章, 標準清單, 參考範例 = st.tabs(["第一章", "第二章", "第三章", "標準清單", "參考範例"])

    with 第一章: # Get Chapter I General requirements details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=2)  # replace NaN as blank, read the columns from E to G to get Chinese details, and the header is 2nd row of excel
        chapterI_C = chapterI_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_C = chapterI_C.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_C)

    with 第二章: # Get Chapter II Requirements regarding design and manufacture details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=26)
        chapterII_C = chapterII_C.replace("\n", ", ", regex=True) 
        chapterII_C = chapterII_C.iloc[:141]
        st.dataframe(chapterII_C)

    with 第三章: # Get Chapter III Requirements regarding the information supplied with the device details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=169)
        chapterIII_C = chapterIII_C.replace("\n", ", ", regex=True) 
        chapterIII_C = chapterIII_C.iloc[:265]
        st.dataframe(chapterIII_C)

    with 標準清單: # Get Standard details in Mandarin
        st.subheader("標準清單")
        st.markdown("""
                    * **ISO:** [International Organization for Standardization](https://www.iso.org/home.html)

                    * **IEC:** [International Electrotechnical Commission](https://www.iec.ch/homepage)
                    
                    * **IMDRF:** [International Medical Device Regulators Forum](https://www.imdrf.org/)

                    * **CEN and CENELEC:** [European Committee for Standardisation and European Committee for Electrotechnical Standardisation](https://www.cencenelec.eu/)
                    """)
        standards_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_C = standards_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_C = standards_C.iloc[:30]
        st.dataframe(standards_C)
        
    with 參考範例:
        st.subheader("參考範例")
        st.markdown("""
                    * **MDCG 2021-08:** [Checklist of general safety and performance requirements, Standards, common specifications and scientific advice](https://ec.europa.eu/health/sites/default/files/md_sector/docs/mdcg_2021-8_annex6.docx)
                    1. 請點選連結下載模板
                    2. 請確認申請之醫療器材符合:rainbow[歐盟醫療器材法規] 或 :rainbow[歐盟體外診斷醫療器材法規]的要求
                    3. 如果遵循體外診斷醫療器材法規條文，請變更一般安全與性能要求內容，因為模板為醫療器材法規條文
                    4. 請查看第一章、第二章和第三章中的醫療器材資訊，以幫助您適當填寫表格
                    """)
        st.image('imageA.jpg', caption='A. 標準、一般規範、科學建議')
        st.image('imageB_example.png', caption=' 範例：B. 一般安全與性能要求模型')
        st.image('imageB_說明.png', caption=' 說明：B. 一般安全與性能要求模型')





#---------------------------------#
def Survey(): # Collecting user inputs for later analysis
    st.header(" :memo: Survey 調查")
    st.markdown("""
                Thank you so much for providing your experience after testing this system in English or Mandarin for later analysis, and the collected result data will displayed on the next page for every participant to understand more information. :thought_balloon:
                
                非常感謝您在測試系統後，提供英文或中文的使用經驗供後續分析，而收集的結果數據將顯示在下一頁，供每位參與者了解更多信息。:thought_balloon:
                """)
    url = "https://docs.google.com/spreadsheets/d/1S3lA6Hk_N4bldzq4jKRTIS_R-7F7AL_zz9ZE76JDzV4" # The Google sheet url
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes=["https://www.googleapis.com/auth/spreadsheets"]) # Set up Google API credentials
    client = gspread.authorize(creds)
    
    col1, col2 = st.tabs(["User Experience Survey", "使用者體驗調查"])
 
    with col1:
        st.subheader("User Experience Survey")   
        day = st.text_input("Date ", (datetime.date.today()), disabled=True)
        background = st.selectbox("Please select the business type of your background?", ("", "Academics", "Notified Body (NB)", "Contract Research Organization (CRO)", "Manufacturer", "Importer", "Distributor", "Wholesaler", "Others",))
        role = st.selectbox("Please select your current role?", ("", "Professionals", "Professor", "Student", "Reviewer", "Clinical Research Associate (CRA)", "Manager", "Engineer", "Officer", "Sales Representative", "Assistant", "Others", "Prefer not to say"))

        category_E = st.selectbox("Which EMDN code category of medical device are you particularly interested in searching for on this application?", list(emdn_E_part)) # set index to none means there is no default options
        group_E = emdn_E_part.groupby(by=[category_E], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_E = st.selectbox("Which EMDN code type of medical device are you particularly interested in searching for on this application?", list(group_E.iloc[:,0]))
        category_E_all = st.selectbox("Which EMDN code category of medical device are you interested in searching for in the future?", list(emdn_E_all)) # set index to none means there is no default options
        group_E_all = emdn_E_all.groupby(by=[category_E_all], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_E_all = st.selectbox("Which EMDN code type of medical device are you interested in searching for in the future?", list(group_E_all.iloc[:,0]))
        
        information = st.selectbox("How would you rate the provided device information on this website application overall?", ("","1: Absolutely appropriate and clear", "2: Appropriate and clear", "3: Neutral", "4: Inappropriate and unclear", "5: Absolutely inappropriate and unclear"))
        experience = st.selectbox("How would you rate the benefits of having the regulation decision website application?", ("","1: Extremely useful and meaningful", "2: Useful and meaningful", "3: Neutral", "4: Useless and meaningless", "5: Extremely useless and meaningless"))
        others = st.text_area("What other information would you like to see on this page? (Optional)")
        feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve? (Optional)")
        submit = st.button(label="Submit")
        
        if submit == True: # if the submit button is pressed
            st.success("Successfully submitted. !! Thank you so much for your support !! ")       
            sheet = client.open_by_url(url).worksheet('survey')  # Access the Google Sheet
            data = [day,background,role,category_E,type_E,category_E_all,type_E_all,information,experience,others,feedback] # Read data from the user input
            sheet.append_row(data) # Append data to the Google sheet


    with col2:
        st.subheader("使用者體驗調查")
        day_C = st.text_input("日期", (datetime.date.today()), disabled=True)
        background_C = st.selectbox("請問您的背景", ("", "學術單位", "驗證機構(NB)", "受託研究機構(CRO)", "製造商", "進口商", "經銷商", "其他",))
        role_C = st.selectbox("請問您目前的職位", ("", "專業人士", "教授", "學生", "審查員", "臨床試驗人員", "經理", "工程師", "專員", "業務", "助理", "其他", "不方便提供"))               
    
        category_C = st.selectbox("應用程式顯示的資訊，請問您對哪種 EMDN 分類的醫療器材特別感興趣搜尋?", list(emdn_C_part)) # set index to none means there is no default options
        group_C = emdn_C_part.groupby(by=[category_C], as_index=False).sum() # Group the EMDN code type based on the specific category chosen
        type_C = st.selectbox("請問您對哪種 EMDN 類型的醫療器材特別感興趣搜尋?", list(group_C.iloc[:,0]))
        category_C_all = st.selectbox("Which EMDN code category of medical device are you interested in searching for in the future?", list(emdn_C_all)) # set index to none means there is no default options
        group_C_all = emdn_C_all.groupby(by=[category_C_all], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_C_all = st.selectbox("Which EMDN code type of medical device are you interested in searching for in the future?", list(group_C_all.iloc[:,0]))

        information_C = st.selectbox("請問您對本網站所提供的整體醫材資訊評價如何？", ("","1: 非常適當和明確", "2: 適當和明確", "3: 普通", "4: 不適當和不明確", "5: 非常不適當和不明確"))
        experience_C = st.selectbox("請問您對使用監管決策網站的優勢有何評價？", ("","1: 非常有幫助和有意義", "2: 有幫助和有意義", "3: 普通", "4: 無幫助和無意義", "5: 非常無幫助和無意義"))
        others_C = st.text_area("請問您希望在此頁面上看到哪些其他資訊？")
        feedback_C = st.text_area("請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？")
        submit_C = st.button(label="提交")
        
        if submit_C == True: # if the submit button is pressed
            st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")      
            sheet_C = client.open_by_url(url).worksheet('調查')  # Access the Google Sheet
            data_C = [day_C,background_C,role_C,category_C,type_C,category_C_all,type_C_all,information_C,experience_C,others_C,feedback_C] # Read data from the user input
            sheet_C.append_row(data_C) # Append data to the Google sheet    
            
     

    
#---------------------------------#
def Analysis(): # Plotting and data visualisation to analyse user experience survey result
    st.header(" :bar_chart: Data Analysis 數據分析")
    st.markdown("""
                Thank you so much for participating in this research. The data plotting and visualisation shown are according to user experience survey results, which separate information from English and Mandarin for statistical analysis. Please note that the data illustrated is only for personal review because some related information may be incorrect. :blush:
                
                非常感謝您參與這項研究。所顯示的數據圖表和視覺化是根據使用者體驗調查結果，其英文和中文的資料分別進行統計分析。請注意，所示數據僅供個人參考，因為某些相關資訊可能不正確。:blush:
                """)
    
    url = "https://docs.google.com/spreadsheets/d/1S3lA6Hk_N4bldzq4jKRTIS_R-7F7AL_zz9ZE76JDzV4" # The Google sheet url
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes=["https://www.googleapis.com/auth/spreadsheets"]) # Set up Google API credentials
    client = gspread.authorize(creds)
    
    sheet_E = client.open_by_url(url).worksheet("survey") # the survey in English
    data_E = sheet_E.get_all_values()
    data_E = pd.DataFrame(data_E[1:], columns=data_E[0])
    
    sheet_C = client.open_by_url(url).worksheet("調查") # the survey in Mandarin
    data_C = sheet_C.get_all_values()
    data_C = pd.DataFrame(data_C[1:], columns=data_C[0])

    Counts, Analysis, 數量, 分析 = st.tabs(["Counts", "Analysis", "數量", "分析"])

    with Counts: # User select the x-axis to plot the counts
        xvalue_E = st.selectbox("Please select X-Axis value to calculate the total values", options=data_E.columns[1:7])
        count_E = data_E[xvalue_E].value_counts().reset_index()
        fig_E = px.bar(data_E, x=xvalue_E, title="Bar chart: {} distribution".format(xvalue_E)) # Show the distribution of x-axis across all species
        st.plotly_chart(fig_E)
        fig2_E = px.pie(count_E, values=xvalue_E, names="index", title="Pie chart: {} distribution".format(xvalue_E)) # Display the distribution of species in the data
        st.plotly_chart(fig2_E)
        
        expander_E = st.expander("Count Results")
        data1_E = data_E[[xvalue_E]].groupby(xvalue_E).value_counts().sum()
        data2_E = data_E[[xvalue_E]].groupby(xvalue_E).value_counts()
        expander_E.write(data1_E)
        expander_E.write(data2_E)

    with Analysis: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_E = st.selectbox("Please select X-Axis value", options=data_E.columns[0:7])
        yaxis_E = st.selectbox("Please select Y-Axis value", options=data_E.columns[1:7])
        plot_E = px.scatter(data_E, x=xaxis_E, y=yaxis_E, title="Scatter plot: the searched {} by {}".format(yaxis_E,xaxis_E)) # visualize the relationship between x-axis and y-axis 
        color_E = st.color_picker("Please select the plot color") # user select the particular color                
        plot_E.update_traces(marker=dict(color=color_E)) # Update the plot color after the user chosen 
        st.plotly_chart(plot_E) # Display the data
        plot2_E = px.box(data_E, x=xaxis_E, y=yaxis_E, title="Box plot: The searched {} by {}".format(yaxis_E,xaxis_E)) # visualize the distribution of y-axis for each x-axis using a box plot
        plot2_E.update_traces(marker=dict(color=color_E))
        st.plotly_chart(plot2_E)

        expander2_E = st.expander("Analysis Results")
        data3_E = data_E[[xaxis_E, yaxis_E]].groupby(by=xaxis_E)[yaxis_E].value_counts().sum()
        data4_E = data_E[[xaxis_E, yaxis_E]].groupby(by=xaxis_E)[yaxis_E].sum()
        expander2_E.write(data3_E)
        expander2_E.write(data4_E)
    
    with 數量: # User select the x-axis to plot the counts  
        xvalue_C = st.selectbox("請選擇X軸值來計算總數量", options=data_C.columns[1:7])
        count_C = data_C[xvalue_C].value_counts().reset_index()
        fig_C = px.bar(data_C, x=xvalue_C, title="長條圖: {}分佈".format(xvalue_C)) # Show the distribution of x-axis across all species
        st.plotly_chart(fig_C)
        fig2_C = px.pie(count_C, values=xvalue_C, names="index", title="圓餅圖: {}分佈".format(xvalue_C)) # Display the distribution of species in the data
        st.plotly_chart(fig2_C)
        
        expander_C = st.expander("計算結果")
        data1_C = data_C[[xvalue_C]].groupby(by=xvalue_C).value_counts().sum()
        data2_C = data_C[[xvalue_C]].groupby(by=xvalue_C).value_counts()
        expander_C.write(data1_C)
        expander_C.write(data2_C)

    with 分析: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_C = st.selectbox("請選擇X軸值", options=data_C.columns[0:7])
        yaxis_C = st.selectbox("請選擇Y軸值", options=data_C.columns[1:7])        
        plot_C = px.scatter(data_C, x=xaxis_C, y=yaxis_C, title="散佈圖: 依照{}搜尋{}".format(yaxis_C,xaxis_C))
        st.plotly_chart(plot_C) # Display the data
        plot2_C = px.box(data_C, x=xaxis_C, y=yaxis_C, title="箱形圖: 依照{}搜尋{}".format(yaxis_C,xaxis_C)) # visualize the distribution of y-axis for each x-axis using a box plot
        st.plotly_chart(plot2_C)
        
        expander2_C = st.expander("分析結果")
        data3_C = data_C[[xaxis_C, yaxis_C]].groupby(by=xaxis_C)[yaxis_C].value_counts().sum()
        data4_C = data_C[[xaxis_C, yaxis_C]].groupby(by=xaxis_C)[yaxis_C].sum()
        expander2_C.write(data3_C)
        expander2_C.write(data4_C)



    
#---------------------------------#
# Create the sidebar for choosing the specific page
options = st.sidebar.radio("Pages", options=[":stethoscope: Home", " :star2: GSPR", " :memo: Survey", " :bar_chart: Analysis"])

if options == ":stethoscope: Home":
    Home()
elif options == " :star2: GSPR":
    EMDN()
elif options == " :memo: Survey":
    Survey()
elif options == " :bar_chart: Analysis":
    Analysis()





