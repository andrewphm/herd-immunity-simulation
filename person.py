import random

# random.seed(42)
from virus import Virus


class Person(object):
    # Define a person.
    def __init__(self, _id, is_vaccinated, infection=None):
        # A person has an id, is_vaccinated and possibly an infection
        self._id = _id  # int
        # TODO Define the other attributes of a person here
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True
        pass

    def did_survive_infection(self):
        # This method checks if a person survived an infection.
        # TODO Only called if infection attribute is not None.
        # Check generate a random number between 0.0 - 1.0
        # If the number is less than the mortality rate of the
        # person's infection they have passed away.
        # Otherwise they have survived infection and they are now vaccinated.
        # Set their properties to show this
        # TODO: The method Should return a Boolean showing if they survived.
        if self.infection:
            random_percent = random.random()
            if random_percent < self.infection.mortality_rate:
                self.is_alive = False
                return False
            else:
                self.is_vaccinated = True
                return True
        else:
            return True


if __name__ == "__main__":
    # This section is incomplete finish it and use it to test your Person class
    # TODO Define a vaccinated person and check their attributes
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    # Create an unvaccinated person and test their attributes
    unvaccinated_person = Person(2, False)
    # TODO Test unvaccinated_person's attributes here...
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    # Test an infected person. An infected person has an infection/virus
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.07, 0.2)
    # Create a Person object and give them the virus infection
    infected_person = Person(3, False, virus)
    # TODO: complete your own assert statements that test
    # the values of each attribute
    # assert ...
    assert type(infected_person.did_survive_infection()) is bool
    assert infected_person._id == 3
    assert type(infected_person.is_vaccinated) is bool
    # You need to check the survival of an infected person. Since the chance
    # of survival is random you need to check a group of people.
    # Create a list to hold 100 people. Use the loop below to make 100 people
    people = []
    for i in range(0, 100):
        # TODO Make a person with an infection
        person = Person(i, False, virus)
        # TODO Append the person to the people list
        people.append(person)

    # Now that you have a list of 100 people. Resolve whether the Person
    # survives the infection or not by looping over the people list.

    did_survived = 0
    did_not_survive = 0
    # Count the people that survived and did not survive:

    # TODO Loop over all of the people
    # TODO If a person is_alive True add one to did_survive
    # TODO If a person is_alive False add one to did_not_survive
    for person in people:
        survived = person.did_survive_infection()
        if survived:
            did_survived += 1
        else:
            did_not_survive += 1

    print(f"Survived: {did_survived}")
    print(f"Died: {did_not_survive}")

    # TODO When the loop is complete print your results.
    # The results should roughly match the mortality rate of the virus
    # For example if the mortality rate is 0.2 rough 20% of the people
    # should succumb.

    uninfected_people = []
    infected_people = []

    for i in range(0, 100):
        person = Person(i, False)
        uninfected_people.append(person)

    for person in uninfected_people:
        random_number = random.random()
        if random_number < virus.repro_rate:
            person.infection = virus
            infected_people.append(person)

    print(
        f"With a reproductive rate of 0.07 and out of 100 people, there were {len(infected_people)} infections."
    )
    # Stretch challenge!
    # Check the infection rate of the virus by making a group of
    # unifected people. Loop over all of your people.
    # Generate a random number. If that number is less than the
    # infection rate of the virus that person is now infected.
    # Assign the virus to that person's infection attribute.

    # Now count the infected and uninfect people from this group of people.
    # The number of infectedf people should be roughly the same as the
    # infection rate of the virus.
