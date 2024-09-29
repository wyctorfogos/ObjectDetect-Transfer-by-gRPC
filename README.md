# ObjectDetect-Transfer-by-gRPC

This project detects objects in frams and send its throught a gRPC conection to the server-size, which decodes and plot the transmited frame.

# conda env 
The first step is: create a conda env with the necessary libraries to encode, send and decode the frames.
Command: `conda create -n gRPCAndYOLO`

To install the libs:
Go to the main folder and write the command bellow:
`pip install -t requirements.txt`

# Generate the .proto (if changed):
On the folder `src/scripts/utils`, write the command:
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. video.proto`

# 

