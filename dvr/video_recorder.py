from datetime import datetime

import ffmpeg


class VideoRecorder:
    def __init__(self, input_rtsp_url: str) -> None:
        self._rtsp_url: str = input_rtsp_url
        self._rec_process = None
        self._path = ''

    @staticmethod
    def __get_name() -> str:
        name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        return name + '.mp4'

    def set_path(self, path: str) -> None:
        self._path = path

    def low_quality(self) -> None:
        name = self._path + self.__get_name()

        ffmpeg.input(
            self._rtsp_url,
            rtsp_transport='tcp',
            fflags='nobuffer',
            flags='low_delay',
        ).output(
            name,
            vcodec='libx264',
            crf=28,
            acodec='aac',
            audio_bitrate='128k',
            vf='scale=640:360',
            r=15,
            t=3600,
            f='mp4',
        ).run()

    def high_quality_start(self) -> None:
        name = self._path + 'event.' + self.__get_name()

        self._rec_process = (
            ffmpeg.input(self._rtsp_url)
            .output(name, f='mp4')
            .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        )

    def high_quality_stop(self) -> None:
        if self._rec_process:
            self._rec_process.terminate()
            self._rec_process.wait()
