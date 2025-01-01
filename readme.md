
# Music Server Setup with Docker Compose

Transform your music library into a powerful, self-hosted streaming platform with this easy-to-use Docker Compose setup. Featuring Navidrome for seamless music streaming, a robust API container for managing and organizing your collection, and a sleek web frontend for effortless interaction, this project has everything you need. Plus, supercharge your experience with an Edge browser plugin that lets you queue downloads directly. Perfect for music enthusiasts who want total control over their listening experience!

## Prerequisites

- Docker and Docker Compose installed on your system.
- A `.env` file with the required environment variables. See the `.env.example` file for the values you need.

## Services

### 1. Navidrome
[Navidrome](https://www.navidrome.org/) is a lightweight, self-hosted music server and streamer.

- **Image**: `deluan/navidrome:latest`
- **Port**: `4533` (accessible at `http://localhost:4533`)
- **Volumes**:
  - `${NAVI_DATA_PATH}:/data`: Stores Navidrome metadata and configurations.
  - `${MUSIC_PATH}:/music:ro`: Mounts your music folder (read-only).
- **Environment Variables**: Define in `.env`.

### 2. API Container
A custom container for managing and organizing your music library. It uses Streamrip for downloading music.

- **Dockerfile**: Located at `api/Dockerfile`.
- **Port**: `5000`.
- **Volumes**:
  - `${STREAMRIP_DATA_PATH}:/root/.config/streamrip/`: Stores Streamrip configurations.
  - `${MUSIC_PATH}:/root/Music/`: Mounts the music library for management.
- **Environment Variables**: Define in `.env`.

### 3. Web Frontend
A web-based frontend built with Streamlit to interact with the API.

- **Dockerfile**: Located at `web/Dockerfile`.
- **Port**: `8501` (accessible at `http://localhost:8501`).
- **Environment Variables**: Define in `.env`.

### 4. Edge Plugin
A custom Edge browser plugin located in the `plugin` folder. This plugin allows users to send music URLs directly to the API for processing.

## Networking

All services share a custom bridge network (`music_server_net`) with the following configuration:
- **Subnet**: `192.168.100.0/24`

## How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/rhabraken/music-server
cd music-server
```

### 2. Create the `.env` File
Define the necessary environment variables for Navidrome, the API container, and the Web Frontend. See `.env.example` for the variables you could use.

Example:
```
# Navidrome Environment Variables
ND_SCANSCHEDULE=1m
ND_LOGLEVEL=info
ND_SESSIONTIMEOUT=24h

# Volume Paths
NAVI_DATA_PATH=./navi_data
STREAMRIP_DATA_PATH=./streamrip_data
MUSIC_PATH=/path/to/your/music

# API and Web Environment Variables
API_SECRET_TOKEN=your-secret-token
API_URL=http://localhost:5000/
```

### 3. Customize the Dockerfiles
Edit the `api/Dockerfile` and `web/Dockerfile` to include additional tools or configurations if needed.

### 4. Start the Containers
Use Docker Compose to spin up the containers:
```bash
docker-compose up -d
```

### 5. Access Services
- **Navidrome**: [http://localhost:4533](http://localhost:4533)
- **Web Frontend**: [http://localhost:8501](http://localhost:8501)

### 6. Configure Streamrip
Streamrip will only work well if you define the `config.toml`. For Tidal and Qobuz, you NEED a premium subscription and enter the auth information.

### 7. Use the Edge Plugin
1. Navigate to the `plugin` folder.
2. Load the plugin into Edge as an unpacked extension.
3. Use the plugin to send music URLs to the API directly.

### 8. Stop the Containers
To stop the services, run:
```bash
docker-compose down
```

### 9. Updating the Services
To update the images or rebuild the custom containers:
```bash
docker-compose pull
docker-compose up -d --build
```

## Folder Structure

The project directory is organized as follows:
```
.
├── docker-compose.yml       # Docker Compose configuration
├── api/                     # API container Dockerfile and related files
│   └── Dockerfile           # Custom Dockerfile for API
├── web/                     # Web frontend Dockerfile and related files
│   └── Dockerfile           # Custom Dockerfile for Web Frontend
├── plugin/                  # Edge plugin source code
├── .env                     # Environment variables
├── navi_data/               # Persistent Navidrome data
├── streamrip_data/          # Persistent Streamrip data
├── music/                   # Music library (read-only)
├── downloads/               # Temporary downloads folder
```

## Troubleshooting

- **Missing Music Files in Navidrome**: Ensure the `MUSIC_PATH` is set correctly in the `.env` file and points to a directory with your music files.
- **Port Conflicts**: Ensure ports `4533`, `5000`, and `8501` are not used by other services on your system.
- **Permission Issues**: Check the folder permissions on your host machine if containers cannot access mounted volumes.
- **Plugin Not Working**: Ensure the API is running and the plugin configuration matches the API URL and secret token.
- **Downloaded Music Not Showing**: Ensure you have configured Streamrip correctly. 

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Navidrome](https://www.navidrome.org/)
- [Docker](https://www.docker.com/)
- [Streamlit](https://streamlit.io/)

---