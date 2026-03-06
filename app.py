import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları ve Tasarım (CSS)
st.set_page_config(page_title="NeuroQuadruplex", page_icon="🧬", layout="wide")

# Özel CSS ile daha profesyonel bir görünüm (Biyoteknoloji start-up tarzı)
st.markdown("""
    <style>
    .card { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 6px solid #2c3e50; margin-top: 20px;}
    .g4-sequence { font-family: 'Courier New', Courier, monospace; background-color: #f8f9fa; padding: 15px; border-radius: 8px; color: #d35400; letter-spacing: 3px; font-weight: bold; font-size: 16px; text-align: center; border: 1px solid #e9ecef;}
    .metric-label { font-size: 13px; color: #7f8c8d; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;}
    .metric-value { font-size: 16px; color: #2c3e50; font-weight: 500;}
    .highlight-box { background-color: #e8f8f5; padding: 15px; border-radius: 8px; border-left: 5px solid #1abc9c; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# 2. Üst Kısım (Header)
col1, col2 = st.columns([1, 10])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022300.png", width=70)
with col2:
    st.title("NeuroQuadruplex")
    st.markdown("**Alzheimer Hastalığı G-Quadruplex (G4) ve Terapötik Hedefler Veritabanı**")
st.divider()

# 3. Veri Çekme Motoru (Google Sheets)
@st.cache_data(ttl=60) # Veriyi 60 saniyede bir günceller
def load_data():
    sheet_id = "1FBU7cRTLMsL-k1UvaraQb4CTWCAqZBlJ4Vl3QbIJkkE"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    return df

try:
    df = load_data()
    gen_kolonu = df.columns[0] # "Gen Sembolü" kolonu
    
    # 4. Sol Menü (Araştırma Paneli)
    st.sidebar.title("🔍 Araştırma Paneli")
    st.sidebar.markdown("İncelemek istediğiniz geni arayın veya listeden seçin.")
    
    # Arama veya Seçme
    gen_listesi = df[gen_kolonu].dropna().unique().tolist()
    secim = st.sidebar.selectbox("Gen Seçiniz:", ["Tüm Veritabanı"] + gen_listesi)
    arama = st.sidebar.text_input("Veya Gen Sembolü Yazın (Örn: APP)", "")
    
    # Filtreleme Mantığı
    if arama:
        gosterilen_df = df[df[gen_kolonu].astype(str).str.contains(arama, case=False, na=False)]
    elif secim != "Tüm Veritabanı":
        gosterilen_df = df[df[gen_kolonu] == secim]
    else:
        gosterilen_df = df
        
    # İstatistikler (Ana Ekran Üst)
    st.markdown("### 📊 Veritabanı İstatistikleri")
    c1, c2, c3 = st.columns(3)
    c1.metric(label="🧬 Analiz Edilmiş Gen Sayısı", value=len(df))
    c2.metric(label="🎯 G-Quadruplex Hedefi", value=len(df[df.columns[3]].dropna()))
    c3.metric(label="🔄 Sistem Durumu", value="Canlı (API Aktif)")
    st.divider()

    # 5. Görünüm (Tüm Tablo veya Tek Gen Kartı)
    if (secim == "Tüm Veritabanı" and not arama) or len(gosterilen_df) > 1:
        st.subheader("📚 Biyoinformatik Veri Havuzu")
        st.markdown("Aşağıdaki tablodan tüm genlerin özet verilerine ulaşabilir, sol menüden indirebilirsiniz.")
        st.dataframe(gosterilen_df, use_container_width=True, hide_index=True)
        
    elif len(gosterilen_df) == 1:
        row = gosterilen_df.iloc[0]
        st.subheader(f"🔬 Araştırma Özeti: {row.iloc[0]}")
        
        # Profesyonel "Gen Kartı" Tasarımı
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                <div style="flex: 1; min-width: 200px;">
                    <div class="metric-label">🧠 İlgili Hücresel Yolak</div>
                    <div class="metric-value">{row.iloc[1]}</div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div class="metric-label">⚠️ Önemli Mutasyonlar</div>
                    <div class="metric-value">{row.iloc[2]}</div>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div class="metric-label">📍 G-Quadruplex Bölgesi</div>
                    <div class="metric-value">{row.iloc[3]}</div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <div class="metric-label" style="text-align: center;">🧬 Potansiyel G-Quadruplex Dizilimi (PQS)</div>
                <div class="g4-sequence">{row.iloc[4]}</div>
            </div>
            
            <div class="highlight-box">
                <div class="metric-label" style="color: #16a085;">💊 Terapötik (İlaç) Potansiyeli ve Yorumu</div>
                <div class="metric-value" style="font-size: 15px;">{row.iloc[5]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 6. Veri İndirme Butonu (Ticari Kurumsal Hissiyatı İçin)
    st.sidebar.divider()
    st.sidebar.markdown("### 📥 Veri Dışa Aktarım")
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Tüm Veritabanını İndir (.CSV)",
        data=csv,
        file_name='NeuroQuadruplex_Export.csv',
        mime='text/csv'
    )
    st.sidebar.caption("© 2026 NeuroQuadruplex")

except Exception as e:
    st.error(f"⚠️ Veritabanına bağlanılamadı. Lütfen Google Tablonun herkese açık olduğundan emin olun.")
