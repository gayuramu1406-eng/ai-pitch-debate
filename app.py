import time
import streamlit as st
from debate import take_turn, OWNER, VC

st.set_page_config(page_title="AI Pitch Debate", page_icon="🎤", layout="wide")

st.title("🎤 AI Pitch Debate: Founder vs VC")
st.caption("Two LLMs. One pitch. One verdict.")


def typewriter(text, placeholder, delay=0.04):
    """Stream text word-by-word into a Streamlit placeholder."""
    # Escape $ so Streamlit doesn't treat it as LaTeX math
    safe_text = text.replace("$", "\\$")
    words = safe_text.split(" ")
    shown = ""
    for word in words:
        shown += word + " "
        placeholder.markdown(shown + "▌")
        time.sleep(delay)
    placeholder.markdown(shown.strip())


# --- Inputs ---
idea = st.text_input(
    "Startup idea",
    value=(
        "An AI medical scribe that listens to patient consultations and "
        "automatically generates clinical notes, prescriptions, and "
        "follow-up plans — saving doctors 2 hours of admin work per day."
    ),
)
rounds = st.slider("Debate rounds", 1, 5, 3)
speed = st.slider("Typing speed (seconds per word)", 0.0, 0.15, 0.04, 0.01)

start = st.button("🚀 Start Pitch", type="primary")


# --- Layout: two columns ---
col_owner, col_vc = st.columns(2)

with col_owner:
    st.subheader("👨‍💼 Alex (Founder)")
    st.caption("Cohere · command-a-03-2025")
    owner_box = st.container()

with col_vc:
    st.subheader("💼 Morgan (VC)")
    st.caption("Groq · openai/gpt-oss-20b")
    vc_box = st.container()

# Verdict banner placeholder (below columns)
verdict_placeholder = st.empty()


def speak(speaker, box, nudge=None, transcript=None):
    """
    Have the speaker respond, show a spinner while thinking,
    then typewriter their reply into the chat.
    """
    with box:
        with st.chat_message(speaker["name"]):
            with st.spinner(f"{speaker['name']} is thinking..."):
                reply = take_turn(speaker, transcript, nudge=nudge)
            ph = st.empty()
            typewriter(reply, ph, delay=speed)
    return reply


# --- Run the debate ---
if start:
    transcript = []

    # 1. Opening pitch from Alex
    opening_prompt = (
        f"You are about to pitch your startup to a VC. "
        f"Your startup idea: {idea}. Give a concise opening pitch."
    )
    speak(OWNER, owner_box, nudge=opening_prompt, transcript=transcript)

    # 2. Alternating rounds
    for r in range(1, rounds + 1):
        # VC asks questions — explicitly told NOT to give a verdict yet
        vc_nudge = "Continue the diligence. Do NOT give a verdict yet."
        speak(VC, vc_box, nudge=vc_nudge, transcript=transcript)

        # Founder responds (no nudge needed — history ends with VC's turn)
        speak(OWNER, owner_box, transcript=transcript)

    # 3. Final verdict from Morgan
    verdict_nudge = (
        "The meeting is now over. Give your final decision in this exact structure:\n"
        "1. Strongest point in the founder's pitch (1 sentence)\n"
        "2. Biggest concern (1 sentence)\n"
        "3. Why that concern is or isn't a dealbreaker (1-2 sentences)\n"
        "4. Final line, exactly: 'VERDICT: DEAL' or 'VERDICT: NO DEAL'"
    )
    final_reply = speak(VC, vc_box, nudge=verdict_nudge, transcript=transcript)

    # 4. Verdict banner
    if "VERDICT: NO DEAL" in final_reply:
        verdict_placeholder.error("## 🔴 VERDICT: NO DEAL")
    elif "VERDICT: DEAL" in final_reply:
        verdict_placeholder.success("## 🟢 VERDICT: DEAL")
    else:
        verdict_placeholder.warning("## ⚪ VERDICT: UNKNOWN")

    # 5. Download button
    transcript_text = "\n\n".join(
        f"[{t['speaker']}]\n{t['content']}" for t in transcript
    )
    st.download_button(
        "📄 Download transcript",
        transcript_text,
        file_name="pitch_debate.txt",
        mime="text/plain",
    )