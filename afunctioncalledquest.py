from uuid import uuid4
from random import choice, randrange, random
from math import floor, ceil

# NUM_LOCATIONS = 100
# POP_DENSITY_MODIFIER = 10
NUM_LOCATIONS = 10
POP_DENSITY_MODIFIER = 1
LOCATION_WEALTH_MODIFIER = 0.1
PERSONAL_WEALTH_MODIFIER = 0.5
CONNECTIVITY_MODIFIER = 0.25

VERBOSE = False


#  #  #  #  #  #  #  #  #  #


item_types = 'wand;book;jewelry'.split(';')

action_types = 'move_to;pick_up;buy;steal;read;use;cast;attack'

actions_on = {
    'wand': ['pick_up', 'steal', 'buy'],
    'book': ['pick_up', 'read', 'steal', 'buy'],
    'jewelry': ['pick_up', 'steal', 'buy'],
    'location': ['move_to'],
    # 'person': ['attack'],
    # 'self': ['cast'],
}

action_preconditions = {
    'move_to': ['@0.location is_not @1.self', '@0.location.connections includes @1.self', '@0.locations_known includes @1.self'],
    'pick_up': ['@0.location is @1.location', '@1.owner is None', '@0.items_known includes @1.unique'],
    'buy': ['@0.location is @1.location', '@1.inventory includes @2.self', '@0.gold greater_than @2.price'],
    'steal': ['@0.location is @1.location', '@1.inventory includes @2.self', '@0.items_known includes @1.unique'],
    'read': ['@0.inventory includes @1.self'],
    # 'cast': ['@0.spells_known includes @1.self'],
    # 'attack': ['@0.location is @1.location'],
    # 'use': ['@0.inventory includes @1.self'],
}

action_postconditions = {
    'move_to': ['@0.location becomes @1.self'],
    'pick_up': ['@1.self added_to @0.inventory'],
    'buy': ['@0.gold reduced_by @2.price', '@2.self removed_from @1.inventory', '@1.gold increased_by @2.price', '@2.self added_to @0.inventory'],
    'steal': ['@1.disposition[@0.self] assigned_to {-1}', '@2.self added_to @0.inventory'],
    'read': ['@1.about added_to @0.spells_known'],
    # 'cast': ['@1.self added_to @0.spells_cast'],
    # 'attack': ['@0.health reduced_by {@0.combat - @1.combat}', '@1.health reduced_by {@1.combat - @0.combat}'],
    # 'use': ['@1.spell added_to @0.spells_cast'],
}


#  #  #  #  #  #  #  #  #  #


c = 'w,st,p,l,k,g'.split(',')
v = 'oo,u,ee,a,o,y,ia'.split(',')
def random_name():
    out = ''
    length = randrange(2, 5)
    last = choice(['c', 'v'])
    for i in range(length):
        if last == 'v':
            out += choice(c)
            last = 'c'
        else:
            out += choice(v)
            last = 'v'
    return out


#  #  #  #  #  #  #  #  #  #


generated_location_keys = []
generated_locations = {}
class Location:
    def __init__(self):
        self.id = str(uuid4())
        self.name = random_name() + ' ' + choice(['city', 'village', 'township', 'county', 'town', 'court', 'state'])
        self.connections = []

    def random_walk(self, n):
        if n == 0:
            return [choice(self.connections)]

        next = choice(self.connections)
        out = [next] + generated_locations[next].random_walk(n-1)
        return list(set(out))

    def copy(self):
        out = Location()
        out.id = self.id
        out.name = self.name
        out.connections = [e for e in self.connections]
        return out

    def __str__(self):
        return self.name + ':\n' + '\n'.join(['\t' + generated_locations[c].name for c in self.connections])

for i in range(NUM_LOCATIONS):
    loc = Location()
    generated_location_keys.append(loc.id)
    generated_locations[loc.id] = loc

for i, loc_id in enumerate(generated_location_keys):
    loc = generated_locations[loc_id]
    neighbors_ct = ceil(CONNECTIVITY_MODIFIER*10/((i/25)**4+1))

    if len(loc.connections) >= neighbors_ct:
        continue

    for j in range(neighbors_ct):
        neighbor = choice(generated_location_keys)
        if neighbor not in loc.connections:
            loc.connections.append(neighbor)
            generated_locations[neighbor].connections.append(loc.id)


generated_people_keys = []
generated_people = {}
class Person:
    def __init__(self):
        self.id = str(uuid4())

        self.name = random_name() + ' ' + random_name()

        self.curiosity = randrange(10)+1
        self.greed = randrange(10)+1

        self.selfishness = randrange(10)+1

        self.location = ''

        self.gold = 100
        self.inventory = []

        self.locations_known = []
        self.items_known = [] # unique items known, not item types
        self.people_known = []

        self.spells_known = []
        self.spells_cast = []

    def happiness(self):
        happiness = 0

        wealth = self.gold
        for item in self.inventory:
            # note: for trading, need a system to find proper amount of gold to
            #       offer to offset this (also taking into account disposition
            #       toward the other party). This won't necessarily be zero-sum,
            #       so there must also be some other motive for one party to be
            #       trading (dynamic percieved value of items + gold?)
            # In general, should prefer to hold wealth in items (due to inflation)
            wealth += 1.1*generated_items[item].price
        wealth *= 0.001
        happiness += wealth * self.greed

        knowledge = 0
        knowledge += len(self.locations_known)
        knowledge += len(self.items_known)
        knowledge += len(self.people_known)
        knowledge += 2*len(self.spells_known)
        knowledge *= 0.5
        happiness += knowledge * self.curiosity

        return happiness

    def actions(self):
        # return all legal actions based on current state of self

    def copy(self):
        out = Person()
        out.id = self.id
        out.name = self.name
        out.curiosity = self.curiosity
        out.greed = self.greed
        out.selfishness = self.selfishness
        out.location = self.location
        out.gold = self.gold
        out.inventory = [e for e in self.inventory]
        out.locations_known = [e for e in self.locations_known]
        out.items_known = [e for e in self.items_known]
        out.people_known = [e for e in self.people_known]
        out.spells_known = [e for e in self.spells_known]
        out.spells_cast = [e for e in self.spells_cast]
        return out

    def __str__(self):
        return self.name + ' of ' + generated_locations[self.location].name\
               + ':\n\tgold: ' + str(self.gold)\
               + '\n\tlocations_known: ' + str(len(self.locations_known))\
               + '\n\tnum_items: ' + str(len(self.inventory))\
               + '\n\tc,g,s: ' + str(self.curiosity) + ',' + str(self.greed) + ',' + str(self.selfishness)\
               + '\n\thappiness: ' + str(floor(self.happiness()))

