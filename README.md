MICROSERVICE APPLICATION FOR A CHATTING APPLICATION FOR A CLIENT

Tool requirement for the project

1.	Python 3.11+ installed (for FastAPI services)
2.	Docker & Docker Compose installed
3.	VS Code extensions (optional but helpful):
4.  Python (for code highlighting, virtualenv)
5.  Docker (to manage containers)
6.  Pylance (for type checking)
7.  REST Client (optional, test APIs from VS Code)
8.  Live Share (optional, for collaboration)

Project overview and steps to execution
* The various tools and required programs above were duly installed prior to project exection
* we had the chat-service and the user-service as two seperate folders which included the various directory
* The chat service and user service each have their dockerfiles to help with building the images
* A docker-compose file was used to help build final images from the above dockerfiles within their individual setups

Errors encountered during the Backend project
  ---
1. **First error appears in   using the docker-compose –build**
   
   error details
   
    APPLICATION/chat-app/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion

First error here is associated with the docker compose file, which relies the docker hub login/authentication when pulling the postgres:14 image: This is showing incorrect username or password in relation to dockerhub.   

2. **Third error we are experiencing was the dockerfiles and its content within the individual applications for both chat service and user service**

3. **Importerror:**
   cannot import name 'Message' from 'models' (/app/models.py) . This error means that inside the chat-service, /appmodels.py has a class message that does not exist or is named differently

    This is a common cause in Django or Flask applications. It occurs when two or more modules attempt to import from each other, creating a dependency loop that the interpreter cannot resolve. For example, if models.py imports something from            views.py, and views.py then tries to import Message from models.py, a circular dependency exists.
