try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
    from tkFileDialog import askopenfilename
    import signal
    import os
    import sys

except ImportError:
    # for Python3
    from tkinter import *   ## notice here too
root = Tk()
root.withdraw()
file_path = askopenfilename()

file = open("buffer.txt", 'w')
file.write(file_path)
print sys.argv[1]
os.kill(int(sys.argv[1]), signal.CTRL_BREAK_EVENT)
