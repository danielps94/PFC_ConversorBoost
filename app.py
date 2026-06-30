# ============================================================
# PFC BOOST DCM
#
# Trabalho - Eletrônica de Potência II
#
# Autor: Daniel PS
#
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.integrate import quad

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(

    page_title="PFC Boost DCM",

    page_icon="⚡",

    layout="wide"

)

# ============================================================
# CABEÇALHO
# ============================================================

st.title("⚡ Projeto de PFC Boost em DCM")

st.markdown("""
Este aplicativo implementa a metodologia completa de projeto
de um Conversor Boost utilizado como Correção de Fator de
Potência (PFC) operando em Modo de Condução Descontínua (DCM).

Todo o projeto segue a metodologia apresentada em sala de aula.
""")

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Parâmetros")

st.sidebar.markdown("### Entrada")

Vg_min = st.sidebar.number_input(

    "Vg mínimo (Vrms)",

    value=90.0,

    step=1.0

)

Vg_max = st.sidebar.number_input(

    "Vg máximo (Vrms)",

    value=240.0,

    step=1.0

)

Vg = st.sidebar.slider(

    "Vg atual (Vrms)",

    min_value=float(Vg_min),

    max_value=float(Vg_max),

    value=127.0

)

Po_min = st.sidebar.number_input(

    "Po mínimo (W)",

    value=50.0

)

Po_max = st.sidebar.number_input(

    "Po máximo (W)",

    value=150.0

)

Po = st.sidebar.slider(

    "Po atual (W)",

    min_value=float(Po_min),

    max_value=float(Po_max),

    value=100.0

)

Vo = st.sidebar.number_input(

    "Vo (V)",

    value=450.0

)

DeltaVo = st.sidebar.number_input(

    "Ripple (%)",

    value=10.0

)

fs = st.sidebar.number_input(

    "Frequência de chaveamento (Hz)",

    value=50000.0

)

fr = st.sidebar.number_input(

    "Frequência da rede (Hz)",

    value=60.0

)

st.sidebar.divider()

st.sidebar.markdown("### Projeto")

margem_dcm = st.sidebar.slider(

    "Margem sobre Dcrit",

    0.70,

    0.99,

    0.90

)

# ============================================================
# CONVERSÕES
# ============================================================

Vg_min_pk = Vg_min*np.sqrt(2)

Vg_max_pk = Vg_max*np.sqrt(2)

Vg_pk = Vg*np.sqrt(2)

DeltaVo_V = DeltaVo*Vo/100

# ============================================================
# VERIFICAÇÕES
# ============================================================

if Vo <= Vg_max_pk:

    st.error(

        "A tensão de saída deve ser maior que a tensão máxima retificada."

    )

    st.stop()

# ============================================================
# DADOS GERAIS
# ============================================================

Dc = 1-(Vg_max_pk/Vo)

D_proj = margem_dcm*Dc

# ============================================================
# TABELA RESUMO
# ============================================================

st.subheader("Resumo dos Dados")

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(

        "Vg Atual",

        f"{Vg:.1f} Vrms"

    )

with c2:

    st.metric(

        "Po Atual",

        f"{Po:.1f} W"

    )

with c3:

    st.metric(

        "Duty Crítico",

        f"{Dc:.4f}"

    )

with c4:

    st.metric(

        "Duty Projeto",

        f"{D_proj:.4f}"

    )

st.divider()

# ============================================================
# FUNÇÕES MATEMÁTICAS
# ============================================================

def integral_indutor(theta,Vgpk,Vo):

    return (

        np.sin(theta)**2

    )/(

        1-(Vgpk/Vo)*np.sin(theta)

    )


def integral_capacitor(

    t,

    Vgpk,

    Po,

    D,

    Vo,

    fs,

    fr

):

    Mb=Vo/Vgpk

    termo1=(

        D**2*

        Vgpk**2

    )/(

        2*np.pi*

        Po*

        fs

    )

    termo2=(

        np.sin(

            2*np.pi*fr*t

        )**2

    )/(

        Mb-

        np.sin(

            2*np.pi*fr*t

        )

    )

    termo3=Po/Vo

    return np.abs(

        termo1*

        termo2-

        termo3

    )