for i, loc_id in enumerate(generated_location_keys):
    loc = generated_locations[loc_id]

    J = len(loc.connections)*POP_DENSITY_MODIFIER
    for j in range(J):
        dude = Person()
        dude.location = loc_id
        dude.locations_known = loc.random_walk(10)
        # print(map(lambda id: generated_locations[id].name, dude.locations_known))

        dude.gold = floor(1000*(((j+1)/(J+1))**2)*random())

        generated_people_keys.append(dude.id)
        generated_people[dude.id] = dude

# items known

# people known


generated_items_keys = []
generated_items = {}
class Item:
    def __init__(self, owner=None, location=None):
        self.id = str(uuid4())

        self.type = choice(item_types)
        self.name = choice([self.type + ' of ' + random_name(), random_name() + ' ' + self.type])
        self.price = randrange(1000)

        self.owner = owner
        self.location = location

        if self.owner is not None:
            self.unique = self.owner + self.id
        elif self.location is not None:
            self.unique = self.location + self.id

    def copy(self):
        out = Item(self.owner, self.location)
        out.id = self.id
        out.unique = self.unique
        out.type = self.type
        out.name = self.name
        out.price = self.price
        return out

    def __str__(self):
        owner_location = '\n\tlimbo error (oops)'
        if self.owner is not None:
            owner_location = '\n\towner: ' + generated_people[self.owner].name
        elif self.location is not None:
            owner_location = '\n\tlocation: ' + generated_locations[self.location].name

        return self.name\
               + ': \n\tprice: ' + str(self.price)\
               + owner_location

for i, loc_id in enumerate(generated_location_keys):
    loc = generated_locations[loc_id]
    J = floor(len(loc.connections)**2*LOCATION_WEALTH_MODIFIER)
    for j in range(J):
        item = Item(location=loc_id)
        generated_items_keys.append(item.id)
        generated_items[item.id] = item

for i, dude_id in enumerate(generated_people_keys):
    dude = generated_people[dude_id]
    J = floor((2*dude.greed+dude.curiosity)*PERSONAL_WEALTH_MODIFIER)
    for j in range(J):
        item = Item(owner=dude_id)
        generated_items_keys.append(item.id)
        generated_items[item.id] = item
        dude.inventory.append(item.id)

class WorldState:
    def __init__(self, locations, people, items):
        self.locations = locations
        self.people = people
        self.items = items

    def copy(self):
        new = WorldState({}, {}, {})
        for k, v in self.locations.items():
            new.locations[k] = v.copy()

        for k, v in self.people.items():
            new.people[k] = v.copy()

        for k, v in self.items.items():
            new.items[k] = v.copy()

        return new

    def take_action(self, action):
        # check preconditions
        # set postconditions


#  #  #  #  #  #  #  #  #  #


if VERBOSE:
    print(len(generated_items_keys), len(generated_people_keys), len(generated_location_keys))
    [print(loc) for _, loc in generated_locations.items()]
    [print(dude) for _, dude in generated_people.items()]
    [print(item) for _, item in generated_items.items()]

# open preconditions can include (location not known), (person not known), (item not known),

ws = WorldState(generated_locations, generated_people, generated_items)

SIMULATIONS = 100
TIMESTEPS = 10


# create a lxmxn array of random actions
# l: number of simulations to run
# m: number of timesteps per simulation
# n: number of actors
actions = []

# create a similar array, but for happiness
happinesses = [[[None for p in range(len(generated_people_keys))] for t in range(TIMESTEPS)] for s in range(SIMULATIONS)]

for s in range(SIMULATIONS):
    wsc = ws.copy()
    sim = []
    for t in range(TIMESTEPS):
        this_timestep_actions = []
        # note: by doing this, no one can act simultaneously
        for i, id in enumerate(generated_people_keys):
            person = generated_people[id]

            # set happiness for previous action (having now seen all other actors act)
            if t > 0:
                happinesses[s][t-1][i] = person.happiness()

            # take a random action
            action = choice(person.actions())
            wsc.take_action(action)
            this_timestep_actions.append(action)

        sim.append(this_timestep_actions)
    actions.append(sim)

# actions[simulation_number][timestep][actor]
# weight simulations by their effect:
#   sum_over_sims[(1-happiness_timestep/m)(happiness_timestep - happiness_(timestep-1))]/l
# choose the sim with the highest weight. take the first action in that sim
aggregated_happinesses = []
for s in range(len(happinesses)):
    for t in range(len(happinesses[0])):
        for p in range(len(happinesses[0][0])):
            continue
