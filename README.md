# ObjectDetect-Transfer-by-gRPC

This project detects objects in frames and send it's throught a gRPC conection to the server size, which decodes and plot the transmited frame.

# conda env 
The first step is: create a conda env with the necessary libraries to encode, send, and decode the frames.
Command: `conda create -n gRPCAndYOLO`

To install the libs:
Go to the main folder and write the command bellow:
`pip install -t requirements.txt`

# Generate the .proto (if changed):
On the folder `src/scripts/utils`, write the command:
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. video.proto`

# Run the scripts:
Open to terminals, one to run the script `server.py`:
`python3 src/scripts/server.py`

Then, run the script `client.py`:
`python3 src/scripts/client.py`

![Recovered frame - example 1](https://github.com/wyctorfogos/ObjectDetect-Transfer-by-gRPC/blob/main/images/Screenshot%20from%202024-09-29%2017-44-31.png)
