import tkinter as tk
from PIL import Image, ImageTk

#def increaseOne(label):
    #label.config(text=str(counter))
test = False
def change():
    global test
    test = True    
def increase(label):
    current_number = int(label.cget("text"))
    label.config(text=str(current_number + 1))

# Function to reset labels and toggle button text
def reset():
    for label in labels:
        label.config(text="1")
    if button.cget("text") == "Start":
        button.config(text="Out of Balls")
    else:
        button.config(text="Start")

# Function to increase a specific label by one
def increase_specific_label(index):
    if 0 <= index < len(labels):
        increase(labels[index])

# Create the main window
root = tk.Tk()

root.configure(background='pink')
ico = Image.open('paddleIcon.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.title("Adaptive Serve: Ping Pong Pratice")

root.geometry('700x400')

# Create a frame for the labels
frame = tk.Frame(root, bg="pink")
frame.pack()

# Create labels
labels = []
label_texts = ["Frequency", "Oscillation", "Backspin", "Topspin"]
for i in range(4):
    # Create a sub-frame for each label
    sub_frame = tk.Frame(frame,bg='pink')
    sub_frame.pack(side=tk.LEFT, padx=50,pady=50)  # Use pack with side=tk.LEFT to arrange the sub-frames horizontally

    # Create the number label
    number_label = tk.Label(sub_frame, text="1", font=("Arial", 50),bg='pink')
    number_label.pack()

    # Create the text label
    text_label = tk.Label(sub_frame, text=label_texts[i],bg="pink")
    text_label.pack()

    labels.append(number_label)  # Add the number label to the list

labels[0].config(text=str(1))
labels[1].config(text=str(4))
labels[2].config(text=str(3))
labels[3].config(text=str(3))
# Create button with initial text "Start"
button = tk.Button(root, text="Out of Balls", command=reset, height=5, width=25, bg='pink')
button.pack()

# Increase the third label by one
#increase_specific_label(2)

# Create a label for displaying the number of balls hit
balls_hit_label = tk.Label(root, text="Balls hit: 5", font=("Arial", 16), bg='pink',anchor="w",justify="left")
balls_hit_label.pack()

# Create a label for displaying accuracy percentage
accuracy_label = tk.Label(root, text="Accuracy: 40%", font=("Arial", 16), bg='pink',anchor="w",justify="left")
accuracy_label.pack()

#change()
if(test == True):
    print("hello")
    increase(labels[0])

labels[0].update()
# Start the main loop
root.mainloop()
