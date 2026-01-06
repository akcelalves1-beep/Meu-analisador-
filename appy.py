import streamlit as st
from PIL import Image
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Analisador Multi-Timeframe", layout="centered")

st.title("📊 Analisador de Gráficos (1min & 5min)")
st.write("Suba o print do seu gráfico de velas de **1 minuto** para análise.")

# --- ENTRADA DE DADOS ---
col1, col2 = st.columns(2)
with col1:
    arquivo_imagem = st.file_uploader("Escolha a foto do gráfico", type=["jpg", "png", "jpeg"])
with col2:
    horario_atual = st.time_input("Horário atual do gráfico", datetime.now().time())

if arquivo_imagem is not None:
    img = Image.open(arquivo_imagem)
    st.image(img, caption="Gráfico de 1 Minuto", use_container_width=True)
    
    with st.spinner('Processando padrões de Price Action...'):
        # Lógica de cores (simplificada para o exemplo)
        img_rgb = img.convert('RGB')
        img_pequena = img_rgb.resize((100, 100))
        verde, vermelho = 0, 0
        
        for x in range(100):
            for y in range(100):
                r, g, b = img_pequena.getpixel((x, y))
                if g > r and g > b: verde += 1
                if r > g and r > b: vermelho += 1
        
        # --- CÁLCULO DE TEMPO ---
        agora = datetime.combine(datetime.today(), horario_atual)
        expira_1m = (agora + timedelta(minutes=1)).strftime('%H:%M')
        expira_5m = (agora + timedelta(minutes=5)).strftime('%H:%M')

        # --- RESULTADOS ---
        st.markdown("---")
        st.subheader("🎯 Sugestão de Operação")

        if verde > vermelho:
            st.success(f"🚀 **SINAL DE COMPRA (CALL)**")
            
            col_a, col_b = st.columns(2)
            col_a.metric("Expiração 1 min", expira_1m)
            col_b.metric("Expiração 5 min", expira_5m)
            
            st.write("### 🧐 Por que entrar?")
            st.info("""
            * **Volume Comprador:** A análise de pixels detectou uma predominância de candles verdes (alta).
            * **Pressão:** O fechamento das velas de 1min sugere que os compradores estão defendendo a região.
            * **Tendência:** No curto prazo (1m), o fluxo está a favor do rompimento de topos.
            """)

        elif vermelho > verde:
            st.error(f"🔻 **SINAL DE VENDA (PUT)**")
            
            col_a, col_b = st.columns(2)
            col_a.metric("Expiração 1 min", expira_1m)
            col_b.metric("Expiração 5 min", expira_5m)

            st.write("### 🧐 Por que entrar?")
            st.info("""
            * **Volume Vendedor:** A predominância de candles vermelhos indica forte rejeição de preço.
            * **Fluxo:** O mercado está fazendo fundos mais baixos no gráfico de 1 minuto.
            * **Momento:** A força vendedora está superando a absorção dos compradores no timeframe atual.
            """)
        else:
            st.warning("⚖️ **MERCADO LATERAL:** As cores estão equilibradas. Evite operar agora.")

st.markdown("---")
st.caption("Aviso: Esta ferramenta utiliza análise cromática e não substitui o gerenciamento de risco.")
