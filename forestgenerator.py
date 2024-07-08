import random
import pygame
import os

current_dir = os.path.dirname(__file__)
# Initialize pygame and load images (placeholders for actual file paths)
pygame.init()
castle_image = pygame.image.load(os.path.join(current_dir, "castle.jpg"))
hollow_tree_image = pygame.image.load(os.path.join(current_dir, "hollow_tree.jpeg"))
forest_fork1_image = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_fork1.jpg"))
monastary_image = pygame.image.load(os.path.join(current_dir, "monastary_forest.jpg"))
monastery_room = pygame.image.load(os.path.join(current_dir, "monastery.jpg"))

forest_road1 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road1.jpg"))
forest_road2 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road2.jpg"))
forest_road3 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road3.jpg"))
forest_road4 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road4.jpg"))
forest_road5 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road5.jpg"))
forest_road6 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road6.jpg"))
forest_road7 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road7.jpg"))
forest_road8 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road8.jpg"))
forest_road9 = pygame.image.load(os.path.join(current_dir, fr"forest_roads\forest_road9.jpg"))

graveyard_entrance_image = pygame.image.load(os.path.join(current_dir, "graveyard_entrance.jpeg"))
graveyard_catacomb_image = pygame.image.load(os.path.join(current_dir, "graveyard_catacomb.jpeg"))
graveyard_road1 = pygame.image.load(os.path.join(current_dir, "graveyard_road1.jpeg"))
graveyard_road2 = pygame.image.load(os.path.join(current_dir, "graveyard_road2.jpeg"))
graveyard_road3 = pygame.image.load(os.path.join(current_dir, "graveyard_road3.jpg"))
graveyard_road4 = pygame.image.load(os.path.join(current_dir, "graveyard_road4.jpg"))

hollow_tree_road1 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree1.jpeg"))
hollow_tree_road2 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree2.jpeg"))
hollow_tree_road3 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree3.jpeg"))
hollow_tree_road4 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree4.jpeg"))
hollow_tree_road5 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree5.jpeg"))
hollow_tree_road6 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree6.jpeg"))
hollow_tree_road7 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree7.jpeg"))

hollow_tree_fork = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree_fork.jpeg"))
hollow_tree_end1 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree_end1.jpeg"))
hollow_tree_end2 = pygame.image.load(os.path.join(current_dir, fr"hollow_tree\hollow_tree_end2.jpeg"))

hollow_tree_roads = [hollow_tree_road1,hollow_tree_road2,hollow_tree_road3,hollow_tree_road4,
                      hollow_tree_road5,hollow_tree_road6,hollow_tree_road7]

map_images = [forest_road1,forest_road2,forest_road3,forest_road4,
              forest_road5,forest_road6,forest_road7,forest_road8,forest_road9]

graveyard_map_images = [graveyard_road1,graveyard_road2]
# Example usage
regular_node_images = map_images
special_images = {
    'graveyard': {'entrance': graveyard_entrance_image, 'path': [graveyard_road1, graveyard_road2,graveyard_road3,graveyard_road4], 'graveyard catacomb': graveyard_catacomb_image},
    'castle': {'end': castle_image},
    'hollow tree': {'end': hollow_tree_image},
    'monastery': {'end': monastary_image}
}

import random
import pygame

# Initialize Pygame (necessary to create surfaces)
pygame.init()

# Node classes
class RegularNode:
    def __init__(self, image,node_type = 'regular',combat = False,number = 0,spawned_somthing = False):
        self.prev = None
        self.next = None
        self.image = image
        self.node_type = node_type
        self.combat = combat
        self.number = number
        self.spawned_somthing = spawned_somthing
class ComplexNode:
    def __init__(self, image, node_type = 'regular',number = 0):
        self.prev = None
        self.left = None
        self.right = None
        self.image = image
        self.node_type = node_type
        self.number = number
