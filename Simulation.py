import random, sys
from random import randrange, randint
from Person import Person
from Virus import Virus
from FileWriter import FileWriter

class Simulation:
  
    def __init__(self, initial_vaccinated, initial_infected, initial_healthy, virus, resultsfilename):
        '''Set up the initial simulation values'''

        self.virus = virus 
        self.initial_infected = initial_infected 
        self.initial_healthy = initial_healthy
        self.initial_vaccinated = initial_vaccinated

        self.population = []

        self.population_size = initial_infected + initial_healthy + initial_vaccinated


        self.total_dead = 0
        self.total_vaccinated = initial_vaccinated

        self.file_writer = FileWriter(resultsfilename)


    def create_population(self):
        '''Creates the population (a list of Person objects) consisting of initial infected people, initial healthy non-vaccinated people, and 
        initial healthy vaccinated people. Adds them to the population list'''

        for i in range(self.initial_infected):
        	person = Person(False, virus)
        	self.population.append(person)

        for i in range(self.initial_healthy):
            person = Person(False, None)
            self.population.append(person)

        for i in range(self.initial_vaccinated):
            person = Person(True, None)
            self.population.append(person)
        	
    def print_population(self):
        '''Prints out every person in the population and their current attributes'''
        #TODO: finish this method
        for person in self.population:
            
            print("Alive {}".format(person.is_alive))
            print("Vaccinated {}".format(person.is_vaccinated))
            print()


    def get_infected(self):
        '''Gets all the infected people from the population and returns them as a list'''
        #TODO: finish this method
        all_infected = []
        
        for person in self.population:
            if person.infection != None and person.is_alive:
                all_infected.append(person)
        return all_infected


    def simulation_should_continue(self):
        '''Determines whether the simulation should continue.
        If everyone in the population is dead then return False, the simulation should not continue
        If everyone in the population is vaccinated return False
        If there are no more infected people left and everyone is either vaccinated or dead return False
        In all other cases return True'''
        #TODO: finish this method    
        if self.total_dead == self.population_size:
            print('first trial')
            return False
            
        elif self.total_vaccinated == self.population_size:
            print('first trial test')
            return False 

        elif len(self.get_infected()) == 0:
            print('second trial test')
            return False

        else:
            print('third trial test')
            return True


    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        
        self.create_population()
        random.shuffle(self.population)

        self.print_population()
        
        time_step_counter = 0

        self.file_writer.init_file(self.virus, self.population_size, self.initial_vaccinated, self.initial_healthy, self.initial_infected)

        #keep looping until the simulation ends
        while self.simulation_should_continue():

            #save the current infected
            old_infected = self.get_infected()
            self.time_step(old_infected)
            #time step will create newly infected people, just determine the survivial of the previous infected people
            self.determine_survival(old_infected)
            time_step_counter += 1

        print(f'The simulation has ended after {time_step_counter} turns.')
        self.file_writer.write_results(time_step_counter, self.total_dead, self.total_vaccinated)

    def determine_survival(self, infected):
        '''Check if the current infected people survive their infection
        Call the did_survive_infection() method
        if it returns false then the person is no longer alive, does not have an infection and one is added to total dead
        if it returns true then the person no longer has an infection and is vaccinated, one is added to total vaccinated'''
        #TODO: finish this method
        for infected_person in infected:
            if infected_person.did_survive_infection() == False:
                infected_person.infection = None
                infected_person.is_alive = False
                self.total_dead += 1

            elif infected_person.did_survive_infection() == True:
                infected_person.infection = None
                infected_person.is_vaccinated == True
                self.total_vaccinated += 1


    def time_step(self, infected):
        ''' For every infected person interact with a random person from the population 10 times'''

        for infected_person in infected:

            for i in range(10):
                #TODO: get a random index for the population list

                #TODO: using the random index get a random person from the population
                random_person = random.choice(self.population)

                #TODO: call interaction() with the current infected person and the random person
                self.interaction(infected_person, random_person)
        
            


    def interaction(self, infected_person, random_person):
        '''If the infected person is the same object as the random_person return and do nothing
        if the random person is not alive return and do nothing
        if the random person is vaccinated return and do nothing
        if the random person is not vaccinated:
            generate a random float between 0 and 1
            if the random float is less then the infected person's virus reproduction number then the random person is infected
            othersie the random person is vaccinated and one is added to the total vaccinated'''
        #TODO: finish this method
        if infected_person is random_person:
            return

        if random_person.is_alive == False:
            return

        if random_person.is_vaccinated == True:
            return

        else:
            random_float = randrange(0.0,1.0)
            if random_float < infected_person.infection.reproduction_num:
                random_person.infection = infected_person.infection

            else:
                random_person.is_vaccinated = True
                self.total_vaccinated += 1


if __name__ == "__main__":

    #Set up the initial simulations values
    virus_name = "Malaise"
    reproduction_num = 0.70
    mortality_num = .50

    initial_healthy = 800
    initial_vaccinated = 200

    initial_infected = 200

    virus = Virus(virus_name, reproduction_num, mortality_num)

    simulation = Simulation(initial_vaccinated, initial_infected, initial_healthy, virus, "results.txt")

    #run the simulation
    simulation.run()