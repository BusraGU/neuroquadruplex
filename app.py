import streamlit as st
import pandas as pd

# Sayfa ayarları
st.set_page_config(
    page_title="Database for G-Quadruplex Targets in Neurodegenerative Diseases",
    page_icon="🧬",
    layout="wide"
)

# Başlık ve açıklama
st.title("🧬 Database for G-Quadruplex Targets in Neurodegenerative Diseases")
st.markdown("""
Bu veritabanı; Alzheimer, Parkinson, ALS-FTD ve Huntington gibi nörodejeneratif hastalıkların 
patogenezinde rol oynayan ve G-quadruplex (G4) oluşturan gen hedeflerinin nükleotid dizilimlerini ve lokasyonlarını listeler.
""")

# 32 Genlik Tam Sekanslı Veriseti
data = [
    # Alzheimer Genleri
    {"Gen": "APP", "Hastalık": "Alzheimer", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGGCGGGUGGGGAGGGG", "Mekanizma/Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_201414.2", "Referans": "NM_201414.2"},
    {"Gen": "BACE1", "Hastalık": "Alzheimer", "Lokasyon": "pre-mRNA Ekson 3", "G4 Sekansı": "GGGAAGGGGCGGGGAGGG", "Mekanizma/Etki": "Alternatif kırpılma regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_012104.5", "Referans": "NM_012104.5"},
    {"Gen": "ADAM10", "Hastalık": "Alzheimer", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGCGGGCGGGCGGGCGGG", "Mekanizma/Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001110.4", "Referans": "NM_001110.4"},
    {"Gen": "MAPT", "Hastalık": "Alzheimer / FTD", "Lokasyon": "Promoter / 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_016835.5", "Referans": "NM_016835.5"},
    {"Gen": "APOE", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000041.4", "Referans": "NM_000041.4"},
    {"Gen": "PSEN1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGGCGGGAGGG", "Mekanizma/Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000021.4", "Referans": "NM_000021.4"},
    {"Gen": "TREM2", "Hastalık": "Alzheimer", "Lokasyon": "5'-UTR / Promoter", "G4 Sekansı": "GGGACGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018965.4", "Referans": "NM_018965.4"},
    {"Gen": "BIN1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_139343.3", "Referans": "NM_139343.3"},
    {"Gen": "CLU", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001831.4", "Referans": "NM_001831.4"},
    {"Gen": "ABCA7", "Hastalık": "Alzheimer", "Lokasyon": "Promoter / İntron", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_019112.4", "Referans": "NM_019112.4"},
    {"Gen": "CD33", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001772.4", "Referans": "NM_001772.4"},
    {"Gen": "SORL1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGAGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_003105.6", "Referans": "NM_003105.6"},
    {"Gen": "PICALM", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007166.4", "Referans": "NM_007166.4"},
    {"Gen": "GSK3B", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002093.4", "Referans": "NM_002093.4"},
    {"Gen": "FYN", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002037.5", "Referans": "NM_002037.5"},
    {"Gen": "LRP1", "Hastalık": "Alzheimer", "Lokasyon": "Promoter", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002332.3", "Referans": "NM_002332.3"},
    
    # Parkinson Genleri
    {"Gen": "SNCA", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Translasyonel inhibisyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000345.4", "Referans": "NM_000345.4"},
    {"Gen": "LRRK2", "Hastalık": "Parkinson", "Lokasyon": "mRNA 3'-UTR / 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_198578.4", "Referans": "NM_198578.4"},
    {"Gen": "PRKN", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGGCGGGGAGGGGCGGG", "Mekanizma/Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004562.3", "Referans": "NM_004562.3"},
    {"Gen": "PINK1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_032409.3", "Referans": "NM_032409.3"},
    {"Gen": "GBA1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000157.4", "Referans": "NM_000157.4"},
    {"Gen": "PARK7", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007262.5", "Referans": "NM_007262.5"},
    {"Gen": "UCHL1", "Hastalık": "Parkinson", "Lokasyon": "Promoter", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004181.5", "Referans": "NM_004181.5"},
    {"Gen": "VPS35", "Hastalık": "Parkinson", "Lokasyon": "mRNA 5'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Translasyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018206.6", "Referans": "NM_018206.6"},
    
    # ALS-FTD Genleri
    {"Gen": "C9orf72", "Hastalık": "ALS-FTD", "Lokasyon": "İntron 1", "G4 Sekansı": "GGGGCCGGGGCCGGGGCCGGGGCC", "Mekanizma/Etki": "Toksik RNA/Dipeptit, R-loop", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018325.5", "Referans": "NM_018325.5"},
    {"Gen": "TARDBP", "Hastalık": "ALS-FTD", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Otoregülasyon mekanizması", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007375.4", "Referans": "NM_007375.4"},
    {"Gen": "FUS", "Hastalık": "ALS-FTD", "Lokasyon": "mRNA 3'-UTR", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004960.4", "Referans": "NM_004960.4"},
    {"Gen": "SOD1", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000454.5", "Referans": "NM_000454.5"},
    {"Gen": "GRN", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter / 5'-UTR", "G4 Sekansı": "GGGCCGGGCCGGGCCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002087.4", "Referans": "NM_002087.4"},
    {"Gen": "VCP", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007126.5", "Referans": "NM_007126.5"},
    {"Gen": "TBK1", "Hastalık": "ALS-FTD", "Lokasyon": "Promoter", "G4 Sekansı": "GGGGCGGGGCGGGGCGGG", "Mekanizma/Etki": "İfade regülasyonu", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_013254.4", "Referans": "NM_013254.4"},
    
    # Huntington Geni
    {"Gen": "HTT", "Hastalık": "Huntington", "Lokasyon": "Promoter", "G4 Sekansı": "GGGAGGGAGGGAGGG", "Mekanizma/Etki": "Transkripsiyonel regülasyon", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002111.8", "Referans": "NM_002111.8"}
]

df = pd.DataFrame(data)

# Sidebar - Filtreleme Sistemi
st.sidebar.header("Filtreleme Seçenekleri")
hastaliklar = df["Hastalık"].unique().tolist()
secilen_hastaliklar = st.sidebar.multiselect(
    "Hedef Hastalık Seçin:",
    options=hastaliklar,
    default=hastaliklar
)

# Veriyi filtrele
filtrelenmis_df = df[df["Hastalık"].isin(secilen_hastaliklar)]

# Arayüzde Tabloyu Gösterme
st.subheader(f"Veritabanı Tablosu ({len(filtrelenmis_df)} Gen)")

st.dataframe(
    filtrelenmis_df,
    column_config={
        "NCBI_Link": st.column_config.LinkColumn(
            "NCBI Referans Linki",
            display_text=r"https://www\.ncbi\.nlm\.nih\.gov/nuccore/(.*?)"
        ),
        "Gen": st.column_config.TextColumn("Gen Sembolü", width="small"),
        "Hastalık": st.column_config.TextColumn("Hedef Hastalık", width="small"),
        "Lokasyon": st.column_config.TextColumn("G4 Lokasyonu", width="medium"),
        "G4 Sekansı": st.column_config.TextColumn("G4 Sekansı (5' -> 3')", width="large"),
        "Mekanizma/Etki": st.column_config.TextColumn("Mekanizma / Etki", width="medium"),
        "Referans": None 
    },
    hide_index=True,
    use_container_width=True
)

st.sidebar.markdown("---")
st.sidebar.info("Araştırmacılar için G-quadruplex hedeflerini derleyen açık kaynaklı bir veritabanı platformudur.")
