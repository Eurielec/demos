"""
Credits for the idea and implementation to:
Álvaro Escribano @ Eurielec
@javierantonyuste @ GitHub

I just refactored it using classes, python3 and environment variables.
@d3vv3 @ GitHub
"""

from dotenv import load_dotenv

from modules import plant

if __name__ == "__main__":
    load_dotenv()
    # print("STARTED")
    p = plant.Plant()
    p.loop(iteration_time=15*60*100)
