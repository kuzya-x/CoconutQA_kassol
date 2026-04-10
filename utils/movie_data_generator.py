import random
import string
from faker import Faker
faker = Faker('en_US')

class MovieDataGenerator:

    @staticmethod
    def generate_name():
        return faker.catch_phrase()
    @staticmethod
    def generate_image_url():
        return faker.image_url()
    @staticmethod
    def generate_price():
        return random.randint(100, 2000)
    @staticmethod
    def generate_description():
        return faker.sentence()
    @staticmethod
    def generate_location():
        locations = ["SPB", "MSK"]
        return random.choice(locations)
    @staticmethod
    def generate_published():
        return random.choice([True, False, True, True])
    @staticmethod
    def generate_genre_id():
        return random.randint(1, 10)

    @staticmethod
    def generate_rating():
        return random.randint(0, 100)

    @staticmethod
    def generate_movie_data():
        return {
            "name": MovieDataGenerator.generate_name(),
            "imageUrl": MovieDataGenerator.generate_image_url(),
            "price": MovieDataGenerator.generate_price(),
            "description": MovieDataGenerator.generate_description(),
            "location": MovieDataGenerator.generate_location(),
            "published": MovieDataGenerator.generate_published(),
            "genreId": MovieDataGenerator.generate_genre_id()
        }