# ============================================================
# LISTA DOS CASOS LIMITES
# ============================================================

casos=[

("Caso 1",Vg_min,Po_min),

("Caso 2",Vg_min,Po_max),

("Caso 3",Vg_max,Po_min),

("Caso 4",Vg_max,Po_max)

]

# ============================================================
# ABAS
# ============================================================

aba1,aba2,aba3,aba4,aba5,aba6=st.tabs([

"📖 Metodologia",

"📐 Indutor",

"🔋 Capacitor",

"📊 Resultados",

"📈 Gráficos",

"ℹ️ Sobre"

])

# ============================================================
# ABA 1 - METODOLOGIA
# ============================================================

with aba1:

    st.header("📖 Metodologia do Projeto")

    st.markdown("""
    
## Conversor Boost em DCM para Correção de Fator de Potência

### O que é PFC?

Correção de Fator de Potência (Power Factor Correction) é uma técnica utilizada para 
melhorar a eficiência energética e reduzir harmônicas em sistemas elétricos.

### Modo de Condução Descontínua (DCM)

No DCM, a corrente do indutor retorna a zero antes do próximo ciclo de chaveamento.
Isso oferece vantagens como:

- Menor EMI (Electromagnetic Interference)
- Operação sem sensor de corrente
- Dinâmica de controle simplificada

### Procedimento de Projeto

1. **Dimensionamento do Indutor** - Avaliação dos 4 casos limites
2. **Dimensionamento do Capacitor** - Cálculo com integração numérica
3. **Análise de Performance** - Fator de potência e THD
4. **Validação** - Verificação dos critérios de operação

### Parâmetros Principais

- **Vg**: Tensão de entrada (AC)
- **Po**: Potência de saída
- **Vo**: Tensão de saída (DC)
- **fs**: Frequência de chaveamento
- **L**: Indutância
- **C**: Capacitância

    """)

# ============================================================
# ABA 2 - DIMENSIONAMENTO DO INDUTOR
# ============================================================

with aba2:

    st.header("Dimensionamento da Indutância")

    st.markdown("""
O dimensionamento da indutância é realizado avaliando
os quatro casos limites definidos pelo projeto.

Para cada caso é resolvida numericamente a integral
da expressão deduzida em aula.
""")

    st.latex(r"""
L=
\frac{D^2V_g^2}{2P_of_s}
\cdot
\frac1\pi
\int_0^\pi
\frac{\sin^2(\theta)}
{1-\frac{V_g}{V_o}\sin(\theta)}
d\theta
""")

    tabela_indutor=[]

    L_valores=[]

    integrais=[]

    for nome,Vg_rms,Po_caso in casos:

        Vgpk=Vg_rms*np.sqrt(2)

        integral,erro=quad(

            integral_indutor,

            0,

            np.pi,

            args=(Vgpk,Vo)

        )

        integrais.append(integral)

        L=((Vgpk**2)*(D_proj**2))

        L=L/(2*Po_caso*fs)

        L=L*(1/np.pi)

        L=L*integral

        L_valores.append(L)

        tabela_indutor.append({

            "Caso":nome,

            "Vg (Vrms)":Vg_rms,

            "Po (W)":Po_caso,

            "Integral":round(integral,5),

            "L (µH)":round(L*1e6,2)

        })

    df_indutor=pd.DataFrame(tabela_indutor)

    st.dataframe(

        df_indutor,

        use_container_width=True

    )

    indice=np.argmin(L_valores)

    L_adotado=L_valores[indice]

    caso_critico=tabela_indutor[indice]

    st.success(

        f"Indutância adotada = {L_adotado*1e6:.2f} µH"

    )

    st.info(

        f"Caso crítico: {caso_critico['Caso']}"

    )

    st.markdown(f"""

**Tensão utilizada**

- {caso_critico['Vg (Vrms)']} Vrms

**Potência**

- {caso_critico['Po (W)']} W

Este foi o caso que produziu a menor indutância.

Esse valor será utilizado nas próximas etapas
do projeto.

""")

    col1,col2,col3=st.columns(3)

    with col1:

        st.metric(

            "Menor L",

            f"{min(L_valores)*1e6:.2f} µH"

        )

    with col2:

        st.metric(

            "Maior L",

            f"{max(L_valores)*1e6:.2f} µH"

        )

    with col3:

        st.metric(

            "Caso crítico",

            caso_critico["Caso"]

        )

    fig,ax=plt.subplots(figsize=(8,4))

    ax.bar(

        df_indutor["Caso"],

        df_indutor["L (µH)"],

        color="steelblue",

        alpha=0.7

    )

    ax.set_ylabel("Indutância (µH)")

    ax.set_title("Comparação entre os quatro casos")

    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

