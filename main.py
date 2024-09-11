from utils.videoUtils import record_video, read_video, save_video
from ball_tracker import BallTracker
from serve_machine.serves import Serves
from joblib import load


def main():

    first_run = True # flag for initial training
    duration = 8 # in seconds
    counter = total_balls_hit = repeat = hit_percentage = 0 # counter for video path name
    ball_tracker = BallTracker(model_path=r"yoloM\best.pt") # object for ball detection
    serve_params = Serves(backspin=4, topspin=4) # serves object for sending info to machine

    # model for the the first run
    initial_model = load(r'yoloM\initial_multi_linear_regression_model.joblib')
    # model for subsequent runs
    realtime_model = load(r'yoloM\realtime_multi_linear_regression_model.joblib')

    while True:

        # training for the first time will test the player on all serve variations
        if first_run:
            # duration for initial is 26 seconds 
            video_frames = serve_params.initial_serves(duration=32)

        # after initial run, will record snippets of player playing and alter serves accordingly
        else:
            video_frames = record_video(duration)

        detections = ball_tracker.detect_frames(video_frames) # runs yolov8 inference on each frame
        detections = ball_tracker.interpolate_ball_positions(detections) # interpolates ball position of missing detections
        ball_hit_frames = ball_tracker.get_ball_shot_frames(detections, screen_height=video_frames[0].shape[0]) # returns int array of frames where a ball hit the table

        output_frames = ball_tracker.draw_info(video_frames, detections, ball_hit_frames) # draws ball bounding boxes and ball hit frames on video
        save_video(output_frames, f'output_videos/output{counter}.avi')
        
        counter += 1
        total_balls_hit += len(ball_hit_frames)
                                            # 16 balls in the first run and 5 balls in each run after
        hit_percentage = (total_balls_hit) / (16 + repeat*5)


        if first_run:
            first_run = False
            serve_params.initial_learn_and_set_params(ball_hit_frames, initial_model)
        else: 
            serve_params.learn_and_set_params(ball_hit_frames, realtime_model)
            repeat += 1 

        print(f"Total Balls Hit: {total_balls_hit}\tHit Percentage: {hit_percentage}")

            
        save_video(video_frames, f'output_videos/output{counter}.avi')



if __name__ == '__main__':
    main()

