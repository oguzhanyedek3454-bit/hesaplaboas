import streamlit as st

st.set_page_config(page_title="Trendyol & Amazon Kâr Analizi", page_icon="📊", layout="centered")

st.title("📊 Trendyol & Amazon Kâr Analiz Paneli")
st.markdown("Tüm vergiler, komisyonlar, kargo ve KDV mahsuplaşması dahil gerçek net kâr hesaplayıcı.")
st.markdown("---")

# 1. GİRİŞ ALANLARI (En üstte)
col1, col2 = st.columns(2)
with col1:
    alis_input = st.number_input("Amazon Alış Fiyatı (TL)", value=None, min_value=0.0, step=1.0, format="%d", placeholder="Örn: 200")
with col2:
    satis_input = st.number_input("Trendyol Satış Fiyatı (TL)", value=None, min_value=0.0, step=1.0, format="%d", placeholder="Örn: 300")

st.markdown("---")

# 2. ALT KISIMDAKİ AYARLARIN DEĞERLERİNİ ÖNCE BURADA TANIMLIYORUZ (Hesaplama için)
# (Aşağıdaki widget'lardan gelecek değerler anlık olarak buraya yansıyacak)

# Not: Python yukarıdan aşağıya okuduğu için widget'ları aşağıya koyacağız, 
# ancak Streamlit her etkileşimde sayfayı yeniden çalıştırdığı için aşağıdaki değerleri üstteki hesapta kullanabiliriz.
