import streamlit as st
from datetime import datetime, date
import random
import requests
import json

# --- CONFIGURAÇÃO DA API (Preencha aqui com os dados da Z-API) ---
ZAPI_ID = "SEU_ID_DA_INSTANCIA"
ZAPI_TOKEN = "SEU_TOKEN_DA_ZAPI"
NUMEROS_DESTINO = ["5531993276411", "5531991927401"]

st.set_page_config(page_title="BARGEND | Sistema Pro", page_icon="✂️", layout="wide")

# --- FUNÇÃO DE DISPARO REAL (INVISÍVEL PARA O CLIENTE) ---
def disparar_whatsapp(mensagem):
    url = f"https://api.z-api.io/instances/{ZAPI_ID}/token/{ZAPI_TOKEN}/send-text"
    headers = {'Content-Type': 'application/json'}
    
    for numero in NUMEROS_DESTINO:
        payload = {
            "phone": numero,
            "message": mensagem
        }
        try:
            # O servidor do site avisa o servidor da API, que manda o Zap
            requests.post(url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            print(f"Erro ao enviar: {e}")

# --- BANCO DE DADOS EM SESSÃO ---
if 'agenda' not in st.session_state:
    st.session_state.agenda = []

UNIDADES = {
    "Unidade 1 - Bairro Ipê": {"barbeiros": ["Thailo", "Jefferson", "Junior"]},
    "Unidade 2 - Bairro Boa Vista": {"barbeiros": ["Davi", "Cabral"]}
}

# --- INTERFACE ---
st.title("BARGEND - Agendamento Inteligente")

with st.form("form_agendamento"):
    unidade = st.selectbox("Escolha a Unidade", list(UNIDADES.keys()))
    barbeiro = st.selectbox("Profissional", UNIDADES[unidade]["barbeiros"])
    data = st.date_input("Data", min_value=date.today())
    hora = st.selectbox("Horário", ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"])
    servico = st.selectbox("Serviço", ["Corte", "Barba", "Combo VIP"])
    nome_cliente = st.text_input("Seu Nome")
    
    enviar = st.form_submit_button("CONFIRMAR AGENDAMENTO")

    if enviar:
        if nome_cliente:
            id_agend = random.randint(1000, 9999)
            
            # Salva no sistema
            st.session_state.agenda.append({
                "id": id_agend, "cliente": nome_cliente, "unidade": unidade, 
                "barbeiro": barbeiro, "data": str(data), "hora": hora
            })
            
            # Monta a mensagem
            texto = (f"🚨 *NOVO AGENDAMENTO BARGEND*\n\n"
                     f"👤 Cliente: {nome_cliente}\n"
                     f"✂️ Serviço: {servico}\n"
                     f"📅 Data: {data.strftime('%d/%m/%Y')}\n"
                     f"⏰ Hora: {hora}\n"
                     f"📍 Unidade: {unidade}\n"
                     f"🧔 Barbeiro: {barbeiro}\n"
                     f"🆔 ID: {id_agend}")
            
            # DISPARO 100% AUTOMÁTICO VIA API
            disparar_whatsapp(texto)
            
            st.success(f"Feito, {nome_cliente}! Agendamento confirmado. ID: {id_agend}")
            st.balloons()
        else:
            st.error("Por favor, preencha seu nome.")

# --- ÁREA ADM ---
st.sidebar.title("Painel de Controle")
senha = st.sidebar.text_input("Senha ADM", type="password")
if senha == "ramos657":
    st.sidebar.success("Acesso Liberado")
    st.write("### Lista de Agendamentos (Agenda do App)")
    if st.session_state.agenda:
        st.table(st.session_state.agenda)
    else:
        st.info("Nenhum agendamento registrado nesta sessão.")
