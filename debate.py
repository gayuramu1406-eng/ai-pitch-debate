from clients import ask_cohere, ask_groq
from personas import OWNER_SYSTEM, VC_SYSTEM

# Which model plays which character
OWNER = {
    "name": "Alex (Founder)",
    "system": OWNER_SYSTEM,
    "ask": ask_cohere,
}

VC = {
    "name": "Morgan (VC)",
    "system": VC_SYSTEM,
    "ask": ask_groq,
}


def build_messages(speaker, transcript, nudge=None):
    """
    Build the message list for the given speaker.
    - The speaker's own past turns -> 'assistant'
    - The other party's past turns  -> 'user' (prefixed with their name)
    - If a nudge is provided, it becomes the final 'user' message.
    - If no nudge and the last message is 'assistant', append a neutral
      'Continue.' user message (required by Cohere's compatibility API).
    """
    messages = [{"role": "system", "content": speaker["system"]}]

    for entry in transcript:
        if entry["speaker"] == speaker["name"]:
            messages.append({
                "role": "assistant",
                "content": entry["content"],
            })
        else:
            messages.append({
                "role": "user",
                "content": f"[{entry['speaker']}]: {entry['content']}",
            })

    if nudge:
        messages.append({"role": "user", "content": nudge})
    elif messages[-1]["role"] == "assistant":
        messages.append({"role": "user", "content": "Continue."})

    return messages


def take_turn(speaker, transcript, nudge=None):
    """Have the speaker produce one reply, append it to transcript, return it."""
    messages = build_messages(speaker, transcript, nudge=nudge)
    reply = speaker["ask"](messages)
    transcript.append({
        "speaker": speaker["name"],
        "content": reply,
    })
    return reply