import streamlit as st
from datetime import datetime

# =====================================
# PHYSIOCARE - TINGKATAN 2 ASK PROJECT
# =====================================

st.set_page_config(
    page_title="PhysioCare",
    page_icon="🩵",
    layout="centered"
)

# =====================================
# DESIGN
# =====================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #e8f7ff, #ffffff);
}
h1 {
    color: #247ba0;
    text-align: center;
}
h2, h3 {
    color: #287da5;
}
.stButton button {
    background-color: #55afd1;
    color: white;
    border-radius: 12px;
    border: none;
    width: 100%;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# SESSION MEMORY
# =====================================

if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "name" not in st.session_state:
    st.session_state.name = ""

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================
# CHAT FUNCTIONS
# =====================================

def bot(message):
    st.session_state.messages.append(
        {"role": "assistant", "content": message}
    )


def user(message):
    st.session_state.messages.append(
        {"role": "user", "content": message}
    )


# =====================================
# HEADER
# =====================================

st.title("🩵 PhysioCare")

st.markdown(
    "<center><b>Every step towards feeling better matters.</b></center>",
    unsafe_allow_html=True
)

st.write("Your friendly physiotherapy companion!")

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# =====================================
# JUJUKAN: WELCOME
# =====================================

if st.session_state.step == "welcome":

    st.info(
        "👋 Hello! Welcome to PhysioCare. "
        "I'm here to listen and help you. "
        "What should I call you?"
    )

    with st.form("welcome_form"):

        name = st.text_input("Enter your name")

        submit = st.form_submit_button("Let's begin 💙")

    if submit:

        if name.strip() == "":
            st.warning("Please enter your name.")

        else:
            st.session_state.name = name.strip()

            user(name)
            bot(
                f"Nice to meet you, {name}! 😊 "
                "Which part of your body is bothering you today?"
            )

            st.session_state.step = "body"
            st.rerun()


# =====================================
# JUJUKAN: BODY PART
# =====================================

elif st.session_state.step == "body":

    st.subheader(
        f"How are you feeling, {st.session_state.name}? 💙"
    )

    with st.form("body_form"):

        body = st.radio(
            "Choose the affected body part:",
            [
                "Neck",
                "Shoulder",
                "Back",
                "Knee",
                "Wrist",
                "Ankle",
                "Other"
            ]
        )

        submit = st.form_submit_button("Continue")

    if submit:

        st.session_state.answers["body"] = body

        user(body)
        bot(
            "Thank you for sharing that with me. "
            "How painful is it from 1 to 10?"
        )

        st.session_state.step = "pain"
        st.rerun()


# =====================================
# JUJUKAN: PAIN LEVEL
# =====================================

elif st.session_state.step == "pain":

    st.subheader("🩺 Pain Assessment")

    with st.form("pain_form"):

        pain = st.slider(
            "Rate your pain level:",
            min_value=1,
            max_value=10,
            value=3
        )

        st.caption(
            "1 = Mild pain | 10 = Extremely painful"
        )

        submit = st.form_submit_button("Continue")

    if submit:

        st.session_state.answers["pain"] = pain

        user(f"Pain level: {pain}/10")

        bot(
            "I understand. How long have you "
            "been experiencing this discomfort?"
        )

        st.session_state.step = "duration"
        st.rerun()


# =====================================
# JUJUKAN: DURATION
# =====================================

elif st.session_state.step == "duration":

    with st.form("duration_form"):

        duration = st.radio(
            "How long have you experienced the discomfort?",
            [
                "Just started",
                "A few hours",
                "1–2 days",
                "3–7 days",
                "1–4 weeks",
                "More than a month"
            ]
        )

        submit = st.form_submit_button("Continue")

    if submit:

        st.session_state.answers["duration"] = duration

        user(duration)

        bot(
            "One more important question. "
            "Are you experiencing any warning symptoms?"
        )

        st.session_state.step = "warning"
        st.rerun()


# =====================================
# JUJUKAN: WARNING SYMPTOMS
# =====================================

elif st.session_state.step == "warning":

    with st.form("warning_form"):

        warning = st.multiselect(
            "Select all symptoms that apply:",
            [
                "Severe or sudden pain",
                "Significant swelling",
                "Numbness or tingling",
                "Difficulty moving",
                "Pain after a serious injury",
                "None of these"
            ]
        )

        submit = st.form_submit_button(
            "See my guidance 💙"
        )

    if submit:

        if len(warning) == 0:

            st.warning("Please select at least one option.")

        elif "None of these" in warning and len(warning) > 1:

            st.warning(
                "Select 'None of these' only if "
                "you have no warning symptoms."
            )

        else:

            st.session_state.answers["warning"] = warning

            user(", ".join(warning))

            bot(
                "Thank you for answering everything! "
                "Let me check your responses. 💙"
            )

            st.session_state.step = "result"
            st.rerun()


# =====================================
# PILIHAN + PILIHAN BERSARANG
# PERSONALIZED GUIDANCE
# =====================================

elif st.session_state.step == "result":

    name = st.session_state.name
    body = st.session_state.answers["body"]
    pain = st.session_state.answers["pain"]
    warning = st.session_state.answers["warning"]

    st.subheader("💙 Your Personalised Guidance")

    st.write(f"Hello, {name}! Here is your guidance.")

    # PILIHAN: WARNING SYMPTOMS

    if "None of these" not in warning:

        st.error(
            "⚠️ Warning symptoms detected. "
            "Please seek medical assessment. "
            "Do not attempt exercises."
        )

        # PILIHAN BERSARANG

        if (
            "Severe or sudden pain" in warning
            or "Pain after a serious injury" in warning
            or "Difficulty moving" in warning
        ):

            st.warning(
                "Please seek urgent medical attention."
            )

    else:

        # IF, ELIF, ELSE: PAIN LEVEL

        if pain <= 3:

            st.success(
                "Your reported pain level is mild. "
                "Gentle movement may be comfortable. "
                "Stop if pain increases."
            )

        elif pain <= 6:

            st.warning(
                "Your reported pain level is moderate. "
                "Avoid painful movements and consider "
                "consulting a physiotherapist."
            )

        else:

            st.error(
                "Your reported pain level is high. "
                "Please seek prompt medical assessment."
            )

        # PILIHAN BERSARANG: BODY PART

        if pain <= 3:

            if body == "Knee":

                st.info("🦵 Knee tip: Avoid forcing painful bending.")

            elif body == "Neck":

                st.info("🧍 Neck tip: Avoid sudden neck movements.")

            elif body == "Shoulder":

                st.info("💪 Shoulder tip: Avoid painful lifting.")

            elif body == "Back":

                st.info("Back tip: Avoid movements that increase pain.")

            elif body == "Wrist":

                st.info("✋ Wrist tip: Avoid painful gripping.")

            elif body == "Ankle":

                st.info("🦶 Ankle tip: Avoid painful weight-bearing.")

            else:

                st.info("Please seek professional guidance.")

    # SAVE HISTORY

    st.session_state.history.append({
        "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Body Part": body,
        "Pain Level": f"{pain}/10",
        "Duration": st.session_state.answers["duration"]
    })

    st.success("Assessment completed! 💙")

    st.session_state.step = "another"


# =====================================
# ULANGAN: REPEAT ASSESSMENT
# =====================================

elif st.session_state.step == "another":

    st.subheader("🔄 What's next?")

    choice = st.radio(
        f"Would you like to check another body part, "
        f"{st.session_state.name}?",
        ["Yes", "No"]
    )

    if st.button("Continue"):

        if choice == "Yes":

            st.session_state.answers = {}
            st.session_state.step = "body"

            bot(
                f"Of course, {st.session_state.name}! 😊 "
                "Which other body part would you like to check?"
            )

            st.rerun()

        else:

            bot(
                f"Take care, {st.session_state.name}! 💙 "
                "Remember to listen to your body. "
                "Thank you for using PhysioCare!"
            )

            st.session_state.step = "goodbye"
            st.rerun()


# =====================================
# GOODBYE
# =====================================

elif st.session_state.step == "goodbye":

    st.success(
        f"Thank you for using PhysioCare, "
        f"{st.session_state.name}! 🩵"
    )

    if st.button("Start a new session"):

        st.session_state.name = ""
        st.session_state.answers = {}
        st.session_state.step = "welcome"
        st.session_state.messages = []

        st.rerun()


# =====================================
# PREVIOUS SESSIONS
# =====================================

st.divider()

st.subheader("📊 Previous Sessions")

if st.session_state.history:

    st.dataframe(
        st.session_state.history,
        use_container_width=True
    )

else:

    st.write("Your previous sessions will appear here.")


# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
    "⚕️ PhysioCare provides general guidance only. "
    "It cannot diagnose medical conditions or replace "
    "a qualified healthcare professional."
)
