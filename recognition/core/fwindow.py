#from PIL import Image
from itertools import chain

def frames_list(image, frame_size):
    fx, fy = frame_size
    px, py = image.size
    #frames_num_x, frames_num_y = px/fx, py/fy

    step_x, step_y = 3, 3
    frames_num_x, frames_num_y = (px - fx)/step_x, (py - fy)/step_y

    print "Frames num: ", (frames_num_x, frames_num_y)
    print "image.size: ", image.size
    for xn in range(frames_num_x):
        for yn in range(frames_num_y):
            x_top, y_top = xn*step_x, yn*step_y
            fragment = image.crop((x_top, y_top, x_top + fx, y_top + fy))
            fragment.save("./pictures/%s_%s.bmp" % (str(frame_size), str((x_top, y_top, x_top + fx, y_top + fy))))
            yield fragment


def floating_window(image):
    init_frame_size = (40, 40)
    max_frame_size = (image.size, image.size) #map(lambda x: x/2, image.size)
    step_x, step_y = 10, 10
    return chain(*chain(frames_list(image, (fx, fy))
                        for fx in range(init_frame_size[0], max_frame_size[0], step_x)
                        for fy in range(init_frame_size[1], max_frame_size[1], step_y))
                )


def squared_floating_window(image):
    init_frame_size = 30
    max_frame_size = min(map(lambda x: x/2, image.size))
    step = 10
    return chain(*chain(frames_list(image, (fx, fx))
                        for fx in range(init_frame_size, max_frame_size, step))
                )