import streamlit as st

def render():
    """Renders the FAQs page."""
    with st.container(border=True):
        st.subheader("❓ Frequently Asked Questions (FAQs)")
        st.markdown("""
        Here are some common questions and answers related to miscarriage.

        ---

        **Q: What is a miscarriage?**
        A: A miscarriage is the spontaneous loss of a pregnancy before the 20th week. It's a common occurrence, affecting about 10-20% of known pregnancies.

        ---

        **Q: What causes miscarriage?**
        A: Most miscarriages (around 80%) are caused by chromosomal abnormalities in the embryo, meaning the baby isn't developing as it should. Other causes can include hormonal imbalances, uterine abnormalities, infections, or certain chronic health conditions in the mother. Lifestyle factors generally do not cause miscarriage.

        ---

        **Q: Is it my fault if I have a miscarriage?**
        A: Absolutely not. Miscarriages are rarely caused by anything a person did or didn't do. It's a common misconception that stress, exercise, or minor falls can cause miscarriage, but this is generally untrue. The vast majority are due to factors beyond anyone's control.

        ---

        **Q: What are the common symptoms of miscarriage?**
        A: Common symptoms include vaginal bleeding (which can range from light spotting to heavy bleeding), abdominal cramping or pain, and the passing of tissue or fluid from the vagina. However, some people may experience a "missed miscarriage" with no outward symptoms.

        ---

        **Q: How long does the physical recovery take after a miscarriage?**
        A: Physical recovery varies for each individual, but it typically takes a few days to a few weeks. Bleeding and cramping may last for a week or two. It's important to follow your healthcare provider's advice for post-miscarriage care.

        ---

        **Q: How long does the emotional recovery take?**
        A: Emotional recovery is highly individual and can take much longer than physical recovery. Grief is a natural response, and it's normal to experience a range of emotions, including sadness, anger, guilt, and anxiety. There's no set timeline for healing, and seeking emotional support can be very helpful.

        ---

        **Q: When can I try to conceive again after a miscarriage?**
        A: This is a question best answered by your healthcare provider, as it depends on individual circumstances and the type of miscarriage. Medically, many providers suggest waiting for at least one normal menstrual cycle before trying again, but emotional readiness is also a key factor.
        """)
