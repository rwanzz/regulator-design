import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Regulator Design AI Assistant", page_icon="🌊")

st.title("🌊 Regulator Design Assistant")
st.write("مساعد ذكي لتصميم المنظمات الهيدروليكية وحساب الأبعاد المبدئية")

st.divider()

# الشريط الجانبي لإدخال البيانات
st.sidebar.header("📥 مدخلات التصميم")

Q = st.sidebar.number_input("التصرف المار Q (m³/s)", min_value=0.1, value=25.0, step=0.5)
USWL = st.sidebar.number_input("منسوب الأمام U.S.W.L (m)", value=12.5, step=0.1)
DSWL = st.sidebar.number_input("منسوب الخلف D.S.W.L (m)", value=12.0, step=0.1)
C_bligh = st.sidebar.number_input("معامل بلع C (Bligh's Coefficient)", min_value=1.0, value=12.0, step=0.5)

# قيم افتراضية للتصميم
st.sidebar.subheader("⚙️ فرضيات التصميم")
S_gate = st.sidebar.slider("عرض الفتحة الواحدة S (m)", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
V_assumed = st.sidebar.slider("السرعة المسموحة V (m/s)", min_value=1.0, max_value=2.5, value=1.5, step=0.1)

# زر إجراء الحسابات
if st.button("🚀 احسب أبعاد المنظم"):
    # 1. حساب فرق المنسوب (Head Loss)
    dH = USWL - DSWL
    
    if dH <= 0:
        st.error("❌ خطأ: يجب أن يكون منسوب الأمام (U.S.W.L) أكبر من منسوب الخلف (D.S.W.L)")
    else:
        # 2. حساب مساحة الفتحات وعددها
        A_req = Q / V_assumed
        d_water = DSWL - (DSWL - 2.0)  # عمق الميه المبدئي (فرضاً)
        
        # حساب عدد الفتحات التقريبي
        n = round(A_req / (S_gate * d_water))
        if n < 1: 
            n = 1
            
        # 3. حساب طول الفرشة مانعة التسرب (Bligh's Creep Line)
        L_creep = C_bligh * dH
        
        # عرض النتائج في بطاقات منظمّة
        st.success("✅ تم إجراء الحسابات الهيدروليكية بنجاح!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="عدد الفتحات (N)", value=f"{n} فتحات")
        col2.metric(label="عرض الفتحة (S)", value=f"{S_gate} m")
        col3.metric(label="فرق المنسوب (ΔH)", value=f"{dH:.2f} m")
        
        st.subheader("📋 ملخص نتائج التصميم:")
        st.markdown(f"""
        * **طول خط التسرب المطلوب (Creep Length):** `{L_creep:.2f}` متر (لحماية المنشأ من الـ Piping).
        * **المساحة الهيدروليكية الكلية المطلوبة:** `{A_req:.2f}` m².
        * **السرعة الفعلية التقريبية:** `{Q / (n * S_gate * d_water):.2f}` m/s.
        """)

# قسم توضيحي أسفل الصفحة
with st.expander("ℹ️ نبذة عن المعادلات المستخدمة"):
    st.write("""
    - **Bligh's Creep Theory:** $L = C \\times \\Delta H$
    - **Continuity Equation:** $Q = A \\times V$
    """)
