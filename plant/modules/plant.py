"""
A wrapper for https://github.com/kipe/miplant/blob/master/miplant/miplant.py
"""

from time import sleep
import logging

from miplant import MiPlant
from modules import twitter

logging.basicConfig(level="INFO")


class Plant:

    def __init__(self):
        self.last_battery = 0  # %
        self.last_firmware = ""
        self.last_temperature = 0  # °C
        self.last_light = 0  # lux
        self.last_moisture = 0  # %
        self.last_conductivity = 0  # µS/cm

        self.twitter = twitter.Twitter()

    def scan(self):
        logging.info("Scanning")
        for plant in MiPlant.discover():
            print(plant)
            x = {
                "battery": plant.battery,
                "firmware": plant.firmware,
                "light": plant.light,
                "moisture": plant.moisture,
                "conductivity": plant.conductivity,
                "temperature": plant.temperature
            }
            logging.info(x)
            return x
        logging.warning("No plants found")
        return None

    def update(self, lecture):
        if lecture is None:
            logging.warning("Provided lecture was empty")
            return
        logging.debug("Updating last state")
        print("XXX", lecture)
        self.last_battery = lecture.get("battery", 0)
        self.last_firmware = lecture.get("firmware", "")
        self.last_temperature = lecture.get("temperature", 0)
        self.last_light = lecture.get("light", 0)
        self.last_moisture = lecture.get("moisture", 0)
        self.last_conductivity = lecture.get("conductivity", 0)

    def create_tweet(self, lecture):
        if (self.last_light == 0
                or self.last_moisture == 0
                or self.last_temperature == 0):
            logging.info("Still starting")
            return None
        if (lecture["light"] == 0
            or lecture["moisture"] == 0
                or lecture["temperature"] == 0):
            return None
        tweet = []
        if lecture["moisture"] > 10 and self.last_moisture <= 10:
            tweet.append(
                f"🌱 Thank you for watering me! 😊 (moisture at {lecture['moisture']}%).")
        if lecture["moisture"] < 10:
            tweet.append(
                f"🏜 I need water 😕 (moisture at {lecture['moisture']}%).")
        if lecture["temperature"] > 28:
            tweet.append("🌡 It's hot in here 🥵 (it's %s °C)." %
                         lecture["temperature"])
        if lecture['light'] < 150 and abs(lecture['light'] - self.last_light) > 50:
            tweet.append(
                "🌚 Did someone turn off the light? 🔦 (light at %s lux)." % lecture["light"])
        if lecture['light'] - self.last_light > 400:
            tweet.append("😎 Am I being flashed light at demos now? Hello guys! 👋 (light at %s lux)." %
                         lecture["light"])
        if lecture['light'] >= 2000 and self.last_light < 2000:
            tweet.append("💡 And there was light! Thanks for the sunshine ☀️ (light at %s lux)." %
                         lecture["light"])
        if lecture['battery'] < 25 and self.last_battery != 0 and lecture['battery'] != 0:
            tweet.append("🔌 I'm running low on batteries! (battery at %s)." %
                         lecture["battery"])
        if lecture["conductivity"] < 67:
            tweet.append("🪴 My soil doesn't feel great. (fertility at %s µS/cm)." %
                         lecture["conductivity"])
        if len(tweet) == 0:
            tweet.append(f"""
                🌈 Everything is fine.\n
                Moisture: {lecture["moisture"]}\n
                Light: {lecture["light"]}\n
                Temperature: {lecture["temperature"]}\n
                Fertility: {lecture["conductivity"]}\n
                Battery: {lecture["battery"]}
                """)
        tweet.append("#IamRoot #YoSoyRoot @Eurielec")
        tweet = "\n".join(tweet)
        logging.info(tweet)
        return tweet

    def run(self):
        print("A1")
        lecture = self.scan()
        print("A2")
        if lecture is None:
            logging.warning("Lecture was empty")
            return None
        tweet = self.create_tweet(lecture)
        logging.debug(tweet)
        self.update(lecture)
        print("A3")
        return tweet

    def loop(self, iteration_time=int(15 * 60 * 100)):
        try:
            while True:
                try:
                    print("A")
                    tweet = self.run()
                    print("B")
                    if tweet is None:
                        logging.debug("Skipping iteration")
                        continue
                    else:
                        self.twitter.tweet(tweet)
                        logging.info("Next iteration in: %s %s",
                             iteration_time/60/100, "min")
                        sleep(iteration_time)
                except Exception as e:
                    logging.warn("No luck, trying again")
        except Exception as e:
            logging.error("Something", e)
            logging.info("Closing")
