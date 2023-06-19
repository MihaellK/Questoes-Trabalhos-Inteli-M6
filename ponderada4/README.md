
# Sistema de Visão computacional

## Passo a passo

### Supabase

Primeiramente devemos criar nosso projeto no Supabase, isso possibilitará a criação dos "buckets"
Para que nossa aplicaçõa tenha acesso ao nosso _storage_ do Supabase devemos salvar a URL do Projeto e sua _service role_

![Configurações Supabase](./midia/supaSet.png)


### Publisher

### Subscriber


![]()

1. Criação de um Bucket
2. 
3. 
4. 
5. 
6. 


Criação de Conta no Roboflow
Criação de Dataset no Roboflow
Instalação de Pacotes e Bibliotecas Necessários
Treinamento e Teste do Modelo (Colab - https://colab.research.google.com/drive/1T-39zHE5GTS8R1S-QgunPcdgyicq0w2Z?usp=sharing)
Criação de Publisher - Realiza o envio de todos os frames de um vídeo para o nosso subscriber.
Criação de Subscriber - Responsável por receber cada um dos arquivos de imagens e converter esses arquivos no formato desejato, além da conexão com a rota de backend para o armazenamento local de todas as imagens geradas.
Criação de Um Bucket - Armazenamento de Imagens online com Supabase
Envio das Imagens para o SupaBase - Via Rota com FastAPI
Validação das Imagens via URL do Supabase
