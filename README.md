# Object detection and send it frame by a gRPC connection

This project detects objects in frames and then send by a gRPC connection to the server size, which decodes and shows.
# conda env 
The first step is: Create a conda env with the necessary libraries to encode, send, and decode the frames.
Command: `conda create -n gRPCAndYOLO`

To install the libs:
Go to the main folder and write the command below:
`pip3 install -t requirements.txt`

# Generate the .proto (if changed):
On the folder `src/scripts/utils`, write the command:
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. video.proto`

# Run the scripts:
Open to terminals, one to run the script `server.py`:
`python3 src/scripts/server.py`

Then, run the script `client.py`:
`python3 src/scripts/client.py`

![Recovered frame - webpage visualization](https://github.com/wyctorfogos/object-detect-in-frame-and-tranfering-by-grpc-connection/blob/websocket/images/webpage-with-object-detection-stream.png)
