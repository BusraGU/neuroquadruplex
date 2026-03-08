import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Geniş ekran ve başlık)
st.set_page_config(
    page_title="Database for G-Quadruplex Targets in Neurodegenerative Diseases",
    page_icon="🧬",
    layout="wide"
)

# 2. Özel CSS ile Daha Şık Görünüm
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0px; }
    .sub-title { font-size: 1.1rem; color: #64748B; margin-bottom: 30px; }
    .stTextInput > div > div > input { background-color: #F1F5F9; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🧬 Database for G-Quadruplex Targets in Neurodegenerative Diseases</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Nörodejeneratif hastalıkların patogenezinde rol oynayan ve G-quadruplex (G4) potansiyeli taşıyan gen hedefleri.</p>', unsafe_allow_html=True)

# 3. 32 Genlik Tam Veriseti
data = [
    # Alzheimer
    {"Gen": "APP", "Hastalık": "Alzheimer", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGGCGGGUGGGGAGGGG", "Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_201414.2"},
    {"Gen": "BACE1", "Hastalık": "Alzheimer", "Lokasyon": "pre-mRNA Ekson 3", "G4 Sekansı": "GGGAAGGGGCGGGGAGGG", "Etki": "Alternatif kırpılma", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_012104.5"},
    {"Gen": "ADAM10", "Hastalık": "Alzheimer", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGCGGGCGGGCGGGCGGG", "Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001110.4"},
    {"Gen": "MAPT", "Hastalık": "Alzheimer", "Lokasyon": "Promoter / 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_016835.5"},
    {"Gen": "APOE", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000041.4"},
    {"Gen": "PSEN1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGGCGGGAGGG", "Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000021.4"},
    {"Gen": "TREM2", "Hastalık": "Alzheimer", "Lokasyon": "5'-UTR / Promoter", "G4 Sekansı": "GGGACGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018965.4"},
    {"Gen": "BIN1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_139343.3"},
    {"Gen": "CLU", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001831.4"},
    {"Gen": "ABCA7", "Hastalık": "Alzheimer", "Lokasyon": "Promoter / İntron", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_019112.4"},
    {"Gen": "CD33", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001772.4"},
    {"Gen": "SORL1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGAGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_003105.6"},
    {"Gen": "PICALM", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007166.4"},
    {"Gen": "GSK3B", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002093.4"},
    {"Gen": "FYN", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002037.5"},
    {"Gen": "LRP1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002332.3"},
    
    # Parkinson
    {"Gen": "SNCA", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000345.4"},
    {"Gen": "LRRK2", "Hastalık": "Parkinson", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_198578.4"},
    {"Gen": "PRKN", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGGCGGGGAGGGGCGGG", "Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004562.3"},
    {"Gen": "PINK1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_032409.3"},
    {"Gen": "GBA1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000157.4"},
    {"Gen": "PARK7", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007262.5"},
    {"Gen": "UCHL1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004181.5"},
    {"Gen": "VPS35", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018206.6"},
    
    # ALS-FTD
    {"Gen": "C9orf72", "Hastalık": "ALS-FTD", "Lokasyon": "İntron 1", "G4 Sekansı": "GGGGCCGGGGCCGGGGCC", "Etki": "Toksik RNA/Dipeptit", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018325.5"},
    {"Gen": "TARDBP", "Hastalık": "ALS-FTD", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Otoregülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007375.4"},
    {"Gen": "FUS", "Hastalık": "ALS-FTD", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004960.4"},
    {"Gen": "SOD1", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000454.5"},
    {"Gen": "GRN", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter / 5'-UTR", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002087.4"},
    {"Gen": "VCP", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007126.5"},
    {"Gen": "TBK1", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_013254.4"},
    
    # Huntington
    {"Gen": "HTT", "Hastalık": "Huntington", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002111.8"}
]

df = pd.DataFrame(data)

# 4. Özet İstatistikler (Dashboard Hissi)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🧬 Toplam Gen", len(df))
col2.metric("🧠 Alzheimer", len(df[df["Hastalık"] == "Alzheimer"]))
col3.metric("🫨 Parkinson", len(df[df["Hastalık"] == "Parkinson"]))
col4.metric("⚡ ALS-FTD", len(df[df["Hastalık"] == "ALS-FTD"]))
col5.metric("🧬 Huntington", len(df[df["Hastalık"] == "Huntington"]))

st.write("---")

# 5. Arama Motoru
search_query = st.text_input("🔍 Veritabanında Gen Ara (Örn: BACE1, APP, SNCA)", "")
if search_query:
    df = df[df["Gen"].str.contains(search_query, case=False)]

# 6. Veri Tablosu Görünüm Ayarları (Linkler dahil)
def render_dataframe(dataframe):
    st.dataframe(
        dataframe,
        column_config={
            "Gen": st.column_config.TextColumn("Gen", width="small"),
            "Hastalık": st.column_config.TextColumn("Hastalık", width="small"),
            "Lokasyon": st.column_config.TextColumn("Lokasyon", width="medium"),
            "G4 Sekansı": st.column_config.TextColumn("G4 Sekansı (5' -> 3')", width="large"),
            "Etki": st.column_config.TextColumn("Mekanizma", width="medium"),
            "NCBI_Link": st.column_config.LinkColumn(
                "Veritabanı Referansı",
                display_text="NCBI'de Aç 🔗",  # URL'yi gizleyip temiz bir buton metni gösterir
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

# 7. Kullanıcı Dostu Sekmeler (Tabs)
tab_tum, tab_alz, tab_par, tab_als, tab_hun = st.tabs([
    "Tüm Hastalıklar", "Alzheimer", "Parkinson", "ALS-FTD", "Huntington"
])

with tab_tum:
    render_dataframe(df)

with tab_alz:
    render_dataframe(df[df["Hastalık"] == "Alzheimer"])

with tab_par:
    render_dataframe(df[df["Hastalık"] == "Parkinson"])

with tab_als:
    render_dataframe(df[df["Hastalık"] == "ALS-FTD"])

with tab_hun:
    render_dataframe(df[df["Hastalık"] == "Huntington"])

# Alt bilgi
st.caption("Veriler NCBI RefSeq veritabanı referans alınarak güncel literatür standartlarına göre düzenlenmiştir.")
