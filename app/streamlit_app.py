"""Field Shift · Cerrado — protótipo em Streamlit.

Rodar:  streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from fieldshift.conhecimento import carregar_base  # noqa: E402
from fieldshift.explicar import explicar_clima, explicar_rotacao  # noqa: E402
from fieldshift.indicadores import indicadores_por_safra, resumo_tendencias  # noqa: E402
from fieldshift.locais import LOCAIS, carregar_coordenada  # noqa: E402
from fieldshift.motor import CRITERIOS, PRIORIDADES_PADRAO, comparar, selecionar_tres  # noqa: E402

COR = {
    "verde": "#2A5C0F",
    "broto": "#5E9E28",
    "ouro": "#D4A017",
    "nevoa": "#F4EFE3",
    "terra": "#0F0F0F",
    "alerta": "#B5462B",
    "linha": "#D9D1BE",
}

st.set_page_config(page_title="Field Shift · Cerrado", page_icon="🌱", layout="wide")

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@600;700;800&display=swap');
html, body, [class*="css"], .stMarkdown, p, li, label {{ font-family: 'DM Sans', sans-serif; }}
h1, h2, h3, .fs-titulo {{ font-family: 'Syne', sans-serif !important; letter-spacing: -0.01em; }}
.block-container {{ padding-top: 3.6rem; max-width: 1280px; }}
.fs-titulo {{ font-size: 2.6rem !important; font-weight: 800; color: {COR['terra']}; margin: 0; line-height: 1.05; }}
.fs-sub {{ color: #4a4a42; font-size: 1.02rem; margin-top: .4rem; max-width: 60ch; }}
.fs-card {{ background: #fff; border: 1px solid {COR['linha']}; border-radius: 14px; padding: 1.1rem 1.2rem; height: 100%; }}
.fs-card.melhor {{ border: 2px solid {COR['verde']}; }}
.fs-tag {{ display:inline-block; font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
          padding:.15rem .5rem; border-radius:999px; background:{COR['nevoa']}; color:{COR['verde']}; margin-bottom:.4rem; }}
.fs-tag.atual {{ color:{COR['ouro']}; }}
.fs-nome {{ font-family:'Syne',sans-serif; font-weight:700; font-size:1.15rem; margin:.1rem 0 .3rem; color:{COR['terra']}; }}
.fs-nota {{ font-family:'DM Sans',sans-serif; font-size:2.5rem; font-weight:700; letter-spacing:-0.02em; color:{COR['verde']}; line-height:1; }}
.fs-nota small {{ font-size:1rem; color:#77736a; font-weight:600; }}
.fs-barra {{ margin:.35rem 0; font-size:.86rem; color:#3b3a35; }}
.fs-trilho {{ background:{COR['nevoa']}; border-radius:6px; height:8px; margin-top:.2rem; overflow:hidden; }}
.fs-fill {{ height:8px; border-radius:6px; }}
.fs-clima {{ background:{COR['terra']}; color:{COR['nevoa']}; border-radius:14px; padding:1rem 1.2rem; margin-bottom:1rem; }}
.fs-clima b {{ color:{COR['ouro']}; }}
.fs-aviso {{ font-size:.85rem; color:#5d5a52; border-top:1px solid {COR['linha']}; padding-top:.8rem; margin-top:1.5rem; }}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Buscando o histórico de clima na NASA…")
def dados_do_ponto(lat: float, lon: float) -> pd.DataFrame:
    return carregar_coordenada(lat, lon)


@st.cache_data
def indicadores(lat: float, lon: float, ano_ini: int, ano_fim: int) -> pd.DataFrame:
    return indicadores_por_safra(dados_do_ponto(lat, lon), ano_ini, ano_fim)


base = carregar_base()

st.markdown('<div class="fs-titulo">Field Shift · Cerrado</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="fs-sub">Qual segunda safra aguenta o clima que está mudando no seu talhão? '
    "Comparamos rotações com 24 safras de dados de clima da NASA, o que você prioriza "
    "e uma base agronômica revisável.</p>",
    unsafe_allow_html=True,
)
st.write("")

col_chat, col_res = st.columns([0.36, 0.64], gap="large")

with col_chat:
    with st.chat_message("assistant", avatar="🌱"):
        st.markdown("**Onde fica o talhão?**")
        opcoes = [l.nome for l in LOCAIS] + ["Outro ponto (coordenadas)"]
        escolha = st.selectbox("Local", opcoes, index=0, label_visibility="collapsed")
        if escolha == opcoes[-1]:
            c1, c2 = st.columns(2)
            lat = c1.number_input("Latitude", value=-17.79, format="%.4f")
            lon = c2.number_input("Longitude", value=-50.92, format="%.4f")
            nome_local = f"{lat:.2f}, {lon:.2f}"
        else:
            local = next(l for l in LOCAIS if l.nome == escolha)
            lat, lon, nome_local = local.lat, local.lon, local.nome
        st.caption("O dado da NASA usado aqui tem resolução regional (~50 km).")

    with st.chat_message("assistant", avatar="🌱"):
        st.markdown("**O que você planta depois da soja hoje?**")
        nomes_rot = {r.nome: r.id for r in base.rotacoes}
        padrao = next(i for i, r in enumerate(base.rotacoes) if r.atual_padrao)
        atual_nome = st.selectbox("Rotação atual", list(nomes_rot), index=padrao, label_visibility="collapsed")
        atual_id = nomes_rot[atual_nome]

    with st.chat_message("assistant", avatar="🌱"):
        st.markdown("**O que pesa mais na sua decisão?** (0 = não importa, 5 = muito)")
        prioridades = {}
        for chave, rotulo in CRITERIOS.items():
            prioridades[chave] = st.slider(rotulo, 0, 5, PRIORIDADES_PADRAO[chave])

    with st.expander("Ajustes do período"):
        ano_ini, ano_fim = st.slider("Safras analisadas (ano de início)", 2001, 2024, (2001, 2024))

with col_res:
    try:
        df = dados_do_ponto(lat, lon)
    except Exception as erro:  # noqa: BLE001
        st.error(f"Não consegui buscar os dados da NASA para esse ponto agora ({erro}). Use um dos locais de exemplo.")
        st.stop()

    ind = indicadores(lat, lon, ano_ini, ano_fim)
    if len(ind) < 5:
        st.warning("Período curto demais para uma comparação confiável. Use pelo menos 5 safras.")
        st.stop()

    periodo = f"{ind['safra'].iloc[0]}–{ind['safra'].iloc[-1]}"
    tend = resumo_tendencias(ind)
    frases = explicar_clima(tend, nome_local, periodo)
    st.markdown(
        '<div class="fs-clima"><b>O que mudou no clima</b><br>' + "<br>".join(frases) + "</div>",
        unsafe_allow_html=True,
    )

    avaliacoes = comparar(df, ind, base, prioridades)
    tres = selecionar_tres(avaliacoes, atual_id)
    melhor_id = tres[0].rotacao.id

    cols = st.columns(3, gap="medium")
    for col, av in zip(cols, tres):
        e_atual = av.rotacao.id == atual_id
        tag = "Sua rotação atual" if e_atual else ("Melhor nota" if av.rotacao.id == melhor_id else "Alternativa")
        barras = ""
        for chave, rotulo in CRITERIOS.items():
            v = av.notas[chave]
            cor = COR["verde"] if v >= 7 else (COR["ouro"] if v >= 4 else COR["alerta"])
            barras += (
                f'<div class="fs-barra">{rotulo} · <b>{v:.1f}</b>'
                f'<div class="fs-trilho"><div class="fs-fill" style="width:{v * 10:.0f}%;background:{cor}"></div></div></div>'
            )
        classe = "fs-card melhor" if av.rotacao.id == melhor_id else "fs-card"
        col.markdown(
            f'<div class="{classe}"><span class="fs-tag{" atual" if e_atual else ""}">{tag}</span>'
            f'<div class="fs-nome">{av.nome}</div>'
            f'<div class="fs-nota">{av.nota_geral:.1f}<small> /10</small></div>{barras}</div>',
            unsafe_allow_html=True,
        )
        with col:
            st.markdown(explicar_rotacao(av, prioridades, e_atual))
            with st.expander("De onde vem essa nota"):
                for ev in av.evidencias:
                    st.markdown(f"- {ev.texto}  \n  <small>Fonte: {ev.fonte}</small>", unsafe_allow_html=True)

    st.write("")
    aba1, aba2, aba3, aba4 = st.tabs(["Chuvas ano a ano", "2ª safra, safra a safra", "Todas as rotações", "Dados"])

    with aba1:
        ref = pd.Timestamp("2001-07-01")
        y_ini = [ref + pd.Timedelta(days=d - 1) if pd.notna(d) else None for d in ind["inicio_dia_safra"]]
        y_fim = [ref + pd.Timedelta(days=d - 1) if pd.notna(d) else None for d in ind["fim_dia_safra"]]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ind["safra"], y=y_fim, name="Fim das chuvas", mode="lines+markers",
                                 line=dict(color=COR["ouro"], width=2)))
        fig.add_trace(go.Scatter(x=ind["safra"], y=y_ini, name="Início das chuvas", mode="lines+markers",
                                 line=dict(color=COR["verde"], width=2), fill="tonexty",
                                 fillcolor="rgba(94,158,40,0.12)"))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12),
                          yaxis=dict(tickformat="%d/%m", title=None, gridcolor=COR["linha"]),
                          xaxis=dict(title=None, tickangle=-45))
        st.plotly_chart(fig, width="stretch")
        st.caption("Faixa verde = estação chuvosa. Critério de início e fim em docs/metodo.md. Fonte: NASA POWER.")

    with aba2:
        nomes_tres = [a.nome for a in tres]
        foco_nome = st.radio("Rotação", nomes_tres, horizontal=True, label_visibility="collapsed")
        foco = next(a for a in tres if a.nome == foco_nome)
        ps = foco.por_safra
        cores = [COR["alerta"] if f else COR["broto"] for f in ps["falha"]]
        fig2 = go.Figure(go.Bar(x=ps["safra"], y=ps["chuva_fase_critica_mm"], marker_color=cores,
                                hovertext=ps["motivo"], name="Chuva na fase crítica"))
        fig2.add_hline(y=foco.cultura.chuva_min_fase_critica_mm, line_dash="dash", line_color=COR["terra"],
                       annotation_text=f"mínimo {foco.cultura.chuva_min_fase_critica_mm:.0f} mm")
        fig2.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(title="mm", gridcolor=COR["linha"]),
                           xaxis=dict(title=None, tickangle=-45))
        st.plotly_chart(fig2, width="stretch")
        st.caption(
            f"Chuva nos {foco.cultura.dias_criticos} dias após a semeadura estimada de {foco.cultura.nome.lower()}. "
            "Vermelho = safra com problema (pouca chuva ou plantio depois do limite)."
        )

    with aba3:
        tabela = pd.DataFrame(
            [{"Rotação": a.nome, "Nota": a.nota_geral, **{CRITERIOS[k]: v for k, v in a.notas.items()},
              "Problema (últimas safras)": f"{a.falha_recente:.0%}", "Problema (série toda)": f"{a.falha_total:.0%}"}
             for a in avaliacoes]
        )
        st.dataframe(tabela, hide_index=True, width="stretch")

    with aba4:
        mostrar = ind[["safra", "inicio_chuvas", "fim_chuvas", "duracao_dias", "chuva_estacao_mm",
                       "maior_veranico_dias", "dias_calor"]].copy()
        mostrar["inicio_chuvas"] = mostrar["inicio_chuvas"].dt.strftime("%d/%m/%Y")
        mostrar["fim_chuvas"] = mostrar["fim_chuvas"].dt.strftime("%d/%m/%Y")
        st.dataframe(mostrar, hide_index=True, width="stretch")
        st.download_button("Baixar indicadores (CSV)", ind.to_csv(index=False).encode("utf-8"),
                           file_name="indicadores_safra.csv", mime="text/csv")

    pend = base.pendentes_validacao
    st.markdown(
        '<div class="fs-aviso">Ferramenta de apoio à decisão: quem decide é o produtor com o agrônomo dele. '
        "Dados de clima: NASA POWER (série diária, resolução regional). "
        + (f"Valores agronômicos ainda em validação: {', '.join(pend)}." if pend else "")
        + "</div>",
        unsafe_allow_html=True,
    )
