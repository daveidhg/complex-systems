import random
import MountainCarController as mc

# TODO: implement 4 random parents and use a bigger population for the testing
parents_list = [[random.choice([0, 1]) for _ in range(32)] for _ in range(4)]


mc.render_mode = None

best_velocity = 0
best_position = 0
best_list = []
flip_probability = 0.1

def random_flip(lookup_list):
    new_list = []
    for i in lookup_list:
        if random.random() <= flip_probability:
            new_list.append(1 if i == 0 else 0)
        else:
            new_list.append(i)
    return new_list

def calculate_pos_vel_score(position, velocity):
    position += 0.5  # Move the bottom position to be x-coord 0.
    

for _ in range(50):
    new_lists = [random_flip(parent_list) for _ in range(4)]
    for new_list in new_lists:
        mc.lookup_list = new_list
        mc.initialize()
        while not any([mc.truncated, mc.terminated]): 
            mc.update()

            # TODO: implement a way to use both the velocity and the position for evaluation of performance.
            if abs(mc.observation[1]) > best_velocity:
                best_list = new_list
                best_velocity = mc.observation[1]
        if mc.terminated:
            print(f"{new_list} is a winner!")
    parent_list = best_list
print(best_velocity, best_list)
