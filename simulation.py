import random, sys

# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


(
    file_name,
    pop_size,
    vacc_percentage,
    virus_name,
    mortality_rate,
    repro_rate,
    initial_infected,
) = sys.argv


pop_size = int(pop_size)
vacc_percentage = float(vacc_percentage)
mortality_rate = float(mortality_rate)
repro_rate = float(repro_rate)
initial_infected = int(initial_infected)


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        logger = Logger("sim-logs.txt")
        self.logger = logger
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.total_infected = 0
        self.people = self._create_population()
        self.newly_infected = []
        self.num_new_deaths = 0
        self.num_of_infected = 0
        self.total_deaths = 0
        self.num_interactions = 0

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
            person.infected = True
            self.total_infected += 1
            people.append(person)
            index += 1

        for i in range(
            self.pop_size - self.initial_infected - num_of_people_vaccinated
        ):
            person = Person(index, False)
            people.append(person)
            index += 1

        return people

    def _simulation_should_continue(self):
        """
        Check to see if simulation should end.
        Simulation will end when everyone has been vaccinated or the virus has died out (reached herd immunity)
        """

        if len(self.newly_infected) == 0:
            return False

        for person in self.people:
            if person.is_alive:
                if not person.is_vaccinated:
                    return True
        return False

    def run(self):
        time_step_counter = 0
        should_continue = True
        self.logger.write_metadata(
            pop_size,
            vacc_percentage,
            virus.name,
            virus.mortality_rate,
            virus.repro_rate,
            self.initial_infected,
        )

        while should_continue:
            time_step_counter += 1
            self.num_of_infected = 0
            self.num_new_deaths = 0
            self.num_interactions = 0
            self.time_step()

            self._check_if_survived_infection()
            self.total_deaths += self.num_new_deaths
            should_continue = self._simulation_should_continue()
            self._infect_newly_infected()
            self.total_infected += self.num_of_infected

            self.logger.log_step_summary(
                time_step_counter,
                self.num_new_deaths,
                self.num_of_infected,
                self.num_interactions,
            )

        self.logger.end_log(self.total_deaths, self.total_infected)

    def time_step(self):
        for person in self.people:
            if person.infection and person.is_alive:
                for i in range(100):
                    random_person = random.choice(self.people)
                    while not random_person.is_alive:
                        random_person = random.choice(self.people)
                    self.num_interactions += 1
                    self.interaction(random_person)

    def interaction(self, random_person):
        random_number = random.random()

        if (
            not random_person.is_vaccinated
            and not random_person.infection
            and random_person.is_alive
        ):
            if random_number < self.virus.repro_rate:
                self.newly_infected.append(random_person)

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            if not person.infected:
                person.infection = self.virus
                person.infected = True
                self.num_of_infected += 1

        self.newly_infected = []

    def _check_if_survived_infection(self):
        for person in self.people:
            if person.infection:
                did_survive = person.did_survive_infection()
                if not did_survive:
                    self.num_new_deaths += 1


if __name__ == "__main__":

    virus = Virus(virus_name, repro_rate, mortality_rate)

    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
