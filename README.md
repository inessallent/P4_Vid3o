practice1/
├── main.py             # Application logic with endpoints.
├── semi1.py            # All code and functions of seminar 1
├── Dockerfile          # Docker image setup.
├── docker-compose.yml  # Docker Compose configuration.
├── requirements.txt    # Python dependencies.
└── README.md           # Documentation.


1. First, we create an API following the instructions in https://fastapi.tiangolo.com/
We make sure it's running using this command: fastapi dev main.py

Then we need to put it inside a docker. For that, we create a Dockerfile with all the dependencies and run the Docker container using the image. 
We build the container with this command: docker build -t myfastapi_container .
We run the container, for example, like this: docker run -d -p 80:8000 --name myfastapi_container myfastapi_container
We can enter from here http://localhost:80 or to see it visually here: http://127.0.0.1:8000/docs



2. Now we need to put the ffmpeg inside a Docker. We modify the Dockerfile so that it contains this line: 

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

Using this command, we can see if ffmpeg is running: ffmpeg -version

3. Now we're going to include our previous work, so the seminar 1. For that we created a .py file called semi1 where we put all our code. Then from the main.py we import the functions we need: from semi1 import RGBto_YUV, YUVto_RGB, resize_image, compress_to_bw, encoding, DCT, DWT

4. Next, we created 5 endpoints in the main.py that call the functions from semi1 so we can apply  any parameter we want. More specifically, we implemented convert_rgb_to_yuv, convert_yuv_to_rgb, encoding (run length encoding), encode_dwt and decode_dwt.

In the encoding and decoding, the input needs to be a 1D array separated by commas.
In http://127.0.0.1:8000/docs we can see them working.

5. To do this we created a .yml file called docker-compose with the corresponding configuration.
With this command: 'docker-compose up --build' we build the services. We know it's well configured
because inside the yml file we mount a directory to store media files and it appears in the folder. 
Then when we try to get the API and the ffmpeg docker to communicate it gives a constant error. It
does identify both dockers but we can't get them to communicate.
