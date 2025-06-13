import sys
import time

import cv2
from bot_telegram import BotTelegram
from path_file import dir_path
from ultralytics import YOLO
from video_recorder import VideoRecorder

MAX_DELAY = 15


class MotionDetector:
    def __init__(
        self,
        input_rtsp_url: str,
        chat_id: str = None,
        token_telegram: str = None,
    ) -> None:
        self._rtsp_url: str = input_rtsp_url
        self._is_record = False
        self._total_time_record = 0
        self._video_record = VideoRecorder(self._rtsp_url)
        self._chat_id: str = chat_id
        self._token_telegram: str = token_telegram

    def _start_time(self) -> None:
        self._total_time_record = int(time.time())

    def _total_time(self) -> bool:
        now = int(time.time())

        if (now - self._total_time_record) > MAX_DELAY:
            return True
        else:
            return False

    def _start_record(self) -> None:
        dir_name = dir_path()
        self._video_record.set_path(dir_name)
        self._video_record.high_quality_start()

    def _stop_record(self) -> None:
        self._video_record.high_quality_stop()

    def _send_msg(self) -> None:
        bot = BotTelegram(self._token_telegram, self._chat_id)
        bot.send_message('Movimento Detectado!')

    def start_motion(self) -> None:
        model = YOLO('yolov8n.pt')
        cap = cv2.VideoCapture(self._rtsp_url)

        if not cap.isOpened():
            sys.exit()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                info_image = model(frame)
                for objs in info_image:
                    obj = objs.boxes
                    for datas in obj:
                        if datas.cls[0] == 0:
                            if not self._is_record:
                                self._start_record()
                                self._send_msg()
                            self._is_record = True
                            self._start_time()

                if self._is_record:
                    if self._total_time():
                        self._stop_record()
                        self._is_record = False

                cv2.waitKey(1)

        except Exception:
            print('Gravação encerrada pelo usuário.')

        cap.release()
