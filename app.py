import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="PFC ConversorBoost",
    page_icon="⚡",
    layout="wide"
)

# Título principal
st.title("⚡ PFC ConversorBoost")
st.subheader("Simulador de Conversor de Fator de Potência (PFC)")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    opcao = st.radio(
        "Selecione uma análise:",
        ["Início", "Calculadora PFC", "Simulação Boost", "Análise de Harmônicas"]
    )

# Conteúdo principal
if opcao == "Início":
    st.write("""
    Bem-vindo ao **PFC ConversorBoost**! 
    
    Sistema interativo para análise e simulação de conversores de fator de potência (PFC) 
    e conversores boost em eletrônica de potência.
    
    ### Recursos:
    - 📊 **Calculadora PFC** - Cálculos de fator de potência
    - ⚡ **Simulação Boost** - Análise do conversor boost
    - 📈 **Análise de Harmônicas** - Distorção harmônica total (THD)
    """)
    
    st.info("""
    **Dicas de uso:**
    1. Insira os parâmetros do circuito
    2. Visualize os gráficos e resultados
    3. Exporte os dados para análise adicional
    """)

elif opcao == "Calculadora PFC":
    st.header("📊 Calculadora de Fator de Potência")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Entrada de Dados")
        V_rms = st.number_input("Tensão RMS (V):", value=230.0, min_value=0.0)
        I_rms = st.number_input("Corrente RMS (A):", value=10.0, min_value=0.0)
        phase_angle = st.slider("Ângulo de fase (°):", 0, 90, 30)
        
    with col2:
        st.subheader("Resultados")
        
        # Cálculos
        phase_rad = np.radians(phase_angle)
        P_real = V_rms * I_rms * np.cos(phase_rad)  # Potência Real (W)
        P_reativa = V_rms * I_rms * np.sin(phase_rad)  # Potência Reativa (VAR)
        S_aparente = V_rms * I_rms  # Potência Aparente (VA)
        FP = np.cos(phase_rad)  # Fator de Potência
        
        st.metric("Potência Real (W)", f"{P_real:.2f}")
        st.metric("Potência Reativa (VAR)", f"{P_reativa:.2f}")
        st.metric("Potência Aparente (VA)", f"{S_aparente:.2f}")
        st.metric("Fator de Potência", f"{FP:.4f}")
    
    # Gráfico do triângulo de potências
    st.subheader("Triângulo de Potências")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Desenhar o triângulo
    ax.plot([0, P_real], [0, 0], 'b-', linewidth=2, label='P (Real)')
    ax.plot([P_real, P_real], [0, P_reativa], 'r-', linewidth=2, label='Q (Reativa)')
    ax.plot([0, P_real], [0, P_reativa], 'g-', linewidth=2, label='S (Aparente)')
    
    ax.scatter([0, P_real, P_real], [0, 0, P_reativa], s=100, c=['black', 'blue', 'red'])
    ax.set_xlabel('Potência Real (W)', fontsize=12)
    ax.set_ylabel('Potência Reativa (VAR)', fontsize=12)
    ax.set_title('Triângulo de Potências', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.axis('equal')
    
    st.pyplot(fig)

elif opcao == "Simulação Boost":
    st.header("⚡ Simulação do Conversor Boost")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros do Circuito")
        V_in = st.number_input("Tensão de Entrada (V):", value=12.0, min_value=0.1)
        V_out = st.number_input("Tensão de Saída (V):", value=24.0, min_value=0.1)
        L = st.number_input("Indutância (mH):", value=1.0, min_value=0.1)
        C = st.number_input("Capacitância (µF):", value=100.0, min_value=1.0)
        f_switch = st.number_input("Frequência de Comutação (kHz):", value=100.0, min_value=1.0)
    
    with col2:
        st.subheader("Resultados")
        
        # Cálculos
        duty_cycle = 1 - (V_in / V_out)
        V_out_calc = V_in / (1 - duty_cycle)
        T_period = 1 / (f_switch * 1000)
        t_on = duty_cycle * T_period
        t_off = (1 - duty_cycle) * T_period
        
        st.metric("Ciclo de Trabalho (D)", f"{duty_cycle:.4f} ({duty_cycle*100:.2f}%)")
        st.metric("Tensão de Saída (V)", f"{V_out_calc:.2f}")
        st.metric("Período (µs)", f"{T_period*1e6:.2f}")
        st.metric("Tempo ON (µs)", f"{t_on*1e6:.2f}")
        st.metric("Tempo OFF (µs)", f"{t_off*1e6:.2f}")
    
    # Gráfico de tensão e corrente
    st.subheader("Formas de Onda")
    
    time = np.linspace(0, 5*T_period, 1000)
    V_indutor = np.where(np.mod(time, T_period) < t_on, V_in - V_out, V_in)
    I_media = V_in / (L * 1e-3) * t_on
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    # Gráfico de tensão no indutor
    ax1.plot(time*1e6, V_indutor, 'b-', linewidth=2)
    ax1.set_ylabel('Tensão no Indutor (V)', fontsize=11)
    ax1.set_title('Tensão no Indutor', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    
    # Gráfico de comutação
    switching = np.where(np.mod(time, T_period) < t_on, 1, 0)
    ax2.fill_between(time*1e6, switching, step='pre', alpha=0.5, label='Switch ON')
    ax2.set_xlabel('Tempo (µs)', fontsize=11)
    ax2.set_ylabel('Estado do Switch', fontsize=11)
    ax2.set_title('Sinal de Comutação', fontsize=12, fontweight='bold')
    ax2.set_ylim(-0.1, 1.1)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)

elif opcao == "Análise de Harmônicas":
    st.header("📈 Análise de Harmônicas (THD)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros de Entrada")
        I_fundamental = st.number_input("Corrente Fundamental (A RMS):", value=10.0, min_value=0.1)
        THD_target = st.slider("THD Alvo (%):", 0, 100, 30)
        harmonics = st.slider("Número de harmônicas:", 3, 21, 11)
    
    with col2:
        st.subheader("Componentes Harmônicas")
        
        # Gerar espectro harmônico
        harmonic_data = []
        total_I_rms = I_fundamental
        
        for h in range(1, harmonics + 1):
            I_h = I_fundamental / h if h > 1 else I_fundamental
            harmonic_data.append({
                'Harmônica': f'{h}ª',
                'Frequência (Hz)': h * 50,
                'Corrente (A)': I_h,
                '% Fundamental': (I_h / I_fundamental) * 100 if h > 1 else 100
            })
        
        df_harmonics = pd.DataFrame(harmonic_data)
        st.dataframe(df_harmonics, use_container_width=True)
    
    # Gráfico do espectro harmônico
    st.subheader("Espectro Harmônico")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    harmonicas = [row['Harmônica'] for row in harmonic_data]
    correntes = [row['Corrente (A)'] for row in harmonic_data]
    
    bars = ax.bar(range(len(harmonicas)), correntes, color='steelblue', alpha=0.7)
    ax.set_xlabel('Ordem da Harmônica', fontsize=12)
    ax.set_ylabel('Corrente (A RMS)', fontsize=12)
    ax.set_title(f'Espectro Harmônico (THD ≈ {THD_target}%)', fontsize=13, fontweight='bold')
    ax.set_xticks(range(len(harmonicas)))
    ax.set_xticklabels(harmonicas, rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Colorir a fundamental diferente
    bars[0].set_color('darkblue')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Cálculo de THD
    thd_calc = np.sqrt(sum([c**2 for c in correntes[1:]]) / correntes[0]**2) * 100 if correntes[0] != 0 else 0
    st.info(f"**THD Calculada: {thd_calc:.2f}%**")
