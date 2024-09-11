import cv2

def read_video(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(frames, output_path, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        out.write(frame)
    out.release()

def record_video(duration):
    cap = cv2.VideoCapture(0)  # Open default camera

    frames = []
    start_time = cv2.getTickCount() / cv2.getTickFrequency()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        if current_time - start_time > duration:
            break

    cap.release()
    return frames

# x= read_video(r'yoloM\tt_cropTrim.mp4')
# print(x)

