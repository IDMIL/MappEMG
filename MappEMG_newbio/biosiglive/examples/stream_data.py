"""
This example show how to use the StreamData class to stream data from an interface, process it using several process to
finally send the data through a server to a client. Each task in a separate process to allow the streaming and the
 processing to be done in real-time. Please note that for now only a number equal to the number of cores of the computer
  is supported.
First an interface is created and device and marker_set are added to it (please refer to EMG_streming.py and
marker_streaming.py for more details).
Then a StreamData object is created. The StreamData object takes as argument the targeted frequency at which the data will
be streamed. Then the interface is added to the StreamData object. If the user want to start a server to
disseminate the data a server can be added to the StreamData object specifying the ip address and the port and the
data buffer for the device and the marker set. The data buffer is the number of frame that will be stored in the server,
it will be use if the client need a specific amount of data.
Then the streaming will be started with all the data streaming, processing and the server in seperate process. If no
 processing method is specified the data will be streamed as it is and no additional process will be started. A file can
  be specified to save the data. The data will be saved in a *.bio file at each loop of the data streaming by default or
  at the save frequency specified in the start method.
Please note that it is not yet possible to plot the data in real-time.
"""
from custom_interface import MyInterface
from biosiglive.interfaces.pytrigno_interface import PytrignoClient
from biosiglive.interfaces.vicon_interface import ViconClient
from biosiglive.streaming.stream_data import StreamData
from biosiglive.enums import DeviceType
from biosiglive.enums import InverseKinematicsMethods
from biosiglive.enums import RealTimeProcessingMethod
from biosiglive.enums import InterfaceType
from biosiglive.interfaces.bitalino_interface import BitalinoClient



if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 5005
    interface_type = InterfaceType.Custom

    interface = BitalinoClient(ip="20:19:07:00:7E:19")
    interface.add_device(
        "Bitalino",
        rate=1000, system_rate=1000,
        acq_channels=[0], device_data_file_key="emg",
        processing_method=RealTimeProcessingMethod.ProcessEmg,
        data_buffer_size=1000,
        processing_window=1000,
        moving_average_window=100,
        moving_average=True,
        low_pass_filter=False,
        band_pass_filter=True,
        normalization=False,
    )

    data_streaming = StreamData(stream_rate=100)
    data_streaming.add_interface(interface)
    data_streaming.add_server(server_ip, server_port, device_buffer_size=10)
    data_streaming.start(save_streamed_data=False)
