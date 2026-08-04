import random


def should_create_invalid_record(probability):
    random_value = random.random()
    return random_value < probability