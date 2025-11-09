-- Consulta a tabela toda
select * from sensores_fazenda;

-- Conta quantos registros tem a tabela
select count(*) as total_registros from sensores_fazenda;

-- Confere qual a primeira e a ultima leitura
select min(captured_date) as data_primeira_leitura,
       max(captured_date) as data_ultima_leitura
from sensores_fazenda;

-- Traz a media de alguns indicadores
select avg(temperature_c) as media_temperatura_c, 
       trunc(avg(humidity_percent),2) as media_umidade_percent,
       trunc(avg(soil_moisture_percent),2) as media_umidade_solo,
       trunc(avg(ph),2) as media_ph
from sensores_fazenda;

-- registros quando umidade do solo (abaixo de 40%) e status da bomba
select captured_date,
       captured_time,
       soil_moisture_percent,
       irrigation_command
from sensores_fazenda
where soil_moisture_percent < 40;

-- ocorrencias de ph fora da faixa ideal (6,5 a 7,5)
select captured_date,
       captured_time,
       ph
from sensores_fazenda
where ph < 5.5 or ph > 7.5;

-- ocorrencias de estresse térmico (temperatura > 30 °c e umidade < 40%)
select captured_date,
       captured_time,
       temperature_c,
       humidity_percent
from sensores_fazenda
where temperature_c > 30 and humidity_percent < 40;

-- médias diárias de temperatura e umidade do ar
select captured_date as data_leitura,
       round(avg(temperature_c), 2) as media_temperatura_c,
       round(avg(humidity_percent), 2) as media_umidade_percent
from sensores_fazenda
group by captured_date
order by data_leitura;

-- Ranking top 5 leituras com menor ph
select *
from sensores_fazenda
order by ph asc
fetch first 5 rows only;