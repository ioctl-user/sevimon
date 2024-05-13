import cv2

from lib.i18n import _


class cam_class():
    skip_frames = 0 # How many frames to skip to achive configured FPS
    cfg = None # Config structure
    cap = None

    def __init__(self, cfg):
        self.cfg = cfg

	# Find and open camera
    def find_camera(self):
        self.cap = cv2.VideoCapture(self.cfg.camera_dev)
        ret = self.cap is not None and self.cap.isOpened()
        if ret is False:
            print (_("Can't open camera {}").format(self.cfg.camera_dev))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cfg.res[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.res[1])
        self.cap.set(cv2.CAP_PROP_FPS, self.cfg.fps * 2)  # FPS, multiplication by 2 because of hack to clean buffer
        real_fps = int(self.cap.get(5))  # Get actual FPS from hardware
        self.skip_frames = real_fps / self.cfg.fps - 1  # Is there a better way?

        return ret, self.cap

    # Get the next frame with required FPS
    def get_next_frame(self):
        for i in range(int(self.skip_frames)):
            self.cap.grab()
        return self.cap.read()

# vi: tabstop=4 shiftwidth=4 expandtab
