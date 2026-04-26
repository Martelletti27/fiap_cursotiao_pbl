# FarmTech Solutions - Fase 2

Irrigação inteligente: **ESP32** (Wokwi), integração **Python** com API meteorológica (Open-Meteo) e análise em **R** para apoiar a decisão de irrigação.

## Estrutura

```
Fase 2/apps/
├── esp32_app/            # Firmware ESP32 + Wokwi (simulação)
├── python_integration/   # Cliente Open-Meteo e token para o Wokwi
└── r_integration/        # Análises e apoio à decisão de irrigação
```

Cada subpasta possui o próprio README com detalhes.

## Como executar o código

| Módulo | O que fazer | Documentação |
|--------|-------------|--------------|
| **ESP32 / Wokwi** | Compilar com PlatformIO e simular no Wokwi | [apps/esp32_app/README.md](apps/esp32_app/README.md) |
| **Python (Open-Meteo)** | Ambiente virtual e CLI para gerar token meteorológico | [apps/python_integration/README.md](apps/python_integration/README.md) |
| **R** | Scripts de análise e integração com o fluxo do ESP32 | [apps/r_integration/README.md](apps/r_integration/README.md) |

**Ordem sugerida:** subir o token/API com `python_integration` se for usar o fluxo com clima; em seguida, simular o `esp32_app` no Wokwi; usar `r_integration` conforme a atividade.

---

## Visão geral (IoT + API)

- Sensores simulados: N/P/K, pH (LDR), umidade (DHT22), relé de bomba
- Decisão de irrigação com base em leituras e previsão de chuva (integração Python)

Para pinagem de hardware e tabela de condições, veja o README do [esp32_app](apps/esp32_app/README.md).
