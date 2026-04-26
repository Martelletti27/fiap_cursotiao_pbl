# FarmTech Solutions - Fase 1

Manejo agrícola e cálculo de insumos: aplicação em **Python** (CLI) para planejamento de áreas, doses e manejos, e análise em **R** para tratamentos e exportação em CSV.

## Estrutura

```
Fase 1/
├── apps/
│   ├── python_app/     # Interface CLI (menu interativo)
│   └── r_app/         # Análise estatística (R)
└── docs/              # Demos / links (ex.: YouTube)
```

## Como executar o código

### Aplicação Python (CLI)

No terminal, a partir da pasta `apps` (onde o pacote `python_app` é reconhecido):

```bash
cd Fase 1/apps
python -m python_app
```

**Requisitos:** Python 3.10+ (ajuste se o projeto exigir outra versão).

### Scripts R

Com o [R](https://www.r-project.org/) instalado, execute no diretório do script (ajuste o caminho conforme seu SO):

```bash
cd Fase 1/apps/r_app
Rscript analysis.R
```

*(Se o projeto usar RStudio, abra `analysis.R` e execute o arquivo.)*

---

## Funcionalidades (resumo)

- Cálculo de área plantada (retangular ou pivô circular)
- Estimativa de insumos e aplicações por hectare
- Registro de manejos e produtos
- Exportação de dados em CSV para análise no R
