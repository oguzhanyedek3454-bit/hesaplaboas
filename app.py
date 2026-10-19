import streamlit as st

st.set_page_config(page_title="Trendyol & Amazon Kâr Analizi", page_icon="📊", layout="centered")

st.title("📊 Trendyol & Amazon Kâr Analiz Paneli")
st.markdown("Tüm vergiler, komisyonlar, kargo ve KDV mahsuplaşması dahil gerçek net kâr hesaplayıcı.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    alis = st.number_input("Amazon Alış Fiyatı (TL - KDV Dahil)", value=400.0, step=10.0)
with col2:
    satis = st.number_input("Trendyol Satış Fiyatı (TL - KDV Dahil)", value=1000.0, step=10.0)

st.markdown("### ⚙️ Sabit Giderler ve Oranlar")
col3, col4, col5 = st.columns(3)
with col3:
    kargo = st.number_input("Kargo (TL)", value=84.0)
with col4:
    platform = st.number_input("Platform Bedeli (TL)", value=13.2)
with col5:
    paket = st.number_input("Paketleme (TL)", value=10.0)

col6, col7 = st.columns(2)
with col6:
    komisyon_orani = st.number_input("Trendyol Komisyonu (%)", value=20.0) / 100.0
with col7:
    gorunmeyen_oran = st.number_input("Görünmeyen Gider (%)", value=5.0) / 100.0

# Hesaplamalar
toplam_sabit_gider = alis + kargo + platform + paket
net_oran = 1 - komisyon_orani - gorunmeyen_oran
basabas = (toplam_sabit_gider / net_oran) if net_oran > 0 else 0

st.info(f"💡 **Başabaş Noktası:** Zarar etmemek için minimum **{basabas:,.2f} TL**'ye satmalısınız.")

komisyon = satis * komisyon_orani
gorunmeyen = satis * gorunmeyen_oran
operasyonel = kargo + platform + paket
faturali_giderler = alis + operasyonel + komisyon

odenecek_kdv = (satis - faturali_giderler) - ((satis - faturali_giderler) / 1.2)
if odenecek_kdv < 0:
    odenecek_kdv = 0

vergi_oncesi_kar = satis - faturali_giderler - gorunmeyen - odenecek_kdv

stopaj = (satis / 1.2) * 0.01
toplam_gelir_vergisi = vergi_oncesi_kar * 0.3 if vergi_oncesi_kar > 0 else 0
kalan_vergi = toplam_gelir_vergisi - stopaj
if kalan_vergi < 0:
    kalan_vergi = 0

gercek_net_kar = vergi_oncesi_kar - toplam_gelir_vergisi
kar_marji = (gercek_net_kar / satis) * 100 if satis > 0 else 0
roi = (gercek_net_kar / alis) * 100 if alis > 0 else 0

st.markdown("---")
st.subheader("📈 Finansal Döküm")

st.markdown(f"""
- **Trendyol Komisyonu:** -{komisyon:,.2f} TL
- **Operasyonel Giderler (Kargo+Plt+Paket):** -{operasyonel:,.2f} TL
- **Görünmeyen Gider (%5):** -{gorunmeyen:,.2f} TL
- **Devlete Ödenecek Net KDV:** -{odenecek_kdv:,.2f} TL
- **%1 Peşin Stopaj (Trendyol Kesintisi):** -{stopaj:,.2f} TL
- **Kalan Gelir Vergisi (%30 Matrahtan):** -{kalan_vergi:,.2f} TL
""")

if gercek_net_kar > 0:
    st.success(f"### 💰 CEBE KALAN GERÇEK NET KÂR: {gercek_net_kar:,.2f} TL")
else:
    st.error(f"### ❌ ZARAR: {gercek_net_kar:,.2f} TL")

st.metric(label="Net Kâr Marjı & Yatırım Getirisi (ROI)", value=f"%{kar_marji:.1f}", delta=f"ROI: %{roi:.1f}")
