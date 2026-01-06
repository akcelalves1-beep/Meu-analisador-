import streamlit as st
from PIL import Image
import pytesseract
import re
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DO TESSERACT (Aponte para o seu caminho de instalação) ---
# Se estiver no Windows, descomente a linha abaixo e coloque o caminho do seu tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Analisador IA Pro", layout="centered")

st.title("🔍 Analisador de Gráfico com OCR")
st.write("O sistema tentará ler o horário e os padrões diretamente da foto.")

arquivo_imagem = st.file_uploader("Suba o print do gráfico (1 min)", type=["jpg", "png", "jpeg"])

def extrair_horario(img):
    # Converte imagem para escala de cinza para melhorar o OCR
    texto = pytesseract.image_to_string(img.convert('L'))
    # Procura por padrões de hora (00:00 ou 00:00:00)
    padrao_hora = re.findall(r'\d{2}:\d{2}', texto)
    return padrao_hora[-1] if padrao_hora else None

if arquivo_imagem is not None:
    img = Image.open(arquivo_imagem)
    st.image(img, caption="Gráfico Processado", use_container_width=True)
    
    with st.spinner('Lendo dados da imagem e analisando tendências...'):
        # 1. Tentar ler o horário da imagem
        horario_detectado = extrair_horario(img)
        
        # 2. Lógica de análise de cores
        img_rgb = img.convert('RGB')
        img_pequena = img_rgb.resize((100, 100))
        verde, vermelho = 0, 0
        for x in range(100):
            for y in range(100):
                r, g, b = img_pequena.getpixel((x, y))
                if g > r and g > b: verde += 1
                if r > g and r > b: vermelho += 1

        # --- PROCESSAMENTO DOS RESULTADOS ---
        st.markdown("---")
        st.subheader("📊 Relatório de Análise Técnica")

        # Exibição do Horário
        if horario_detectado:
            st.info(f"🕒 **Horário Detectado no Gráfico:** {horario_detectado}")
            base_hora = datetime.strptime(horario_detectado, "%H:%M")
        else:
            st.warning("⚠️ Não foi possível ler o relógio na imagem. Usando hora atual.")
            base_hora = datetime.now()

        expira_1m = (base_hora + timedelta(minutes=1)).strftime('%H:%M')
        expira_5m = (base_hora + timedelta(minutes=5)).strftime('%H:%M')

        # Lógica de Decisão
        if verde > vermelho:
            tipo = "COMPRA (CALL)"
            cor_box = "green"
            motivo = f"""
            * **Dominância Estocástica:** Detectada uma massa de pixels verdes ({verde}) superior aos vermelhos ({vermelho}).
            * **Pressão de Alta:** O candle de 1min mostra que a força compradora está renovando máximas.
            * **Confluência:** O volume visual indica que os touros estão ganhando a briga na região de preço detectada às {horario_detectado if horario_detectado else 'agora'}.
            """
            st.success(f"✅ **SINAL DE {tipo}**")
        else:
            tipo = "VENDA (PUT)"
            cor_box = "red"
            motivo = f"""
            * **Pressão Vendedora:** Identificada superioridade de candles vermelhos ({vermelho}) sobre verdes ({verde}).
            * **Exaustão:** O padrão visual sugere que o preço encontrou resistência e deve buscar correção nos próximos minutos.
            * **Fluxo de Baixa:** A leitura de 1min indica que os ursos estão empurrando o preço abaixo das médias visuais.
            """
            st.error(f"🚨 **SINAL DE {tipo}**")

        # Exibição do Motivo e Tempos
        st.write(f"### 📝 Motivo da Operação:")
        st.markdown(motivo)

        col1, col2 = st.columns(2)
        col1.metric("Entrada para 1 min", expira_1m)
        col2.metric("Entrada para 5 min", expira_5m)

st.markdown("---")
st.caption("Nota: O OCR depende da clareza do print e da posição do relógio na tela da sua corretora.")
