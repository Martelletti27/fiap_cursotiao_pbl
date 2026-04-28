# Fase 6 – Parte 2

Entrega da Parte 2 da Fase 6 (PBL): comparativo entre três abordagens de visão
computacional para detecção e classificação de objetos em fazendas (classes:
`maquinarios` e `animais`).

---

## Vídeo (YouTube)

> Link será adicionado em breve.

---

## Dataset

O mesmo conjunto de imagens utilizado na Parte 1 (Matheus) foi reaproveitado
nesta entrega. As imagens, rótulos e metadados (`images/`, `labels/`, `dataset.yaml`)
estão publicados no Google Drive do colega:

**[Abrir pasta do dataset (Google Drive)](https://drive.google.com/drive/folders/11R9UVX61jsb6zilf1-w5yRy4QxGQtnvL?usp=sharing)**

Após o download, ajuste o campo `path:` em `dataset.yaml` para o caminho local
(ou de ambiente de treino, ex.: Colab) onde a pasta do dataset estiver.

---

## Notebooks

| Abordagem | Arquivo | Descrição |
|-----------|---------|-----------|
| YOLOv5n | `Felipe_rm567521_pbl_fase6_Yolo5n.ipynb` | Detecção com YOLOv5n — 30 épocas |
| CNN do Zero | `Felipe_rm567521_pbl_fase6_CNN.ipynb` | Classificação binária com CNN treinada do zero — 30 épocas |

---

## Comparativo dos Três Modelos

A Fase 6 contempla três abordagens distintas aplicadas ao mesmo dataset,
permitindo uma análise comparativa direta entre detecção e classificação de objetos.

### Métricas de Desempenho

| Métrica | YOLOv8n (Parte 1 — 30 épocas) | YOLOv8n (Parte 1 — 60 épocas) | YOLOv5n (Parte 2 — 30 épocas) |
|---------|-------------------------------|-------------------------------|-------------------------------|
| Precision |0.8771 |0.8266 |0.818 | N/A |
| Recall |0.7827 |0.7557 |0.847| N/A |
| mAP50 |0.8570 |0.8596 | 0.859 | N/A |
| mAP50-95 |0.5965 |0.5945 |0.523 | N/A |

| CNN do Zero (Parte 2 — 30 épocas) |
|-----------------------------------|
| Acurácia no teste |0.500 |
| Loss no teste |60.4551 |
| Tempo de treinamento (30 épocas) | 47.04 segundos |
| Tempo médio de inferência por imagem |0.0135|

---

### Análise Comparativa

**YOLOv8n vs YOLOv5n (detecção)**

Ambos realizam detecção de objetos com bounding box, identificando *onde* e
*o quê* é cada objeto na imagem. O YOLOv8 é a versão mais recente da família
YOLO, com melhorias de arquitetura em relação ao YOLOv5. A comparação entre
30 e 60 épocas no YOLOv8 (Parte 1) permite observar o ganho de desempenho
com mais iterações de treino, ao custo de maior tempo computacional.

**YOLO vs CNN (detecção vs classificação)**

A CNN treinada do zero realiza apenas *classificação global*: recebe a imagem
inteira e decide qual classe predomina, sem localizar o objeto. O YOLO, por outro
lado, localiza e classifica cada objeto simultaneamente com bounding boxes.

Para um dataset pequeno e desbalanceado como o utilizado (74 instâncias de
`animais` vs 12 de `maquinarios`), a CNN do zero apresentou acurácia próxima
de 50% — equivalente a um chute aleatório — enquanto o YOLOv5 atingiu
mAP50 = 0.859. Isso se deve a dois fatores principais: o YOLO se beneficia de
pesos pré-treinados no COCO (transfer learning implícito), e sua arquitetura é
especializada para detectar objetos mesmo com poucos exemplos por classe.

**Conclusão**

Para aplicações reais de monitoramento de fazendas — onde é fundamental saber
*onde* o animal ou maquinário está na cena — arquiteturas de detecção como
YOLO são amplamente superiores a classificadores CNN do zero, especialmente
quando o dataset é pequeno. A CNN seria mais competitiva com um dataset maior,
balanceado e com técnicas de transfer learning aplicadas.

---

## Estrutura

---

Fase 6/Parte 2/ ├── Felipe_rm567521_pbl_fase6_Yolo5n.ipynb ├── Felipe_rm567521_pbl_fase6_CNN.ipynb └── README.md

---

## Como Executar

**YOLOv5:**
1. Abra o notebook `Felipe_rm567521_pbl_fase6_Yolo5n.ipynb` no Colab
2. Ative GPU T4 em `Ambiente de execução → Alterar tipo de ambiente de execução`
3. Execute as células em ordem — o notebook clona o repositório YOLOv5, instala
   as dependências e aponta para o dataset no Drive automaticamente
4. O `dataset.yaml` utilizado é o mesmo da Parte 1

**CNN:**
1. Abra o notebook `Felipe_rm567521_pbl_fase6_CNN.ipynb` no Colab
2. Execute as células em ordem — o notebook reorganiza as imagens do Drive
   em subpastas por classe e treina a CNN com Keras/TensorFlow
3. Dependências: `tensorflow`, `numpy`, `matplotlib`, `Pillow`
   (já disponíveis no Colab por padrão)

> Atenção: sempre execute a partir da primeira célula após uma reconexão do Colab,
> pois as pastas em `/content/` são perdidas ao reiniciar a sessão.
