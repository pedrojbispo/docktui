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