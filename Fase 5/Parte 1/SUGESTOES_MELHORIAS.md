# Sugestões de melhorias — PBL Fase 5

Sugestões para aplicarmos futuramente ao notebook de previsão de rendimento de safra.

---

## 1. Validação cruzada (quando retomada)

Se voltar a usar validação cruzada no lugar do split único:

- **Estratificação por cultura:** Usar `StratifiedKFold` ou `GroupKFold` com `Crop` como grupo, pois Yield tem escalas muito diferentes por cultura (Cocoa, Oil palm, Rice, Rubber). Isso evita folds desbalanceados e métricas instáveis.

- **Bug de desvio padrão:** Ao exibir RMSE e MAE na CV, verificar o sinal das métricas negativas do sklearn (`neg_mean_squared_error`, `neg_mean_absolute_error`). O desvio padrão não deve aparecer negativo — garantir que seja sempre `std()` positivo nos arrays de métricas.

---

## 2. Treinamento por cultura

- Avaliar treinar um modelo específico por cultura (Cocoa, Oil palm, Rice, Rubber), já que cada uma tem relação distinta com clima (ex.: Rubber com correlação negativa).
- **Cuidado:** Com ~39 amostras por cultura, o risco de overfitting é alto. Vale mais a pena em cenários com mais dados.

---

## 3. Outras melhorias

- Reexecutar o notebook após alterações para que os outputs exibidos reflitam o código atual (split único vs CV).
