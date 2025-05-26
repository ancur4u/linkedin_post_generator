import random
import streamlit as st
import urllib.parse
from openai import OpenAI

# Streamlit UI setup
st.set_page_config(page_title="📢 LinkedIn Post Generator", layout="centered")
st.title("📢 LinkedIn Post Generator")

# Step 1: Enter API Key
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Hashtag options
popular_tags = [
    "#AI", "#CareerGrowth", "#Leadership", "#Tech", "#Innovation",
    "#OpenToWork", "#MachineLearning", "#GenAI", "#Hiring"
]

# Step 2: Post content inputs
with st.form("form"):
    topic = st.text_input("📝 What's the post about?")
    emotion = st.selectbox("🎭 Tone", ["Grateful", "Proud", "Inspired", "Reflective", "Excited"])
    call_to_action = st.text_input("📣 Call to Action", placeholder="Let’s connect!")
    tags = st.multiselect("🏷 Choose Hashtags", popular_tags, default=["#AI", "#CareerGrowth"])
    extra_tags = st.text_input("➕ Extra Hashtags (comma-separated)", "")
    style = st.selectbox("🎨 Style", ["Make it more engaging", "Make it more professional", "Make it funnier"])
    submitted = st.form_submit_button("✨ Generate LinkedIn Post")

if submitted:
    # Merge all hashtags
    all_tags = tags + [
        f"#{tag.strip()}" if not tag.strip().startswith("#") else tag.strip()
        for tag in extra_tags.split(",") if tag.strip()
    ]
    final_tags = " ".join(sorted(set(all_tags)))

    # Emoji and intro line
    emojis = {
        "Grateful": "🙏", "Proud": "🔥", "Inspired": "✨",
        "Reflective": "🧠", "Excited": "🚀"
    }

    hooks = {
        "Grateful": ["Feeling grateful for this journey.", "Truly thankful for this opportunity."],
        "Proud": ["Big news to share!", "Proud of this milestone."],
        "Inspired": ["Inspired to keep pushing.", "This moment really moved me."],
        "Reflective": ["Taking a moment to reflect...", "Lessons learned recently..."],
        "Excited": ["Thrilled to share this!", "So excited to announce..."]
    }

    intro = random.choice(hooks[emotion])
    raw_post = f"""{emojis[emotion]} {intro}

{topic}

{call_to_action}

{final_tags}
"""

    # Call OpenAI
    try:
        prompt = f"Take the following LinkedIn post and {style.lower()} while preserving the emoji, topic, and hashtags:\n\"\"\"{raw_post}\"\"\""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        polished = response.choices[0].message.content.strip()

        # Output
        st.markdown("### ✅ Your LinkedIn Post")
        st.text_area("📋 Copy this post", polished, height=300, key="linkedin_post")

        st.markdown("✅ Now click below to open LinkedIn and paste your post:")

        st.markdown(f"""
        <a href="https://www.linkedin.com/feed/" target="_blank">
            <button style='background-color:#0a66c2; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px; cursor:pointer;'>
            🔗 Share on LinkedIn
            </button>
        </a>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error from OpenAI: {e}")