******
https://support.stackpath.com/hc/en-us/articles/360022987711-Edge-Computing-Building-a-Containerized-Python-Web-App-Using-Flask
******

C:\Users\Docker\Projects\docker_waitress\src
	
docker build -t docker-waitress .

docker run -p 48160:80 docker-waitress

This command aliases port 80 on our container instance to port 48160 on our local machine. Access localhost:48160 in the browser





