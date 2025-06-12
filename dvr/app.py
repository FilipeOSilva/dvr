import os
import threading

from dotenv import load_dotenv
from motion_detector import MotionDetector
from path_file import dir_path
from video_recorder import VideoRecorder


def record(rtsp_url):
    app = VideoRecorder(rtsp_url)

    while True:
        dir_name = dir_path()
        app.set_path(dir_name)
        app.low_quality()


def motion_dec(rtsp_url, chat_id, token):
    app = MotionDetector(
        rtsp_url,
        chat_id,
        token,
    )
    app.start_motion()


if __name__ == '__main__':
    load_dotenv()
    rtsp_url = os.environ.get('RTSP_URL')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    token = os.environ.get('TELEGRAM_TOKEN')

    rec_thread = threading.Thread(target=record, args=(rtsp_url,))
    mot_thread = threading.Thread(
        target=motion_dec, args=(rtsp_url, chat_id, token)
    )

    rec_thread.start()
    mot_thread.start()

    rec_thread.join()
    mot_thread.join()
