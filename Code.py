import streamlit as st
import pandas as pd
import numpy as np
import hydralit as hy
import hydralit_components as hc
import re
import spacy
from streamlit_lottie import st_lottie
import requests
import ast
import pyarabic.araby as araby
from farasa.stemmer import FarasaStemmer
from tashaphyne.stemming import ArabicLightStemmer
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem import PorterStemmer

# Loading Dataset
df = pd.read_excel("Quran.xlsx")
references_df = pd.read_excel("References.xlsx")

# converting to string
df["Arabic Verse"] = df["Arabic Verse"].astype(str)
df['Chapter Title'] = df['Chapter Title'].astype(str)
df['Arabic Chapter Title'] = df['Arabic Chapter Title'].astype(str)
df['Concept'] = df['Concept'].astype(str)
df['Arabic Concept'] = df['Arabic Concept'].astype(str)
df['Link to Environment'] = df['Link to Environment'].fillna('no explanation')
df['Link to Environment in Arabic'] = df['Link to Environment in Arabic'].fillna('لا يوجد')
df['Reference'] = df['Reference'].fillna('no source')
df['Arabic Reference'] = df['Arabic Reference'].fillna('لا يوجد')

# removing whitespaces
df["Arabic Verse"] = df["Arabic Verse"].apply(lambda x: x.strip())
df["Chapter Title"] = df["Chapter Title"].apply(lambda x: x.strip())
df["Arabic Chapter Title"] = df["Arabic Chapter Title"].apply(lambda x: x.strip())
df["Concept"] = df["Concept"].apply(lambda x: x.strip())
df["Arabic Concept"] = df["Arabic Concept"].apply(lambda x: x.strip())
df["English Keyword"] = df["English Keyword"].astype(str).apply(lambda x: " ".join([word for word in x.split(" ") if word not in STOP_WORDS]))

# converting to numeric
pd.to_numeric(df["Chapter Nb."], downcast="integer")
pd.to_numeric(df["Verse Nb."], downcast="integer")


# Function for making spaces
def space(n,element=st): # n: number of lines
    for i in range(n):
        element.write("")

# Funtion for drawing a line
def draw_line(height="3px", color="#006400", bg_color="#006400"):
  st.markdown(f"""<hr style="height:{height};border:none;color:{color};background-color:{bg_color};" /> """, unsafe_allow_html=True)

# Display lottie animations
def load_lottieurl(url):
  # get the url
  r = requests.get(url)
  # if error 200 raised return Nothing
  if r.status_code !=200:
    return None
  return r.json()

# Load css style file from local disk
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

# Load css style from url
def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',unsafe_allow_html = True)

