import random
import MountainCarController as mc

parent_list = [random.choice([0, 1]) for _ in range(32)]
mc.render_mode = None

best_position = 0
best_list = []
flip_probability = 0.9

def random_flip(lookup_list):
    new_list = []
    for i in lookup_list:
        if random.random() >= flip_probability:
            new_list.append(1 if i == 0 else 1)
        else:
            new_list.append(i)
    return new_list

for _ in range(500):
    new_lists = [random_flip(parent_list) for _ in range(4)]
    for new_list in new_lists:
        mc.initialize()
        while not any([mc.truncated, mc.terminated]): 
            mc.lookup_list = new_list
            mc.update()
            if mc.observation[0] > best_position:
                best_list = new_list
                best_position = mc.observation[1]
        if mc.terminated:
            print(f"{new_list} is a winner!")
    parent_list = best_list
print(best_position, best_list)
