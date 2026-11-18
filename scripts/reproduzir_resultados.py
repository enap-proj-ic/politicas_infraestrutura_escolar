#!/usr/bin/env python3
"""Reproduz M0/M1/M2, S1/S2 e S3 da base pública congelada.

Implementação independente de documentos e diretórios privados, adaptada das
rotinas analíticas congeladas do estudo. Não recalcula/transforma as fontes INEP
originais: começa da base analítica disponibilizada no pacote.

Uso: python scripts/reproduzir_resultados.py [--rapido] [--saida caminho]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import linalg, stats

BASE_SHA256 = 'd275195c7d2692f47507349015e3e17666458038fb41f9b1863f9cce3c7ad2ca'
TERMS = ['biblioteca_leitura', 'banheiro_acessivel', 'lab_ciencias', 'servicos_gerais']
SPECS = [
    ('M0', False, None, False),
    ('M1', True, None, False),
    ('M2', True, 'servicos_gerais', False),
    ('S1_log_pessoal', True, 'log1p_servicos', False),
    ('S2_referencia', True, 'servicos_gerais', False),
    ('S2_abandono22', True, 'servicos_gerais', True),
]


def design(d: pd.DataFrame, physical=False, staff=None, abandon=False):
    """Mesmo projeto de matriz do protocolo congelado; referências menores códigos."""
    names = ['inse21', 'ird22', 'log_matriculas']
    if physical: names += ['biblioteca_leitura', 'banheiro_acessivel', 'lab_ciencias']
    if staff: names += [staff]
    if abandon: names += ['abandono22']
    z = d[names].astype(float).copy()
    cats = pd.get_dummies(d[['icg22', 'dependencia', 'localizacao', 'uf']].astype(str),
                          drop_first=True, dtype=float)
    return pd.concat([pd.Series(1., index=d.index, name='Intercepto'), z, cats], axis=1)


def solve(X, y, groups):
    """OLS, sandwich CR1 (município) e HC3; mesmas correções do estudo."""
    n, k = X.shape
    coef, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    if rank != k: raise ValueError(f'Matriz sem posto completo: {rank}/{k}')
    Q, R = np.linalg.qr(X, mode='reduced')
    if not np.allclose(coef, linalg.solve_triangular(R, Q.T @ y), rtol=1e-7, atol=1e-8):
        raise AssertionError('OLS via QR difere do lstsq')
    invR = linalg.solve_triangular(R, np.eye(k))
    bread = invR @ invR.T
    resid = y - X @ coef
    leverage = (Q * Q).sum(axis=1)
    group_names, group_index = np.unique(groups, return_inverse=True)
    G = len(group_names)
    scores = np.zeros((G, k))
    np.add.at(scores, group_index, X * resid[:, None])
    cr1 = (G/(G-1) * (n-1)/(n-k)) * bread @ (scores.T @ scores) @ bread
    weighted = X * (resid/(1-leverage))[:, None]
    hc3 = bread @ (weighted.T @ weighted) @ bread
    r2 = 1 - (resid @ resid) / np.sum((y-y.mean())**2)
    return dict(coef=coef, cr1=cr1, hc3=hc3, G=G, n=n, k=k, R2=r2)


def estimates(name, columns, result, types=('cluster','hc3')):
    rows = []
    n,k,G=result['n'],result['k'],result['G']
    for typ in types:
        cov = result['cr1' if typ == 'cluster' else 'hc3']
        df = G-1 if typ=='cluster' else n-k
        se = np.sqrt(np.diag(cov)); crit=stats.t.ppf(.975,df)
        for idx,term in enumerate(columns):
            b=result['coef'][idx]
            rows.append(dict(modelo=name,termo=term,covariancia=typ,beta=b,
                erro_padrao=se[idx],ic95_inf=b-crit*se[idx],ic95_sup=b+crit*se[idx],
                p=2*stats.t.sf(abs(b/se[idx]),df),N=n,municipios=G,R2=result['R2']))
    return rows


def spline(x, t):
    """Base de splines cúbicos restritos: quatro nós, dois termos não lineares."""
    return np.column_stack([
        (np.maximum(x-t[j],0)**3
         - np.maximum(x-t[-2],0)**3*(t[-1]-t[j])/(t[-1]-t[-2])
         + np.maximum(x-t[-1],0)**3*(t[-2]-t[j])/(t[-1]-t[-2]))/(t[-1]-t[0])**2
        for j in range(2)
    ])


def verify_rows(observed, reference_path, model_column='modelo'):
    ref = pd.read_csv(reference_path)
    keys = ['modelo','termo'] + (['covariancia'] if 'covariancia' in ref.columns else [])
    left = observed.set_index(keys)
    right = ref.set_index(keys)
    for key in right.index:
        if key not in left.index:
            raise AssertionError(f'Linha faltando: {key} em {reference_path.name}')
        for col in ['beta','ic95_inf','ic95_sup','p']:
            a=float(left.loc[key,col]); b=float(right.loc[key,col]);
            if abs(a-b)>2e-7:
                raise AssertionError(f'{reference_path.name}: {key} {col}: {a} != {b}')
    return len(ref)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rapido',action='store_true',help='Reproduz apenas M0–M2')
    parser.add_argument('--saida',default=None,help='Pasta opcional para CSV gerados')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    data_path=root/'data/base_analitica_final.csv'
    observed_hash=hashlib.sha256(data_path.read_bytes()).hexdigest()
    if observed_hash != BASE_SHA256:
        raise AssertionError(f'Hash da base divergente: {observed_hash}')
    d=pd.read_csv(data_path,dtype={'CO_ENTIDADE':'string','municipio':'string'})
    assert len(d)==27315 and d.municipio.nunique()==5228 and d.CO_ENTIDADE.is_unique
    allrows=[]; fits=[]
    for name,physical,staff,abandon in SPECS[:3] if args.rapido else SPECS:
        frame=d.dropna(subset=['abandono22']) if name.startswith('S2_') else d
        matrix=design(frame,physical,staff,abandon)
        result=solve(matrix.to_numpy(),frame.ideb23.to_numpy(),frame.municipio.to_numpy())
        allrows.extend(estimates(name,matrix.columns,result))
        fits.append(dict(modelo=name,N=result['n'],municipios=result['G'],R2=result['R2']))
        print(f'{name}: N={result["n"]}, municípios={result["G"]}, R²={result["R2"]:.9f}',flush=True)
    output=pd.DataFrame(allrows)
    checked=verify_rows(output[output.modelo.isin(['M0','M1','M2'])],root/'resultados/TABELA_2_MODELOS.csv')
    print('Conferidas linhas M0–M2:',checked,flush=True)
    if not args.rapido:
        checked_sens=verify_rows(output[~output.modelo.isin(['M0','M1','M2'])],root/'resultados/SENSIBILIDADES.csv')
        print('Conferidas linhas S1/S2:',checked_sens,flush=True)
        z=design(d,True,'servicos_gerais')
        for c in ['inse21','ird22','log_matriculas']:
            knots=d[c].quantile([.05,.35,.65,.95],interpolation='linear').to_numpy()
            extra=spline(d[c].to_numpy(),knots)
            for j in range(2): z[f'{c}_spline_{j+1}']=extra[:,j]
        r=solve(z.to_numpy(),d.ideb23.to_numpy(),d.municipio.to_numpy())
        assert r['k']==46
        rows=estimates('S3_controles_flexiveis',z.columns,r,types=('cluster',))
        s3=pd.DataFrame(rows)
        checked_s3=verify_rows(s3,root/'resultados/S3_COEFICIENTES.csv')
        print(f'S3: R²={r["R2"]:.9f}; conferidas {checked_s3} linhas',flush=True)
        output=pd.concat([output,s3],ignore_index=True)
        fits.append(dict(modelo='S3_controles_flexiveis',N=r['n'],municipios=r['G'],R2=r['R2']))
    f=pd.DataFrame(fits).set_index('modelo')
    assert abs(f.loc['M0','R2']-0.450678)<1e-6
    assert abs(f.loc['M1','R2']-0.451774)<1e-6
    assert abs(f.loc['M2','R2']-0.451903)<1e-6
    print('Delta R² M2−M0:',f.loc['M2','R2']-f.loc['M0','R2'])
    if args.saida:
        p=Path(args.saida);p.mkdir(parents=True,exist_ok=True)
        output.to_csv(p/'coeficientes_reproduzidos.csv',index=False)
        f.to_csv(p/'ajuste_reproduzido.csv')
    print('REPLICAÇÃO NUMÉRICA CONFERIDA',flush=True)

if __name__=='__main__': main()