# Function to draw the footer of the pages
def footer():
    # Load css style
    local_css('footer_style.txt')
    st.markdown("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Untitled</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="footer-dark">
        <footer>
            <div class="container">
                <div class="row">
                    <div class="col-md-6 item text">
                        <h3>AUB NATURE CONSERVATION CENTER (AUB-NCC)</h3>
                        <p style="line-height: 2">
                        ​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​The AUB Nature Conservation Center (AUB-NCC) is the leading​ transdisciplinary academic center addressing nature conservation in the MENA region. 
                        <br><br>Aims to promote the conservation and sustainable use of biodiversity and enable 
                        people to become the guardians and beneficiaries of their own natural heritage. ​
                        ​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​</p>
                    </div>
                    <div class="col-md-1 item text">
                    </div>
                    <div class="col-md-5 item text">
                        <h3>FIND US</h3>
                        <ul>
                           <li><a href="tel:+9611350000" target="_blank">Phone Number: +961-1-350000 ext. 2699</a></li>
                            <li><p><br>P.O. Box 11-0236 / AUB </p></li>
                            <li><br><a href="https://maps.app.goo.gl/11twoobQS1VzuDcc8" target="_blank">Address: AUB Mary Dodge Hall, Riad El Solh, Beirut 1107 2020, Lebanon</a></li>
                        </ul>
                    </div>
                    <div class="col item social"><a href="https://www.aub.edu.lb/natureconservation/Pages/default.aspx" target="_blank"><i class="icon ion-social-google"></i></a><a href="https://www.facebook.com/aubncc" target="_blank"><i class="icon ion-social-facebook"></i></a><a href="https://twitter.com/aubncc" target="_blank"><i class="icon ion-social-twitter"></i></a><a href="https://www.instagram.com/aubncc/" target="_blank"><i class="icon ion-social-instagram"></i></a></div>
                </div>
                <p class="copyright">AUB NATURE CONSERVATION CENTER (AUB-NCC)</p>
            </div>
        </footer>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/js/bootstrap.bundle.min.js"></script>
</body>
</html>
<br>
<p style="text-align: right;"><i class="fa fa-circle" style="font-size:13px;color:#60cc60; margin-right:5px"></i><em> Powered by <a style="color: #C00000" href="https://www.aub.edu.lb/osb/MSBA/Pages/default.aspx" target="_blank">
<b>MSBA</font></b></em></a></p>
""", unsafe_allow_html=True)



# KPI Card
def kpi_card(streamlit_element, icon, title, text):
    # Load css style
    local_css('kpi_card_style.txt')
    streamlit_element.markdown(f"""
        <html>
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <title>Card Hover Effect</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" type="text/css" media="screen" href="style.css" />
            <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN"
            crossorigin="anonymous">
        </head>
        <body>
        <div class="container">
                <div class="card">
                <div class="slide slide1">
                    <div class="content">
                        <div class="icon">
                        <i class="material-icons" aria-hidden="true">{icon}</i>
                        </div>
                    </div>
                </div>
            <div class="slide slide2">
                <div class="content">
                <h3>
                {title}
                </h3>
                <p>{text}</p>
            </div>
            </div>
            </div>
            </div>
            </body>
            </html>""", unsafe_allow_html = True)

# About Card
def about_card(title1,title2,title3,text1,text2,text3_points_list):
    local_css("about_card_style.txt")
    st.markdown(f"""
    <div class="container">
  <div class="box">
    <span></span>
    <div class="content">
      <h2>{title1}</h2>
      <p>{text1}</p>
    </div>
  </div>
  <div class="box">
    <span></span>
    <div class="content">
      <h2>{title2}</h2>
      <p>{text2}</p>
    </div>
  </div>
  <div class="box">
    <span></span>
    <div class="content">
      <h2>{title3}</h2>
      <ul>
      <li>{text3_points_list[0]}</li><br>
      <li>{text3_points_list[1]}</li>
      </ul>
    </div>
  </div>
</div>
    """, unsafe_allow_html=True)

# info card
def ar_info_card(title, content, icon):
      st.markdown(f"""<p dir="rtl" style="color:#2A4657; font-size: 28px; text-align: right ;background-color:#f0f2f6; padding: 0.5em;height:auto"><b>{title}</b>
    <i class="fa fa-{icon}" style="float: left; align: left; font-size:42px;color:#006400"></i>
    <br><br><font color="#006400">{content}</p>
    """, unsafe_allow_html=True)

# Setting page layout
st.set_page_config(layout='wide', page_icon = "https://icon-library.com/images/environment-icon-png/environment-icon-png-3.jpg", page_title = "Islam and the Environment")

# hide streamlit features
# hide_streamlit_style = """
#                 <style>
#                 div[data-testid="stToolbar"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 div[data-testid="stDecoration"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 div[data-testid="stStatusWidget"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 #MainMenu {
#                 visibility: hidden;
#                 height: 0%;
#                 }
#                 header {
#                 visibility: hidden;
#                 height: 0%;
#                 }
#                 </style>
#                 """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# specify the primary menu definition
menu_data = [
    {'id':"Environmental Search",'icon': "fa fa-search", 'label':"Environmental Search",'ttip':"Environmental Search"},
    {'id':"General Search",'icon': "fa fa-search", 'label':"General Search",'ttip':"General Search"},
    {'id':"References",'icon': "fa fa-table", 'label':"References",'ttip':"References"},
    {'id':"Contact Us",'icon': "fa fa-user-circle", 'label':"Contact Us",'ttip':"Contact Us"}]

over_theme = {'txc_inactive': 'white','menu_background':'#006400'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    hide_streamlit_markers=False,
    sticky_nav=True, #at the top or not
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
)

# Home Page
if menu_id=='Home':
  col1,col2,col3 = st.columns([1.2,0.5,1])

  col1.image("logo.png", width=300)
  # Title
  col1.markdown("""<h1 style="font-size:56px;"><b>Islam and the  <font color="#006400">Environment</font></b></h1>""", unsafe_allow_html=True)
  
  # adjusting the format of the clickable links
  #local_css("link_style.txt")  

  # Caption under the title
  col1.markdown("""<h1 style="font-size:20px; color:rgb(49, 51, 63); line-height: 1.5; font-weight: 505">
    an initiative by the <a  style="color: #006400" href="https://www.aub.edu.lb/natureconservation/Pages/default.aspx" target="_blank"><b>Nature Conservation Center (AUB-NCC)</a> with the support of the 
    <a style="color: #006400" href="https://www.aub.edu.lb/fas/zayed/Pages/default.aspx" target="_blank"><b>Sheikh Zayed Chair for Arabic and Islamic Studies</a>
    and <a style="color: #006400" href="https://www.aub.edu.lb/osb/MSBA/Pages/default.aspx" target="_blank"><b>MSc in Business Analytics Program (MSBA)</a> at the American University of Beirut
   </h1>
   """, unsafe_allow_html=True)

  space(4,col3)

  # The main image in the home page
  col3.image("quran_tree.png")

  space(9)
  draw_line()

  # About title
  st.markdown("""<h1 style="font-size:35px; color:#006400; font-family: Myriad pro Semibold">About</h1>""", unsafe_allow_html=True)

  # number of of verses related to environment
  env_verses_count = len(df['Arabic Verse'].unique())

  # number of of environmental concepts
  env_concepts_count = len(df['Concept'].unique())

  # Text under the about part
  st.markdown(f"""<p style="font-size: 20px; color:rgb(49, 51, 63); line-height: 1.5; font-weight: 505;">
  Starting from the scriptural authority of the Quran, Muslims will discern the importance of protecting the environment, where approximately {env_verses_count} verses discuss environmental elements.</p>""",
    unsafe_allow_html=True)
  
  space(2)

  # Cards of the about part showing some info about the website
  about_card(
  title1= "Islam and the Environment",
  title2= "Goals",
  title3= "Services",
  text1= "This project will survey the deep and long-standing connections between Islamic teachings and environmentalism, the results of which are shared in this application. Subsequently, it will strengthen the connection between Islam and modern Muslim Communities and the environment through interpreting scriptures, raising awareness, and promoting policies.",
  text2 = "Conveying the environmental elements found in the verses of the Quran through an application that is easy to navigate",
  text3_points_list=["Searching the Quran by environmental topics, then presenting the association of each resulted verse with the environment",
    "Searching the Quran using general words and phrases while presenting the association with the environment"]
    )

  space(6)
  draw_line()

  space(6)
  col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

  # Cards showing some stats of the results
  kpi_card(col2, 'book', 'Quran Verses', 6236)
  kpi_card(col4, 'spa', 'Environmental Verses', env_verses_count)
  kpi_card(col6, "search", "Environmental Concepts Covered", env_concepts_count)
  space(6)
  
  # Footer of the page
  footer()

# Environmental Search 
if menu_id=='Environmental Search':
  col1,col2,col3,col4,col5=st.columns([1,2,2,2,0.4])
  #local_css("lang_style.txt")
  local_css("border_style.txt")
  lang = col5.radio('', ['EN', 'AR'])
  
  if lang=="EN":
    # styling the page
    local_css("environmental_search_style_en.txt")
    with col1:
      space(2,col1)
      draw_line()
    with col2:
      # concept filter
      concepts_list = df['Concept'].unique()
      concept = st.multiselect("Select Environmental Topic(s)",concepts_list, default=["Pollution"])
    with col3:
      # chapter filter
      chapters_list = ['All']
      for c in df['Chapter Title'].unique():
        chapters_list.append(c)
      chapter = st.multiselect("Select Chapter Title(s)",chapters_list, default= ["All"])
    with col4:
      space(2,col4)
      draw_line()

    # applying filters
    if chapter== ["All"]:
      df = df[df['Concept'].isin(concept)]
    else:
      df = df[(df['Concept'].isin(concept)) & (df['Chapter Title'].isin(chapter))]

    if chapter!= ["All"]:
      displayed_chapters = chapter
      if "All" in displayed_chapters:
        displayed_chapters.remove("All")
      if len(displayed_chapters)==1:
        statement="Verses Related to " + ' & '.join(concept) + " in " + ' & '.join(displayed_chapters) + " Chapter"
      elif  len(displayed_chapters)>1:
        statement="Verses Related to " + ' & '.join(concept) + " in " + ' & '.join(displayed_chapters) + " Chapters"

    elif chapter==["All"]:
      statement="Verses Related to " + ' & '.join(concept) + " in All Chapters"

    if len(concept)!=0 and len(chapter)!=0:
      hc.info_card(title=statement, content= len(df['Arabic Verse']), theme_override = {'bgcolor': '#f0f2f6','title_color': '#2A4657','content_color': 
      '#006400','progress_color': '#006400','icon_color': '#006400', 'icon': 'fa fa-search'})

    
    # a function to highlight words
    def highlight_words(text, words):
      for word in words:
        rep = "<mark><b>" + word + "</b></mark>"
        try:
          text = re.sub(word,rep,text)
        except:
          text = text
      return text

    # a function to get unique values in a list
    def unique(list_of_elements):
      unique_array = np.unique(np.array(list_of_elements))
      unique_list = unique_array.tolist()
      return unique_list

    # gets all envirionmental concepts in a verse
    def find_concept_env(i):
        filtered_df = df[(df["Chapter Nb."]==df["Chapter Nb."].iloc[i])& (df["Verse Nb."]==df["Verse Nb."].iloc[i])]
        concept = filtered_df["Concept"].to_list()
        return ', '.join(concept)

    # gets all the environmental keywords in a verse
    def find_keywords(i):
      filtered_df_words_for_highlight = df[(df["Chapter Nb."]==df["Chapter Nb."].iloc[i])& (df["Verse Nb."]==df["Verse Nb."].iloc[i])]
      filtered_df_words_for_highlight = filtered_df_words_for_highlight["English Keyword"].to_list()
      words_lists=[str(word_string).split() for word_string in filtered_df_words_for_highlight]
      words = unique(sum(words_lists, []))
      return words

    # forming html text to be used in the card
    def search_card_html(verse,chapter_title,verse_number,concept,link_to_environment,source):
      sc_html = f"""<div class="col-xs-12 col-sm-6 col-md-4">
                  <div class="image-flip" ontouchstart="this.classList.toggle('hover');">
                      <div class="mainflip">
                          <div class="frontside">
                              <div class="card">
                              <h1 class="card-title">
                                      <div class="qFrame qFrameTop">
                                      </div>
                                      <div class="qFrame qFrameMiddle " id="middleFrame">
                                      <div class="quranText" id="quranText" style="font-family: hafs; font-size: 1.2em; text-align: justify;"><div class="suraHeaderFrame rtl"><b>{chapter_title}</b></div>
                                      </h1>
                                  <div class="card-body text-center">
                                      <p direction="ltl" class="card-text" style="font-family: hafs;Times New Roman;text-align: left;font-size:18px;line-height: 1.5;"><em>{verse} </em>﴾{verse_number}﴿</p>
                                      <a class="btn btn-outline-success"><i class="fa fa-arrow-right"></i></a>
                                  </div>
                              </div>
                          </div>
                          <div class="backside">
                              <div class="card">
                                  <div class="card-body mt-4">
                                      <h4 class="card-title" style="text-align: left;font-size:17px;line-height: 1.5;"><em>{verse}</em></h4>
                                      <p class="card-text">
                                      <ul style="list-style: none;">
                                      <li><b>Chapter Title: </b>{chapter_title}</li>
                                      <li><b>Verse Number: </b>{verse_number}</li>
                                      <li><b>Environmental Concept(s): </b>{concept}</li>
                                      <li><b>Link to Environment: </b>{link_to_environment}</li>
                                      <li><b>Source: </b>{source}</li>
                                      </ul>
                                      </p>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>"""
      return sc_html
        
    # the design of the card
    def search_card(html):
      local_css("search_card_style_en.txt")
      st.markdown(f"""
  <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <section id="team" class="pb-5">
      <div class="container">
          <div class="row">
              {html}
          </div>
      </div>
  </section>
  """, unsafe_allow_html=True)
      
    # showing the cards with the highlights  
    sc_html=""
    for i in range(len(df["Arabic Verse"])):
      #words = unique(str(df["English Keyword"].iloc[i]).split())
      words = find_keywords(i)
      highlighted_verse = highlight_words(df["English Verse"].iloc[i], words)
      sc_html = sc_html + search_card_html(highlighted_verse,df["Chapter Title"].iloc[i],df["Verse Nb."].iloc[i],find_concept_env(i),
      df["Link to Environment"].iloc[i],df["Reference"].iloc[i])
      
    if sc_html!="":
      search_card(sc_html)          
      
    space(10)
    footer()

  if lang=="AR":
    # styling the page
    local_css("environmental_search_style_ar.txt")
    with col1:
      space(2,col1)
      draw_line()
    with col2:
      # chapter filter
      chapters_list = ['الكل']
      for c in df['Arabic Chapter Title'].unique():
        chapters_list.append(c)
      chapter = st.multiselect("اختر السورة",chapters_list, default= ["الكل"])
    with col3:
      # concept filter
      concepts_list = df['Arabic Concept'].unique()
      concept = st.multiselect("اختر الموضوع البيئي",concepts_list, default=["التلوث"])
    with col4:
      space(2,col4)
      draw_line()
    
    # applying filters
    if chapter== ["الكل"]:
      df = df[df['Arabic Concept'].isin(concept)]
    else:
      df = df[(df['Arabic Concept'].isin(concept)) & (df['Arabic Chapter Title'].isin(chapter))]

    # card
    if chapter!= ["الكل"]:
      displayed_chapters = chapter
      if "الكل" in displayed_chapters:
        displayed_chapters.remove("الكل")
      if len(displayed_chapters)==1:
        statement="الآيات المتعلقة ب" + ' و'.join(concept) + " في " + "سورة " + ' ، '.join(displayed_chapters)
      elif  len(displayed_chapters)>1:
        statement="الآيات المتعلقة ب" + ' و'.join(concept) + " في " + "سور " + ' و'.join(displayed_chapters)

    elif chapter== ["الكل"]:
      statement="الآيات المتعلقة ب" + ' و'.join(concept) + " " + "في السور كلها"
    

    if len(concept)!=0 and len(chapter)!=0:
      ar_info_card(statement, len(df),'search')

    # a function to highlight words
    def highlight_words(text, words):
      for word in words:
        rep = "<mark><b>" + word + "</b></mark>"
        text = re.sub(word,rep,text)
      return text

    # a function to get unique values in a list
    def unique(list_of_elements):
      unique_array = np.unique(np.array(list_of_elements))
      unique_list = unique_array.tolist()
      return unique_list
    
    # gets env concepts in a verse
    def find_concept_env(i):
        filtered_df = df[(df["Chapter Nb."]==df["Chapter Nb."].iloc[i])& (df["Verse Nb."]==df["Verse Nb."].iloc[i])]
        concept = filtered_df["Arabic Concept"].to_list()
        return '، '.join(concept)

    # gets env keywords in a verse
    def find_keywords(i):
      filtered_df_words_for_highlight = df[(df["Chapter Nb."]==df["Chapter Nb."].iloc[i])& (df["Verse Nb."]==df["Verse Nb."].iloc[i])]
      filtered_df_words_for_highlight = filtered_df_words_for_highlight["Arabic Keyword"].to_list()
      words_lists=[str(word_string).split() for word_string in filtered_df_words_for_highlight]
      words = unique(sum(words_lists, []))
      return words

    # forming html text to be used in the card
    def search_card_html(verse_ar,chapter_title,verse_number,concept,link_to_environment,source):
      sc_html = f"""<div class="col-xs-12 col-sm-6 col-md-4">
                  <div class="image-flip" ontouchstart="this.classList.toggle('hover');">
                      <div class="mainflip">
                          <div class="frontside">
                              <div class="card">
                              <h1 class="card-title">
                                      <div class="qFrame qFrameTop">
                                      </div>
                                      <div class="qFrame qFrameMiddle " id="middleFrame">
                                      <div class="quranText" id="quranText" style="font-family: hafs; font-size: 1.2em; text-align: justify; direction: rtl;"><div class="suraHeaderFrame rtl"><b>{chapter_title}</b></div>
                                      </h1>
                                  <div class="card-body text-center">
                                      <p dir="rtl" class="card-text" style="font-family: hafs;Times New Roman;text-align: right;font-size:22px;line-height: 1.5;">{verse_ar} ﴿{verse_number}﴾</p>
                                      <a class="btn btn-outline-success"><i class="fa fa-arrow-left"></i></a>
                                  </div>
                              </div>
                          </div>
                          <div class="backside">
                              <div class="card">
                                  <div class="card-body mt-4">
                                      <h4 dir="rtl" class="card-title" style="text-align: right;font-size:20px;line-height: 1.5;">﴿ {verse_ar} ﴾</h4>
                                      <p class="card-text">
                                      <ul style="list-style: none; text-align: right;">
                                      <li style="font-size:20px;"><b>السورة: </b>{chapter_title}</li>
                                      <li style="font-size:20px;"><b>رقم الآية: </b>{verse_number}</li>
                                      <li style="font-size:20px;"><b>المفهوم البيئي: </b>{concept}</li>
                                      <li style="font-size:20px;"><b>العلاقة مع البيئة: </b>{link_to_environment}</li>
                                      <li style="font-size:20px;"><b>المصدر: </b>{source}</li>
                                      </ul>
                                      </p>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>"""
      return sc_html
        
    # the design of the card
    def search_card(html):
      local_css("search_card_style_ar.txt")
      st.markdown(f"""
  <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <section dir="rtl" id="team" class="pb-5" >
      <div class="container">
          <div class="row">
              {html}
          </div>
      </div>
  </section>
  """, unsafe_allow_html=True)
      
    # showing the cards with the highlights  
    sc_html=""
    for i in range(len(df["Arabic Verse"])):
      #words = unique(str(df["Arabic Keyword"].iloc[i]).split())
      words = find_keywords(i)
      highlighted_verse = highlight_words(df["Arabic Verse"].iloc[i], words)
      sc_html = sc_html + search_card_html(highlighted_verse,df["Arabic Chapter Title"].iloc[i],df["Verse Nb."].iloc[i],find_concept_env(i),
      df["Link to Environment in Arabic"].iloc[i],df["Arabic Reference"].iloc[i])
      
    if sc_html!="":
      search_card(sc_html)          
      
    space(10)
    footer()
    

# general search page
if menu_id=='General Search':
  col1,col2,col3,col4,col5=st.columns([1,2,2,2,0.4])
  #local_css("lang_style.txt")
  local_css("border_style.txt")
  lang = col5.radio('', ['EN', 'AR'])

  if lang=="EN":
    # styling the page
    local_css("general_search_style_en.txt")
    # loading the arabic normalized dataframe of quran
    quran_df = pd.read_excel("EN_Quran_Normalized.xlsx")

    # a function for the expander
    def expander(verse,chapter_title,verse_number,ar_verse,env_relation,concept_heading="",concept="",env_verse_heading="",env_verse="",
    link_to_env_heading="", link_to_env="", source_heading = "", source=""):
        local_css("expander_style_en.txt")
        st.markdown(f"""
        <label class="accordion-wrapper">
    <input type="checkbox" class="accordion" hidden />
    <div class="title">
      <strong><em>{verse} [{chapter_title} {verse_number}]</em></strong>
      <svg viewBox="0 0 256 512" width="12" title="angle-right" class="side-icon" fill="#006400">
        <path d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z" />
      </svg>
      <svg viewBox="0 0 320 512" height="24" title="angle-down" class="down-icon" fill="#006400">
        <path d="M143 352.3L7 216.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.2 9.4-24.4 9.4-33.8 0z" />
      </svg>
    </div>
    <div class="content">
      <p><ul style="list-style: none;">
                                      <li><b>Verse in Arabic: </b></li><h5 dir="rtl" style="padding-bottom: 0rem;text-align: right;">{ar_verse}</h5>
                                      <li><b>Verse in English: </b><em>{verse}</em></li>
                                      <li><b>Chapter Title: </b>{chapter_title}</li>
                                      <li><b>Verse Number: </b>{verse_number}</li>
                                      <li><b>Related to Environment: </b>{env_relation}</li>
                                      <li><b>{concept_heading}</b>{concept}</li>
                                      <li><b>{env_verse_heading}</b>{env_verse}</li>
                                      <li><b>{link_to_env_heading}</b>{link_to_env}</li>
                                      <li><b>{source_heading}</b>{source}</li>
        </ul>
      </p>
    </div>
  </label>
        """, unsafe_allow_html=True)
    # returns the unique elements in a list
    def unique(list_of_elements):
      unique_array = np.unique(np.array(list_of_elements))
      unique_list = unique_array.tolist()
      return unique_list

    # a function to highlight the matching words in the literal search
    def highlight_literal(match_df, match_index):
        words_of_search_query = search.split()
        
        indices = []
        for search_word in words_of_search_query:
          for j in range(len(ast.literal_eval(match_df["tokenized_verse_for_highlight2"].iloc[match_index]))):
            if search_word in ast.literal_eval(match_df["tokenized_verse_for_highlight2"].iloc[match_index])[j] and j not in indices:
              indices.append(j)
        
        verse_tokenized_with_punc = ast.literal_eval(match_df["tokenized_verse_for_highlight"].iloc[match_index])
        for i in indices:
          verse_tokenized_with_punc[i] = '<mark><b>' + verse_tokenized_with_punc[i] + '</b></mark>'
        
        highlighted_verse_with_punc = " ".join(verse_tokenized_with_punc)
        highlighted_verse_with_punc = re.sub("\s\.",".",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\;",";",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\:",":",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\,",",",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\!","!",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\?","?",highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub('''\s"''','''"''',highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub('''"\s''','''"''',highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\(\s",'(',highlighted_verse_with_punc)
        highlighted_verse_with_punc = re.sub("\s\)",')',highlighted_verse_with_punc)
        return highlighted_verse_with_punc
    
    def find_match_stem(match_df, norm_col, match_index, lemmas_stems_search_query_list_of_lists): 
      indices = []
      different_words_matched=[]
      for i in range(len(lemmas_stems_search_query_list_of_lists)):
        for search_lemma_stem in lemmas_stems_search_query_list_of_lists[i]:
          for j in range(len(ast.literal_eval(match_df[norm_col].iloc[match_index]))):
            if search_lemma_stem in ast.literal_eval(match_df[norm_col].iloc[match_index])[j] and j not in indices:
              different_words_matched.append(i)
              indices.append(j)
      different_words_matched = unique(different_words_matched)
      return (different_words_matched, indices)

    def highlight_stem(match_df, norm_col, match_index, lemmas_stems_search_query_one_list):
      indices = []
      for search_lemma_stem in lemmas_stems_search_query_one_list:
        for j in range(len(ast.literal_eval(match_df[norm_col].iloc[match_index]))):
          if search_lemma_stem in ast.literal_eval(match_df[norm_col].iloc[match_index])[j] and j not in indices:
            indices.append(j)

      verse_tokenized_with_punc = ast.literal_eval(match_df["tokenized_verse_for_highlight"].iloc[match_index])
      for i in indices:
        verse_tokenized_with_punc[i] = '<mark><b>' + verse_tokenized_with_punc[i] + '</b></mark>'

      highlighted_verse_with_punc = " ".join(verse_tokenized_with_punc)
      highlighted_verse_with_punc = re.sub("\s\.",".",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\;",";",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\:",":",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\,",",",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\!","!",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\?","?",highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub('''\s"''','''"''',highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub('''"\s''','''"''',highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\(\s",'(',highlighted_verse_with_punc)
      highlighted_verse_with_punc = re.sub("\s\)",')',highlighted_verse_with_punc)
      return highlighted_verse_with_punc

    def environment_test(match,i):
        filtered_env_df = df[df["Chapter Nb."]==match["eng_chapter_nb"].iloc[i]]
        return match["eng_verse_nb"].iloc[i] in filtered_env_df["Verse Nb."].to_list()
    
    def find_concept(match,i):
        filtered_df = df[(df["Chapter Nb."]==match["eng_chapter_nb"].iloc[i])& (df["Verse Nb."]==match["eng_verse_nb"].iloc[i])]
        concept = list(np.unique(filtered_df["Concept"].to_list()))
        env_link = list(np.unique(filtered_df["Link to Environment"].to_list()))
        source = list(np.unique(filtered_df["Reference"].to_list()))
        if len(env_link)>1 and "no link" in env_link:
          env_link.remove("no link")
        if len(source)>1 and "no source" in source:
          source.remove("no source")
        return ', '.join(concept), ', '.join(env_link), ', '.join(source)
    
    def highlight_words(text, words):
        for word in words:
          rep = '<mark><b>' + word + '</b></mark>'
          text = re.sub(word,rep,text)
        return text

    def highlight_search_on_env(match,i):
        try:
          filtered_env_df = df[(df["Chapter Nb."]==match["eng_chapter_nb"].iloc[i])& (df["Verse Nb."]==match["eng_verse_nb"].iloc[i])]
          filtered_df_words_for_highlight = filtered_env_df["English Keyword"].to_list()
          words_lists=[str(word_string).split() for word_string in filtered_df_words_for_highlight]
          words = unique(sum(words_lists, []))
          highlighted_verse = highlight_words(filtered_env_df["English Verse"].iloc[0], words)
        except:
          highlighted_verse=""
        return highlighted_verse

    def remove_stop_words(tokens, stopwords):
      cleaned_tokens = [token for token in tokens if token not in stopwords]
      return cleaned_tokens 
 
    nlp = spacy.load("en_core_web_sm")
    porter = PorterStemmer()   

    with col1:
      space(2,col1)
      draw_line()
    with col2:
      # chapter filter
      chapters_list = ['All']
      for c in quran_df['English Chapter Title'].unique():
        chapters_list.append(c)
      chapter = st.multiselect("Select Chapter Title(s)",chapters_list, default= ["All"])
      # applying filters
      if chapter!= ["All"]:
        quran_df = quran_df[quran_df['English Chapter Title'].isin(chapter)]
    with col3:
      search_type = st.selectbox('Select Search Type', ['Literal Search', 'Stem Search'])
    with col4:
      space(2,col4)
      draw_line()
      
    col1,col2,col3 = st.columns([3,0.1,1])

    search = col1.text_input("Word or Phrase in English", placeholder="Type Here")
    search = search.lower()

    space(2,col3)
    #col2.image("https://cdn-icons-png.flaticon.com/512/2807/2807005.png")
    with col3:
      lottie_churn = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_0589tdzw.json")
      st_lottie(lottie_churn, key = "churn", height = 200, width = 300)

    if search_type == "Literal Search":
      if len(search) != 0:
          match = quran_df[quran_df["eng_verse_no_punc"].str.contains(search)]
          
          with col1:
            # card to show search results
            hc.info_card(title="Number of Verses Found", content= match.shape[0], theme_override = {'bgcolor': '#f0f2f6','title_color': '#2A4657','content_color': 
            '#006400','progress_color': '#006400','icon_color': '#006400', 'icon': 'fa fa-check'})
          
          # showing the results
          if len(match)!=0:
            for i in range(len(match)):
              if environment_test(match,i)==True:
                env_concept, env_link, env_source = find_concept(match,i)
                expander(highlight_literal(match, i), match["English Chapter Title"].iloc[i], match["eng_verse_nb"].iloc[i],match["arabic_verse"].iloc[i],
                "Yes",concept_heading="Environmental Concept(s): ",concept=env_concept,
                env_verse_heading="Verse with Environmental Words: ",env_verse= highlight_search_on_env(match,i),
                link_to_env_heading="Link to Environment: ", link_to_env=env_link, source_heading = "Source: ", source=env_source)
              else:
                expander(highlight_literal(match, i), match["English Chapter Title"].iloc[i], match["eng_verse_nb"].iloc[i],match["arabic_verse"].iloc[i],
                "No")            
    
    elif search_type == "Stem Search":
      if len(search) != 0:
        # query preprocessing

        # removing punctuations and special characters
        def remove_punc(text):
          return re.sub(r'[^a-zA-Z0-9\s]', '', text)

        query_no_punc = remove_punc(search)
        query_tokenized = search.split()
        query_cleaned = unique(remove_stop_words(query_tokenized, STOP_WORDS))
        query_cleaned_combined = " ".join(query_cleaned)
        
        query_doc = nlp(query_cleaned_combined)
        query_normalized_list_of_lists=[]
        for token in query_doc:
          query_normalized_list_of_lists.append(unique([token.lemma_,porter.stem(token.text)]))
        
        query_normalized_one_list = sum(query_normalized_list_of_lists, [])

        #query_normalized_combined = " ".join(query_normalized_one_list)

        # filtering verses
        def filtering_verses(elements_list):
          elements_list = ast.literal_eval(elements_list)
          for lemma_stem in query_normalized_one_list:
            if lemma_stem in elements_list:
              return True
          return False
        quran_df["filtering"] = quran_df["normalized_verse"].apply(filtering_verses)
        quran_df_filtered = quran_df[quran_df["filtering"]==True]
        
        if len(quran_df_filtered)!=0:
          number_of_matches=[]
          number_of_different_words_matched = []
          for i in range(len(quran_df_filtered)):
            number_of_different_words_matched.append(len(find_match_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_list_of_lists)[0]))
            number_of_matches.append(len(find_match_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_list_of_lists)[1]))
          quran_df_filtered["number_of_different_matches"] = number_of_different_words_matched
          quran_df_filtered["number_of_matches"] = number_of_matches
          quran_df_filtered = quran_df_filtered.sort_values(by=["number_of_different_matches","number_of_matches"], ascending=[False,False])

        with col1:
          hc.info_card(title="Number of Verses Found", content= quran_df_filtered.shape[0], 
          theme_override = {'bgcolor': '#f0f2f6','title_color': '#2A4657','content_color': 
          '#006400','progress_color': '#006400','icon_color': '#006400', 'icon': 'fa fa-check'})

        if len(quran_df_filtered) != 0:  
          for i in range(len(quran_df_filtered)):
            if environment_test(quran_df_filtered,i)==True:
              env_concept, env_link, env_source = find_concept(quran_df_filtered,i)
              expander(highlight_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_one_list), 
              quran_df_filtered["English Chapter Title"].iloc[i], quran_df_filtered["eng_verse_nb"].iloc[i], quran_df_filtered["arabic_verse"].iloc[i],
              "Yes", concept_heading="Environmental Concept(s): ",concept=env_concept,
              env_verse_heading="Verse with Environmental Words: ",env_verse=highlight_search_on_env(quran_df_filtered,i),
              link_to_env_heading="Link to Environment: ", link_to_env=env_link, source_heading = "Source: ", source=env_source)
            else:
              expander(highlight_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_one_list), 
              quran_df_filtered["English Chapter Title"].iloc[i], quran_df_filtered["eng_verse_nb"].iloc[i], quran_df_filtered["arabic_verse"].iloc[i],
              "No")
    
    space(10)
    footer()

  if lang=="AR":
    # styling the page
    local_css("general_search_style_ar.txt")
    # loading the arabic normalized dataframe of quran
    quran_df = pd.read_excel("AR_Quran_Normalized.xlsx")

    # a function for the expander
    def expander(verse,chapter_title,verse_number,eng_verse,env_relation,concept_heading="",concept="",env_verse_heading="",env_verse="",
    link_to_env_heading="", link_to_env="", source_heading = "", source=""):
        local_css("expander_style_ar.txt")
        st.markdown(f"""
        <label class="accordion-wrapper">
    <input type="checkbox" class="accordion" hidden />
    <div dir:"rtl" style:"text-align:right" class="title">
      <strong dir:"rtl" style:"text-align:right">{verse} [{chapter_title} {verse_number}]</strong>
      <svg viewBox="0 0 256 512" width="12" title="angle-right" class="side-icon" fill="#006400">
        <path d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z" />
      </svg>
      <svg viewBox="0 0 320 512" height="24" title="angle-down" class="down-icon" fill="#006400">
        <path d="M143 352.3L7 216.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.2 9.4-24.4 9.4-33.8 0z" />
      </svg>
    </div>
    <div class="content">
      <p><ul style="list-style: none;text-align:right;">
                                      <li  dir= "rtl" style="font-size:18px"><b>الآية باللغة الإنجليزية: </b></li><h5 dir="ltl" style="font-size:18px; text-align:left;padding-bottom: 0rem;"><em>{eng_verse}</em></h5>
                                      <li dir= "rtl" style="font-size:20px"> <b>الآية باللغة العربية: </b>{verse}</li>
                                      <li dir= "rtl" style="font-size:20px"><b>السورة: </b>{chapter_title}</li>
                                      <li  dir= "rtl" style="font-size:20px"><b>رقم الآية: </b>{verse_number}</li>
                                      <li  dir= "rtl" style="font-size:20px"><b>متعلقة بالبيئة: </b>{env_relation}</li>
                                      <li  dir= "rtl" style="font-size:20px"><b>{concept_heading}</b>{concept}</li>
                                      <li  dir= "rtl" style="font-size:20px"><b>{env_verse_heading}</b>{env_verse}</li>
                                      <li dir= "rtl" style="font-size:20px"><b>{link_to_env_heading}</b>{link_to_env}</li>
                                      <li dir= "rtl" style="font-size:20px"><b>{source_heading}</b>{source}</li>
        </ul>
      </p>
    </div>
  </label>
        """, unsafe_allow_html=True)
    def unique(list_of_elements):
      unique_array = np.unique(np.array(list_of_elements))
      unique_list = unique_array.tolist()
      return unique_list

    # def filtering_literal(quran_df, index):
    #   words_of_search_query = araby.tokenize(search)
    #   for word in words_of_search_query:
    #     if word in quran_df["cleaned_verse_from_special_characters"].iloc[index]:
    #       return True
    #   return False

    # def find_match_literal(match_df, index):
    #   words_of_search_query = araby.tokenize(search)    
    #   indices = []
    #   different_words_matched=[]
    #   for search_word in words_of_search_query:
    #     for j in range(len(ast.literal_eval(match_df["tokenized_verse"].iloc[index]))):
    #       if search_word in ast.literal_eval(match_df["tokenized_verse"].iloc[index])[j] and j not in indices:
    #         different_words_matched.append(search_word)
    #         indices.append(j)
    #   different_words_matched = unique(different_words_matched)
    #   return (different_words_matched, indices)

    # a function to highlight the matching words in the literal search
    def highlight_literal(match_df, match_index):
        words_of_search_query = araby.tokenize(search)
        
        indices = []
        for search_word in words_of_search_query:
          for j in range(len(ast.literal_eval(match_df["tokenized_verse"].iloc[match_index]))):
            if search_word in ast.literal_eval(match_df["tokenized_verse"].iloc[match_index])[j] and j not in indices:
              indices.append(j)
        
        verse_tokenized_with_harakat = ast.literal_eval(match_df["tokenized_verse_for_highlight"].iloc[match_index])
        for i in indices:
          verse_tokenized_with_harakat[i] = '<mark><b>' + verse_tokenized_with_harakat[i] + '</b></mark>'
        
        highlighted_verse_with_harakat = " ".join(verse_tokenized_with_harakat)
        
        return highlighted_verse_with_harakat
    
    def find_match_stem(match_df, norm_col, match_index, lemmas_stems_search_query_list_of_lists): 
      indices = []
      different_words_matched=[]
      for i in range(len(lemmas_stems_search_query_list_of_lists)):
        for search_lemma_stem in lemmas_stems_search_query_list_of_lists[i]:
          for j in range(len(ast.literal_eval(match_df[norm_col].iloc[match_index]))):
            if search_lemma_stem in ast.literal_eval(match_df[norm_col].iloc[match_index])[j] and j not in indices:
              different_words_matched.append(i)
              indices.append(j)
      different_words_matched = unique(different_words_matched)
      return (different_words_matched, indices)

    def highlight_stem(match_df, norm_col, match_index, lemmas_stems_search_query_one_list):
      indices = []
      for search_lemma_stem in lemmas_stems_search_query_one_list:
        for j in range(len(ast.literal_eval(match_df[norm_col].iloc[match_index]))):
          if search_lemma_stem in ast.literal_eval(match_df[norm_col].iloc[match_index])[j] and j not in indices:
            indices.append(j)

      verse_tokenized_with_harakat = ast.literal_eval(match_df["tokenized_verse_for_highlight"].iloc[match_index])
      for i in indices:
        verse_tokenized_with_harakat[i] = '<mark><b>' + verse_tokenized_with_harakat[i] + '</b></mark>'

      highlighted_verse_with_harakat = " ".join(verse_tokenized_with_harakat)
        
      return highlighted_verse_with_harakat

    def environment_test(match,i):
        filtered_env_df = df[df["Chapter Nb."]==match["arabic_chapter_nb"].iloc[i]]
        return match["arabic_verse_nb"].iloc[i] in filtered_env_df["Verse Nb."].to_list()

    def find_concept(match,i):
        filtered_df = df[(df["Chapter Nb."]==match["arabic_chapter_nb"].iloc[i])& (df["Verse Nb."]==match["arabic_verse_nb"].iloc[i])]
        concept = list(np.unique(filtered_df["Arabic Concept"].to_list()))
        env_link = list(np.unique(filtered_df["Link to Environment in Arabic"].to_list()))
        source = list(np.unique(filtered_df["Arabic Reference"].to_list()))
        if len(env_link)>1 and ('لا يوجد' in env_link):
          env_link.remove('لا يوجد')
        if len(source)>1 and ('لا يوجد' in source):
          source.remove('لا يوجد')
        return '، '.join(concept), '، '.join(env_link), '، '.join(source)
    
    def highlight_words(text, words):
        for word in words:
          rep = '<mark><b>' + word + '</b></mark>'
          text = re.sub(word,rep,text)
        return text

    def highlight_search_on_env(match,i):
        filtered_env_df = df[(df["Chapter Nb."]==match["arabic_chapter_nb"].iloc[i])& (df["Verse Nb."]==match["arabic_verse_nb"].iloc[i])]
        filtered_df_words_for_highlight = filtered_env_df["Arabic Keyword"].to_list()
        words_lists=[str(word_string).split() for word_string in filtered_df_words_for_highlight]
        words = unique(sum(words_lists, []))
        highlighted_verse = highlight_words(filtered_env_df["Arabic Verse"].iloc[0], words)
        return highlighted_verse

    def remove_stop_words(tokens, stopwords):
      cleaned_tokens = [token for token in tokens if token not in stopwords]
      return cleaned_tokens 
    file = open('all_arabic_stop_words.txt', 'r', encoding='utf-8') 
    stopwords = file.read().splitlines()

    #stemmer = FarasaStemmer()
    arStem = ArabicLightStemmer()

    with col1:
      space(2,col1)
      draw_line()
    with col2:
      # chapter filter
      chapters_list = ['الكل']
      for c in quran_df['Arabic Chapter Title'].unique():
        chapters_list.append(c)
      chapter = st.multiselect("اختر السورة",chapters_list, default= ["الكل"])
      # applying filters
      if chapter!= ["الكل"]:
        quran_df = quran_df[quran_df['Arabic Chapter Title'].isin(chapter)]
    with col3:
      search_type = st.selectbox('اختر نوع البحث', ['بحث حرفي', 'بحث بأصل الكلمة'])
    with col4:
      space(2,col4)
      draw_line()
      
    col1,col2,col3 = st.columns([1,0.1,3])
    space(1,col1)

    #<div data-baseweb="base-input" class="st-b4 st-b7 st-fk st-b2 st-c1 st-ae st-af st-ag st-ah st-ai st-aj st-cd st-c2">
     #   <input aria-invalid="false" aria-required="false" autocomplete="" inputmode="text" name="" placeholder="اكتب هنا" type="text" 
      #  class="st-cj st-dw st-d8 st-d9 st-da st-db st-dx st-dz st-dy st-e0 st-bx st-b7 st-dv st-cl st-fl st-fb st-fc st-fm st-fn st-ae st-af st-ag st-ah st-ai st-aj st-cd st-fo st-fp st-fq"");
    
    st.markdown("""
     <script type="text/javascript" src="//api.yamli.com/js/yamli_api.js"></script>
    <script type="text/javascript">
      {
        Yamli.yamlifyType('textbox');
        }
    </script>
    """, unsafe_allow_html=True)

    search = col3.text_input("كلمة أو عبارة باللغة العربية", placeholder="اكتب هنا")
    st.markdown("""<html>
    <body>
     <script type="text/javascript" src="//api.yamli.com/js/yamli_api.js"></script>
    <script type="text/javascript">
      {
      Yamli.yamlifyType('textbox');
      }
    </script>
    </body>
    </html>
    """, unsafe_allow_html=True)
    
  
    #col2.image("https://cdn-icons-png.flaticon.com/512/2807/2807005.png")
    with col1:
      lottie_churn = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_0589tdzw.json")
      st_lottie(lottie_churn, key = "churn", height = 200, width = 300)

    if search_type == 'بحث حرفي':
      if len(search) != 0:
          match = quran_df[quran_df["cleaned_verse_from_special_characters"].str.contains(araby.strip_tashkeel(search))]
          # # filtering the dataframe for literal matches
          # filters = []
          # for i in range(len(quran_df)):
          #   filters.append(filtering_literal(quran_df, i))

          # match = quran_df
          # match["filter"] = filters
          # match = match[match["filter"]==True]

          # number_of_different_words_matched_literal = []
          # number_of_matches_literal=[]
          # for i in range(len(match)):
          #   number_of_different_words_matched_literal.append(len(find_match_literal(match, i)[0]))
          #   number_of_matches_literal.append(len(find_match_literal(match, i)[1]))  
          # match["number_of_different_matches"] = number_of_different_words_matched_literal    
          # match["number_of_matches"] = number_of_matches_literal
          # match = match.sort_values(by=["number_of_different_matches","number_of_matches"], ascending=[False,False])
          
          with col3:
            # card to show search results
            ar_info_card("عدد الآيات التي تم العثور عليها", match.shape[0], 'check')
          
          # showing the results
          if len(match)!=0:
            for i in range(len(match)):
              if environment_test(match,i)==True:
                env_concept, env_link, env_source = find_concept(match,i)
                expander(highlight_literal(match, i), match["Arabic Chapter Title"].iloc[i], match["arabic_verse_nb"].iloc[i],match["eng_verse"].iloc[i],
                "نعم",concept_heading="المفهوم البيئي: ",concept=env_concept,
                env_verse_heading="الكلمات البيئية في الآية: ",env_verse=highlight_search_on_env(match,i),
                link_to_env_heading="العلاقة مع البيئة: ", link_to_env=env_link, source_heading = "المصدر: ", source=env_source)
              else:
                expander(highlight_literal(match, i), match["Arabic Chapter Title"].iloc[i], match["arabic_verse_nb"].iloc[i],match["eng_verse"].iloc[i],
                "كلا")

    elif search_type == 'بحث بأصل الكلمة':
      space(1,col3)
      #stem_type = col3.radio("اختر نوع أصل الكلمة", ["الجذر مع زيادات", "الجذر"])
      #col3.caption("**الكلمة:** المُفْسِدونَ - **الجذر مع زيادات:** مُفْسِدٌ - **الجذر:** فَسَدَ")
      #if len(search) != 0 and stem_type=="الجذر":
      if len(search) != 0:
        # query preprocessing
        dediacritized_query = araby.strip_tashkeel(search)
        query_tokenized = araby.tokenize(dediacritized_query)
        query_cleaned = unique(remove_stop_words(query_tokenized, stopwords))

        query_normalized_list_of_lists=[]
        for token in query_cleaned:
          stem = arStem.light_stem(token)
          #query_normalized_list_of_lists.append(unique([stemmer.stem(token),arStem.get_stem(),arStem.get_root()]))
          query_normalized_list_of_lists.append(unique([arStem.get_stem(),arStem.get_root()]))
        query_normalized_one_list = sum(query_normalized_list_of_lists, [])

        #query_normalized_combined = " ".join(query_normalized_one_list)

        # filtering verses
        def filtering_verses(elements_list):
          elements_list = ast.literal_eval(elements_list)
          for lemma_stem in query_normalized_one_list:
            if lemma_stem in elements_list:
              return True
          return False
        quran_df["filtering"] = quran_df["normalized_verse"].apply(filtering_verses)
        quran_df_filtered = quran_df[quran_df["filtering"]==True]
        
        if len(quran_df_filtered)!=0:
          number_of_matches=[]
          number_of_different_words_matched = []
          for i in range(len(quran_df_filtered)):
            number_of_different_words_matched.append(len(find_match_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_list_of_lists)[0]))
            number_of_matches.append(len(find_match_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_list_of_lists)[1]))
          quran_df_filtered["number_of_different_matches"] = number_of_different_words_matched
          quran_df_filtered["number_of_matches"] = number_of_matches
          quran_df_filtered = quran_df_filtered.sort_values(by=["number_of_different_matches","number_of_matches"], ascending=[False,False])

        # card showing the results
        ar_info_card("عدد الآيات التي تم العثور عليها", quran_df_filtered.shape[0], 'check')

        if len(quran_df_filtered) != 0:  
          for i in range(len(quran_df_filtered)):
            if environment_test(quran_df_filtered,i)==True:
              env_concept, env_link, env_source = find_concept(quran_df_filtered,i)
              expander(highlight_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_one_list), 
              quran_df_filtered["Arabic Chapter Title"].iloc[i], quran_df_filtered["arabic_verse_nb"].iloc[i], quran_df_filtered["eng_verse"].iloc[i],
              "نعم", concept_heading="المفهوم البيئي: ",concept=env_concept,
              env_verse_heading="الكلمات البيئية في الآية: ",env_verse=highlight_search_on_env(quran_df_filtered,i),
              link_to_env_heading="العلاقة مع البيئة: ", link_to_env=env_link, source_heading = "المصدر: ", source=env_source)
            else:
              expander(highlight_stem(quran_df_filtered, "normalized_verse_for_highlight", i, query_normalized_one_list), 
              quran_df_filtered["Arabic Chapter Title"].iloc[i], quran_df_filtered["arabic_verse_nb"].iloc[i], quran_df_filtered["eng_verse"].iloc[i],
              "كلا")
        
      # if len(search) != 0 and stem_type=="الجذر مع زيادات":
      #   # query preprocessing
      #   dediacritized_query = araby.strip_tashkeel(search)
      #   query_tokenized = araby.tokenize(dediacritized_query)
      #   query_cleaned = unique(remove_stop_words(query_tokenized, stopwords))

      #   query_lemmatized_list_of_lists=[]
      #   for token in query_cleaned:
      #     query_lemmatized_list_of_lists.append([stemmer.stem(token)])
        
      #   query_lemmatized_one_list = sum(query_lemmatized_list_of_lists, [])
        
      #   #query_lemmatized_combined = " ".join(query_lemmatized_one_list)
      #   # filtering verses
      #   def filtering_verses(elements_list):
      #     elements_list = ast.literal_eval(elements_list)
      #     for lemma in query_lemmatized_one_list:
      #       if lemma in elements_list:
      #         return True
      #     return False
      #   quran_df["filtering"] = quran_df["lemmatized_verse"].apply(filtering_verses)
      #   quran_df_filtered = quran_df[quran_df["filtering"]==True]

      #   if len(quran_df_filtered)!=0:
      #     number_of_matches=[]
      #     number_of_different_words_matched = []
      #     for i in range(len(quran_df_filtered)):
      #       number_of_different_words_matched.append(len(find_match_stem(quran_df_filtered, "lemmatized_verse_for_highlight", i, query_lemmatized_list_of_lists)[0]))
      #       number_of_matches.append(len(find_match_stem(quran_df_filtered, "lemmatized_verse_for_highlight", i, query_lemmatized_list_of_lists)[1]))
      #     quran_df_filtered["number_of_different_matches"] = number_of_different_words_matched
      #     quran_df_filtered["number_of_matches"] = number_of_matches
      #     quran_df_filtered = quran_df_filtered.sort_values(by=["number_of_different_matches","number_of_matches"], ascending=[False,False])
        
      #   ar_info_card("عدد الآيات التي تم العثور عليها",quran_df_filtered.shape[0],"check")

      #   if len(quran_df_filtered) != 0:  
      #     for i in range(len(quran_df_filtered)):
      #       if environment_test(quran_df_filtered,i)==True:
      #         env_concept, env_link, env_source = find_concept(quran_df_filtered,i)
      #         expander(highlight_stem(quran_df_filtered, "lemmatized_verse_for_highlight", i, query_lemmatized_one_list), 
      #         quran_df_filtered["Arabic Chapter Title"].iloc[i], quran_df_filtered["arabic_verse_nb"].iloc[i], quran_df_filtered["eng_verse"].iloc[i],
      #         "نعم", concept_heading="المفهوم البيئي: ",concept=env_concept,
      #         env_verse_heading="الكلمات البيئية في الآية: ",env_verse=highlight_search_on_env(quran_df_filtered,i),
      #         link_to_env_heading="العلاقة مع البيئة: ", link_to_env=env_link, source_heading = "المصدر: ", source=env_source)
      #       else:
      #         expander(highlight_stem(quran_df_filtered, "lemmatized_verse_for_highlight", i, query_lemmatized_one_list), 
      #         quran_df_filtered["Arabic Chapter Title"].iloc[i], quran_df_filtered["arabic_verse_nb"].iloc[i], quran_df_filtered["eng_verse"].iloc[i],
      #         "كلا")        
    space(10)
    footer()

