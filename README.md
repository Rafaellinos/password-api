## password-api


### O que é o projeto?

<p>API para gerar senhas com limite de requisições (visualizações) e tempo.
Senha não pode ser armazenada após sua expiração.</p>
<p>Ex: Usuário solicita senha e define os parâmetros de tempo.</p>

### Quais tecnologias foram usadas?

<p>Devido ao limite de tempo, foi escolhido o framework <a href="https://fastapi.tiangolo.com/">FastAPI</a>
para o desenvolvimento, devido a sua facilidade e velocidade.</p>
<p>Para atender aos requisitos de segurança, foi utilizado o padrão de jwt
 (Json Web tokens) para autenticação e autorização, usando algoritmo HS256.</p>
<p>Para gerar a senha aleatório, foi utilizado a library do python secrets, que 
implementa o Hardware random number generator (HRNG), garantindo senhas únicas e não 
previsíveis.</p>

### Como rodar?

<p>Primeiramente, instalar docker e docker compose, depois subir os containers com o comando: </p>

```console
foo@bar:~$ docker-compose up -d
```
<p>Acesse localhost:8000/docs para interagir com a API. É possível criar o usuário em POST:/api/users e 
obter o access token em POST:/api/login</p>

<p>Os endpoints de requests ficam disponíveis os acessos as solicitações de senhas e 
visualização das requisições.</p>
<p>EX:</p>

```console
foo@bar:~$ sudo apt install httpie
foo@bar:~$ http POST :8000/api/users username=testeuser1 password=testeuser@123 
# cria usuário
foo@bar:~$ access_token=$(http -f POST :8000/api/login username=testeuser1 password=testeuser@123 | cut -c 18-148) 
# obter token
foo@bar:~$ echo $access_token
foo@bar:~$ http GET :8000/api/users/me Authorization:" Bearer $(echo $access_token) 
# obter informações do usuário
foo@bar:~$ http GET :8000/api/request_password Authorization:" Bearer $(echo $access_token)" views_limit==3 expire_in_days==3
# solicitar senha, use o id para obter a senha
foo@bar:~$ http GET :8000/api/requests Authorization:" Bearer $(echo $access_token)"  
# ver histórico de solicitações
foo@bar:~$ http GET :8000/api/password/80f5033b-3a1b-4ae6-92f4-26f68df240cc Authorization:" Bearer $(echo $access_token)" 
# view_counter vai diminuindo a cada nova requisição, ao zerar, não será mais possível visualizar a senha
```

* Informações do retorno:
    - views_counter: Número inteiro da quantidade de solicitações que o usuário pode fazer para ver a senha
    - due_date: Data de vencimento da senha
    - status: 1 para válido e 2 para expirado
    - public_id: id público para visualizar a senha
    
### O que falta fazer?

* Trocar sqlachemy por tortoise para não ter block io
* Endpoint de validação de senha
* Melhorar parte de validações
* Perfil de admin para verificar todos as solicitações
* Incluir parâmetros como Secret key do jwt no .config