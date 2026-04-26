# Fase 6 – Parte 1

Entrega da **Parte 1** da Fase 6 (PBL): **detecção de objetos** com dataset no formato YOLO, com as classes **maquinário** e **animais** (`nc: 2` em `dataset.yaml`).

## Vídeo (YouTube)

Demonstração e contexto do trabalho no canal:

**[Assistir no YouTube](https://youtu.be/EETQwaxnGd4)**

## Dataset

O conjunto de imagens, rótulos e metadados (`images/`, `labels/`, `dataset.yaml`) está publicado no Google Drive:

**[Abrir pasta do dataset (Google Drive)](https://drive.google.com/drive/folders/11R9UVX61jsb6zilf1-w5yRy4QxGQtnvL?usp=sharing)**

Após o download, ajuste o campo **`path:`** em `dataset.yaml` para o caminho local (ou de ambiente de treino, ex.: Colab) onde a pasta do dataset estiver, mantendo `train`, `val` e `test` relativos a esse `path` conforme a estrutura abaixo.

## Notebook (Jupyter)

Treinamento/validação com YOLOv8n. Abra no Jupyter ou VS Code a partir do clone do repositório, ou use o link do GitHub:

- **Arquivo:** [Matheus_rm566767_pbl_fase6_Yolo8n.ipynb](Matheus_rm566767_pbl_fase6_Yolo8n.ipynb)

## Estrutura

```
Parte 1/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
├── dataset.yaml
├── Matheus_rm566767_pbl_fase6_Yolo8n.ipynb
└── README.md
```

## Como executar o código

- Dependências usuais: **Python 3.10+**, **PyTorch** (conforme seu ambiente) e **Ultralytics** (`pip install ultralytics`) para YOLOv8, ou outro framework indicado no enunciado da disciplina.
- Aponte o treinamento para o `dataset.yaml` desta pasta (ou cópia com `path` corrigido) e use as pastas `images/*` e `labels/*` já alinhadas por split.
- Se usar Colab/Drive, sincronize a pasta do dataset e atualize `path` em `dataset.yaml` de acordo.

---

[Voltar à Fase 6](../README.md)