def profile_card(photo, name, title, aub_page, email, linkedin, twitter):
  st.markdown(f"""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {{
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}}
button {{
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: green;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}}
.css-177yq5e a {{
    color: green;
}}
button:hover, a:hover {{
  opacity: 0.7;
}}
</style>
</head>
<body>
<div class="card">
  <img src={photo} alt={name} style="width:100%; height:250px">
  <h1 style="font-size: 25px; color:green"><b>{name}</b></h1>
  <p style="color:black" class="title">{title}</p>
  <div style="margin: 24px 0;">
    <a font-size: large; href={aub_page} target="_blank"><i class="fa fa-google fa-lg"></i></a>
    <a href={linkedin} target="_blank"><i class="fa fa-linkedin fa-lg"></i></a>
    <a href={twitter} target="_blank"><i class="fa fa-twitter fa-lg"></i></a>  
  </div>
  <a href={email} target="_blank"><button>Contact</button></a>
</div>
</body>
</html>
""", unsafe_allow_html=True)

if menu_id=='References':
  st.table(references_df)

if menu_id=='Contact Us':
    col1,col2,col3 = st.columns([1.3,1,1])
    col2.title("**Meet Our Team**")
    draw_line()
    st.title("Professors")
    space(3)
    col1,col2,col3=st.columns(3)
    with col1:
        profile_card(photo="https://www.aub.edu.lb/articles/PublishingImages/April-21/alain-daou-ncc-thumb.jpg",
        name="Dr. Alain Daou",
        title="Director, Nature Conservation<br> Center (AUB-NCC)",
        aub_page="https://www.aub.edu.lb/pages/profile.aspx?memberId=ad73",
        email="mailto:ad73@aub.edu.lb",
        linkedin="https://www.linkedin.com/in/alain-daou-2a388214/?originalSubdomain=be",
        twitter="https://twitter.com/DaouAlain?s=20&t=huZjEEBMKn_Q5gfuUzCFjg")

    with col2:
        profile_card(photo="https://spservices.aub.edu.lb/PublicWebService.svc/FMIS_GetProfilePicture?memberId=bo00",
        name="Dr. Bilal Orfali",
        title="Chairman, Sheikh Zayed Chair<br> for Arabic and Islamic Studies",
        aub_page="https://www.aub.edu.lb/pages/profile.aspx?MemberId=bo00",
        email="mailto:bo00@aub.edu.lb",
        linkedin="https://www.linkedin.com/in/bilal-orfali-50348b13/?originalSubdomain=lb",
        twitter="https://twitter.com/borfali?s=20&t=NLuk9j2R-THSxsleScoRHw")

    with col3:
        profile_card(photo="https://s.lecommercedulevant.com/storage/attachments/30/Wissam-Sammouri_253994_large.jpg",
        name="Dr. Wissam Sammouri",
        title="Business Analytics<br> Expert",
        aub_page="https://www.aub.edu.lb/pages/profile.aspx?MemberId=ws42",
        email="mailto:ws42@aub.edu.lb",
        linkedin="https://www.linkedin.com/in/wissam-sammouri/",
        twitter="https://twitter.com/WissamSammouri?s=20&t=9mJ3hZAAKW87WiGBrluNgg")
        
    space(8)

    st.title("Graduates & Research Assistants")
    space(3)
    col1,col2,col3=st.columns(3)
    with col1:
      st.markdown("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}
button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: green;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}
.css-177yq5e a {
    color: green;
}
button:hover, a:hover {
  opacity: 0.7;
}
</style>
</head>
<body>
<div class="card">
  <img src="https://media.licdn.com/dms/image/C4E03AQGYYhglXBeeSw/profile-displayphoto-shrink_800_800/0/1656601450069?e=2147483647&v=beta&t=cHV2FkoiHiv19nIdDgDD06B3p5KSGF4AHDFYzfrc5tU" alt="Mahdi Mohammad" style="width:100%; height:300px">
  <h1 style="font-size: 25px; color:green"><b>Mahdi Mohammad</b></h1>
  <p style="color:black" class="title">Graduate<br>MSc. in Business Analytics (MSBA)</p>
  <div style="margin: 24px 0;">
    <a href="https://www.linkedin.com/in/mahdi-mohammad-7b5034201/" target="_blank"><i class="fa fa-linkedin fa-lg"></i></a> 
  </div>
  <a href="mailto:mam127@mail.aub.edu" target="_blank"><button>Contact</button></a>
