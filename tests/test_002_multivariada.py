"""T021/T024 — Funções multivariadas conferidas contra implementações de referência.

Dados simulados aqui servem só para testar o código (correlação conhecida), nunca como resultado.
"""
import numpy as np
import pytest
from sklearn.decomposition import PCA
from sklearn.utils import check_array as _check_array_sklearn

import factor_analyzer.factor_analyzer as fa_mod
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from factor_analyzer.rotator import Rotator

from analise.comum import multivariada as mv


def _adapta_factor_analyzer():
    """factor_analyzer 0.5.1 chama check_array(force_all_finite=...), removido no scikit-learn 1.9."""
    def check_array(X, force_all_finite=True, **kw):
        return _check_array_sklearn(X, ensure_all_finite=force_all_finite, **kw)
    fa_mod.check_array = check_array


_adapta_factor_analyzer()


@pytest.fixture(scope="module")
def dados_2fatores():
    rng = np.random.default_rng(7)
    n = 3000
    L = np.array([[.8, 0], [.7, 0], [.6, .1], [.7, 0], [0, .8], [.1, .7], [0, .6], [0, .7]])
    Phi = np.array([[1, .3], [.3, 1]])
    F = rng.multivariate_normal([0, 0], Phi, n)
    E = rng.standard_normal((n, 8)) * np.sqrt(1 - (L @ Phi * L).sum(axis=1))
    return F @ L.T + E


def _alinha(A, B):
    """Ordem e sinal das colunas de A para casar com B (soluções fatoriais são definidas até permutação e sinal)."""
    k = A.shape[1]
    import itertools
    melhor, err = None, np.inf
    for perm in itertools.permutations(range(k)):
        C = A[:, perm]
        C = C * np.sign(np.sum(C * B, axis=0))
        e = np.abs(C - B).max()
        if e < err:
            melhor, err = C, e
    return melhor


def test_pca_svd_igual_sklearn(dados_2fatores):
    X = dados_2fatores
    r = mv.pca_svd(X)
    ref = PCA().fit(mv.padroniza(X))
    assert np.allclose(r["autovalores"], ref.explained_variance_, atol=1e-8)
    # autovalores da SVD = autovalores da matriz de correlação
    assert np.allclose(r["autovalores"], np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1], atol=1e-8)
    # escores = Z V
    assert np.allclose(r["escores"], r["Z"] @ r["V"], atol=1e-8)


def test_kmo_bartlett_iguais_factor_analyzer(dados_2fatores):
    X = dados_2fatores
    R = np.corrcoef(X, rowvar=False)
    k, msa = mv.kmo(R)
    msa_ref, k_ref = calculate_kmo(X)
    assert abs(k - k_ref) < 1e-6 and np.allclose(msa, msa_ref, atol=1e-6)
    chi2, gl, p = mv.bartlett(R, len(X))
    chi2_ref, p_ref = calculate_bartlett_sphericity(X)
    assert abs(chi2 - chi2_ref) / chi2_ref < 1e-6 and gl == 28


def test_alfa_formula():
    X = np.column_stack([np.arange(10.0)] * 4)
    assert abs(mv.alfa_cronbach(X) - 1) < 1e-12


@pytest.mark.parametrize("metodo", ["ml", "minres"])
def test_af_igual_factor_analyzer(dados_2fatores, metodo):
    # eixos principais iterados convergem para a solução de mínimos quadrados (minres) do factor_analyzer;
    # o "principal" do factor_analyzer é PCA sem iteração e não serve de referência.
    X = dados_2fatores
    R = np.corrcoef(X, rowvar=False)
    ref = FactorAnalyzer(n_factors=2, method=metodo, rotation=None, is_corr_matrix=True).fit(R)
    meu = mv.af_ml(R, 2) if metodo == "ml" else mv.af_eixos_principais(R, 2)
    A = _alinha(meu["cargas"], ref.loadings_)
    assert np.allclose(A, ref.loadings_, atol=2e-3)
    assert np.allclose(meu["comunalidades"], ref.get_communalities(), atol=2e-3)


def test_rotacoes_iguais_factor_analyzer(dados_2fatores):
    R = np.corrcoef(dados_2fatores, rowvar=False)
    L = mv.af_ml(R, 2)["cargas"]
    v, _ = mv.varimax(L)
    v_ref = Rotator(method="varimax", max_iter=5000, tol=1e-12).fit_transform(L)
    assert np.allclose(_alinha(v, v_ref), v_ref, atol=1e-4)
    # o factor_analyzer não aplica a normalização de Kaiser no oblimin; comparamos sem normalizar
    o, Phi, _ = mv.oblimin(L, normaliza=False)
    rot = Rotator(method="oblimin", max_iter=5000, tol=1e-10)
    o_ref = rot.fit_transform(L)
    assert np.allclose(_alinha(o, o_ref), o_ref, atol=1e-3)
    assert abs(abs(Phi[0, 1]) - abs(rot.phi_[0, 1])) < 1e-3
    assert 0.2 < abs(Phi[0, 1]) < 0.4          # correlação verdadeira 0,3


def test_policorica_recupera_correlacao_conhecida():
    rng = np.random.default_rng(11)
    rho = 0.6
    Z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], 20000)
    x = np.digitize(Z[:, 0], [-1.0, 0.0, 0.8, 1.5])
    y = np.digitize(Z[:, 1], [-0.5, 0.5, 1.2])
    r = mv.policorica_par(x, y)
    assert abs(r - rho) < 0.02
    # Pearson nas categorias subestima
    assert np.corrcoef(x, y)[0, 1] < r


def test_tucker():
    a = np.array([.7, .8, .6])
    assert abs(mv.tucker(a, a) - 1) < 1e-12
    assert abs(mv.tucker([1, 0], [0, 1])) < 1e-12
    assert abs(mv.tucker(a, 2 * a) - 1) < 1e-12


def test_analise_paralela_reprodutivel():
    a = mv.analise_paralela(500, 5, reps=200, semente=1)
    b = mv.analise_paralela(500, 5, reps=200, semente=1)
    assert np.allclose(a["p95"], b["p95"]) and a["p95"][0] > 1 > a["p95"][-1]


def test_escores_regressao_1fator(dados_2fatores):
    X = dados_2fatores[:, :4]
    R = np.corrcoef(X, rowvar=False)
    L = mv.af_ml(R, 1)["cargas"]
    Z = mv.padroniza(X)
    F = mv.escores_regressao(Z, R, L)
    ref = FactorAnalyzer(n_factors=1, method="ml", rotation=None).fit(X)
    Fr = ref.transform(X)
    assert abs(abs(np.corrcoef(F[:, 0], Fr[:, 0])[0, 1]) - 1) < 1e-4
