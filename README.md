## 🧐 About <a name = "about"></a>

**Bragi - (god of poetry in [Norse mythology](https://en.wikipedia.org/wiki/Bragi)):**
Bragibooks provides a minimal and straightforward webserver that you can run remotely or locally on your server. Since Bragibooks runs in a docker, you no longer need to install dependencies on whichever OS you are on. You can

Some basics of what Bragi does:
- Merge multiple files
- Convert mp3(s)
- Cleanup existing data on an m4b file
- More features on [m4b-merge's help page](https://github.com/djdembeck/m4b-merge)

### Screens

Folder/file selection             |  ASIN input
:-------------------------:|:-------------------------:
![file-selection](../assets/screens/file_picker.png)  |  ![asin-auto-search](../assets/screens/auto_search_panel.png)

Folder/file selection             |  Post-proccess overview
:-------------------------:|:-------------------------:
![asin-custom-search](../assets/screens/custom_search.png)  |  ![post-process](../assets/screens/processing_panel.png)

## 🏁 Getting Started <a name = "getting_started"></a>

You can either install this project directly or run it prepackaged in Docker.

### Prerequisites

#### Docker
- All prerequisites are included in the image.

#### Direct (Gunicorn)
- You'll need to install m4b-tool and it's dependants from [the project's readme](https://github.com/sandreas/m4b-tool#installation)
- Run `pip install -r requirements.txt` from this project's directory.

### Installing

#### Docker
To run Bragibooks as a container, you need to pass some paramaters in the run command:

  | Parameter | Function |
  | :----: | --- |
  | `-v /path/to/input:/input` | Input folder |
  | `-v /path/to/output:/output` | Output folder |
  | `-v /appdata/bragibooks/config:/config` | Persistent config storage |
  | `-p 8000:8000/tcp` | Port for your browser to use |
  | `-e LOG_LEVEL=WARNING` | Choose any [logging level](https://www.loggly.com/ultimate-guide/python-logging-basics/) |
  | `-e DEBUG=False` | Turn django debug on or off (default False) |
  | `-e UID=99` | User ID to run the container as (default 99)|
  | `-e GID=100` | Group ID to run the container as (default 100)|
  | `-e CELERY_WORKERS=1` | The number or celery workers for processing books (default 1)|
  | `-e CSRF_TRUSTED_ORIGINS=https://bragibooks.mydomain.com` | Domains to trust if bragibooks is hosted behind a reverse proxy. |


Which all together should look like: 

	docker run --rm -d --name bragibooks -v /path/to/input:/input -v /path/to/output:/output -v /appdata/bragibooks/config:/config -p 8000:8000/tcp -e LOG_LEVEL=WARNING ghcr.io/djdembeck/bragibooks:main

## Docker Compose
```
version: '3'

services:
  bragi:
    image: ghcr.io/djdembeck/bragibooks:main
    container_name: bragibooks
    environment:
      - CSRF_TRUSTED_ORIGINS=https://bragibooks.mydomain.com
      - LOG_LEVEL=INFO
      - DEBUG=False
      - UID=1000
      - GID=1000
    volumes:
      - path/to/config:/config
      - path/to/input:/input
      - path/to/output/output:/output
      - path/to/done:/done
    ports:
      - 8000:8000
    restart: unless-stopped
```


#### Direct Build (Gunicorn)
  - Copy static assets to  project folder:
    ```
    python manage.py collectstatic
    ```
  - Create the database:
    ```
    python manage.py migrate
    ```
  - Run the celery worker for processing books:
    ```
    celery -A bragibooks_proj worker \
    --loglevel=info \ 
    --concurrency 1 \
    -E
    ```
  - Run the web server:
    ```
    gunicorn bragibooks_proj.wsgi \
    --bind 0.0.0.0:8000 \
    --timeout 1200 \
    --worker-tmp-dir /dev/shm \
    --workers=2 \
    --threads=4 \
    --worker-class=gthread \
    --reload \
    --enable-stdio-inheritance
    ```

## 🎈 Usage <a name="usage"></a>

The Bragibooks process is a linear, 3 step process:
1. __Select input__ - Use the file multi-select box to choose which books to process this session, and click next.
2. __Submit ASINs__ - Bragi will auto search for the audiobook data on [Audible.com](https://www.audible.com) (US only). If the data found is incorrect you can do a custom search to find the correct title and then submit for processing.
3. Wait for books to finish processing. This can take anywhere from 10 seconds to a few hours, depending on the number and type of files submitted. This will be done in the background.
4. __Books page__ - Page where you can see the data assigned to each book after it has finished processing. You can also check the status of the books still being processed.

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.djangoproject.com/) - Server/web framework
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) - Task queue and worker
- [Bulma](https://bulma.io/) - Frontend CSS framework
- [audnexus](https://github.com/laxamentumtech/audnexus) - API backend for metadata
- [m4b-merge](https://github.com/djdembeck/m4b-merge) - File merging and tagging
