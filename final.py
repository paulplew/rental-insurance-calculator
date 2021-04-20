#! /usr/bin/env python3

# Nathaniel Peters & Paul Plew
#
# A Program to advise drivers whether or not they should
# purchase car insurance when renting a car based on their
# age group and the car type.
#
# Tested and functional on Python 3.9.2
#
# unless otherwise stated the data is taken from
# https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/811059

import math


# Represents a driver
class Driver:
    # the total number of cars driving in a day
    daily_cars = 1.15 * 10**8
    # the total number of wrecks in a year
    total_wrecks = 6 * 10**6
    # the total number of wrecks daily
    daily_wrecks = total_wrecks / 365
    # Probability of an accident on a given day
    wreck_prob = daily_wrecks / daily_cars

    def __init__(self, car_g_accident, age_g_accident, car_type, age):
        self.car_g_accident = car_g_accident
        self.age_g_accident = age_g_accident
        self.car_type = car_type
        self.age = age

    # calculates the probability of getting
    def calculate_probability(self):
        bayes_numerator = self.car_g_accident * self.age_g_accident * self.wreck_prob
        bayes_denominator = self.car_type * (self.age / 2)
        return bayes_numerator / bayes_denominator


# Base Class for custom exceptions
class Error(Exception):
    pass


# the input given is too large
class InputTooLargeError(Error):
    pass


# the input given is too small
class InputTooSmallError(Error):
    pass


# rounds the given number to the given number of decimal places
def round(num, decimals):
    num *= (10 ** decimals)
    num = math.floor(num)
    num /= (10 ** decimals)
    return num


# The different types of cars and their frequencies in wrecks
# the frequencies are mapped to the types:
# "1) Passenger, 2) SUV, 3) Light Truck, 4) Other"
car_type_given_accident = [0.567, 0.188, 0.133, 0.073, 0.039]

# Data from https://bit.ly/3wEHF0a
# U.S. car demand: by segment in April 2020
car_type = [0.519, 0.086, 0.164, 0.159]

male_age_group_given_accident = [0.106, 0.095, 0.082, 0.046, 0.051]
female_age_group_given_accident = [0.102, 0.074, 0.055, 0.04, 0.034]

age_group = [0.173, 0.170, 0.188, 0.170, 0.173]


print("The purpose of this tool is to help you decide if you want to "
      "purchase insurance when renting a car.")
print("")

print("What is your age group?")
print("1) 26-35, 2) 36-45, 3) 46-55, 4) 56-65, 5) Over 65")
while True:
    try:
        age_index = int(input("Enter the number of your age group : ")) - 1
        if age_index < 0:
            raise InputTooSmallError
        elif age_index > 4:
            raise InputTooLargeError
        print("")
        break
    except InputTooLargeError:
        print("The given value is too large, try again.")
    except InputTooSmallError:
        print("The given value is too small, try again.")
    except ValueError:
        print("Please enter a number.")

print("Male or Female?")
while True:
    try:
        gender = int(input("Enter 0 for male, and 1 for female : "))
        if gender < 0:
            raise InputTooSmallError
        elif gender > 1:
            raise InputTooLargeError
        print("")
        break
    except InputTooLargeError:
        print("The given value is too large, try again.")
    except InputTooSmallError:
        print("The given value is too small, try again.")
    except ValueError:
        print("Please enter a number.")

print("The available car types are :")
print("1) Passenger, 2) SUV, 3) Light Truck, 4) Other")

while True:
    try:
        car_index = int(input("Enter the number of your car type : ")) - 1
        if car_index < 0:
            raise InputTooSmallError
        elif car_index > 3:
            raise InputTooLargeError
        print("")
        break
    except InputTooLargeError:
        print("The given value is too large, try again.")
    except InputTooSmallError:
        print("The given value is too small, try again.")
    except ValueError:
        print("Please enter a number.")


person = ""
if gender == 0:
    person = Driver(car_type_given_accident[car_index],
                    male_age_group_given_accident[age_index],
                    car_type_given_accident[car_index],
                    age_group[age_index])
else:
    person = Driver(car_type_given_accident[car_index],
                    female_age_group_given_accident[age_index],
                    car_type_given_accident[car_index],
                    age_group[age_index])

personal_wreck_probability = round(person.calculate_probability() * 100, 4)
daily_cost = round(person.calculate_probability() * 3144, 2)

print("Your probability of getting in an accident on "
      "a given day is: \n{}%".format(personal_wreck_probability))
print("You should buy insurance if it costs less than: "
      "\n${} per day".format(daily_cost))
