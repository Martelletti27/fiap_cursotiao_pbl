# Manual de Importação da Base de Sensores no Oracle

Este manual descreve o procedimento para importar a base de dados `fase2_sensor_readings.csv` para o banco de dados Oracle, utilizando o Oracle SQL Developer.  
As imagens que ilustram as etapas estão armazenadas na pasta `assets/prints_oracle`.

## Pré-requisitos

- Acesse um ambiente Oracle válido (schema `RM####` (seu RM FIAP) no banco `BD_FIAP_ORCL`).
- Instale e conecte o Oracle SQL Developer ao schema de destino.
- Mantenha o arquivo `assets/fase2_sensor_readings.csv` disponível no diretório local.

## Etapas de Importação

### 1. Abra o assistente de importação
Clique com o botão direito em **Tables** e selecione **Import Data**.  
Escolha o arquivo `assets/fase2_sensor_readings.csv`.  
Defina o delimitador como ponto e vírgula para facilitar a leitura de dados Float.
Confira os dados para confirmar a leitura correta.

![Visualização do arquivo CSV](assets/prints_oracle/step%201.png)

### 2. Defina o método de importação e a tabela de destino
Selecione o método **Insert** e informe o nome da tabela **SENSORES_FAZENDA**.  
Confirme a opção de criação automática da tabela.

![Configuração do método de importação](assets/prints_oracle/step%202.png)

### 3. Selecione as colunas do arquivo
Confirme se todas as colunas do arquivo CSV foram detectadas e estão na ordem correta.

![Seleção das colunas](assets/prints_oracle/step%203.png)

### 4. Configure os tipos de dados
Revise o tipo de dados de cada coluna.  
Defina as colunas numéricas (`ph`, `temperature_c`, `humidity_percent`, etc.) como **FLOAT** e atribua **escala 1** para preservar os valores decimais.  
Mantenha o tipo **VARCHAR2** para campos textuais (`captured_at`, `irrigation_command`).

![Definição das colunas de destino](assets/prints_oracle/step%204.png)

### 5. Revise o resumo da importação
Verifique a conexão, o arquivo de origem, os tipos de dados e as colunas selecionadas.  
Clique em **Finish** para executar a importação.

![Resumo antes de finalizar](assets/prints_oracle/step%205.png)

### 6. Confirme a conclusão
Aguarde a mensagem de sucesso do assistente e clique em **OK**.

![Importação concluída](assets/prints_oracle/step%206.png)

### 7. Valide a estrutura da tabela
Abra a tabela **SENSORES_FAZENDA** no painel de objetos e confirme a criação correta das colunas.

![Estrutura da tabela criada](assets/prints_oracle/step%207.png)

### 8. Confira o script gerado
Visualize o script SQL gerado automaticamente pelo SQL Developer.

![Script de criação da tabela](assets/prints_oracle/step%208.png)

```sql
CREATE TABLE "RM566767"."SENSORES_FAZENDA"
   (    "MEASUREMENT_ID" NUMBER(38,0),
        "CAPTURED_DATE" DATE,
        "CAPTURED_TIME" VARCHAR2(26 BYTE),
        "SOIL_MOISTURE_PERCENT" FLOAT(126),
        "PH" FLOAT(126),
        "TEMPERATURE_C" FLOAT(126),
        "HUMIDITY_PERCENT" FLOAT(126),
        "NITROGEN_ALERT" NUMBER(38,0),
        "PHOSPHORUS_ALERT" NUMBER(38,0),
        "POTASSIUM_ALERT" NUMBER(38,0),
        "RAIN_MM_FORECAST" FLOAT(126),
        "RAIN_PROBABILITY_PERCENT" NUMBER(38,0),
        "RAIN_BLOCK" NUMBER(38,0),
        "IRRIGATION_COMMAND" VARCHAR2(26 BYTE),
        "RELAY_ON" NUMBER(38,0)
   ) SEGMENT CREATION IMMEDIATE
    PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255
   NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "TSBC_ALUNOS";


### 9. Execute a validação final
Realize a validação da importação executando o comando SQL abaixo para visualizar os registros carregados na tabela.

![Consulta geral da tabela](assets/prints_oracle/step%209.png)

```sql
select * from sensores_fazenda;
```

Confirme se os valores decimais e demais campos foram importados corretamente.  
Essa consulta permite verificar a integridade e o formato dos dados armazenados.

### 10. Referência adicional
Consulte o script completo com todas as consultas SQL utilizadas para análise e validação da base.

O arquivo encontra-se no diretório:

```
scripts/Consultas.sql
```
