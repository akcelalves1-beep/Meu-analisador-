import streamlit as st
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Analisador de Mercado 5min", layout="centered")

st.title("📊 Analisador de Gráficos")
st.write("Tire uma foto do gráfico para análise de tendência (5 min).")

# --- ETAPA 1: Carregar a Imagem ---
arquivo_imagem = st.file_uploader("Escolha a foto do gráfico", type=["jpg", "png", "jpeg"])

if arquivo_imagem is not None:
    # Mostrar a imagem carregada
    img = Image.open(arquivo_imagem)
    st.image(img, caption="Gráfico Carregado", use_container_width=True)
    
    with st.spinner('Analisando padrões de cores...'):
        # --- ETAPA 2: Lógica de Processamento ---
        img_rgb = img.convert('RGB')
        img_pequena = img_rgb.resize((100, 100))
        
        verde, vermelho = 0, 0
        
        for x in range(100):
            for y in range(100):
                r, g, b = img_pequena.getpixel((x, y))
                # Detetar predominância de cores de candles
                if g > r and g > b: verde += 1
                if r > g and r > b: vermelho += 1
        
        # --- ETAPA 3: Resultado ---
        st.subheader("Resultado da Análise:")
        
        if verde > vermelho:
            st.success("📈 TENDÊNCIA DE ALTA: Possível COMPRA para 5 minutos.")
            st.info(f"Força Compradora identificada na imagem.")
        elif vermelho > verde:
            st.error("📉 TENDÊNCIA DE BAIXA: Possível VENDA para 5 minutos.")
            st.info(f"Força Vendedora identificada na imagem.")
        else:
            st.warning("⚖️ MERCADO LATERAL: Aguarde um sinal mais claro.")

st.markdown("---")
st.caption("Nota: Esta ferramenta é um auxílio didático baseado em cores e não garante lucros.")
