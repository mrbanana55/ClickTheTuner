from tkinter import *
INSTRUCTIONS_BACKGROUND = "#0697c7"
INSTRUCTIONS_FORECOLOR = "#ffffff"
class Gui:
    def __init__(self):
        #Create window
        self.window = Tk()
        self.window.title("Click the tuner")
        self.window.geometry("800x400")
        self.window.resizable(False, False)
        self.window.iconphoto(True, PhotoImage(file="Assets\\Icon.png"))

        #Create a frame for the instructions
        self.instructionsFrame = Frame(self.window,
                                       bg=INSTRUCTIONS_BACKGROUND,
                                       pady=80)
        
        #Create mouse instructions
        self.mouseInstructionsFrame = Frame(self.instructionsFrame,
                                            bg=INSTRUCTIONS_BACKGROUND,
                                            pady=20)
        self.mouseSetupTitle = Label(self.mouseInstructionsFrame, 
                           text="SETUP MOUSE POSITION",
                           font=("arial", 16, 'bold'),
                           bg=INSTRUCTIONS_BACKGROUND,
                           fg=INSTRUCTIONS_FORECOLOR)
        self.mouseSetupTitle.pack()
        self.mouseSetupInstructions = Label(self.mouseInstructionsFrame,
                                            text="""1. Click the Mouse Setup button.
2. Place your mouse where the tuner's on/off button is.
3. Press enter to save the mouse coordinates.                        """,
                                            font=("arial", 12),
                                            justify='left',
                                            bg=INSTRUCTIONS_BACKGROUND,
                                            fg=INSTRUCTIONS_FORECOLOR)
        self.mouseSetupInstructions.pack()
        self.mouseInstructionsFrame.pack()

        #Create switch instructions
        self.switchInstructionsFrame = Frame(self.instructionsFrame,
                                            bg=INSTRUCTIONS_BACKGROUND,
                                            pady=20)
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

        
        #Mouse button and coordinates
        self.buttonsFrame = Frame(self.window)
        self.mouseFrame = Frame(self.buttonsFrame)
        self.mouseButton = Button(self.mouseFrame ,text="mouse setup", width=30, height=3)
        self.mouseButton.grid(row=0, column=0, columnspan=3)
        self.mouseXCoordinate = Label(self.mouseFrame, text="X: 000")
        self.mouseXCoordinate.grid(row=1, column=0)
        self.mouseYCoordinate = Label(self.mouseFrame, text="Y: 000")
        self.mouseYCoordinate.grid(row=1, column=2)

        #MIDI Button
        self.midiButton = Button(self.buttonsFrame, text="Assign Switch", width=30, height=3)

        self.instructionsFrame.grid(row=0, column=0)
        self.buttonsFrame.grid(row=0, column=1)
        self.mouseFrame.grid(row=0, column=0, padx=80, pady=25)
        self.midiButton.grid(row=1, column=0, pady=25)
        self.window.mainloop()  # Start the main event loop
