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




#---------------------------------#
# Create the Home page
def Home():
    st.title(" :stethoscope: Medical Device Regulatory Tool Application")

    st.markdown("""
                **Ethical Clearance Reference Number:**  MRSU-23/24-45195
                
                **Title of study:**  Design of a Medical Device Regulatory Tool Application
                
                **Invitation paragraph:**  I would like to invite you to participate in this research project which forms part of my dissertation research. Before you decide whether you want to take part, it is important for you to understand why the research is being done and what your participation will involve. Please take time to read the following information carefully and discuss it with others if you wish. Ask me if there is anything that is not clear or if you would like more information.

                **What is the purpose of the study?**  Thank you so much for taking the time to participate in this research for a postgraduate student dissertation. This study aims to design a regulatory tool to correctly filter and select the appropriate regulatory requirements that need to be met by medical devices. The specific objectives of this study are to assess usability of the prototype application and collect initial user experiences to understand the need for the tool and provide insight for improvements in future development.
                In more detail, this system briefly analyses the European Union (EU) regulation requirements with relative standards for medical devices from the European Medical Device Nomenclature (EMDN), which according to Annex I: general safety and performance requirements (GSPR) as listed in the Medical Device Regulation (MDR) (2017/745) as well as the In Vitro Diagnostic Medical Devices Regulation (IVDR) (2017/746).

                **Why have I been invited to take part?**  You are being invited to participate in this study because you are interested in medical device development, e.g. through academic study or are working in the healthcare industry.

                **What will happen if I take part?**  If you agree to take part, you will test this tool application, complete a survey anonymously, and interact with data analysis. This system will provide a few available EMDN code categories and groups for users to search for. The selected device would return relative standards and EMDN device types according to the GSPR rules. The process will take you approximately 3~5 minutes to complete.   

                **Do I have to take part?**  Participation is completely voluntary. You should only take part if you want to and choosing not to take part will not disadvantage you in anyway. If you choose to take part you will be asked to provide your consent. To do this you will be asked to indicate that you have read and understand the information provided and that you consent to your anonymous data being used for the purposes explained. You are free to withdraw at any point during completion of the survey, without having to give a reason. Withdrawing from the study will not affect you in any way. Once you submit the survey, it will no longer be possible to withdraw from the study because the data will be fully anonymous. Please do not include any personal identifiable information in your responses.

                **Data handling and confidentiality:**  This research is anonymous. This means that nobody, including the researchers, will be aware of your identity, and that nobody will be able to connect you to the answers you provide, even indirectly. Your answers will nevertheless be treated confidentially and the information you provide will not allow you to be identified in any research outputs/publications. Your data will be held securely on password-protected devices with limited access by the researcher. After the completion of the research, the data will be securely destroyed or archived as per ethical guidelines.

                **What will happen to the results of the study?**  The results of the study will be summarised in the dissertation of MSc Healthcare Technologies as part of postgraduate research. All the research data will be anonymous data, and it will not be shared with any third parties or made publicially available.

                **Who should I contact for further information?**  If you have any questions or require more information about this research, please use the following contact details: Yen-Hua Ho (yen-hua.ho@kcl.ac.uk)

                **What if I have further questions, or if something goes wrong?**  If this study has harmed you in any way or if you wish to make a complaint about the conduct of the study you can contact King's College London using the details below for further advice and information: Yen-Hua Ho (yen-hua.ho@kcl.ac.uk), Dr. Clare Heaysman (clare.heaysman@kcl.ac.uk) 

                Please be aware that all information this system provides is for reference only, as regulations are updated frequently and the database may delay follow-up. Thank you for reading this information sheet and for considering taking part in this research. 🔎
                """)
    
    st.markdown("""
                
                **研究主題：**  醫療器材監管工具應用的設計

                **邀請段落：**  本人誠摯地邀請您參與這個研究項目，這是我碩士學位研究的一部分。在您決定是否參與之前，了解研究的目的及參與的內容是非常重要的。請您仔細閱讀以下信息，如果您願意也可以與他人討論，若有任何不明之處或需要更多信息，請隨時向我詢問。

                **研究目的？**  非常感謝您抽出寶貴時間參與這項碩士生論文研究。本研究旨在設計一種監管工具，以正確過濾和選擇醫療器材所需滿足的適當監管要求。具體目標是評估應用程式的可用性並收集初始使用者體驗，以了解該工具的需求並為未來開發的改進提供見解。
                該系統根據歐洲醫療器材命名法(EMDN)所提及的醫療器材，簡要分析了歐盟(EU)法規要求的相關標準。而歐盟法規來源於參考醫療器材法規(MDR)(2017/745)、以及體外診斷醫療器材法規(IVDR)(2017/746)中，其中附件一的一般安全和性能要求(GSPR)所列出內容。
                
                **為什麼邀請我參加？**  邀請您參與這項研究是因為您對醫療設備發展感興趣，例如透過學術學習或在醫療產業工作。
                
                **若參加會發生什麼？**  如果您同意參與，您將測試此工具應用系統、匿名完成調查問卷、並與資料分析進行互動，花費時間約需3~5分鐘完成。

                **我必須參加嗎？**  參與完全是自願的，選擇不參加不會對您造成任何不利影響。如果您選擇參加，您將被要求表明您已閱讀並理解所提供的訊息，並同意您的匿名數據用於上述研究目的。在填寫問卷期間，您可以隨時退出，不需要提供理由。退出研究不會對您造成任何影響。一旦您提交問卷，由於數據是完全匿名的，將無法撤回參與。請不要在您的回答中包含任何可識別您的個人資訊。

                **數據處理和保密性：**  這項研究是匿名的。這意味著包括研究人員在內，沒有人會知道您的身份，也沒有人能夠間接地將您與您提供的答案聯繫起來。您的回答將被保密處理，您提供的訊息不會使您在任何研究成果或出版物中被識別，且您的數據將被安全地保存。
                
                **研究結果會如何處理？**  研究結果僅會發表在醫療保健技術碩士學位論文中進行總結，所有研究資料皆為匿名數據，不會與任何第三方分享或公開提供。
                
                **應該聯繫誰以獲得更多資訊？**  如果您對於本研究有任何疑問或需要更多信息，請透過以下聯繫方式：Yen-Hua Ho (yen-hua.ho@kcl.ac.uk)

                **如果我有進一步的問題，或者出了問題怎麼辦？**  如果這項研究以任何方式對您造成了傷害，或者如果您希望對研究提出投訴，您可以使用以下詳細資訊聯繫倫敦國王學院以獲取進一步的建議和訊息：Yen-Hua Ho (yen-hua.ho@kcl.ac.uk), Dr. Clare Heaysman (clare.heaysman@kcl.ac.uk)
                
                請注意，本系統提供的所有資訊僅供參考，因法規日益更新而資料庫可能延遲跟進。最後感謝您閱讀此資訊並考慮參與這項研究 🔎
                """)




