import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import py3Dmol
from streamlit_agraph import agraph, Node, Edge, Config

# 1. Sayfa Ayarları
st.set_page_config(page_title="NeuroQuadruplex | Nörodejeneratif G4 Atlası", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# 2. ÜST DÜZEY ESTETİK CSS (Sekmeler Silindi, Beton Kasa ve Menü Butonları Eklendi)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Gerçek DNA Sarmalı Filigranı */
    .stApp {
        background-color: #f4f6f9;
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Dna_strand_1.png/1024px-Dna_strand_1.png");
        background-size: 50%;
        background-position: right center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(248, 250, 252, 0.93); 
        z-index: -1; pointer-events: none;
    }

    /* Şık Header */
    .header-container {
        background: rgba(15, 23, 42, 0.90); backdrop-filter: blur(10px);
        padding: 25px; border-radius: 16px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.2);
        display: flex; align-items: center; gap: 20px;
    }
    .header-title { font-size: 38px; font-weight: 800; margin: 0; background: -webkit-linear-gradient(45deg, #38bdf8, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .header-subtitle { font-size: 16px; font-weight: 500; color: #cbd5e1; margin-top: 5px; letter-spacing: 0.5px;}

    /* 🔴 İŞTE KESİN ÇÖZÜM: BEMBEYAZ İÇERİK KASASI (VAULT) 🔴 */
    /* Animasyon (fade) olmadığı için bu kasa asla şeffaflaşmaz, beton gibi bembeyaz kalır. */
    .main-content-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #cbd5e1;
        margin-top: 5px;
    }
    
    /* Kasadaki her yazıyı zorunlu siyah/lacivert yapıyoruz */
    .main-content-box p, .main-content-box h1, .main-content-box h2, .main-content-box h3, .main-content-box span {
        color: #0f172a !important; 
    }

    [data-testid="stDataFrame"] { background-color: #ffffff !important; border-radius: 8px; padding: 10px; border: 1px solid #cbd5e1; }
    [data-testid="stDataFrame"] * { color: #0f172a !important; }
    
    /* Radyo Butonlarını Şık Menü Butonlarına Dönüştürme Sihri */
    div[role="radiogroup"] {
        background-color: #ffffff;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        display: inline-flex;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    div[role="radiogroup"] label {
        background-color: transparent !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        margin-right: 5px;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover { background-color: #f1f5f9 !important; }
    div[role="radiogroup"] label[data-checked="true"] { background-color: #0f172a !important; }
    div[role="radiogroup"] label[data-checked="true"] p { color: #ffffff !important; font-weight: 700 !important; }
    div[role="radiogroup"] p { color: #64748b !important; font-weight: 600 !important; font-size: 15px !important; margin: 0; }

    /* Özel Renkli Kutular */
    .g4-box { background: #0f172a !important; font-family: 'Courier New', monospace; padding: 15px; border-radius: 8px; font-size: 20px; font-weight: 800; letter-spacing: 4px; text-align: center; margin-top: 15px;}
    .g4-box, .g4-box * { color: #34d399 !important; }
    
    .therapy-box { background: #ecfdf5 !important; border: 1px solid #10b981 !important; padding: 20px; border-radius: 8px; font-weight: 500; margin-top: 20px;}
    .therapy-box, .therapy-box * { color: #065f46 !important; }
    
    .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; margin-bottom: 15px;}
    .badge, .badge * { color: #ffffff !important; }
    .badge-alz { background-color: #3b82f6 !important; } 
    .badge-par { background-color: #8b5cf6 !important; } 
    .badge-als { background-color: #ef4444 !important; }
    .badge-hun { background-color: #f59e0b !important; }

    /* Kartlar ve Metrikler */
    .info-card { background: white; padding: 25px; border-radius: 12px; border-left: 5px solid #38bdf8; border: 1px solid #e2e8f0;}
    .metric-box { background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 10px;}
    .metric-title { font-size: 12px; color: #64748b !important; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .metric-value { font-size: 16px; color: #0f172a !important; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER
logo_html = '<div style="font-size: 45px; display: flex; align-items: center; justify-content: center; width: 85px; height: 85px; background: rgba(255,255,255,0.05); border-radius: 50%; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); letter-spacing: -5px;">🧠🧬</div>'

st.markdown(f"""
<div class="header-container">
{logo_html}
<div>
<h1 class="header-title">NeuroQuadruplex Atlas</h1>
<p class="header-subtitle">Nörodejeneratif Hastalıklar G-Quadruplex Terapötik Ağı</p>
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
        st.markdown(f'<div style="display: flex; justify-content: center; margin-bottom: 25px;">{logo_html}</div>', unsafe_allow_html=True)
        st.title("🔬 Atlas Filtresi")
        
        hastalik_listesi = df[hastalik_kolonu].dropna().unique().tolist()
        secili_hastalik = st.selectbox("🧠 Hastalık Seçin:", ["Tüm Hastalıklar"] + sorted(hastalik_listesi))
        
        if secili_hastalik != "Tüm Hastalıklar":
            hastalik_df = df[df[hastalik_kolonu] == secili_hastalik]
        else:
            hastalik_df = df
            
        gen_listesi = hastalik_df[gen_kolonu].dropna().unique().tolist()
        secim = st.selectbox("🧬 Gen Seçin:", ["Tüm Veritabanı ve Ağ Haritası"] + sorted(gen_listesi))
        arama = st.text_input("Gelişmiş Arama (Örn: C9orf72)", "")
        
        st.divider()
        st.markdown("### 📊 Platform Metrikleri")
        st.metric(label="🦠 Kapsanan Hastalıklar", value=len(hastalik_listesi))
        st.metric(label="🧬 Taranan Toplam Gen", value=len(df))
        
        st.divider()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Atlası Dışa Aktar (.CSV)", data=csv, file_name='NeuroQuadruplex_Atlas.csv', mime='text/csv')

    gosterilen_df = hastalik_df
    if arama:
        gosterilen_df = gosterilen_df[gosterilen_df.apply(lambda row: row.astype(str).str.contains(arama, case=False).any(), axis=1)]
    elif secim != "Tüm Veritabanı ve Ağ Haritası":
        gosterilen_df = gosterilen_df[gosterilen_df[gen_kolonu] == secim]

    # 6. GÖRÜNÜM KISMI (ANA SAYFA)
    if (secim == "Tüm Veritabanı ve Ağ Haritası" and not arama) or len(gosterilen_df) > 1:
        
        # Sekme Sistemi Yerine Yeni Kusursuz Radyo Butonları
        mod = st.radio("Seçim:", ["🕸️ Hastalık-Gen Ağı", "📚 Biyoinformatik Veritabanı"], horizontal=True, label_visibility="collapsed")
        
        # İçerik Kasasının Başlangıcı
        st.markdown('<div class="main-content-box">', unsafe_allow_html=True)
        
        if mod == "🕸️ Hastalık-Gen Ağı":
            st.markdown(f"<h3 style='margin-top:0;'>🧠 Nörodejeneratif Etkileşim Haritası</h3>", unsafe_allow_html=True)
            nodes = []
            edges = []
            
            yolaklar = set()
            hastaliklar = set()
            
            for index, row in gosterilen_df.iterrows():
                if pd.notna(row.iloc[2]): yolaklar.add(str(row.iloc[2]).split('/')[0].split(' ve ')[0].strip())
                if pd.notna(row.iloc[0]): hastaliklar.add(str(row.iloc[0]))
                
            for h in hastaliklar:
                nodes.append(Node(id=h, label=h, size=35, color="#ef4444", shape="box", font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True})) 
                
            for y in yolaklar:
                nodes.append(Node(id=y, label=y, size=25, color="#8b5cf6", shape="box", font={'color': 'white', 'size': 14, 'face': 'Inter'})) 
                
            for index, row in gosterilen_df.iterrows():
                g_adi = str(row.iloc[1])
                h_adi = str(row.iloc[0])
                tam_yolak = str(row.iloc[2])
                if pd.notna(g_adi) and pd.notna(tam_yolak):
                    nodes.append(Node(id=g_adi, label=g_adi, size=20, color="#0ea5e9", shape="box", font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True})) 
                    bagli_oldugu_yolak = tam_yolak.split('/')[0].split(' ve ')[0].strip()
                    edges.append(Edge(source=g_adi, target=bagli_oldugu_yolak, color="#cbd5e1", width=2))
                    edges.append(Edge(source=bagli_oldugu_yolak, target=h_adi, color="#fca5a5", width=2))
                
            config = Config(width="100%", height=650, directed=True, physics=True, hierarchical=False)
            agraph(nodes=nodes, edges=edges, config=config)
            
        elif mod == "📚 Biyoinformatik Veritabanı":
            st.markdown("<h3 style='margin-top:0;'>📚 Veri Havuzu</h3>", unsafe_allow_html=True)
            st.dataframe(gosterilen_df, use_container_width=True, hide_index=True)
            
        st.markdown('</div>', unsafe_allow_html=True) # Kasanın Bitişi
        
    # 7. GÖRÜNÜM (TEK BİR GEN SEÇİLDİĞİNDE)
    elif len(gosterilen_df) == 1:
        row = gosterilen_df.iloc[0]
        hastalik = str(row.iloc[0])
        aktif_gen = row.iloc[1]
        
        badge_class = "badge-alz"
        if "Parkinson" in hastalik: badge_class = "badge-par"
        elif "ALS" in hastalik: badge_class = "badge-als"
        elif "Huntington" in hastalik: badge_class = "badge-hun"
        
        # Sekme Sistemi Yerine Yeni Kusursuz Radyo Butonları
        mod = st.radio("Seçim:", ["📝 Gen Analizi", "🧬 3D DNA Simülasyonu", "🕸️ Hastalık-Gen Ağı"], horizontal=True, label_visibility="collapsed")
        
        st.markdown('<div class="main-content-box">', unsafe_allow_html=True)
        
        if mod == "📝 Gen Analizi":
            st.markdown(f"<h3 style='margin-top:0;'>🔬 Biyolojik Hedef: <b>{aktif_gen}</b></h3>", unsafe_allow_html=True)
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
<div class="metric-title" style="text-align: center; margin-top: 15px; color: #0ea5e9 !important;">🧬 Tespit Edilen PQS (G-Quadruplex) Dizilimi</div>
<div class="g4-box">{row.iloc[5]}</div>
<div class="therapy-box">
<span style="font-size: 18px;">💊</span> <b>Terapötik (İlaç) Potansiyeli:</b><br>{row.iloc[6]}
</div>
</div>
""", unsafe_allow_html=True)

        elif mod == "🧬 3D DNA Simülasyonu":
            st.markdown(f"<h3 style='margin-top:0;'>🧬 {aktif_gen} G-Quadruplex 3 Boyutlu Konformasyonu</h3>", unsafe_allow_html=True)
            st.caption("Farenizle modeli döndürebilir, tekerlek ile yakınlaştırıp uzaklaştırabilirsiniz.")
            view = py3Dmol.view(query='pdb:1XAV', width=800, height=500)
            view.setStyle({'cartoon': {'color': 'spectrum'}, 'stick': {'radius': 0.15}})
            view.addSurface(py3Dmol.VDW, {'opacity': 0.2, 'color': 'white'})
            view.setBackgroundColor('#ffffff') 
            view.zoomTo()
            
            html_code = view._make_html()
            components.html(html_code, height=500, width=800)
            
        elif mod == "🕸️ Hastalık-Gen Ağı":
            st.markdown(f"<h3 style='margin-top:0;'>🕸️ {aktif_gen} Spesifik Etkileşim Ağı</h3>", unsafe_allow_html=True)
            nodes, edges = [], []
            yolak_basit = str(row.iloc[2]).split('/')[0].split(' ve ')[0].strip()
            
            nodes.append(Node(id=hastalik, label=hastalik, size=35, color="#ef4444", shape="box", font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True}))
            nodes.append(Node(id=yolak_basit, label=yolak_basit, size=25, color="#8b5cf6", shape="box", font={'color': 'white', 'size': 14, 'face': 'Inter'}))
            nodes.append(Node(id=aktif_gen, label=aktif_gen, size=20, color="#0ea5e9", shape="box", font={'color': 'white', 'size': 16, 'face': 'Inter', 'bold': True}))
            
            edges.append(Edge(source=aktif_gen, target=yolak_basit, color="#cbd5e1", width=2))
            edges.append(Edge(source=yolak_basit, target=hastalik, color="#fca5a5", width=2))
            
            config = Config(width="100%", height=500, directed=True, physics=True, hierarchical=False)
            agraph(nodes=nodes, edges=edges, config=config)
            
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Sistem Başlatılıyor... Sayfayı 15 saniye sonra yenileyin. (Hata: {e})")
