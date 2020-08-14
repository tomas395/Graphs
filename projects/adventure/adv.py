from player import Player
from world import World
from ast import literal_eval
from util import Queue
import random

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverse_path = []
rooms = {}
done = False
previous_room_id = -1
previous_direction = 'n'
opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


def get_room_exits():
    exits = player.current_room.get_exits()
    # what room and direction did they come from
    if player.current_room.id not in rooms:
        rooms[player.current_room.id] = {'n': '?', 'e': '?', 's': '?', 'w': '?'}
        rooms[player.current_room.id]['n'] = '?' if 'n' in exits else None
        rooms[player.current_room.id]['e'] = '?' if 'e' in exits else None
        rooms[player.current_room.id]['s'] = '?' if 's' in exits else None
        rooms[player.current_room.id]['w'] = '?' if 'w' in exits else None
        if previous_room_id != -1:
            rooms[player.current_room.id][opposite_direction[previous_direction]] = previous_room_id
    else:
        rooms[player.current_room.id][opposite_direction[previous_direction]] = previous_room_id


def is_explored(room):
    # if there are no more ? remaining to be explored, we're done
    if room['n'] != '?' and room['e'] != '?' and room['s'] != '?' and room['w'] != '?':
        return True
    else:
        return False


def move_direction(direction):
    # question: why does previous direction and previous_room_id need to be in the global scope but traversal_path doesnt?
    global previous_direction
    global previous_room_id
    traversal_path.append(direction)
    previous_direction = direction
    previous_room_id = player.current_room.id
    player.travel(direction)
    if rooms[previous_room_id][direction] == '?':
        rooms[previous_room_id][direction] = player.current_room.id


def move_to_next_unexplored():
    room = rooms[player.current_room.id]
    print("current room not explored", room)
    valid_exits = []
    if room['w'] == '?':
        valid_exits.append('w')
    if room['s'] == '?':
        valid_exits.append('s')
    if room['n'] == '?':
        valid_exits.append('n')
    if room['e'] == '?':
        valid_exits.append('e')

    # if room['n'] == '?':
    #     next_direction = 'n'
    # elif room['e'] == '?':
    #     next_direction = 'e'
    # elif room['s'] == '?':
    #     next_direction = 's'
    # elif room['w'] == '?':
    #     next_direction = 'w'
    # else:
    #     print('Error: That wont do...')

    random.shuffle(valid_exits)
    next_direction = valid_exits[0]
    print(f"moving to {next_direction}")
    move_direction(next_direction)


def move_backwards():
    directions = find_path_to_unexplored(player.current_room.id)
    print('moving backwards!!!', directions)
    if len(directions) > 0:
        for direction in directions:
            move_direction(direction)


# this is the BFS to find the nearest unexplored room
def find_path_to_unexplored(start):
    visited = {}
    q = Queue()
    q.enqueue([(None, start)])
    directions = []

    while q.size() > 0:
        path = q.dequeue()
        current_room = path[-1]
        current_room_id = current_room[1]
        if current_room_id in visited:
            continue

        visited[current_room_id] = path
        for direction in rooms[current_room_id]:
            next_room = rooms[current_room_id][direction]
            current_path = path.copy()
            if next_room == '?':
                for n in current_path:
                    if n[0] is not None:
                        directions.append(n[0])
                return directions
            if next_room is not None:
                current_path.append((direction, next_room))
                q.enqueue(current_path)
    # if nothing is found this will return an empty list
    return directions


def done_exploring():
    if len(rooms) < len(room_graph):
        return False
    else:
        result = True
        for room in rooms:
            if not is_explored(rooms[room]):
                result = False
        print('done?')
        print(result)
        return result


# ↓ main exploration loop in 3 steps:
while not done:
    # 1. get current room information, and compare it to what we already know
    get_room_exits()

    # 2. figure out where to move
    if not is_explored(rooms[player.current_room.id]):
        # A) move an unexplored direction if we can
        move_to_next_unexplored()
    else:
        # B) move back to the nearest room with an explored direction
        move_backwards()

    # 3. figure out if were done by looping thru every room and making sure it has no ?s
    if done_exploring():
        done = True


#  TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
