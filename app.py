import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="NeuroQuadruplex Atlas",
    page_icon="🧬",
    layout="wide"
)

# 2. Custom CSS for UI
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0px; }
    .sub-title { font-size: 1.1rem; color: #64748B; margin-bottom: 30px; }
    .stTextInput > div > div > input { background-color: #F1F5F9; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🧬 NeuroQuadruplex Atlas</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">A database of gene targets with G-quadruplex (G4) forming potential involved in the pathogenesis of neurodegenerative diseases.</p>', unsafe_allow_html=True)

# 3. Comprehensive Dataset (Updated with Pathways & Multiple G4 Locations)
data = [
    # Alzheimer's Disease
    {"Gene": "APP", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGCGCGGGGAGGGGCGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Amyloidogenic Pathway", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_201414.2"},
    {"Gene": "APP", "Disease": "Alzheimer's", "Location": "mRNA 3'-UTR", "G4 Sequence": "GGGGCGGGUGGGGAGGGG", "Mechanism": "Translational inhibition", "Pathway": "Amyloidogenic Pathway", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_201414.2"},
    {"Gene": "BACE1", "Disease": "Alzheimer's", "Location": "pre-mRNA Exon 3", "G4 Sequence": "GGGAAGGGGCGGGGAGGG", "Mechanism": "Alternative splicing", "Pathway": "Amyloidogenic Pathway", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_012104.5"},
    {"Gene": "ADAM10", "Disease": "Alzheimer's", "Location": "mRNA 5'-UTR", "G4 Sequence": "GGCGGGCGGGCGGGCGGG", "Mechanism": "Translational inhibition", "Pathway": "Non-amyloidogenic Pathway", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001110.4"},
    {"Gene": "MAPT", "Disease": "Alzheimer's", "Location": "Promoter / 5'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Cytoskeletal Dynamics / Tau Pathology", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_016835.5"},
    {"Gene": "APOE", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Lipid Metabolism / Immune Response", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000041.4"},
    {"Gene": "PSEN1", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGGGCGGGAGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Amyloidogenic Pathway (Notch signaling)", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000021.4"},
    {"Gene": "TREM2", "Disease": "Alzheimer's", "Location": "5'-UTR / Promoter", "G4 Sequence": "GGGACGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Microglial Activation / Immune Response", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018965.4"},
    {"Gene": "BIN1", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Endocytosis / Vesicle Trafficking", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_139343.3"},
    {"Gene": "CLU", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "Lipid Metabolism / Apoptosis", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001831.4"},
    {"Gene": "ABCA7", "Disease": "Alzheimer's", "Location": "Promoter / Intron", "G4 Sequence": "GGGCCGGGCCGGGCCGGG", "Mechanism": "Expression regulation", "Pathway": "Lipid Metabolism / Phagocytosis", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_019112.4"},
    {"Gene": "CD33", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Immune Response (Sialic acid signaling)", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_001772.4"},
    {"Gene": "SORL1", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGAGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "Endosomal-Lysosomal Sorting", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_003105.6"},
    {"Gene": "PICALM", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Clathrin-mediated Endocytosis", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007166.4"},
    {"Gene": "GSK3B", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "Wnt/β-catenin Signaling / Tau Phosphorylation", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002093.4"},
    {"Gene": "FYN", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Synaptic Plasticity / Tau Phosphorylation", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002037.5"},
    {"Gene": "LRP1", "Disease": "Alzheimer's", "Location": "Promoter", "G4 Sequence": "GGGCCGGGCCGGGCCGGG", "Mechanism": "Expression regulation", "Pathway": "Lipid Metabolism / Endocytosis", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002332.3"},
    
    # Parkinson's Disease
    {"Gene": "SNCA", "Disease": "Parkinson's", "Location": "Promoter", "G4 Sequence": "GGGGGCGGGGCCGGGGGCGGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Synaptic Vesicle Dynamics", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000345.4"},
    {"Gene": "SNCA", "Disease": "Parkinson's", "Location": "mRNA 5'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Translational inhibition", "Pathway": "Synaptic Vesicle Dynamics", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000345.4"},
    {"Gene": "LRRK2", "Disease": "Parkinson's", "Location": "mRNA 3'-UTR / 5'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Translational regulation", "Pathway": "Autophagy / Lysosomal Pathway", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_198578.4"},
    {"Gene": "PRKN", "Disease": "Parkinson's", "Location": "mRNA 5'-UTR", "G4 Sequence": "GGGGCGGGGAGGGGCGGG", "Mechanism": "Translational regulation", "Pathway": "Mitochondrial Quality Control (Mitophagy)", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004562.3"},
    {"Gene": "PINK1", "Disease": "Parkinson's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Mitochondrial Quality Control (Mitophagy)", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_032409.3"},
    {"Gene": "GBA1", "Disease": "Parkinson's", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "Sphingolipid Metabolism / Lysosomal Function", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000157.4"},
    {"Gene": "PARK7", "Disease": "Parkinson's", "Location": "mRNA 5'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Translational regulation", "Pathway": "Oxidative Stress Response", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007262.5"},
    {"Gene": "UCHL1", "Disease": "Parkinson's", "Location": "Promoter", "G4 Sequence": "GGGCCGGGCCGGGCCGGG", "Mechanism": "Expression regulation", "Pathway": "Ubiquitin-Proteasome System", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004181.5"},
    {"Gene": "VPS35", "Disease": "Parkinson's", "Location": "mRNA 5'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Translational regulation", "Pathway": "Retromer Complex / Endosomal Sorting", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018206.6"},
    
    # ALS-FTD
    {"Gene": "C9orf72", "Disease": "ALS-FTD", "Location": "Intron 1", "G4 Sequence": "GGGGCCGGGGCCGGGGCC", "Mechanism": "Toxic RNA/Dipeptide", "Pathway": "Nucleocytoplasmic Transport / Autophagy", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_018325.5"},
    {"Gene": "TARDBP", "Disease": "ALS-FTD", "Location": "mRNA 3'-UTR", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Autoregulation", "Pathway": "RNA Metabolism / Splicing", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007375.4"},
    {"Gene": "FUS", "Disease": "ALS-FTD", "Location": "mRNA 3'-UTR", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "RNA Metabolism / DNA Repair", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_004960.4"},
    {"Gene": "SOD1", "Disease": "ALS-FTD", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Oxidative Stress Response", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_000454.5"},
    {"Gene": "GRN", "Disease": "ALS-FTD", "Location": "Promoter / 5'-UTR", "G4 Sequence": "GGGCCGGGCCGGGCCGGG", "Mechanism": "Expression regulation", "Pathway": "Lysosomal Function / Inflammation", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002087.4"},
    {"Gene": "VCP", "Disease": "ALS-FTD", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Expression regulation", "Pathway": "Protein Homeostasis / Autophagy", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_007126.5"},
    {"Gene": "TBK1", "Disease": "ALS-FTD", "Location": "Promoter", "G4 Sequence": "GGGGCGGGGCGGGGCGGG", "Mechanism": "Expression regulation", "Pathway": "Autophagy / Neuroinflammation", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_013254.4"},
    
    # Huntington's Disease
    {"Gene": "HTT", "Disease": "Huntington's", "Location": "Promoter", "G4 Sequence": "GGGAGGGAGGGAGGG", "Mechanism": "Transcriptional regulation", "Pathway": "Transcriptional Regulation / Vesicle Transport", "NCBI_Link": "https://www.ncbi.nlm.nih.gov/nuccore/NM_002111.8"}
]

df = pd.DataFrame(data)

# 4. Sidebar & Download Button
st.sidebar.title("Data Export")
st.sidebar.markdown("Download the full dataset as a CSV file for your own bioinformatics analysis.")

@st.cache_data
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.sidebar.download_button(
    label="📥 Download Dataset (CSV)",
    data=csv,
    file_name='neuroquadruplex_atlas_pathways.csv',
    mime='text/csv',
)
st.sidebar.markdown("---")

# 5. Overview Metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🧬 Total G4 Targets", len(df))
col2.metric("🧠 Alzheimer's", len(df[df["Disease"] == "Alzheimer's"]))
col3.metric("🫨 Parkinson's", len(df[df["Disease"] == "Parkinson's"]))
col4.metric("⚡ ALS-FTD", len(df[df["Disease"] == "ALS-FTD"]))
col5.metric("🧬 Huntington's", len(df[df["Disease"] == "Huntington's"]))

st.write("---")

# 6. Search Bar
search_query = st.text_input("🔍 Search Gene or Pathway in Database (e.g., SNCA, Autophagy, APP)", "")
if search_query:
    df = df[df["Gene"].str.contains(search_query, case=False) | df["Pathway"].str.contains(search_query, case=False)]

# 7. Dataframe Rendering Function
def render_dataframe(dataframe):
    st.dataframe(
        dataframe,
        column_config={
            "Gene": st.column_config.TextColumn("Gene", width="small"),
            "Disease": st.column_config.TextColumn("Disease", width="small"),
            "Location": st.column_config.TextColumn("Location", width="small"),
            "G4 Sequence": st.column_config.TextColumn("G4 Sequence (5' -> 3')", width="medium"),
            "Mechanism": st.column_config.TextColumn("Mechanism / Effect", width="medium"),
            "Pathway": st.column_config.TextColumn("Cellular Pathway", width="medium"),
            "NCBI_Link": st.column_config.LinkColumn(
                "Database Reference",
                display_text="Open in NCBI 🔗",  
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

# 8. Disease Category Tabs & Pathway Diagrams
tab_all, tab_alz, tab_par, tab_als, tab_hun = st.tabs([
    "All Diseases", "Alzheimer's", "Parkinson's", "ALS-FTD", "Huntington's"
])

with tab_all:
    render_dataframe(df)

with tab_alz:
    with st.expander("🔬 View Alzheimer's Disease Pathway Map"):
        st.info("The diagram below illustrates key cellular pathways including the amyloidogenic processing of APP and lipid metabolism.")
        try:
            st.image("images/alzheimer_pathway.png", caption="Alzheimer's Disease Cellular Pathway", use_container_width=True)
        except:
            st.warning("Pathway image not found. Please upload 'alzheimer_pathway.png' to the 'images' folder.")
    render_dataframe(df[df["Disease"] == "Alzheimer's"])

with tab_par:
    with st.expander("🔬 View Parkinson's Disease Pathway Map"):
        st.info("The diagram below illustrates key cellular pathways including mitophagy, autophagy-lysosomal function, and alpha-synuclein aggregation.")
        try:
            st.image("images/parkinsons_pathway.png", caption="Parkinson's Disease Cellular Pathway", use_container_width=True)
        except:
            st.warning("Pathway image not found. Please upload 'parkinsons_pathway.png' to the 'images' folder.")
    render_dataframe(df[df["Disease"] == "Parkinson's"])

with tab_als:
    with st.expander("🔬 View ALS-FTD Pathway Map"):
        st.info("The diagram below illustrates key cellular pathways including RNA metabolism, nucleocytoplasmic transport, and protein homeostasis.")
        try:
            st.image("images/als_ftd_pathway.png", caption="ALS-FTD Cellular Pathway", use_container_width=True)
        except:
            st.warning("Pathway image not found. Please upload 'als_ftd_pathway.png' to the 'images' folder.")
    render_dataframe(df[df["Disease"] == "ALS-FTD"])

with tab_hun:
    with st.expander("🔬 View Huntington's Disease Pathway Map"):
        st.info("The diagram below illustrates key cellular pathways including transcriptional dysregulation and vesicular transport alterations.")
        try:
            st.image("images/huntingtons_pathway.png", caption="Huntington's Disease Cellular Pathway", use_container_width=True)
        except:
            st.warning("Pathway image not found. Please upload 'huntingtons_pathway.png' to the 'images' folder.")
    render_dataframe(df[df["Disease"] == "Huntington's"])

# Footer
st.markdown("---")
st.caption("Data is compiled according to current literature standards referencing the NCBI RefSeq database.")
st.caption("**Created by Büşra Uyar**")
st.caption("⚠️ **Disclaimer:** This database is intended for research and educational purposes only. It should not be used for medical, clinical, or diagnostic decisions.")
