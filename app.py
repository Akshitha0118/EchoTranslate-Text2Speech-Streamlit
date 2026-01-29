import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# ---------------------------------------------
# READ LANGUAGE DATASET
# ---------------------------------------------
df = pd.read_csv(r'C:\Users\Admin\Desktop\multi lang trasnlate\language.csv')
df.dropna(inplace=True)

lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()

# Create dictionary: Language → ISO Code
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# ---------------------------------------------
# STREAMLIT UI
# ---------------------------------------------
st.set_page_config(page_title="Language Translator", layout="wide")
st.title("🌐 Multi-Language Translator with Indian Languages")

inputtext = st.text_area(
    "✍️ Enter text to translate",
    height=120
)

choice = st.sidebar.selectbox(
    "🌍 Select Language",
    langlist
)

# ---------------------------------------------
# SUPPORTED SPEECH LANGUAGES (gTTS)
# ---------------------------------------------
speech_langs = {
    # Common
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "bn": "Bengali",
    "ur": "Urdu",
    "pa": "Punjabi",
    "or": "Odia",
    "as": "Assamese",
    "ne": "Nepali",

    # Other supported
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese"
}

# ---------------------------------------------
# AUDIO DOWNLOAD FUNCTION
# ---------------------------------------------
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    return f'''
        <a href="data:application/octet-stream;base64,{bin_str}"
        download="{os.path.basename(bin_file)}">
        📥 Download {file_label}
        </a>
    '''

# ---------------------------------------------
# OUTPUT LAYOUT
# ---------------------------------------------
c1, c2 = st.columns([4, 3])

# ---------------------------------------------
# TRANSLATION LOGIC
# ---------------------------------------------
if inputtext.strip():
    try:
        translated_text = translate(
            inputtext,
            lang_array[choice]
        )

        with c1:
            st.subheader("📝 Translated Text")
            st.text_area(
                "",
                translated_text,
                height=220
            )

        # ---------------------------------------------
        # TEXT TO SPEECH (IF SUPPORTED)
        # ---------------------------------------------
        if lang_array[choice] in speech_langs:
            try:
                tts = gTTS(
                    text=translated_text,
                    lang=lang_array[choice],
                    slow=False
                )
                tts.save("lang.mp3")

                with c2:
                    st.subheader("🔊 Audio Output")
                    st.audio("lang.mp3")
                    st.markdown(
                        get_binary_file_downloader_html(
                            "lang.mp3", "Audio File"
                        ),
                        unsafe_allow_html=True
                    )

            except:
                with c2:
                    st.warning(
                        "⚠️ Text-to-Speech not supported for this language."
                    )
        else:
            with c2:
                st.info(
                    "ℹ️ Audio not available for this language."
                )

    except Exception as e:
        st.error(f"❌ Error: {e}")
