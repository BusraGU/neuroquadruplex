import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import py3Dmol
from streamlit_agraph import agraph, Node, Edge, Config

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="NeuroQuadruplex | Alzheimer G4 Veritabanı", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# CSS: Bilimsel, Modern ve Şık Tasarım
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    
    /* Üst Banner */
    .header-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 30px; border-radius: 16px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 25px;
    }
    .header-title {
        font-size: 42px; font-weight: 800; margin: 0; letter-spacing: -1px;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .header-subtitle { font-size: 16px; font-weight: 400; color: #cbd5e1; margin-top: 5px; }
    
    /* Kart Tasarımı */
    .info-card { background-color: #ffffff; padding: 25px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; border-left: 5px solid #38bdf8;}
    .metric-box { background: #f1f5f9; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .metric-title { font-size: 12px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .metric-value { font-size: 16px; color: #0f172a; font-weight: 600; }
    
    /* G4 Dizilimi Kutu */
    .g4-box {
        background: #0f172a; color: #34d399; font-family: 'Courier New', monospace;
        padding: 20px; border-radius: 12px; font-size: 20px; font-weight: 800;
        letter-spacing: 4px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        margin: 20px 0; border: 1px solid #1e293b;
    }
    
    /* Terapötik Yorum */
    .therapy-box { background: #ecfdf5; border: 1px solid #10b981; padding: 20px; border-radius: 12px; color: #065f46; font-weight: 500; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# 2. Kurumsal Header (Başlık ve Şık Logo)
st.markdown("""
<div class="header-container">
    <img src="https://cdn-icons-png.flaticon.com/512/9322/9322127.png" width="90" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));">
    <div>
        <h1 class="header-title">NeuroQuadruplex Platform</h1>
        <p class="header-subtitle">Yüksek Çözünürlüklü Alzheimer Hastalığı G-Quadruplex (PQS) ve Terapötik Ağı</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Veri Çekme Motoru
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1FBU7cRTLMsL-k1UvaraQb4CTWCAqZBlJ4Vl3QbIJkkE"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(csv_url)
    return df

try:
    df = load_data()
    gen_kolonu = df.columns[0]
    yolak_kolonu = df.columns[1]
    
    # 4. Sol Menü ve Arama
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/9322/9322127.png", width=60)
        st.title("🔬 Arama Motoru")
        
        gen_listesi = df[gen_kolonu].dropna().unique().tolist()
        secim = st.selectbox("İncelenecek Geni Seçin:", ["Tüm Veritabanı ve Ağ Haritası"] + sorted(gen_listesi))
        arama = st.text_input("Gelişmiş Arama (Örn: Mikroglia, Tau)", "")
        
        st.divider()
        st.markdown("### 📊 Platform Metrikleri")
        st.metric(label="🧬 Taranan Toplam Gen", value=len(df))
        st.metric(label="🎯 G4 Terapötik Hedefi", value=len(df[df.columns[3]].dropna()))
        
        st.divider()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Veritabanını Dışa Aktar (.CSV)", data=csv, file_name='NeuroQuadruplex_V2.csv', mime='text/csv')
        st.caption("© 2026 NeuroQuadruplex BioTech")

    # Filtreleme
    if arama:
        gosterilen_df = df[df.apply(lambda row: row.astype(str).str.contains(arama, case=False).any(), axis=1)]
    elif secim != "Tüm Veritabanı ve Ağ Haritası":
        gosterilen_df = df[df[gen_kolonu] == secim]
    else:
        gosterilen_df = df

    # 5. Görünüm (Sekmeli Yapı)
    if (secim == "Tüm Veritabanı ve Ağ Haritası" and not arama) or len(gosterilen_df) > 1:
        tab_ag, tab_veri = st.tabs(["🕸️ Hücresel Yolak Ağı (Network)", "📚 Biyoinformatik Veritabanı"])
        
        with tab_ag:
            st.markdown("### 🧠 Alzheimer Gen-Yolak Etkileşim Ağı")
            st.info("Bu interaktif harita, genlerin hastalıkla ilgili hangi mekanizmalarda rol oynadığını gösterir. **Düğümleri (noktaları) farenizle sürükleyebilir, tekerlekle yakınlaştırabilirsiniz.**")
            nodes = []
            edges = []
            
            # Yolakları ve Genleri Çiz
            yolaklar = set()
            for p in df[yolak_kolonu].dropna():
                basit_yolak = str(p).split('/')[0].split(' ve ')[0].strip()
                yolaklar.add(basit_yolak)
                
            for y in yolaklar:
                nodes.append(Node(id=y, label=y, size=35, color="#ef4444", shape="diamond")) 
                
            for index, row in df.iterrows():
                g_adi = str(row.iloc[0])
                tam_yolak = str(row.iloc[1])
                if pd.notna(g_adi) and pd.notna(tam_yolak):
                    nodes.append(Node(id=g_adi, label=g_adi, size=20, color="#0ea5e9", shape="dot")) 
                    bagli_oldugu_yolak = tam_yolak.split('/')[0].split(' ve ')[0].strip()
                    edges.append(Edge(source=g_adi, target=bagli_oldugu_yolak, color="#cbd5e1"))
                
            config = Config(width="100%", height=600, directed=False, physics=True, hierarchical=False)
            agraph(nodes=nodes, edges=edges, config=config)
            
        with tab_veri:
            st.markdown("### 📚 Alzheimer - G4 Biyoinformatik Veri Havuzu")
            st.dataframe(gosterilen_df, use_container_width=True, hide_index=True)
        
    elif len(gosterilen_df) == 1:
        row = gosterilen_df.iloc[0]
        aktif_gen = row.iloc[0]
        aktif_yolak = str(row.iloc[1])
        
        tab1, tab2, tab3 = st.tabs(["📝 Gen ve G4 Analizi", "🧬 3D DNA Simülasyonu", "🕸️ Hücresel Etkileşim Ağı"])
        
        # SEKME 1: ANALİZ KARTI
        with tab1:
            st.markdown(f"### 🔬 Biyolojik Hedef: **{aktif_gen}**")
            st.markdown(f"""
            <div class="info-card">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">🧠 İlgili Hücresel Yolak</div><div class="metric-value">{aktif_yolak}</div></div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">⚠️ Klinik Mutasyonlar / GWAS</div><div class="metric-value">{row.iloc[2]}</div></div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <div class="metric-box"><div class="metric-title">📍 G4 Bölgesi (Lokalizasyon)</div><div class="metric-value">{row.iloc[3]}</div></div>
                    </div>
                </div>
                
                <div class="metric-title" style="text-align: center; margin-top: 15px; color: #0ea5e9;">🧬 Tespit Edilen PQS (G-Quadruplex) Dizilimi</div>
                <div class="g4-box">{row.iloc[4]}</div>
                
                <div class="therapy-box">
                    <span style="font-size: 18px;">💊</span> <b>Terapötik (İlaç) Potansiyeli ve Yorum:</b><br>{row.iloc[5]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # SEKME 2: 3D MODELLEME (HATASIZ DOĞRUDAN HTML KODU)
        with tab2:
            st.markdown("### 🧬 G-Quadruplex 3 Boyutlu Konformasyonu")
            st.caption("Farenizle modeli döndürebilir, tekerlek ile yakınlaştırıp uzaklaştırabilirsiniz. (Referans Model: PDB 1XAV - İnsan G4 DNA Yapısı)")
            
            # Doğrudan HTML Component ile Kusursuz Çizim (stmol kütüphanesini baypas ettik!)
            view = py3Dmol.view(query='pdb:1XAV', width=800, height=500)
            view.setStyle({'cartoon': {'color': 'spectrum'}, 'stick': {'radius': 0.15}})
            view.addSurface(py3Dmol.VDW, {'opacity': 0.2, 'color': 'white'})
            view.setBackgroundColor('#f8fafc')
            view.zoomTo()
            
            html_code = view._make_html()
            components.html(html_code, height=500, width=800)

        # SEKME 3: NETWORK AĞI
        with tab3:
            st.markdown(f"### 🕸️ {aktif_gen} Etkileşim Haritası")
            st.info("Bu grafik, seçilen genin hücresel mekanizmalarla ve Alzheimer patolojisiyle olan etkileşimini haritalandırır. Düğümleri farenizle sürükleyebilirsiniz.")
            
            nodes, edges = [], []
            
            # Merkez ve Yolak Düğümleri
            nodes.append(Node(id=aktif_gen, label=aktif_gen, size=35, color="#0ea5e9", shape="diamond"))
            nodes.append(Node(id="G4", label="G-Quadruplex\nRegülasyonu", size=25, color="#f59e0b", shape="hexagon"))
            nodes.append(Node(id="AD", label="Alzheimer\nHastalığı", size=40, color="#ef4444", shape="dot"))
            nodes.append(Node(id="Yolak", label=aktif_yolak.split('/')[0].split(',')[0], size=30, color="#8b5cf6", shape="box"))
            
            if pd.notna(row.iloc[2]) and row.iloc[2] != "":
                nodes.append(Node(id="Mut", label="Mutasyonlar:\n" + str(row.iloc[2]), size=20, color="#64748b", shape="text"))
                edges.append(Edge(source="Mut", target=aktif_gen, label="Fonksiyonu Bozar", color="#94a3b8"))

            edges.append(Edge(source="G4", target=aktif_gen, label="İfadeyi Kontrol Eder", color="#f59e0b"))
            edges.append(Edge(source=aktif_gen, target="Yolak", label="Rol Alır", color="#0ea5e9"))
            edges.append(Edge(source="Yolak", target="AD", label="Patolojiyi Etkiler", color="#8b5cf6"))
            
            config = Config(width="100%", height=500, directed=True, physics=True, hierarchical=False)
            agraph(nodes=nodes, edges=edges, config=config)

except Exception as e:
    st.error(f"⚠️ Sistem Başlatılıyor veya Veritabanı Bekleniyor... Sayfayı birazdan yenileyin. (Hata: {e})")
