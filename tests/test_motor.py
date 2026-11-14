import pandas as pd

from fieldshift.conhecimento import carregar_base
from fieldshift.indicadores import indicadores_por_safra
from fieldshift.motor import avaliar_rotacao, comparar, selecionar_tres


def clima(anos=12, fim_chuva="03-31", mm=10.0):
    datas = pd.date_range("2005-07-01", f"{2005 + anos}-06-30", freq="D")
    chuva = pd.Series(0.0, index=datas)
    for a in range(2005, 2005 + anos):
        chuva[f"{a}-10-10":f"{a + 1}-{fim_chuva}"] = mm
    return pd.DataFrame({"chuva_mm": chuva, "temp_max_c": 30.0})


def test_base_carrega_e_rotacoes_sao_coerentes():
    base = carregar_base()
    assert "soja" in base.culturas
    assert len(base.rotacoes) >= 4
    assert any(r.atual_padrao for r in base.rotacoes)


def test_chuva_curta_pesa_mais_no_milho_que_no_milheto():
    base = carregar_base()
    df = clima(fim_chuva="02-28")  # chuva acaba cedo
    ind = indicadores_por_safra(df)
    milho = avaliar_rotacao(df, ind, base, base.rotacao("soja_milho"))
    milheto = avaliar_rotacao(df, ind, base, base.rotacao("soja_milheto"))
    assert milho.falha_recente > milheto.falha_recente
    assert milho.notas["risco"] < milheto.notas["risco"]


def test_chuva_longa_nao_gera_falha_no_milho():
    base = carregar_base()
    df = clima(fim_chuva="05-15")
    ind = indicadores_por_safra(df)
    milho = avaliar_rotacao(df, ind, base, base.rotacao("soja_milho"))
    assert milho.falha_recente == 0
    assert milho.notas["risco"] == 10


def test_prioridade_renda_favorece_milho_em_clima_bom():
    base = carregar_base()
    df = clima(fim_chuva="05-15")
    ind = indicadores_por_safra(df)
    ranking = comparar(df, ind, base, {"renda": 5, "solo": 0, "agua": 0, "risco": 1})
    assert ranking[0].rotacao.segunda in {"milho_safrinha", "milho_braquiaria"}


def test_selecionar_tres_inclui_rotacao_atual():
    base = carregar_base()
    df = clima()
    ind = indicadores_por_safra(df)
    tres = selecionar_tres(comparar(df, ind, base), "soja_crotalaria")
    assert len(tres) == 3
    assert any(a.rotacao.id == "soja_crotalaria" for a in tres)


def test_toda_nota_tem_evidencia():
    base = carregar_base()
    df = clima()
    ind = indicadores_por_safra(df)
    av = avaliar_rotacao(df, ind, base, base.rotacao("soja_sorgo"))
    criterios_com_evidencia = {e.criterio for e in av.evidencias}
    assert set(av.notas) <= criterios_com_evidencia
