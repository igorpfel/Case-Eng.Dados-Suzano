--Construção de um fluxo de engenharia de dados — Indicadores Econômicos (Suzano Case)

Este projeto entrega um pipeline de dados automatizado para ingestão e armazenamento dos indicadores econômicos USD/CNY e Chinese PMI que são encontrados nos link's : 

https://br.investing.com/currencies/usd-cny-historical-data
https://br.investing.com/economic-calendar/chinese-manufacturing-pmi-594

*** Observação : A ideia inicial proposta no case seria extrair os dados de um outro link ( https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596), porem ao acessar o site, constatei que os dados nao estavam completos e nem continha historico, devido a isso, procurei outro indice de pmi da china, onde encontrei o indice industrial que contem os mesmos campos e formas de mensuração das informações. 

** Dificuldades encontradas : Outro ponto em que necessitei alterar o proposto no case, seria a obtençao dos dados, no case nao foi especificado que a obtenção dos  seria algo em tempo real, ou que necessitaria de um webscraping nos sites, apos algumas tentativas de se realizar um scraping porem sem sucesso devido a complexidade e volatilidade dos sites (os mesmos nao possui api publica para conexao) optei por extrair os dados manualmente contendo todo historico de ambas as paginas, com isso gerei as fontes em CSV, e segui todo o processo de criaçao do fluxo, uma sugestão de melhoria deste processo manual  seria a criação de um RPA em Python que navega em um site e mapeia as ações do mouse, utilizando a biblioteca PyAutoGUI. Essa biblioteca permite controlar o mouse e o teclado para interagir com a interface gráfica do usuário onde mapeia por exemplos clics do mouse e replica tudo que o usuario fez na pagina e com isso automatiza essa questao de extrair os dados do site para a fonte. 


* Objetivo

Automatizar a coleta de dois indicadores econômicos.

Armazenar os dados em um banco de dados relacional (PostgreSQL).

Executar o processo diariamente com orquestração via Airflow.

Bônus:

Terraform + GCP para infraestrutura como código.



* Estrutura do Projeto


investing_pipeline/
	fonte/             
	 scripts/
	   └── load_data.py          (ETL)
	 dags/
   	   └──  investing_pipeline.py (AIRFLOW)
	Dockerfile
	 docker-compose.yml
	requirements.txt
	 terraform/                ( GCP)
	└──main.tf
	└──cloud_run.tf
	└──composer.tf
	diagrama.png            
	README.md


* Fontes de Dados

- `fonte/usd_cny_data.csv`:  (Histórico de câmbio USD/CNY)
- `fonte/chinese_pmi_data.csv`: ( Índice PMI da China)


*Tecnologias Utilizadas

- Python 3.10
- Pandas + SQLAlchemy
- PostgreSQL
- Docker + Docker Compose
- Apache Airflow
-Terraform
-Google Cloud Platform (GCP)



* Execução Local

*1. Clonar o repositório e acessar a pasta

git clone <repo-url>
cd investing_pipeline

 2. Subir PostgreSQL + Airflow com Docker Compose

 --bash
docker-compose up -d


 3. Executar o pipeline (ETL)

--bash
docker build -t investing-pipeline .
docker run --rm -v "%cd%/fonte:/app/fonte" --network=projeto_default investing-pipeline


Resultado  : Ira ler os arquivos CSV na fonte realizar o tratamento e inserir os dados no banco de daodos com duas tabelas: `usd_cny_exchange` e `chinese_pmi_index`.



*Estrutura das Tabelas

--Tabela `usd_cny_exchange`

Campo  |	Tipo
date         DATE
close	FLOAT
open	FLOAT
high	FLOAT
low	FLOAT
volume	TEXT

-- Tabela `chinese_pmi_index`

 Campo   | Tipo   

 date               DATE   
 actual_state  FLOAT  
 forecast         FLOAT  
 close              FLOAT  



Orquestração com Airflow

Uma DAG que se chama `investing_pipeline.py` foi criada na pasta `dags/`, e foi agendada agendada para rodar diariamente( confome o case solicitou) e executar o script `load_data.py`.


*Acesse o Airflow:

http://localhost:8080
Usuário: airflow
Senha: airflow

*** Bônus: Provisionamento na Nuvem com Terraform + GCP

Componentes Criados via Terraform

Instância Cloud SQL (PostgreSQL)

Ambiente do Cloud Composer (Apache Airflow gerenciado)

Deploy da aplicação em Cloud Run (container Docker com o ETL)

Etapas

Criar bucket para DAGs no GCS..

Subir scripts para o bucket do Composer.

Executar DAG via interface do Composer.

*** Obs: A DAG no Composer falhou por dependências de pacotes e problemas de path dos CSVs, mas toda a infraestrutura esta correta e é funcional.



-Observações Finais : 

O projeto exibe um pipeline funcional para ingestão e orquestração dos dados provenientes de fontes locais , mas com escalabilidade em mente. Apesar de ajustes necessários devido à limitação dos sites, o resultado atinge os objetivos propostos e está preparada para produção com pequenas melhorias e ajustes principalmente a questao das fontes. 

