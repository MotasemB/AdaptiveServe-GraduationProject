from ultralytics import YOLO 
import cv2
import pickle
import pandas as pd
import numpy as np


class BallTracker:
    def __init__(self,model_path, cuda=False):
        self.model = YOLO(model_path)
        if cuda:
            self.model.to('cuda')

    def interpolate_ball_positions(self, ball_positions):
        ball_positions = [x.get(1,[]) for x in ball_positions]
        
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        # interpolate the missing values
        df_ball_positions = df_ball_positions.interpolate(limit=10)
        df_ball_positions = df_ball_positions.bfill(limit=10)

        ball_positions = [{1:x} for x in df_ball_positions.to_numpy().tolist()]

        return ball_positions

    def get_ball_shot_frames(self,ball_positions, minimum_change_frames_for_hit=7, screen_height = 480):
        ball_positions = [x.get(1,[]) for x in ball_positions]
        # convert the list into pandas dataframe
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        df_ball_positions['ball_hit'] = 0

        df_ball_positions['mid_y'] = (df_ball_positions['y1'] + df_ball_positions['y2'])/2
        df_ball_positions['mid_y_rolling_mean'] = df_ball_positions['mid_y'].rolling(window=5, min_periods=1, center=False).mean()
        df_ball_positions['delta_y'] = df_ball_positions['mid_y_rolling_mean'].diff()

        for i in range(1,len(df_ball_positions)- int(minimum_change_frames_for_hit*1.2) ):
            # check if ball hits the bottom half of the screen (with extra room for error)
            if df_ball_positions['mid_y'].iloc[i] > screen_height / 2.5:  
                # checking for change in y coords
                negative_position_change = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[i+1] <0
                positive_position_change = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[i+1] >0

                # if there is change check if there are opposite y changes --> V 
                if negative_position_change or positive_position_change:
                    change_count = 0 
                    for change_frame in range(i+1, i+int(minimum_change_frames_for_hit*1.2)+1):
                        negative_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] >0 and df_ball_positions['delta_y'].iloc[change_frame] <0
                        positive_position_change_following_frame = df_ball_positions['delta_y'].iloc[i] <0 and df_ball_positions['delta_y'].iloc[change_frame] >0

                        # count the frames where change happens
                        if negative_position_change and negative_position_change_following_frame:
                            change_count+=1
                        elif positive_position_change and positive_position_change_following_frame:
                            change_count+=1
                
                    # if enough frames show opposite change, count it as ball hit
                    if change_count>minimum_change_frames_for_hit-1:
                        df_ball_positions.loc[i, 'ball_hit'] = 1

        frame_nums_with_ball_hits = df_ball_positions[df_ball_positions['ball_hit']==1].index.tolist()

        return frame_nums_with_ball_hits
    

    def detect_frames(self,frames):
        ball_detections = []

        for frame in frames:
            player_dict = self.detect_frame(frame)
            ball_detections.append(player_dict)
        
        return ball_detections

    def detect_frame(self,frame, conf=0.15):
        results = self.model.predict(frame,conf=conf)[0]

        ball_dict = {}
        for box in results.boxes:
            result = box.xyxy.tolist()[0]
            ball_dict[1] = result
        
        return ball_dict

    def draw_info(self,video_frames, ball_detections, frames_ball_hit):
        output_video_frames = []
        
        for index, (frame, ball_dict) in enumerate(zip(video_frames, ball_detections)):
            # Draw Bounding Boxes
            for track_id, bbox in ball_dict.items():
                if any(np.isnan(bbox)):
                    continue
                x1, y1, x2, y2 = bbox
                cv2.putText(frame, f"Ball ID: {track_id}",(int(bbox[0]),int(bbox[1] -10 )),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

            # Displaying Ball Hit text on frames where the ball hit the table (+- 1 frame to be more visible)
            if any(index - 1 <= hit_index <= index + 1 for hit_index in frames_ball_hit):
                cv2.putText(frame, "Ball Hit", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            output_video_frames.append(frame)
        
        return output_video_frames


    