# Forest Generator class
class ForestGenerator:
    def __init__(self, regular_node_images, special_images, max_regular_nodes=6, max_complex_nodes=5):
        self.regular_node_images = regular_node_images
        self.hollow_node_images = hollow_tree_roads
        self.special_images = special_images
        self.max_regular_nodes = max_regular_nodes
        self.max_complex_nodes = max_complex_nodes
        self.regular_nodes = []
        self.complex_nodes = []
        self.head = None
        self.tail = None
        self.last_image = None
        self.special_deadends = ['castle','graveyard','hollow tree','monastery','regular']

    def generate_forest(self):
        self.head = RegularNode(self._get_random_image())
        self.tail = self.head
        self.regular_nodes.append(self.head)
        random.shuffle(self.special_deadends)

        last_was_complex = False
        complex_left = self.max_complex_nodes - len(self.complex_nodes)
        regular_left = self.max_regular_nodes - len(self.complex_nodes)
        total_left = complex_left + regular_left
        iteration = 0
        while complex_left > 0 or regular_left > 0:
            iteration+=1
            print(iteration)
            chance = random.random()
            if complex_left > 0  and chance < complex_left/total_left and not last_was_complex:
                self._add_complex_node()
                last_was_complex = True
                complex_left -= 1
                total_left -= 1
            elif regular_left > 0:
                self._add_regular_node()
                last_was_complex = False
                regular_left -= 1
                total_left -= 1
            elif complex_left >= 1 and regular_left == 0:
                regular_left += 1
                total_left += 1
        print(iteration)
        return self.head
    
    def _get_random_image(self,regular = True):
        if regular:
            images = self.regular_node_images
        else:
            images = self.hollow_node_images
        image = random.choice(images)
        while image == self.last_image:
            image = random.choice(images)
        self.last_image = image
        return image

    def _add_complex_node(self):
        complex_node = ComplexNode(forest_fork1_image)
        complex_node.prev = self.tail
        self.tail.next = complex_node
        self.tail = complex_node
        self.complex_nodes.append(complex_node)
        deadend_chosen = self.special_deadends.pop()
        if deadend_chosen == "regular":
            deadend_head = self._create_deadend()
            deadend_head.prev = complex_node
            if random.choice([True, False]):
                complex_node.left = deadend_head
            else:
                complex_node.right = deadend_head
        else:
            deadend_head_spcl = self._create_special_deadend(deadend_chosen)
            deadend_head_spcl.prev = complex_node
            if random.choice([True,False]):
                complex_node.left = deadend_head_spcl
            else:
                complex_node.right = deadend_head_spcl
        
        regular_node = RegularNode(self._get_random_image())
        regular_node.prev = complex_node
        if complex_node.left is None:
            complex_node.left = regular_node
        else:
            complex_node.right = regular_node
        self.tail = regular_node
        self.regular_nodes.append(regular_node)

    def _add_regular_node(self):
        regular_node = RegularNode(self._get_random_image())
        regular_node.prev = self.tail
        self.tail.next = regular_node
        self.tail = regular_node
        self.regular_nodes.append(regular_node)

    def _create_deadend(self,path_type = 'regular',regular = True):
        deadend_length = random.randint(2, 5)
        deadend_head = RegularNode(self._get_random_image(regular),path_type)
        current = deadend_head
        for _ in range(deadend_length - 1):
            next_node = RegularNode(self._get_random_image(regular),path_type)
            current.next = next_node
            next_node.prev = current
            current = next_node
        return deadend_head

    def _create_special_deadend(self, deadend_type):
        special_images = self.special_images[deadend_type]
        if deadend_type == 'graveyard':
            deadend_length = 5
            head = RegularNode(special_images['entrance'],'graveyard entrance')
            current = head
            for _ in range(deadend_length - 2):
                next_node = RegularNode(random.choice(special_images['path']),deadend_type)
                current.next = next_node
                next_node.prev = current
                current = next_node
            end = RegularNode(special_images['graveyard catacomb'],'graveyard catacomb')
            current.next = end
            end.prev = current
            return head
        else:
            deadend_length = random.randint(3, 5)
            head = RegularNode(self._get_random_image(),'regular')
            current = head
            for _ in range(deadend_length - 2):
                next_node = RegularNode(self._get_random_image(),'regular')
                current.next = next_node
                next_node.prev = current
                current = next_node
            end = RegularNode(special_images['end'],'end '+ deadend_type)
            
            current.next = end
            end.prev = current
            if deadend_type == 'monastery':
                monastery_room_node = RegularNode(monastery_room, deadend_type + ' room')
                end.next = monastery_room_node
                monastery_room_node.prev = end
            if deadend_type == 'hollow tree':
                hollow_path = self._create_hollow_tree()
                end.next = hollow_path
                hollow_path.prev = end
            return head

    def _create_hollow_tree(self):
        head = self._create_deadend('inside hollow tree',False)
        fork = ComplexNode(hollow_tree_fork,'inside hollow tree')
        hollow_end1 = RegularNode(hollow_tree_end1,'hollow tree end1')
        hollow_end2 = RegularNode(hollow_tree_end2,'hollow tree end2')
        current = head
        while current.next != None:
            current = current.next
        current.next = fork
        fork.prev = current
        left = self._create_deadend('inside hollow tree',False)
        right = self._create_deadend('inside hollow tree',False)
        current1 = left
        current2 = right
        side = random.choice([True,False])
        while current1.next != None:
            current1 = current1.next
        while current2.next != None:
            current2 = current2.next
        if side:
            current1.next = hollow_end1
            hollow_end1.prev = current1
            current2.next = hollow_end2
            hollow_end2.prev = current2
        else:
            current1.next = hollow_end2
            hollow_end2.prev = current1
            current2.next = hollow_end1
            hollow_end1.prev = current2
        fork.left = left
        left.prev = fork
        fork.right = right
        right.prev = fork
        return head
    
    def print_forest(self):
        self._print_node(self.head, "", True)

    def _print_node(self, node, prefix, is_tail):
        if isinstance(node, RegularNode):
            print(prefix + ("└── " if is_tail else "├── ") + f"RegularNode {node.node_type}")
            if node.next:
                self._print_node(node.next, prefix + ("    " if is_tail else "│   "), True)
        elif isinstance(node, ComplexNode):
            print(prefix + ("└── " if is_tail else "├── ") + "ComplexNode")
            if node.left:
                self._print_node(node.left, prefix + ("    " if is_tail else "│   "), False)
            if node.right:
                self._print_node(node.right, prefix + ("    " if is_tail else "│   "), True)
            if node.prev and node.prev.next != node:
                self._print_node(node.prev.next, prefix, is_tail)


def generate():
    forest_gen = ForestGenerator(regular_node_images, special_images)
    forest_gen.generate_forest()
    forest_gen.print_forest()
    return forest_gen
