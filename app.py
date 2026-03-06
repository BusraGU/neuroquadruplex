import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import py3Dmol
from streamlit_agraph import agraph, Node, Edge, Config

# 1. Sayfa Ayarları
st.set_page_config(page_title="NeuroQuadruplex | Nörodejeneratif G4 Atlası", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# 2. ÜST DÜZEY ESTETİK CSS (Silik DNA Arkaplanı ve Buzlu Cam Tasarımı)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Muazzam Silik DNA Arkaplanı */
    .stApp {
        background-color: #f8fafc;
        background-image: url("https://images.unsplash.com/photo-1614935151651-0bea6508c9ce?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(248, 250, 252, 0.90); /* Görseli %90 oranında beyazlatıp silikleştirir */
        z-index: -1; pointer-events: none;
    }

    /* Buzlu Cam (Glassmorphism) Paneller */
    .header-container {
        background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        padding: 30px; border-radius: 16px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.2);
        display: flex; align-items: center; gap: 25px;
    }
    .header-title { font-size: 42px; font-weight: 800; margin: 0; letter-spacing: -1px; background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .header-subtitle { font-size: 16px; font-weight: 400; color: #cbd5e1; margin-top: 5px; }
    
    .info-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px); padding: 25px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid rgba(226, 232, 240, 0.8); border-left: 5px solid #38bdf8;}
    .metric-box { background: rgba(241, 245, 249, 0.8); padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(226, 232, 240, 0.6); }
    .metric-title { font-size: 12px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .metric-value { font-size: 16px; color: #0f172a; font-weight: 600; }
    
    .g4-box {
        background: rgba(15, 23, 42, 0.95); color: #34d399; font-family: 'Courier New', monospace;
        padding: 20px; border-radius: 12px; font-size: 20px; font-weight: 800;
        letter-spacing: 4px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        margin: 20px 0; border: 1px solid #1e293b;
    }
    .therapy-box { background: rgba(236, 253, 245, 0.9); border: 1px solid #10b981; padding: 20px; border-radius: 12px; color: #065f46; font-weight: 500; line-height: 1.6; backdrop-filter: blur(5px);}
    
    /* Hastalık Etiketleri */
    .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; color: white; margin-bottom: 15px;}
    .badge-alz { background-color: #3b82f6; } 
    .badge-par { background-color: #8b5cf6; } 
    .badge-als { background-color: #ef4444; }
    .badge-hun { background-color: #f59e0b; }
    
    /* Saydam Arkaplanlı Tablo Kutusu */
    .stDataFrame { background: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown("""
<div class="header-container">
    <img src="https://cdn-icons-png.flaticon.com/512/9322/9322127.png" width="90" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.4));">
    <div>
        <h1 class="header-title">NeuroQuadruplex Atlas</h1>
        <p class="header-subtitle">Pan-Nörodejeneratif Hastalıklar G-Quadruplex (PQS) Terapötik Ağı</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Veri Çekme Motoru
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1FBU7cRTLMsL-k1UvaraQb4CTWCAqZBlJ4Vl3QbIJkkE"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    return df

try:
    df = load_data()
    hastalik_kolonu = df.columns[0]
    gen_kolonu = df.columns[1]
    yolak_kolonu = df.columns[2]
    
    # 5. Sol Menü ve Arama
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/9322/9322127.png", width=60)
        st.title("🔬 Atlas Filtresi")
        
        # HASTALIK FİLTRESİ
        hastalik_listesi = df[hastalik_kolonu].dropna().unique().tolist()
        secili_hastalik = st.selectbox("🧠 Hastalık Seçin:", ["Tüm Hastalıklar"] + sorted(hastalik_listesi))
        
        if secili_hastalik != "Tüm Hastalıklar":
            hastalik_df = df[df[hastalik_kolonu] == secili_hastalik]
        else:
            hastalik_df = df
            
        gen_listesi = hastalik_df[gen_kolonu].dropna().unique().tolist()
        secim = st.selectbox("🧬 Gen Seçin:", ["Tüm Veritabanı ve Ağ Haritası"] + sorted(gen_listesi))
        arama = st.text_input("Gelişmiş Arama (Örn: C9orf72, Otofaji)", "")
        
        st.divider()
        st.markdown("### 📊 Platform Metrikleri")
        st.metric(label="🦠 Kapsanan Hastalıklar", value=len(hastalik_listesi))
        st.metric(label="🧬 Taranan Toplam Gen", value=len(df))
        
        st.divider()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Atlası Dışa Aktar (.CSV)", data=csv, file_name='NeuroQuadruplex_Atlas.csv', mime='text/csv')

    # Filtreleme Uygulaması
    gosterilen_df = hastalik_df
    if arama:
        gosterilen_df = gosterilen_df[gosterilen_df.apply(lambda row: row.astype(str).str.contains(arama, case=False).any(), axis=1)]
    elif secim != "Tüm Veritabanı ve Ağ Haritası":
        gosterilen_df = gosterilen_df[gosterilen_df[gen_kolonu] == secim]

    # 6. GÖRÜNÜM KISMI
    if (secim == "Tüm Veritabanı ve Ağ Haritası" and not arama) or len(gosterilen_df) > 1:
        tab_ag, tab_veri = st.tabs(["🕸️ Okunabilir Gen-Hastalık Ağı", "📚 Biyoinformatik Veritabanı"])
        
        with tab_ag:
            st.markdown(f"### 🧠 Pan-Nörodejeneratif Ağ")
            st.info("✨ **Tasarım Güncellendi:** Yazılar artık birbirine girmeyecek şekilde renkli kutular (Box) içine alındı.")
            nodes = []
            edges = []
            
            yolaklar = set()
            hastaliklar = set()
            
            for index, row in gosterilen_df.iterrows():
                if pd.notna(row.iloc[2]): yolaklar.add(str(row.iloc[2]).split('/')[0].split(' ve ')[0].strip())
                if pd.notna(row.iloc[0]): hastaliklar.add(str(row.iloc[0]))
                
            # Hastalık Kutuları (Kırmızı)
            for h in hastaliklar:
                nodes.append(Node(id=h, label=h, size=35, color="#ef4444", shape="box", 
                                  font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True})) 
                
            # Yolak Kutuları (Mor)
            for y in yolaklar:
                nodes.append(Node(id=y, label=y, size=25, color="#8b5cf6", shape="box", 
                                  font={'color': 'white', 'size': 14, 'face': 'Inter'})) 
                
            # Gen Kutuları (Mavi)
            for index, row in gosterilen_df.iterrows():
                g_adi = str(row.iloc[1])
                h_adi = str(row.iloc[0])
                tam_yolak = str(row.iloc[2])
                if pd.notna(g_adi) and pd.notna(tam_yolak):
                    nodes.append(Node(id=g_adi, label=g_adi, size=20, color="#0ea5e9", shape="box",
                                      font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True})) 
                    bagli_oldugu_yolak = tam_yolak.split('/')[0].split(' ve ')[0].strip()
                    
                    # Geni yolağa, yolağı hastalığa bağla (Hiyerarşi)
                    edges.append(Edge(source=g_adi, target=bagli_oldugu_yolak, color="#cbd5e1", width=2))
                    edges.append(Edge(source=bagli_oldugu_yolak, target=h_adi, color="#fca5a5", width=2))
                
            config = Config(width="100%", height=650, directed=True, physics=True, hierarchical=False)
            agraph(nodes=nodes, edges=edges, config=config)
            
        with tab_veri:
            st.markdown("### 📚 Pan-Nörodejeneratif Veri Havuzu")
            # Arka plandan etkilenmemesi için dataframe arkaplanını beyaz yapıyoruz
            st.markdown('<div style="background-color: rgba(255,255,255,0.9); padding: 10px; border-radius: 10px;">', unsafe_allow_html=True)
            st.dataframe(gosterilen_df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
    elif len(gosterilen_df) == 1:
        row = gosterilen_df.iloc[0]
        hastalik = str(row.iloc[0])
        aktif_gen = row.iloc[1]
        
        # Hastalığa Göre Renkli Etiket Belirleme
        badge_class = "badge-alz"
        if "Parkinson" in hastalik: badge_class = "badge-par"
        elif "ALS" in hastalik: badge_class = "badge-als"
        elif "Huntington" in hastalik: badge_class = "badge-hun"
        
        tab1, tab2 = st.tabs(["📝 Gen ve G4 Analizi", "🧬 3D DNA Simülasyonu"])
        
        with tab1:
            st.markdown(f"### 🔬 Biyolojik Hedef: **{aktif_gen}**")
            st.markdown(f"""
            <div class="info-card">
                <span class="badge {badge_class}">{hastalik}</span>
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">🧠 Etkilenen Yolak</div><div class="metric-value">{row.iloc[2]}</div></div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">⚠️ Mutasyonlar</div><div class="metric-value">{row.iloc[3]}</div></div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">📍 G4 Bölgesi</div><div class="metric-value">{row.iloc[4]}</div></div>
                    </div>
                </div>
                
                <div class="metric-title" style="text-align: center; margin-top: 15px; color: #0ea5e9;">🧬 Tespit Edilen PQS (G-Quadruplex) Dizilimi</div>
                <div class="g4-box">{row.iloc[5]}</div>
                
                <div class="therapy-box">
                    <span style="font-size: 18px;">💊</span> <b>Terapötik (İlaç) Potansiyeli:</b><br>{row.iloc[6]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 🧬 G-Quadruplex 3 Boyutlu Konformasyonu")
            view = py3Dmol.view(query='pdb:1XAV', width=800, height=500)
            view.setStyle({'cartoon': {'color': 'spectrum'}, 'stick': {'radius': 0.15}})
            view.addSurface(py3Dmol.VDW, {'opacity': 0.2, 'color': 'white'})
            view.setBackgroundColor('#ffffff') 
            view.zoomTo()
            
            html_code = view._make_html()
            components.html(html_code, height=500, width=800)

except Exception as e:
    st.error(f"⚠️ Sistem Başlatılıyor... Sayfayı 15 saniye sonra yenileyin. Lütfen tablonuzun 1. sütununun 'Hastalık' olduğundan emin olun. (Hata: {e})")
