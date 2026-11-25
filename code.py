"""K&G Vision AI Coder — Project Genesis #001.
Project maintainer: Kaio Gabriel da Silva (Kgasil).
Educational inspiration: DSA AI Coder, Data Science Academy.
Public implementation prepared with ChatGPT assistance.
"""

import streamlit as st
from groq import Groq

MODEL = "openai/gpt-oss-20b"
INSTRUCTIONS = (
    "Você é o K&G Coder, um tutor de Python para iniciantes. "
    "Ajude com programação e recuse educadamente assuntos fora do tema. "
    "Explique o conceito em linguagem simples, apresente exemplos de código "
    "comentados quando úteis, explique seu funcionamento e indique referências "
    "oficiais relevantes. Não invente referências."
)


def generate_answer(api_key, history):
    """Send the conversation to Groq and return the assistant's answer."""
    conversation = [{"role": "system", "content": INSTRUCTIONS}, *history]
    response = Groq(api_key=api_key).chat.completions.create(
        model=MODEL,
        messages=conversation,
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content or "Nenhuma resposta recebida."


def main():
    st.set_page_config(page_title="K&G Vision AI Coder", page_icon="🤖", layout="wide")
    st.title("K&G Vision — AI Coder")
    st.caption("Project Genesis #001 | Seu assistente de estudos em Python")
    history = st.session_state.setdefault("history", [])

    with st.sidebar:
        st.header("Configurações")
        key = st.text_input("Chave da API Groq", type="password")
        st.markdown("[Obtenha sua chave na Groq](https://console.groq.com/keys)")
        if st.button("Limpar conversa"):
            history.clear()
        st.info("Confira as respostas da IA antes de utilizar o código sugerido.")
        st.markdown("Projeto educacional inspirado no DSA AI Coder.")

    for entry in history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    if not key.strip():
        st.info("Insira uma chave da API na barra lateral para começar.")

    question = st.chat_input("Qual é sua dúvida sobre Python?", disabled=not key.strip())
    if question:
        history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Preparando a resposta..."):
                    answer = generate_answer(key.strip(), history)
            except Exception:
                st.error("Não foi possível obter uma resposta. Confira sua chave e conexão.")
            else:
                history.append({"role": "assistant", "content": answer})
                st.markdown(answer)


if __name__ == "__main__":
    main()
