import random, sys

# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        logger = Logger("sim-logs.txt")
        self.logger = logger
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.people = self._create_population()
        self.newly_infected = []
        self.num_new_deaths = []
        self.num_newly_infected = []

    def _create_population(self):
        people = []
        num_of_people_vaccinated = int(self.vacc_percentage * self.pop_size)
        index = 0

        for i in range(num_of_people_vaccinated):
            person = Person(index, True)
            people.append(person)
            index += 1

        for i in range(initial_infected):
            person = Person(index, False, self.virus)
            people.append(people)
            index += 1

        for i in range(
            self.pop_size - self.initial_infected - num_of_people_vaccinated
        ):
            person = Person(index, False)
            people.append(person)
            index += 1

        return people

    def _simulation_should_continue(self):
        for person in self.people:
            if person.is_alive:
                if not person.is_vaccinated:
                    return True
        return False

    def run(self):
        # This method starts the simulation. It should track the number of
        # steps the simulation has run and check if the simulation should
        # continue at the end of each step.
        time_step_counter = 0
        should_continue = True
        self.logger.write_metadata(
            pop_size,
            vacc_percentage,
            virus.name,
            virus.mortality_rate,
            virus.repro_rate,
        )

        while should_continue:
            # TODO: Increment the time_step_counter
            time_step_counter += 1
            # TODO: for every iteration of this loop, call self.time_step()
            # Call the _simulation_should_continue method to determine if
            # the simulation should continue
            self.time_step()
            self._check_if_survived_infection()
            self._infect_newly_infected()
            should_continue = self._simulation_should_continue()

        # TODO: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.
        self.logger.end_log()

    def time_step(self):
        # This method will simulate interactions between people, calulate
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other
        # people in the population
        # TODO: Loop over your population
        for person in self.people:
            if person.infection and person.is_alive:
                for i in range(100):
                    random_person = random.choice(self.people)
                    self.interaction(random_person)

    def interaction(self, random_person):
        if not random_person.is_alive:
            return

        if random_person.is_vaccinated:
            return

        if random_person.infection:
            return

        random_number = random.random()
        if random_number < self.virus.repro_rate:
            self.newly_infected.append(random_person)

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus

        self.num_newly_infected = len(self.newly_infected)
        self.newly_infected = []

    def _check_if_survived_infection(self):
        for person in self.people:
            if person.infection:
                did_survive = person.did_survive_infection()
                if not did_survive:
                    self.num_new_deaths += 1


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.12
    initial_infected = 100

    # Make a new instance of the imulation
    # virus = Virus(virus, pop_size, vacc_percentage, initial_infected)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    # sim.run()
