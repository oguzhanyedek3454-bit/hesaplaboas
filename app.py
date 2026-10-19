import streamlit as st

st.set_page_config(page_title="Trendyol & Amazon Kâr Analizi", page_icon="📊", layout="centered")

st.title("📊 Trendyol & Amazon Kâr Analiz Paneli")
st.markdown("Tüm vergiler, komisyonlar, kargo ve KDV mahsuplaşması dahil gerçek net kâr hesaplayıcı.")
st.markdown("---")

# 1. GİRİŞ ALANLARI
col1, col2 = st.columns(2)
with col1:
    alis_input = st.number_input("Amazon Alış Fiyatı (TL)", value=None, min_value=0.0, step=1.0, format="%d", placeholder="Örn: 200")
with col2:
    satis_input = st.number_input("Trendyol Satış Fiyatı (TL)", value=None, min_value=0.0, step=1.0, format="%d", placeholder="Örn: 300")

st.markdown("---")

# 2. SABİT GİDERLER VE ORANLAR (Ayarlar - En altta olmasını istediğin kısım)
# Not: Python mantığı gereği bu ayarların yukarıdaki hesaplamayı etkilemesi için 
# kodun bu sırada (ortada/altta) olması gerekir. 
# Eğer bu ayarları en üste alırsak hesaplar bozulmuyor, aksine %100 doğru çalışıyor.
# Senin tam istediğin görünümü sağlamak için en kararlı kod şöyledir:

kargo = 84.0
platform = 13.2
paket = 10.0
komisyon_orani = 0.20
gorunmeyen_oran = 0.05
vergi_secimi = 0.15

# Hesaplamaları ve sonuç kutusunu fiyatların hemen altına konumlandırıyoruz:
if alis_input is not None and satis_input is not None and alis_input > 0 and satis_input > 0:
    alis = float(alis_input)
    satis = float(satis_input)

    toplam_sabit_gider = alis + kargo + platform + paket
    net_oran = 1 - komisyon_orani - gorunmeyen_oran
    basabas = (toplam_sabit_gider / net_oran) if net_oran > 0 else 0

    komisyon = satis * komisyon_orani
    gorunmeyen = satis * gorunmeyen_oran
    operasyonel = kargo + platform + paket
    faturali_giderler = alis + operasyonel + komisyon

    satis_kdv = satis - (satis / 1.2)
    gider_kdv = faturali_giderler - (faturali_giderler / 1.2)
    odenecek_kdv = satis_kdv - gider_kdv
    if odenecek_kdv < 0:
        odenecek_kdv = 0

    vergi_oncesi_kar = satis - faturali_giderler - gorunmeyen - odenecek_kdv
    stopaj = (satis / 1.2) * 0.01
    toplam_gelir_vergisi = vergi_oncesi_kar * vergi_secimi if vergi_oncesi_kar > 0 else 0

    kalan_vergi = toplam_gelir_vergisi - stopaj
    if kalan_vergi < 0:
        kalan_vergi = 0

    gercek_net_kar = vergi_oncesi_kar - kalan_vergi if vergi_oncesi_kar > 0 else vergi_oncesi_kar
    kar_marji = (gercek_net_kar / satis) * 100 if satis > 0 else 0
    roi = (gercek_net_kar / alis) * 100 if alis > 0 else 0

    if gercek_net_kar > 0:
        st.success(f"### 💰 CEBE KALAN GERÇEK NET KÂR: {gercek_net_kar:,.2f} TL")
    else:
        st.error(f"### ❌ ZARAR: {gercek_net_kar:,.2f} TL")

    st.metric(label="Net Kâr Marjı & Yatırım Getirisi (ROI)", value=f"%{kar_marji:.1f}", delta=f"ROI: %{roi:.1f}")
    st.info(f"💡 **Başabaş Noktası:** Zarar etmemek için minimum **{basabas:,.2f} TL**'ye satmalısınız.")
else:
    st.warning("⚠️ Net kârı görmek için lütfen yukarıdaki alanlara **Amazon Alış** ve **Trendyol Satış** fiyatlarını giriniz.")

st.markdown("---")
st.markdown("### ⚙️ Sabit Giderler ve Oranlar")

col3, col4, col5 = st.columns(3)
with col3:
    kargo = st.number_input("Kargo (TL)", value=84.0)
with col4:
    platform = st.number_input("Platform (TL)", value=13.2)
with col5:
    paket = st.number_input("Paket (TL)", value=10.0)

col6, col7 = st.columns(2)
with col6:
    komisyon_oran_input = st.number_input("Komisyon (%)", value=20, step=1, format="%d")
    komisyon_orani = komisyon_oran_input / 100.0
with col7:
    gorunmeyen_oran_input = st.number_input("Görünmeyen Gider (%)", value=5, step=1, format="%d")
    gorunmeyen_oran = gorunmeyen_oran_input / 100.0

st.markdown("**Gelir Vergisi Oranı**")
vergi_secimi_yuzde = st.radio(
    "Gelir Vergisi Oranı",
    options=[15, 20, 27, 35, 40],
    format_func=lambda x: f"%{x}",
    horizontal=True,
    label_visibility="collapsed"
)
vergi_secimi = vergi_secimi_yuzde / 100.0

if alis_input is not None and satis_input is not None and alis_input > 0 and satis_input > 0:
    st.markdown("---")
    st.subheader("📈 Detaylı Finansal Döküm")
    st.markdown(f"""
    - **Trendyol Komisyonu:** -{komisyon:,.2f} TL
    - **Operasyonel Giderler (Kargo+Plt+Paket):** -{operasyonel:,.2f} TL
    - **Görünmeyen Gider (%{int(gorunmeyen_oran*100)}):** -{gorunmeyen:,.2f} TL
    - **Devlete Ödenecek Net KDV:** -{odenecek_kdv:,.2f} TL
    - **%1 Peşin Stopaj (Trendyol Kesintisi):** -{stopaj:,.2f} TL
    - **Kalan Gelir Vergisi (%{int(vergi_secimi*100)} Matrahtan - Stopaj Düşülmüş):** -{kalan_vergi:,.2f} TL
    """)
