# Architecture overview

Visit [this url](https://github.com/snehalkumar5577/gbfs-processor/blob/master/docs/architecture-overview.md)

# Demo screenshots

Visit [this url](https://github.com/snehalkumar5577/gbfs-processor/blob/master/docs/live-application-demo-screenshots.md)

# Local Setup Using Docker Compose

This guide will help you set up the local development environment for the GBFS Processor project using Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Steps

3. **Start the Services**

    Use Docker Compose to build and start the services defined in the `docker-compose.yml` file:

    ```sh
    docker-compose up --build -d
    ```

    This command will build the Docker images (if not already built) and start the containers for the frontend, collector, API server, and MongoDB in detached mode.

4. **Access the Services**

    - **Frontend**: Open your browser and navigate to `http://localhost:3000`
    - **API Server**: The API server will be running at `http://localhost:8000`
    - **MongoDB**: MongoDB will be accessible at `mongodb://localhost:27017`

5. **Stopping the Services**

    To stop the services run:

    ```sh
    docker-compose down
    ```