# ============================================================
# ABA 3 - DIMENSIONAMENTO DO CAPACITOR
# ============================================================

with aba3:

    st.header("Dimensionamento da Capacitância")

    st.markdown("""
O capacitor é dimensionado utilizando a expressão exata apresentada
na metodologia do projeto.

Para cada um dos quatro casos limites são realizados:

- Recalculo do Duty Cycle;
- Integração numérica;
- Cálculo da capacitância exata;
- Comparação com a capacitância de referência.
""")

    tabela_capacitor = []

    C_exato_valores = []

    C_ref_valores = []

    limite_integracao = 1/(4*fr)

    for nome, Vg_rms, Po_caso in casos:

        Vgpk = Vg_rms*np.sqrt(2)

        # -------------------------------------------------
        # Integral do indutor
        # -------------------------------------------------

        integral_L, _ = quad(
            integral_indutor,
            0,
            np.pi,
            args=(Vgpk, Vo)
        )

        # -------------------------------------------------
        # Duty Cycle correspondente ao caso
        # -------------------------------------------------

        termo_D = (
            2*Po_caso*fs*L_adotado
        ) / (
            (Vgpk**2)*(1/np.pi)*integral_L
        )

        D_real = np.sqrt(termo_D)

        # -------------------------------------------------
        # Integral do capacitor
        # -------------------------------------------------

        integral_C, _ = quad(
            integral_capacitor,
            0,
            limite_integracao,
            args=(
                Vgpk,
                Po_caso,
                D_real,
                Vo,
                fs,
                fr
            )
        )

        # -------------------------------------------------
        # Capacitância exata
        # -------------------------------------------------

        C_exato = integral_C/DeltaVo_V

        # -------------------------------------------------
        # Capacitância aproximada (referência)
        # -------------------------------------------------

        C_ref = Po_caso / (
            2*np.pi*fr*Vo*DeltaVo_V
        )

        C_exato_valores.append(C_exato)

        C_ref_valores.append(C_ref)

        tabela_capacitor.append({

            "Caso": nome,

            "Duty": round(D_real,4),

            "C Exato (µF)": round(C_exato*1e6,2),

            "C Ref (µF)": round(C_ref*1e6,2)

        })

    df_capacitor = pd.DataFrame(tabela_capacitor)

    st.dataframe(
        df_capacitor,
        use_container_width=True
    )

    # =========================================================
    # Escolha do capacitor
    # =========================================================

    indice_C = np.argmax(C_exato_valores)

    C_adotado = C_exato_valores[indice_C]

    caso_critico_C = tabela_capacitor[indice_C]

    st.success(
        f"Capacitância adotada = {C_adotado*1e6:.2f} µF"
    )

    st.info(
        f"Caso crítico: {caso_critico_C['Caso']}"
    )

    st.markdown(f"""

**Tensão utilizada**

- {caso_critico_C['Caso']}

**Duty calculado**

- {caso_critico_C['Duty']}

Foi adotado o **maior valor de capacitância**, garantindo
que a ondulação da tensão permaneça dentro do limite
especificado para qualquer condição de operação.

""")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Maior C",
            f"{max(C_exato_valores)*1e6:.2f} µF"
        )

    with col2:

        st.metric(
            "Menor C",
            f"{min(C_exato_valores)*1e6:.2f} µF"
        )

    with col3:

        st.metric(
            "C Referência Médio",
            f"{np.mean(C_ref_valores)*1e6:.2f} µF"
        )

    st.divider()

    # =========================================================
    # Gráfico
    # =========================================================

    fig, ax = plt.subplots(figsize=(8,4))

    largura = 0.35

    x = np.arange(len(df_capacitor))

    ax.bar(
        x-largura/2,
        df_capacitor["C Exato (µF)"],
        largura,
        label="Exato",
        color="steelblue",
        alpha=0.7
    )

    ax.bar(
        x+largura/2,
        df_capacitor["C Ref (µF)"],
        largura,
        label="Referência",
        color="orange",
        alpha=0.7
    )

    ax.set_xticks(x)

    ax.set_xticklabels(df_capacitor["Caso"])

    ax.set_ylabel("Capacitância (µF)")

    ax.set_title("Comparação dos Quatro Casos")

    ax.grid(True, alpha=0.3)

    ax.legend()

    st.pyplot(fig)