</div>
</body>
</html>
""", unsafe_allow_html=True)

    with col2:
      st.markdown("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}
button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: green;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}
.css-177yq5e a {
    color: green;
}
button:hover, a:hover {
  opacity: 0.7;
}
</style>
</head>
<body>
<div class="card">
  <img src="https://media.licdn.com/dms/image/D4E03AQGM8su3oI_9Rw/profile-displayphoto-shrink_800_800/0/1676227642710?e=1682553600&v=beta&t=mauFa6zJ_gEZ8b6phr5kbf5ExwjCvJ8k6kCV1TsjwHA" alt=Mrs. Sara Moussalli style="width:100%; height:300px">
  <h1 style="font-size: 25px; color:green"><b>Mrs. Sara Moussalli</b></h1>
  <p style="color:black" class="title">Research Assistant<br> MA in Islamic Studies</p>
  <div style="margin: 24px 0;">
    <a href="https://www.linkedin.com/in/sara-moussalli/" target="_blank"><i class="fa fa-linkedin fa-lg"></i></a>
    <a href="https://twitter.com/smuslimah95?s=20&t=Do-nTdw3oBR4KQ1WHuQn6g" target="_blank"><i class="fa fa-twitter fa-lg"></i></a>  
  </div>
  <a href="mailto:sam54@mail.aub.edu" target="_blank"><button>Contact</button></a>
</div>
</body>
</html>
""", unsafe_allow_html=True)

    with col3:
      st.markdown("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}
button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: green;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}
.css-177yq5e a {
    color: green;
}
button:hover, a:hover {
  opacity: 0.7;
}
</style>
</head>
<body>
<div class="card">
  <img src="https://media.licdn.com/dms/image/D4E03AQFfEIKCgChsbg/profile-displayphoto-shrink_800_800/0/1677054447083?e=1682553600&v=beta&t=Hp9XpCFdTQQRScYvNeshcdN5liK1jJATcqLTmYnMQGc" alt="Mohammad Tabaja" style="width:100%; height:300px">
  <h1 style="font-size: 25px; color:green"><b>Mohammad Tabaja</b></h1>
  <p style="color:black" class="title">Graduate Student<br>MA in Islamic Studies at AUB</p>
  <div style="margin: 24px 0;">
    <a href="https://www.linkedin.com/in/mohammadtabaja/" target="_blank"><i class="fa fa-linkedin fa-lg"></i></a> 
  </div>
  <a href="mailto:mat49@mail.aub.edu" target="_blank"><button>Contact</button></a>
</div>
</body>
</html>
""", unsafe_allow_html=True)

    space(12)
    footer()

    
    
        



                


    
   
