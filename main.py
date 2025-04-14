from mepgest.loaders import load_delegates
from mepgest.gui import launch_gui

load_delegates("data/delegates.xlsx", verbose=True)
launch_gui()