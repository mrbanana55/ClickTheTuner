from tkinter import *
import threading
import mido

INSTRUCTIONS_BACKGROUND = "#0697c7"
INSTRUCTIONS_FORECOLOR = "#ffffff"

class Gui:
    def __init__(self):
        # Initialize x, y, and cc from the file
        self.x, self.y, self.cc = self.read_coordinates_from_file()

        # Create window
        self.window = Tk()
        self.window.title("Click the tuner")
        self.window.geometry("800x400")
        self.window.resizable(False, False)
        self.window.iconphoto(True, PhotoImage(file="Assets\\Icon.png"))
        self.tracking = False
        self.alert_window = None 

        # Create a frame for the instructions
        self.instructionsFrame = Frame(self.window, bg=INSTRUCTIONS_BACKGROUND, pady=80)
        
        # Create mouse instructions
        self.mouseInstructionsFrame = Frame(self.instructionsFrame, bg=INSTRUCTIONS_BACKGROUND, pady=20)
        self.mouseSetupTitle = Label(self.mouseInstructionsFrame, 
                                     text="SETUP MOUSE POSITION",
                                     font=("arial", 16, 'bold'),
                                     bg=INSTRUCTIONS_BACKGROUND,
                                     fg=INSTRUCTIONS_FORECOLOR)
        self.mouseSetupTitle.pack()
        self.mouseSetupInstructions = Label(self.mouseInstructionsFrame,
                                            text="""1. Click the Mouse Setup button.
2. Place your mouse where the tuner's on/off button is.
3. Press space to save the mouse coordinates.""",
                                            font=("arial", 12),
                                            justify='left',
                                            bg=INSTRUCTIONS_BACKGROUND,
                                            fg=INSTRUCTIONS_FORECOLOR)
        self.mouseSetupInstructions.pack()
        self.mouseInstructionsFrame.pack()

        # Create switch instructions
        self.switchInstructionsFrame = Frame(self.instructionsFrame, bg=INSTRUCTIONS_BACKGROUND, pady=20)
        self.switchSetupTitle = Label(self.switchInstructionsFrame, text="SETUP MIDI SWITCH",
                                      font=("arial", 16, 'bold'),
                                      bg=INSTRUCTIONS_BACKGROUND,
                                      fg=INSTRUCTIONS_FORECOLOR)
        self.switchSetupTitle.pack()
        self.switchSetupInstructions = Label(self.switchInstructionsFrame, 
                                             text="""1. Click the Assign Switch Button.
2. Press the MIDI switch you want to use as your on/off tuner.""",
                                            font=("arial", 12),
                                            justify='left',
                                            bg=INSTRUCTIONS_BACKGROUND,
                                            fg=INSTRUCTIONS_FORECOLOR)
        self.switchSetupInstructions.pack()
        self.switchInstructionsFrame.pack()

        # Mouse button and coordinates
        self.buttonsFrame = Frame(self.window)
        self.mouseFrame = Frame(self.buttonsFrame)
        self.mouseButton = Button(self.mouseFrame, text="Mouse Setup", width=30, height=3, command=self.start_tracking)
        self.mouseButton.grid(row=0, column=0, columnspan=3)
        self.mouseXCoordinate = Label(self.mouseFrame, text=f"X: {self.x}")
        self.mouseXCoordinate.grid(row=1, column=0)
        self.mouseYCoordinate = Label(self.mouseFrame, text=f"Y: {self.y}")
        self.mouseYCoordinate.grid(row=1, column=2)

        # MIDI Button
        self.midiButton = Button(self.buttonsFrame, text="Assign Switch", width=30, height=3,  command=self.show_alert)

        self.instructionsFrame.grid(row=0, column=0)
        self.buttonsFrame.grid(row=0, column=1)
        self.mouseFrame.grid(row=0, column=0, padx=80, pady=25)
        self.midiButton.grid(row=1, column=0, pady=25)

        # Bind space key to stop tracking and save coordinates
        self.window.bind('<space>', self.stop_and_save_coordinates)

        self.window.mainloop()  # Start the main event loop
    
    def show_alert(self):
        """Show alert and start listening for MIDI CC note."""
        # Create the alert window
        self.alert_window = Toplevel(self.window)
        self.alert_window.title("MIDI Switch Setup")
        self.alert_window.geometry("300x100")  # Set window size
        self.alert_window.transient(self.window)
        self.alert_window.grab_set()  # Make the alert modal

        # Calculate the center position
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 300
        window_height = 100
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.alert_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Add the message to the alert
        Label(self.alert_window, text="Waiting for a switch to be pressed...", font=("Arial", 12)).pack(pady=20)

        # Start a separate thread to listen for MIDI messages
        midi_thread = threading.Thread(target=self.listen_for_midi_cc)
        midi_thread.start()

    def listen_for_midi_cc(self):
        """Listen for MIDI CC messages and close the alert when one is detected."""
        try:
            # Open MIDI input port
            with mido.open_input() as port:
                for message in port:
                    if message.type == 'control_change':
                        # Detected MIDI CC message; save and close the alert
                        self.cc = message.control
                        self.update_cc_in_file()
                        self.alert_window.destroy()  # Close alert
                        break
        except Exception as e:
            print("Error with MIDI input:", e)

    def update_cc_in_file(self):
        """Save the CC value to the configuration file."""
        with open("config.txt", "w") as file:
            file.write(f"x = {self.x}\n")
            file.write(f"y = {self.y}\n")
            file.write(f"cc = {self.cc}\n")

    def read_coordinates_from_file(self):
        """Read initial x, y, and cc values from the config file."""
        try:
            with open("config.txt", "r") as file:
                lines = file.readlines()
                # Extract x, y, and cc from the file if they exist
                x = int(lines[0].split('=')[1].strip()) if len(lines) > 0 else 0
                y = int(lines[1].split('=')[1].strip()) if len(lines) > 1 else 0
                cc = int(lines[2].split('=')[1].strip()) if len(lines) > 2 else 0
                return x, y, cc
        except FileNotFoundError:
            # Default values if file does not exist
            return 0, 0, 0
    
    def start_tracking(self):
        """Enable tracking and disable the button."""
        self.tracking = True
        self.mouseButton.config(state="disabled")  
        self.update_mouse_position()
    
    def stop_and_save_coordinates(self, event):
        """Stop tracking and save coordinates to file when Space is pressed."""
        self.tracking = False
        self.mouseButton.config(state="normal")

        # Retrieve current coordinates
        x = self.window.winfo_pointerx()
        y = self.window.winfo_pointery()

        # Update labels
        self.mouseXCoordinate.config(text=f"X: {x}")
        self.mouseYCoordinate.config(text=f"Y: {y}")

        # Save updated coordinates to config.txt
        self.x, self.y = x, y
        with open("config.txt", "w") as file:
            file.write(f"x = {self.x}\n")
            file.write(f"y = {self.y}\n")
            file.write(f"cc = {self.cc}\n")  # Assuming cc remains unchanged

    def update_mouse_position(self):
        """Update label with the current mouse position if tracking is enabled."""
        if self.tracking:
            x, y = self.window.winfo_pointerx(), self.window.winfo_pointery()
            self.mouseXCoordinate.config(text=f"X: {x}")
            self.mouseYCoordinate.config(text=f"Y: {y}")
            # Schedule the next update
            self.window.after(50, self.update_mouse_position)
