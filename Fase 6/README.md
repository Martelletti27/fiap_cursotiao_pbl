# FarmTech Solutions - Fase 6

A **Fase 6** aborda visão computacional aplicada ao contexto do projeto (**FarmTech**), com foco em **detecção de objetos** em imagens (YOLO e formato de dataset padrão YOLO).

A fase divide-se em **duas partes**; cada uma possui o próprio **README** com instruções e links de apoio.

## Partes e READMEs

| Parte | Tema | README |
|--------|------|--------|
| **1** | Dataset de detecção (classes *maquinário* e *animais*), treinamento YOLOv8n com comparação de 30 e 60 épocas, vídeo no YouTube e material no Google Drive | [Parte 1/README.md](Parte%201/README.md) |
| **2** | Comparativo entre YOLOv5n e CNN treinada do zero, análise crítica de 3 abordagens de visão computacional | [Parte 2/README.md](Parte%202/README.md) |

## Estrutura

```
Fase 6/
├── Parte 1/
│   ├── images/
│   │   ├── train/          # 120 imagens (61 animais + 59 maquinários)
│   │   ├── val/            # 20 imagens (10 + 10)
│   │   └── test/           # 20 imagens (10 + 10)
│   ├── labels/
│   │   ├── train/          # 120 rótulos YOLO
│   │   └── val/            # 20 rótulos YOLO
│   ├── dataset.yaml
│   ├── Matheus_rm566767_pbl_fase6_Yolo8n.ipynb
│   └── README.md
├── Parte 2/
│   ├── Felipe_rm567521_pbl_fase6_Yolo5n.ipynb
│   ├── Felipe_rm567521_pbl_fase6_CNN.ipynb
│   └── README.md
└── README.md
```

## Resumo geral

- **Parte 1:** preparação e documentação do **dataset** no formato YOLO para treino/validação/teste de um detector com 2 classes (**maquinário** e **animais**); treinamento com **YOLOv8n** em 30 e 60 épocas; análise comparativa de desempenho. Link do **vídeo** e da **pasta no Drive** estão no [README da Parte 1](Parte%201/README.md).
- **Parte 2:** comparativo entre **YOLOv5n** (YOLO tradicional) e uma **CNN treinada do zero** (Keras/TensorFlow), ambas aplicadas ao mesmo dataset da Parte 1. Avaliação crítica em termos de precisão, facilidade de uso, tempo de treinamento e inferência. Link do **vídeo** e dos **notebooks executados no Drive** estão no [README da Parte 2](Parte%202/README.md).
