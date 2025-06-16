import sys
import time

import cv2
from bot_telegram import BotTelegram
from path_file import dir_path
from video_recorder import VideoRecorder

MAX_DELAY = 15
MIN_MOVIMENT = 10000


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
        self._old_frame = None

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

    def _check_moviment(self, img) -> bool:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        diff = cv2.absdiff(self._old_frame, frame)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        self._old_frame = frame.copy()
        for contour in contours:
            if cv2.contourArea(contour) < MIN_MOVIMENT:
                continue

            return True

        return False

    def start_motion(self) -> None:
        cap = cv2.VideoCapture(self._rtsp_url)

        if not cap.isOpened():
            sys.exit()

        try:
            ret, frame = cap.read()
            if not ret:
                raise Exception('Erro em caputar frame!')

            self._old_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self._old_frame = cv2.GaussianBlur(self._old_frame, (21, 21), 0)

            while True:
                ret, frame = cap.read()

                if not ret:
                    print('Erro em caputar frame!')
                    break

                if self._check_moviment(frame):
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

        except Exception as e:
            print(f"Motivo da parada: {e}")

        cap.release()
