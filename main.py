from multiprocessing import Process
from backend.data_generator import run_data_generator
from backend.video_stream import run_video_stream
from frontend.dashboard import run_dashboard  # Assuming you structured it as discussed before

def main():
    data_file = 'data/sensor_data_log.csv'  # Adjust the path as necessary

    # Start data generation process
    data_process = Process(target=run_data_generator, args=(data_file,))
    data_process.start()

    # Start video streaming process
    video_process = Process(target=run_video_stream)
    video_process.start()

    # Start the dashboard (will run on the main thread)
    run_dashboard()

    # Clean up processes on exit
    data_process.join()
    video_process.join()

if __name__ == "__main__":
    main()
