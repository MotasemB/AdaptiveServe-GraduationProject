import random
import cv2
# from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import network


class Serves:
    def __init__(self, frequency=0, topspin=1, backspin=1, rotation_speed=1):
        self.frequency = frequency
        self.topspin = topspin
        self.backspin = backspin
        self.rotation_speed = rotation_speed
        self.params = {"frequency": frequency,
                       "topspin": topspin-1,
                       "backspin": backspin-1,
                       "rotation": rotation_speed-1}

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_topspin(self, topspin):
        self.topspin = topspin

    def set_backspin(self, backspin):
        self.backspin = backspin

    def set_rotation_speed(self, rotation_speed):
        self.rotation_speed = rotation_speed

    def serve(self):
        print(f"Serving with Topspin: {self.topspin}, Backspin: {self.backspin}, Rotation Speed: {self.rotation_speed}")
        self.send_params_instructions()

    def initial_serves(self, duration=26, fps=30):
        cap = cv2.VideoCapture(1)  # Open default camera

        time_per_serve = 1.6
        serves_per_instruction = 2

        # turns machine on
        self.frequency = 1

        frames = []
        start_time = cv2.getTickCount() / cv2.getTickFrequency()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            
            current_time = cv2.getTickCount() / cv2.getTickFrequency()

            # changing paramaters every set of serves 
            if len(frames) % (fps * time_per_serve * serves_per_instruction) == 0:
                if self.topspin < self.backspin:
                    self.set_topspin(min(4, self.topspin + 1))
                else:
                    self.set_backspin(min(4, self.backspin + 1))

                rotation_speed = random.randint(1, 3) 
                self.set_rotation_speed(rotation_speed)

                # Perform serves with the same parameters
                self.serve()

            if current_time - start_time > duration:
                break
        
        # going back to easier serve parameters during analysis phase
        self.backspin = self.topspin = 4
        self.serve()

        cap.release()
        return frames

    def initial_learn_and_set_params(self, ball_hit_frames, model):

        input = len(ball_hit_frames)
        input = np.array([[input]])

        predictions = model.predict(input)

        topspin = round(predictions[0, 0])
        backspin = round(predictions[0, 1])

        self.set_backspin(min(9, backspin))
        self.set_topspin(min(9, topspin))

        rotation_speed = random.randint(1, 9) 
        self.set_rotation_speed(rotation_speed)

        self.serve()

    def learn_and_set_params(self, ball_hit_frames, model):

        input = len(ball_hit_frames)
        input = np.array([[input]])

        predictions = model.predict(input)

        topspin_change = round(predictions[0, 0])
        backspin_change = round(predictions[0, 1])

        topspin_change = min(max(topspin_change, -2), 2)
        backspin_change = min(max(backspin_change, -2), 2)

        self.set_backspin(max(1, min(9, self.backspin+backspin_change)))
        self.set_topspin(max(1, min(9, self.topspin+topspin_change)))
        
        rotation_speed = random.randint(1, 9) 
        self.set_rotation_speed(rotation_speed)

        self.serve()

    def send_params_instructions(self):
        # Calculate differences between new and old parameter values
        freq_diff = self.frequency - self.params["frequency"]
        topspin_diff = self.topspin - self.params["topspin"]
        backspin_diff = self.backspin - self.params["backspin"]
        rotation_diff = self.rotation_speed - self.params["rotation"]

        # Update stored parameter values
        self.params["frequency"] = self.frequency
        self.params["topspin"] = self.topspin
        self.params["backspin"] = self.backspin
        self.params["rotation"] = self.rotation_speed

        # Send messages to the machine based on parameter differences
        if freq_diff > 0:
            for _ in range(freq_diff):
                network.IncFreq()
        elif freq_diff < 0:
            for _ in range(abs(freq_diff)):
                network.DecFreq()

        if topspin_diff > 0:
            for _ in range(topspin_diff):
                network.IncTop()
        elif topspin_diff < 0:
            for _ in range(abs(topspin_diff)):
                network.DecTop()

        if backspin_diff > 0:
            for _ in range(backspin_diff):
                network.IncBack()
        elif backspin_diff < 0:
            for _ in range(abs(backspin_diff)):
                print(f"backspin diff: {backspin_diff}    backspin: {self.backspin}")
                network.DecBack()

        if rotation_diff > 0:
            for _ in range(rotation_diff):
                network.IncOscil()
        elif rotation_diff < 0:
            for _ in range(abs(rotation_diff)):
                network.DecOscil()
    





        

    


