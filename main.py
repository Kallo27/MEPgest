from mepgest.loaders import load_delegates
from mepgest.gui import launch_gui

load_delegates("data/participants.xlsx", verbose=True)
launch_gui()