#---------------------------------#
# Load excel data
excel_E = pd.ExcelFile('GSPRen.xlsx') # Load the excel data in English
emdn_E = pd.read_excel(excel_E, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN
emdn_E_all = emdn_E.iloc[:29] # Selecting all row from header 2 to row 27
emdn_E_part = pd.read_excel(excel_E, sheet_name='EMDN', na_filter=False, usecols="A:F", header=34) # Load excel worksheet of EMDN
emdn_E_part = emdn_E_part.iloc[::] # Selecting all row from 34 to all row

excel_C = pd.ExcelFile('GSPRcn.xlsx') # Load the excel data in Mandarin
emdn_C = pd.read_excel(excel_C, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN
emdn_C_all = emdn_C.iloc[:29] # Selecting all row from header 2 to row 27
emdn_C_part = pd.read_excel(excel_C, sheet_name='EMDN', na_filter=False, usecols="A:F", header=34) # Load excel worksheet of EMDN
emdn_C_part = emdn_C_part.iloc[::] # Selecting all row from 34 to all row


def EMDN(): # Create the EMDN page
    st.header(" :star2:  General Safety and Performance Requirements 一般安全和性能要求")
    st.markdown("""
                Thank you so much for testing the system function. The table below shows each EMDN code category and group corresponds with specific medical device data. Please select English or Mandarin to offer the EMDN code you would like to search for; then, the system will load the related information immediately. 
                
                非常感謝您測試本系統的功能。下表顯示了每個 EMDN 代碼類別和類群對應特定的醫療器材資料。請選擇英文或中文給予預計搜尋之 EMDN 代碼；然後，系統會立即載入相關資訊供您參考。
                """)

    st.image('image_flowchart.png') # The flowchart introduces how to operate this website
    
    col1, col2 = st.tabs(["EMDN code","EMDN 代碼"])

    with col1:  # Create the EMDN page in English
        st.header("EMDN code")
        st.markdown("""
                    **EMDN:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)
                    Shown is the European Medical Device Nomenclature (EMDN) structure, which characterizes medical device information into different levels
                    """)
        st.dataframe(emdn_E_all) # Display the all EMDN code strature

        st.write("""Due to project time limitations, only a few medical devices of the EMDN code are available to search on the application""")
        category_E = st.selectbox("Please select the EMDN code category", list(emdn_E_part)) # List the EMDN code category, and user can only search a few medical device
        groupby_E = emdn_E_part.groupby(by=[category_E], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        group_E = st.selectbox("Please select the EMDN code group", list(groupby_E.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 
        
        if st.button("Search"): # Set up the button
                st.success("Please wait a few minutes; the page turns on medical device: {} information".format(group_E))
                group_E = group_E.split()[0]  # Split the string of EMDN type into a list and return the first element, which has the same name as the Excel worksheet
                GSPR_E(group_E) # The EMDN type will retun to the GSPR_E function
            # try:
            #     st.success("Please wait a few minutes; the page turns on medical device: {} information".format(group_E))
            #     group_E = group_E.split()[0]  # Split the string of EMDN type into a list and return the first element, which has the same name as the Excel worksheet
            #     GSPR_E(group_E) # The EMDN type will retun to the GSPR_E function
            # except:
            #     st.error('The medical device information is unavailable for search; please select another EMDN code group', icon="🚨")
            

    with col2:  # Create the EMDN page in Mandarin
        st.header("EMDN 代碼")
        st.markdown("""
                    **歐洲醫療器材命名法:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)
                    表格所示為歐洲醫療器材命名法(EMDN)結構，該結構將醫療器材劃分為不同種類
                    """)
        st.dataframe(emdn_C_all) # Display the EMDN code data in Mandarin

        st.write("""由於專案時間限制，目前該應用程式只能搜尋少數 EMDN 代碼的醫療器材資訊""")
        category_C = st.selectbox("請選擇 EMDN 代碼類別", list(emdn_C_part)) # List the EMDN code category
        groupby_C = emdn_C_part.groupby(by=[category_C], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        group_C = st.selectbox("請選擇 EMDN 代碼類群", list(groupby_C.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 
        
        if st.button("搜尋"): # Set up the button
            try:
                st.success("請稍等幾分鐘；頁面將開啟: {}的醫療器材資訊".format(group_C))
                group_C = group_C.split()[0]  # Split the string of EMDN type into a list and return the first element, which has the same name as the Excel worksheet
                GSPR_C(group_C)
            except:
                st.error('該醫療器材資訊目前無法檢索；請選擇其他 EMDN 代碼類群', icon="🚨")



def GSPR_E(group_E):  # Create the GSPR page in English
    st.markdown("""
                **MDR:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745) 
                **IVDR:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                The output medical device information can be searched, fullscreen, and downloaded as a Microsoft Excel file for personal records and edits
                """)

    # Set up different tabs
    ChapterI, ChapterII, ChapterIII, List, Example = st.tabs(["Chapter I", "Chapter II", "Chapter III", "Standard(s) & Device(s)", "Example"])
    
    with ChapterI: # Get Chapter I General requirements details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=group_E, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_E = pd.read_excel(excel_E, sheet_name=group_E, na_filter=False, usecols="A:D", header=2) # replace NaN as blank, read the columns from A to C to get English details, and the header is 2nd row of excel
        chapterI_E = chapterI_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_E = chapterI_E.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_E)
    
    with ChapterII: # Get Chapter II Requirements regarding design and manufacture details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=group_E, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_E = pd.read_excel(excel_E, sheet_name=group_E, na_filter=False, usecols="A:D", header=26)
        chapterII_E = chapterII_E.replace("\n", ", ", regex=True) 
        chapterII_E = chapterII_E.iloc[:141] # Selecting all row from header 26 to row 141
        st.dataframe(chapterII_E)

    with ChapterIII: # Get Chapter III Requirements regarding the information supplied with the device details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=group_E, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_E = pd.read_excel(excel_E, sheet_name=group_E, na_filter=False, usecols="A:D", header=169)
        chapterIII_E = chapterIII_E.replace("\n", ", ", regex=True) 
        chapterIII_E = chapterIII_E.iloc[:265]
        st.dataframe(chapterIII_E)

    with List: # Get Standard details in English
        st.subheader("Standard(s) list")
        st.markdown("""
                    **ISO:** [International Organization for Standardization](https://www.iso.org/home.html)
                    **IEC:** [International Electrotechnical Commission](https://www.iec.ch/homepage)
                    **IMDRF:** [International Medical Device Regulators Forum](https://www.imdrf.org/)
                    **CEN and CENELEC:** [European Committee for Standardisation and European Committee for Electrotechnical Standardisation](https://www.cencenelec.eu/)
                    """)
        standards_E = pd.read_excel(excel_E, sheet_name=group_E, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_E = standards_E.iloc[:40]
        st.dataframe(standards_E)

        st.subheader("Medical device(s) list")
        st.markdown("""The relevant medical devices under the EMDN structure""")
        devices_E = pd.read_excel(excel_E, sheet_name=group_E, na_filter = False, usecols="I", header=2) # replace NaN as blank
        devices_E = devices_E.iloc[:50]
        st.dataframe(devices_E)

    with Example:
        st.subheader("Example template")
        st.markdown("""
                    **MDCG 2021-08:** [Checklist of general safety and performance requirements, Standards, common specifications and scientific advice](https://ec.europa.eu/health/sites/default/files/md_sector/docs/mdcg_2021-8_annex6.docx)
                    1. Please click the link to download the template.
                    2. Please confirm the applied medical device(s) comply with :blue-background[EU MDR] or :blue-background[EU IVDR].
                    3. Please change the general safety and performance requirements (GSPR) information if the device(s) follow IVDR since the template uses MDR content. 
                    4. Please review the device(s) information in the chapter I, II, and III tabs to support you complete the form appropriately. 
                    """)
        st.image('imageA.jpg', caption='A. Standards, common specifications, scientific advice')
        st.image('imageB_example.png', caption='Example: B. Matrix of General safety and performance requirements')
        st.image('imageB_description.png', caption='Description: B. Matrix of General safety and performance requirements')


def GSPR_C(group_C):  # Create the GSPR page in Mandarin
    st.markdown("""
                * **醫療器材法規:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **體外診斷醫療器材法規:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                所顯示的醫療器材資訊結果可以搜尋、全螢幕顯示，也可以下載為Microsoft Excel檔案，以供個人後續記錄和編輯
                """)
    
    #Set up different tabs
    第一章, 第二章, 第三章, 清單, 參考範例 = st.tabs(["第一章", "第二章", "第三章", "標準和醫材清單", "參考範例"])

    with 第一章: # Get Chapter I General requirements details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=group_C, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_C = pd.read_excel(excel_C, sheet_name=group_C, na_filter=False, usecols="A:D", header=2)  # replace NaN as blank, read the columns from E to G to get Chinese details, and the header is 2nd row of excel
        chapterI_C = chapterI_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_C = chapterI_C.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_C)

    with 第二章: # Get Chapter II Requirements regarding design and manufacture details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=group_C, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_C = pd.read_excel(excel_C, sheet_name=group_C, na_filter=False, usecols="A:D", header=26)
        chapterII_C = chapterII_C.replace("\n", ", ", regex=True) 
        chapterII_C = chapterII_C.iloc[:141]
        st.dataframe(chapterII_C)

    with 第三章: # Get Chapter III Requirements regarding the information supplied with the device details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=group_C, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_C = pd.read_excel(excel_C, sheet_name=group_C, na_filter=False, usecols="A:D", header=169)
        chapterIII_C = chapterIII_C.replace("\n", ", ", regex=True) 
        chapterIII_C = chapterIII_C.iloc[:265]
        st.dataframe(chapterIII_C)

    with 清單: # Get Standard details in Mandarin
        st.subheader("標準清單")
        st.markdown("""
                    **ISO:** [International Organization for Standardization](https://www.iso.org/home.html)
                    **IEC:** [International Electrotechnical Commission](https://www.iec.ch/homepage)
                    **IMDRF:** [International Medical Device Regulators Forum](https://www.imdrf.org/)
                    **CEN and CENELEC:** [European Committee for Standardisation and European Committee for Electrotechnical Standardisation](https://www.cencenelec.eu/)
                    """)
        standards_C = pd.read_excel(excel_C, sheet_name=group_C, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_C = standards_C.iloc[:40]
        st.dataframe(standards_C)

        st.subheader("醫療器材清單")
        st.markdown("""在EMDN架構下的相關醫療器械""")
        devices_C = pd.read_excel(excel_C, sheet_name=group_C, na_filter = False, usecols="I", header=2) # replace NaN as blank
        devices_C = devices_C.iloc[:50]
        st.dataframe(devices_C)
    
        
    with 參考範例:
        st.subheader("參考範例")
        st.markdown("""
                    **MDCG 2021-08:** [Checklist of general safety and performance requirements, Standards, common specifications and scientific advice](https://ec.europa.eu/health/sites/default/files/md_sector/docs/mdcg_2021-8_annex6.docx)
                    1. 請點選連結下載模板
                    2. 請確認申請之醫療器材符合:blue-background[歐盟醫療器材法規] 或 :blue-background[歐盟體外診斷醫療器材法規]的要求
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
        background = st.selectbox("Please select your current background?", ("", "Academics", "Notified Body (NB)", "Contract Research Organization (CRO)", "Manufacturer", "Importer", "Distributor", "Wholesaler", "Other",))
        role = st.selectbox("Please select your current role?", ("", "Healthcare Professionals", "Professor", "Student", "Researcher", "Reviewer", "Manager", "Engineer", "Officer", "Sales Representative", "Assistant", "Other", "Prefer not to say"))

        category_E = st.selectbox("For the available searched information on the website, which EMDN code category of the medical device were you interested in reviewing?", list(emdn_E_part)) # set index to none means there is no default options
        groupby_E = emdn_E_part.groupby(by=[category_E], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        group_E = st.selectbox("For the available searched information on the website, which EMDN code group of the medical device were you interested in reviewing?", list(groupby_E.iloc[:,0])) 
        expectation = st.selectbox("Does the output medical device information on this tool system as you expect?", ("", "Yes", "No"))
        information = st.selectbox("How would you rate the provided device information on this tool application overall?", ("","1: Absolutely appropriate and clear", "2: Appropriate and clear", "3: Neutral", "4: Inappropriate and unclear", "5: Absolutely inappropriate and unclear"))
        experience = st.selectbox("How would you rate the benefits of having this regulation tool application?", ("","1: Extremely useful", "2: Useful", "3: Neutral", "4: Useless", "5: Extremely useless"))

        category_E_all = st.selectbox("Which EMDN code category of medical device are you particularly interested in searching for in the future?", list(emdn_E_all)) # set index to none means there is no default options
        groupby_E_all = emdn_E_all.groupby(by=[category_E_all], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        group_E_all = st.selectbox("Which EMDN code group of medical device are you particularly interested in searching for in the future?", list(groupby_E_all.iloc[:,0]))        
        
        others = st.text_area("What other information would you like to see on this tool application? (Optional)")
        feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve? (Optional)")
        submit = st.button(label="Submit")
        
        if submit == True: # if the submit button is pressed
            st.success("Successfully submitted. !! Thank you so much for your support !! ")       
            sheet = client.open_by_url(url).worksheet('survey')  # Access the Google Sheet
            data = [day,background,role,category_E,group_E,expectation,information,experience,category_E_all,group_E_all,others,feedback] # Read data from the user input
            sheet.append_row(data) # Append data to the Google sheet


    with col2:
        st.subheader("使用者體驗調查")
        day_C = st.text_input("日期", (datetime.date.today()), disabled=True)
        background_C = st.selectbox("請問您目前的背景？", ("", "學術單位", "驗證機構(NB)", "受託研究機構(CRO)", "製造商", "進口商", "經銷商", "其他",))
        role_C = st.selectbox("請問您目前的職位？", ("", "健康領域專業人士", "教授", "學生", "研究員", "審查員", "經理", "工程師", "專員", "業務", "助理", "其他", "不方便提供"))               
    
        category_C = st.selectbox("對於網站上可用的搜尋信息，請問您有興趣查看哪個醫療器材的EMDN代碼類別？", list(emdn_C_part)) # set index to none means there is no default options
        groupby_C = emdn_C_part.groupby(by=[category_C], as_index=False).sum() # Group the EMDN code type based on the specific category chosen
        group_C = st.selectbox("對於網站上可用的搜尋信息，請問您有興趣查看哪個醫療器材的EMDN代碼類群？", list(groupby_C.iloc[:,0]))
        expectation_C = st.selectbox("請問本網站系統輸出的醫療器材資訊內容是否符合您的預期？", ("", "是", "否"))
        information_C = st.selectbox("請問您對本網站所提供的整體醫材資訊評價如何？", ("","1: 非常適當和明確", "2: 適當和明確", "3: 普通", "4: 不適當和不明確", "5: 非常不適當和不明確"))
        experience_C = st.selectbox("請問您對使用監管應用網站的優勢有何評價？", ("","1: 非常有幫助", "2: 有幫助", "3: 普通", "4: 無幫助", "5: 非常無幫助"))

        category_C_all = st.selectbox("請問您未來特別感興趣搜尋哪種EMDN代碼類別的醫療器材？", list(emdn_C_all)) # set index to none means there is no default options
        groupby_C_all = emdn_C_all.groupby(by=[category_C_all], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        group_C_all = st.selectbox("請問您未來特別感興趣搜尋哪種EMDN代碼類群的醫療器材？", list(groupby_C_all.iloc[:,0]))
        
        others_C = st.text_area("請問您希望在此網站上看到哪些其他資訊？")
        feedback_C = st.text_area("請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？")
        submit_C = st.button(label="提交")
        
        if submit_C == True: # if the submit button is pressed
            st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")      
            sheet_C = client.open_by_url(url).worksheet('調查')  # Access the Google Sheet
            data_C = [day_C,background_C,role_C,category_C,group_C,expectation_C,information_C,experience_C,category_C_all,group_C_all,others_C,feedback_C] # Read data from the user input
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
        xvalue_E = st.selectbox("Please select X-Axis value to calculate the total values", options=data_E.columns[0:5])
        count_E = data_E[xvalue_E].value_counts().reset_index()
        # fig_E = px.bar(data_E, x=xvalue_E, title="Bar chart: {} distribution".format(xvalue_E)) # Show the distribution of x-axis across all species
        # st.plotly_chart(fig_E)
        fig2_E = px.pie(count_E, values=xvalue_E, names="index", title="Pie chart: {} distribution".format(xvalue_E)) # Display the distribution of species in the data
        st.plotly_chart(fig2_E)
        
        expander_E = st.expander("Count Results")
        data1_E = data_E[[xvalue_E]].groupby(xvalue_E).value_counts().sum()
        data2_E = data_E[[xvalue_E]].groupby(xvalue_E).value_counts()
        expander_E.write(data1_E)
        expander_E.write(data2_E)

    with Analysis: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_E = st.selectbox("Please select X-Axis value", options=data_E.columns[0:5])
        yaxis_E = st.selectbox("Please select Y-Axis value", options=data_E.columns[1:5])
        plot_E = px.scatter(data_E, x=xaxis_E, y=yaxis_E, title="Scatter plot: the searched {} by {}".format(yaxis_E,xaxis_E)) # visualize the relationship between x-axis and y-axis 
        color_E = st.color_picker("Please select the plot color") # user select the particular color                
        plot_E.update_traces(marker=dict(color=color_E)) # Update the plot color after the user chosen 
        st.plotly_chart(plot_E) # Display the data
        # plot2_E = px.box(data_E, x=xaxis_E, y=yaxis_E, title="Box plot: The searched {} by {}".format(yaxis_E,xaxis_E)) # visualize the distribution of y-axis for each x-axis using a box plot
        # plot2_E.update_traces(marker=dict(color=color_E))
        # st.plotly_chart(plot2_E)

        expander2_E = st.expander("Analysis Results")
        data3_E = data_E[[xaxis_E, yaxis_E]].groupby(by=xaxis_E)[yaxis_E].value_counts().sum()
        data4_E = data_E[[xaxis_E, yaxis_E]].groupby(by=xaxis_E)[yaxis_E].sum()
        expander2_E.write(data3_E)
        expander2_E.write(data4_E)
    
    with 數量: # User select the x-axis to plot the counts  
        xvalue_C = st.selectbox("請選擇X軸值來計算總數量", options=data_C.columns[0:5])
        count_C = data_C[xvalue_C].value_counts().reset_index()
        # fig_C = px.bar(data_C, x=xvalue_C, title="長條圖: {}分佈".format(xvalue_C)) # Show the distribution of x-axis across all species
        # st.plotly_chart(fig_C)
        fig2_C = px.pie(count_C, values=xvalue_C, names="index", title="圓餅圖: {}分佈".format(xvalue_C)) # Display the distribution of species in the data
        st.plotly_chart(fig2_C)
        
        expander_C = st.expander("計算結果")
        data1_C = data_C[[xvalue_C]].groupby(by=xvalue_C).value_counts().sum()
        data2_C = data_C[[xvalue_C]].groupby(by=xvalue_C).value_counts()
        expander_C.write(data1_C)
        expander_C.write(data2_C)

    with 分析: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_C = st.selectbox("請選擇X軸值", options=data_C.columns[0:5])
        yaxis_C = st.selectbox("請選擇Y軸值", options=data_C.columns[1:5])        
        plot_C = px.scatter(data_C, x=xaxis_C, y=yaxis_C, title="散佈圖: 依照{}搜尋{}".format(yaxis_C,xaxis_C))
        st.plotly_chart(plot_C) # Display the data
        # plot2_C = px.box(data_C, x=xaxis_C, y=yaxis_C, title="箱形圖: 依照{}搜尋{}".format(yaxis_C,xaxis_C)) # visualize the distribution of y-axis for each x-axis using a box plot
        # st.plotly_chart(plot2_C)
        
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





