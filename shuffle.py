import msvcrt
import os
import random
import signal
import subprocess
import sys
import time


if __name__=="__main__":
  if len(sys.argv) >= 2:
    files = os.listdir(sys.argv[1])
    
    current_process = None
    current_index = 0
    paused = False
    
    while True:
      if current_process is None and not paused:
        if current_index < 0:
          print("Invalid index", current_index)
        elif current_index >= len(files):
          print("End of playlist")
          paused = True
        else:
          args = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            os.path.join(sys.argv[1], files[current_index])
          ]
          current_process = subprocess.Popen(args,
						stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE)
          print("Now playing", current_index, files[current_index])
      
      if current_process is not None and current_process.poll() is not None: # done playing
        current_process = None
        current_index += 1
      
      if msvcrt.kbhit() != 0:
        k = msvcrt.getch()
        if k == b' ': # stop / play
          paused = not paused
          if paused:
            print("Paused")
          if current_process is not None:
            current_process.kill()
            current_process = None
        elif k == b'k': # previous
          if current_index > 0:
            current_index -= 1
            if current_process is not None:
              current_process.kill()
              current_process = None
          else:
            print("Already at beginning of the playlist")
        elif k == b'j': # next
          if current_index < len(files) - 1:
            current_index += 1
            if current_process is not None:
              current_process.kill()
              current_process = None
        elif k == b's': # shuffle
          random.shuffle(files)
          current_index = 0
          if current_process is not None:
            current_process.kill()
            current_process = None
        elif k == b'c': # clear screen
          os.system("cls")
      
      time.sleep(0.050)

  else:
    print("Missing folder argument")
