# docktui
ADS Academic Project

Objectivo: Criar e desenvolver um ferramenta TUI (Text User Interface) que interage e orchestra um maquina/servidor com docker
Criar Docker containers, remover docker containers, verificar o status dos docker containers atravez de uma API
Arquitetura é Cliente-Servidor, ou seja Cliente comunica com servidor que vai expor o docker daemon atravez de uma API.


### Arquitetura de funcionamento da APP
```
┌────────────┐        HTTP / REST        ┌────────────────────┐
│ Cliente    │  ─────────────────────▶  │ Servidor API       │
│ TUI        │                           │ (Flask)            │
│ (Terminal) │  ◀─────────────────────  │                    │
└────────────┘        JSON               │  Docker SDK        │
                                         │                    │
                                         └─────────┬─────────┘
                                                   │
                                             Docker Engine
                                                   │
                                           Containers
```

### Calls 

Client is TUI but all options are CLI commands. The program works in CLI and TUI at the same time.
Client --- Server --- [ Docker, Docker Containers ]

Client > dockcli create nginx --barebone
Server > |
    mkdir nginx
    cp /datastore/barebone/nginx.yml /projects/nginx/docker-compose.yml
    docker compose up -d 
Action: POST

Client > dockcli create test-nginx --custom-compose nginx-custom.yml 
Server > | 
    scp <client-source> <server-dest>
    cp /datastore/custom/nginx-custom.yml /projects/test-nginx/docker-compose.yml
    docker compose up -d 
Action: POST

Client > dockcli delete test-nginx
Server > | 
    cd /projects/test-nginx/ && docker compose down
    rm -fr /projects/test-nginx
Action: DELETE

Client > dockcli status
Server > docker ps 
Action: GET
Client > dockcli status --project nginx-custom
Server > | 
    cd /projects/nginx-custom/ && docker compose ps
Action: GET

Client > dockcli logs --project nginx-custom
Server > | 
    cd /projects/nginx-custom/ && docker compose logs -n 100 nginx-custom
Action: GET