# ============================================================
# ABA 4 - RESULTADOS FINAIS
# ============================================================

with aba4:

    st.header("Resultados Finais do Projeto")

    st.markdown("""
Nesta etapa são apresentados os valores finais adotados para o
projeto do conversor PFC Boost em DCM.
""")

    # =======================================================
    # Duty Cycle para o ponto de operação escolhido
    # =======================================================

    integral_atual, _ = quad(
        integral_indutor,
        0,
        np.pi,
        args=(Vg_pk, Vo)
    )

    termo_D = (
        2 * Po * fs * L_adotado
    ) / (
        (Vg_pk**2) * (1/np.pi) * integral_atual
    )

    D_atual = np.sqrt(termo_D)

    st.subheader("Componentes Adotados")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Indutância",
            f"{L_adotado*1e6:.2f} µH"
        )

    with c2:

        st.metric(
            "Capacitância",
            f"{C_adotado*1e6:.2f} µF"
        )

    with c3:

        st.metric(
            "Duty Cycle",
            f"{D_atual:.4f}"
        )

    st.divider()

    # =======================================================
    # FP e THD
    # =======================================================

    alpha = Vg_pk / Vo

    def integranda_num(theta):

        return (
            np.sin(theta)**2
        ) / (
            1 - alpha*np.sin(theta)
        )

    def integranda_den(theta):

        return (
            np.sin(theta) /
            (
                1 - alpha*np.sin(theta)
            )
        )**2

    num, _ = quad(
        integranda_num,
        0,
        np.pi
    )

    den, _ = quad(
        integranda_den,
        0,
        np.pi
    )

    FP = (
        np.sqrt(2) * num
    ) / (
        np.sqrt(np.pi * den)
    )

    FP = min(FP,1.0)

    THD = np.sqrt(
        (1/(FP**2))-1
    )*100

    st.subheader("Qualidade da Energia")

    c1,c2 = st.columns(2)

    with c1:

        st.metric(

            "Fator de Potência",

            f"{FP:.4f}"

        )

    with c2:

        st.metric(

            "THD",

            f"{THD:.2f} %"

        )

    st.divider()

    # =======================================================
    # Resumo Geral
    # =======================================================

    resumo = pd.DataFrame({

        "Parâmetro":[

            "Vg",

            "Po",

            "Vo",

            "fs",

            "L",

            "C",

            "Duty",

            "FP",

            "THD"

        ],

        "Valor":[

            f"{Vg:.1f} Vrms",

            f"{Po:.1f} W",

            f"{Vo:.1f} V",

            f"{fs:.0f} Hz",

            f"{L_adotado*1e6:.2f} µH",

            f"{C_adotado*1e6:.2f} µF",

            f"{D_atual:.4f}",

            f"{FP:.4f}",

            f"{THD:.2f} %"

        ]

    })

    st.subheader("Resumo do Projeto")

    st.dataframe(

        resumo,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # =======================================================
    # Verificações Automáticas
    # =======================================================

    st.subheader("Validação do Projeto")

    if FP > 0.98:

        st.success("✔ Fator de potência excelente.")

    elif FP > 0.95:

        st.warning("⚠ Fator de potência aceitável.")

    else:

        st.error("✖ Fator de potência abaixo do esperado.")

    if THD < 10:

        st.success("✔ THD dentro do esperado.")

    elif THD < 20:

        st.warning("⚠ THD moderado.")

    else:

        st.error("✖ THD elevado.")

    if D_atual < Dc:

        st.success("✔ Conversor permanece em DCM.")

    else:

        st.error("✖ Duty acima do limite crítico.")

    st.divider()

    st.info(f"""
**Resumo Executivo**

• Indutor adotado: {L_adotado*1e6:.2f} µH

• Capacitor adotado: {C_adotado*1e6:.2f} µF

• Duty de operação: {D_atual:.4f}

• Fator de potência: {FP:.4f}

• THD: {THD:.2f} %

O projeto atende aos critérios definidos para o conversor
Boost operando em Modo de Condução Descontínua (DCM).
""")

# ============================================================
# ABA 5 - GRÁFICOS
# ============================================================

with aba5:

    st.header("📈 Análise Gráfica")

    st.markdown("Visualização dos resultados e análises do projeto.")

    # =========================================================
    # Gráfico 1: Ondulação de Tensão
    # =========================================================

    st.subheader("Ondulação de Tensão de Saída")

    tempo = np.linspace(0, 1/fr, 1000)

    Vg_t = Vg_pk * np.sin(2*np.pi*fr*tempo)

    ondulacao = (DeltaVo/100) * Vo

    V_saida = Vo + ondulacao * np.sin(2*np.pi*fr*tempo)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    ax1.plot(tempo*1000, Vg_t, 'b-', linewidth=2, label='Vg(t)')

    ax1.set_ylabel('Tensão (V)', fontsize=11)

    ax1.set_title('Tensão de Entrada', fontsize=12, fontweight='bold')

    ax1.grid(True, alpha=0.3)

    ax1.legend()

    ax2.plot(tempo*1000, V_saida, 'r-', linewidth=2, label='Vo(t)')

    ax2.axhline(y=Vo, color='k', linestyle='--', linewidth=1, alpha=0.5)

    ax2.fill_between(tempo*1000, Vo-ondulacao/2, Vo+ondulacao/2, alpha=0.2, color='red')

    ax2.set_xlabel('Tempo (ms)', fontsize=11)

    ax2.set_ylabel('Tensão (V)', fontsize=11)

    ax2.set_title('Tensão de Saída com Ripple', fontsize=12, fontweight='bold')

    ax2.grid(True, alpha=0.3)

    ax2.legend()

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    # =========================================================
    # Gráfico 2: Comparação L vs Casos
    # =========================================================

    st.subheader("Indutância por Caso de Operação")

    fig, ax = plt.subplots(figsize=(8, 4))

    cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    ax.bar(df_indutor["Caso"], df_indutor["L (µH)"], color=cores, alpha=0.7)

    ax.axhline(y=L_adotado*1e6, color='r', linestyle='--', linewidth=2, label=f'L adotado: {L_adotado*1e6:.2f} µH')

    ax.set_ylabel('Indutância (µH)', fontsize=11)

    ax.set_title('Seleção da Indutância', fontsize=12, fontweight='bold')

    ax.grid(True, alpha=0.3, axis='y')

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    # =========================================================
    # Gráfico 3: Comparação C vs Casos
    # =========================================================

    st.subheader("Capacitância por Caso de Operação")

    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.arange(len(df_capacitor))

    largura = 0.35

    ax.bar(x-largura/2, df_capacitor["C Exato (µF)"], largura, label='C Exato', color='steelblue', alpha=0.7)

    ax.bar(x+largura/2, df_capacitor["C Ref (µF)"], largura, label='C Referência', color='orange', alpha=0.7)

    ax.axhline(y=C_adotado*1e6, color='r', linestyle='--', linewidth=2, label=f'C adotado: {C_adotado*1e6:.2f} µF')

    ax.set_xticks(x)

    ax.set_xticklabels(df_capacitor["Caso"])

    ax.set_ylabel('Capacitância (µF)', fontsize=11)

    ax.set_title('Seleção da Capacitância', fontsize=12, fontweight='bold')

    ax.grid(True, alpha=0.3, axis='y')

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    # =========================================================
    # Gráfico 4: Fator de Potência vs Potência
    # =========================================================

    st.subheader("Fator de Potência em Diferentes Condições")

    potencias = np.linspace(Po_min, Po_max, 50)

    fps = []

    for po in potencias:

        alpha_temp = Vg_pk / Vo

        def integranda_num_temp(theta):
            return (np.sin(theta)**2) / (1 - alpha_temp*np.sin(theta))

        def integranda_den_temp(theta):
            return (np.sin(theta) / (1 - alpha_temp*np.sin(theta)))**2

        num_temp, _ = quad(integranda_num_temp, 0, np.pi)

        den_temp, _ = quad(integranda_den_temp, 0, np.pi)

        fp_temp = (np.sqrt(2) * num_temp) / (np.sqrt(np.pi * den_temp))

        fps.append(min(fp_temp, 1.0))

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(potencias, fps, 'b-', linewidth=2, marker='o', markersize=5)

    ax.axhline(y=0.95, color='g', linestyle='--', linewidth=1, alpha=0.7, label='Mínimo aceitável (0.95)')

    ax.axhline(y=FP, color='r', linestyle='--', linewidth=1, alpha=0.7, label=f'FP atual: {FP:.4f}')

    ax.fill_between(potencias, 0.95, 1.0, alpha=0.1, color='green')

    ax.set_xlabel('Potência (W)', fontsize=11)

    ax.set_ylabel('Fator de Potência', fontsize=11)

    ax.set_title('Fator de Potência vs Potência de Saída', fontsize=12, fontweight='bold')

    ax.grid(True, alpha=0.3)

    ax.legend()

    ax.set_ylim(0.9, 1.01)

    plt.tight_layout()

    st.pyplot(fig)

# ============================================================
# ABA 6 - SOBRE
# ============================================================

with aba6:

    st.header("ℹ️ Sobre este Projeto")

    st.markdown("""
    
## PFC Boost DCM - Simulador

Este aplicativo foi desenvolvido como ferramenta educacional para 
o projeto de conversores boost operando em modo de condução descontínua 
(DCM) com correção de fator de potência (PFC).

### Características

✅ Cálculo automático de componentes (L e C)

✅ Avaliação de 4 casos limites de operação

✅ Análise de qualidade de energia (FP e THD)

✅ Validação automática de critérios de projeto

✅ Visualização gráfica dos resultados

### Tecnologias Utilizadas

- **Python** - Linguagem de programação
- **Streamlit** - Framework web
- **NumPy** - Computação numérica
- **Pandas** - Manipulação de dados
- **Matplotlib** - Visualização gráfica
- **SciPy** - Integração numérica

### Metodologia

Todo o projeto segue a metodologia apresentada em aula, incluindo:

1. Dimensionamento do indutor com integração numérica
2. Cálculo exato do capacitor
3. Análise de harmônicas
4. Validação de operação em DCM

### Autor

Daniel PS - Trabalho de Eletrônica de Potência II

### Disclaimer

Este é um projeto educacional. Sempre consulte literatura técnica 
e especialistas antes de implementar conversores em aplicações reais.

### Referências

- Barbi, I., "Eletrônica de Potência"
- Erickson, R. W., "Fundamentals of Power Electronics"

---

**Versão**: 1.0

**Data**: 2026

    """)
