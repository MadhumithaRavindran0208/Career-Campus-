"""
ui_components.py
Restrained, Professional Enterprise Design System for CareerCompass AI.
Calibrated for corporate career, talent intelligence, and executive hiring products.
Built on a disciplined slate surface hierarchy, WCAG-compliant typography,
and focused functional status indicators.
"""

import streamlit as st

def inject_custom_theme():
    """Injects restrained, WCAG-compliant enterprise color tokens and styles."""
    st.markdown(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        /* Named Surface Palette */
        --surface-canvas: #0D1117;
        --surface-card: #161C24;
        --surface-elevated: #1F2633;
        --surface-hover: #263040;
        
        /* Borders & Dividers */
        --border-subtle: #222B38;
        --border-card: #2B3545;
        --border-interactive: #3B82F6;
        
        /* Text Hierarchy (WCAG AAA / AA Compliant) */
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        
        /* Primary & Secondary Brand Accents */
        --accent-primary: #2563EB;
        --accent-interactive: #3B82F6;
        --accent-link: #60A5FA;
        --accent-secondary: #64748B;
        
        /* Functional Status Accents */
        --status-success: #10B981;
        --status-success-text: #34D399;
        --status-warning: #F59E0B;
        --status-warning-text: #FBBF24;
        --status-danger: #EF4444;
        --status-danger-text: #F87171;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
        background-color: var(--surface-canvas);
        -webkit-font-smoothing: antialiased;
    }
    
    .stApp {
        background-color: var(--surface-canvas) !important;
        background-image: none !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111620 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        padding: 4px 0 !important;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    p, span, label {
        color: var(--text-secondary);
        font-size: 14px;
        line-height: 1.55;
    }
    
    /* Hero Header Banner */
    .hero-banner {
        background: var(--surface-card);
        border: 1px solid var(--border-card);
        border-radius: 12px;
        padding: 26px 30px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
    }
    
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--accent-link);
        background: rgba(37, 99, 235, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.25);
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    
    /* Restrained Panel Card */
    .ui-panel {
        background: var(--surface-card);
        border: 1px solid var(--border-card);
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
        transition: border-color 0.15s ease;
    }
    .ui-panel:hover {
        border-color: #3B475C;
    }
    
    /* Restrained Metric Cards */
    .metric-card {
        background: var(--surface-card);
        border: 1px solid var(--border-card);
        border-radius: 10px;
        padding: 16px 20px;
        min-height: 102px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        transition: border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: var(--border-interactive);
    }
    .metric-title {
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-muted);
        font-weight: 600;
    }
    .metric-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 4px;
        letter-spacing: -0.02em;
    }
    .metric-sub {
        font-size: 12px;
        color: var(--accent-link);
        font-weight: 500;
        margin-top: 3px;
    }
    
    /* Disciplined Status Badges */
    .badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-emerald {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    .badge-rose {
        background: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
    }
    .badge-cyan, .badge-blue {
        background: rgba(37, 99, 235, 0.12);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    .badge-indigo {
        background: rgba(100, 116, 139, 0.15);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }
    
    /* Professional Skill Pills */
    .skill-pill {
        display: inline-flex;
        align-items: center;
        background: var(--surface-elevated);
        border: 1px solid var(--border-card);
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 12px;
        font-weight: 500;
        color: var(--text-primary);
        margin: 2px 4px 2px 0;
    }
    .skill-pill-missing {
        display: inline-flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 12px;
        font-weight: 500;
        color: #FDE047;
        margin: 2px 4px 2px 0;
    }
    
    /* Explanatory Rule Callouts */
    .rule-box {
        background: var(--surface-elevated);
        border: 1px solid var(--border-card);
        border-left: 3px solid var(--accent-interactive);
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 13px;
        line-height: 1.5;
        color: var(--text-primary);
    }
    
    /* Form Inputs, Select Boxes & Text Areas */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div {
        background-color: var(--surface-elevated) !important;
        border: 1px solid var(--border-card) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        font-size: 13.5px !important;
    }
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--accent-interactive) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Professional Action Buttons */
    .stButton>button {
        background-color: var(--accent-primary) !important;
        background-image: none !important;
        color: #FFFFFF !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
        transition: background-color 0.15s ease !important;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1E40AF !important;
    }
    
    .stDownloadButton>button {
        background-color: var(--surface-elevated) !important;
        border: 1px solid var(--border-card) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        transition: border-color 0.15s ease !important;
    }
    .stDownloadButton>button:hover {
        background-color: var(--surface-hover) !important;
        border-color: var(--border-interactive) !important;
    }
    
    /* Streamlit Native Expanders */
    .streamlit-expanderHeader {
        background-color: var(--surface-elevated) !important;
        border: 1px solid var(--border-card) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
    }
    .streamlit-expanderContent {
        background-color: var(--surface-card) !important;
        border: 1px solid var(--border-card) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Code Blocks */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #111620 !important;
        color: var(--accent-link) !important;
        border: 1px solid var(--border-card) !important;
        border-radius: 6px !important;
    }
    
    /* Dataframe Table Headers & Cells */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-card) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }
    
    hr {
        border-color: var(--border-subtle) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero(title: str, subtitle: str, tag: str = "CAREER INTELLIGENCE PLATFORM"):
    """Renders a restrained, professional header banner."""
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-tag">{tag}</div>
        <h1 style="margin: 0 0 8px; font-size: clamp(22px, 2.5vw, 28px); font-weight: 600; color: #F1F5F9;">{title}</h1>
        <p style="color: #94A3B8; font-size: 14px; line-height: 1.6; margin: 0; max-width: 960px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric(label: str, value: str, note: str = ""):
    """Renders a restrained enterprise metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{label}</div>
        <div class="metric-num">{value}</div>
        <div class="metric-sub">{note}</div>
    </div>
    """, unsafe_allow_html=True)
