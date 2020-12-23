******
https://support.stackpath.com/hc/en-us/articles/360022987711-Edge-Computing-Building-a-Containerized-Python-Web-App-Using-Flask
******

*** NETWORKING ***
https://docs.docker.com/network/network-tutorial-standalone/

*** Server ***

C:\Users\Docker\Projects\docker_waitress\src

docker network create --driver bridge alpine-net

docker build -t docker-waitress .

docker run -it --network alpine-net -p 48156:80 docker-waitress

This command aliases port 80 on our container instance to port 48160 on our local machine. Access localhost:48160 in the browser

*** Front End ***

C:\Users\Docker\Projects\brand_new\src

docker build -t front-end . 

docker run -it --network alpine-net -p 8080:8080 front-end 