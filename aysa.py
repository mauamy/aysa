import tkinter as tk
import asyncio
import os
import sys

from pydub import AudioSegment
from pydub.playback import play


win_width = 600
win_height = 200


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App:
    def __init__(self, time_to_shutdown, debug=False):
        self.tts = time_to_shutdown
        self.debug = debug

    async def exec(self):
        self.window = Window(asyncio.get_event_loop(), self.tts, self.debug)
        await self.window.show()


class Window(tk.Tk):
    def __init__(self, loop, time_to_shutdown, debug):
        self.debug = debug
        self.app_closing = False
        self.loop = loop
        self.root = tk.Tk()
        self.timer = tk.StringVar()
        self.time_to_shutdown = time_to_shutdown
        self.update_timer()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_offset_x = int(screen_width / 2 - win_width / 2)
        center_offset_y = int(screen_height / 2 - win_height / 2)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.root.title('Auto Shutdown')
        self.root.geometry('{}x{}+{}+{}'.format(win_width, win_height, center_offset_x, center_offset_y))

        # Create Labels
        lbl_height = 50
        caption_lbl = tk.Label(self.root, text='The system will be shutdown in: ', fg='red', font=("Helvetica", 20))
        caption_lbl.place(height=lbl_height, x=20, y=win_height / 2 - lbl_height / 2)

        timer_label = tk.Label(self.root, textvariable=self.timer, fg='red', font=("Helvetica", 30))
        timer_label.pack()
        timer_label.place(height=lbl_height, x=430, y=win_height / 2 - lbl_height / 2)

        btn = tk.Button(self.root, text='Stop Shutdown', fg='black', font=("Helvetica", 18), command=self.close_app)
        btn.place(width=win_width - 20, height=40, x=10, y=win_height - 50)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def close_app(self):
        self.app_closing = True

    def update_timer(self):
        self.timer.set('{}'.format(self.time_to_shutdown))

    async def show(self):
        self.loop.create_task(self.count_down())
        while not self.app_closing:
            self.root.update()
            await asyncio.sleep(.1)

    async def play_notification_sound(self):
        try:
            sound = AudioSegment.from_wav(resource_path('data/notification.wav'))
            play(sound)
        except Exception as e:
            print(f"Play sound Error: {e}")

    async def count_down(self):
        await self.play_notification_sound()
        while self.time_to_shutdown > 0:
            self.time_to_shutdown -= 1
            self.update_timer()
            await asyncio.sleep(1)

        if self.debug:
            self.timer.set("TIME'S UP")
        else:
            os.system("shutdown now -h")


if __name__ == '__main__':
    time_to_shutdown = 30
    if len(sys.argv) == 2:
        if sys.argv[1].isnumeric():
            time_to_shutdown = int(sys.argv[1])

    asyncio.run(App(time_to_shutdown, debug=False).exec())
