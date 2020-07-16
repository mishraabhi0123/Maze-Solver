
import numpy as np 
import matplotlib.pyplot as plt 
from collections import deque
import time ,cv2

filename = 'maps/maze2.png'

class Node():
      def __init__(self, parent = None):
            self.position = np.array([])
            self.parent = parent
            self.children = []
            self.hn = 0
            self.gn = 0
            self.fn = 0


      def get_hn(self, method = 'euclid', goal = None):
            # print('calculating hn..',end = '    ')
            x,y = self.position
            hn = 0
            if method == 'manhatten':
                  hn = abs(goal[0] - x) + abs(goal[1] - y)
            elif method == 'euclid':
                  hn = np.sqrt((goal[0] - x)**2 + (goal[1] - y)**2)
            # print(hn)
            return hn


      def get_child_data(self):
            # print('getting children data..')
            global pixels_per_step, opened, closed
            #                AHEAD                 BACK                RIGHT                 LEFT
            moves = [[-pixels_per_step,0], [pixels_per_step,0], [0,pixels_per_step], [0,-pixels_per_step]]
            costs = [1,1,1,1]
            for move in moves:
                  position = self.position + np.array(move)
                  if possible(position):

                        child = Node(parent = self)
                        child.position = position
                        child.hn = child.get_hn(goal = goal_position)
                        child.gn = costs[moves.index(move)]
                        child.fn = child.hn + child.gn
                        self.children.append(child)
                        opened.append(child)
      
      
      def record_ancestor(self):
            # print('recording ancestors..')
            ancestors.clear()
            ancestors.append(self)
            node = self
            while node.parent != None:
                  ancestors.appendleft(node.parent)
                  node = node.parent

def possible(position):
      global closed
      x,y = int(position[0]), int(position[1])
      global image, closed
      possibilty = 1

      if y >= image.shape[0] or x >= image.shape[1] or x < 0 or y < 0 :
            possibilty = 0

      elif image[y,x] == 0:
            possibilty = 0

      else:
            possibilty = 1

      for node in closed:
            if node.position[0] == position[0] and node.position[1] == position[1]:
                  possibilty = 0
      return possibilty


def ALGORITHM(algo = "A-STAR", node = None):
      if algo == 'A-STAR':
            min_node = None
            min_fn = 100000
            for node in opened:
                  if node.fn  < min_fn:
                        min_fn = node.fn
                        min_node = node

            return min_node

      elif algo == 'BEST FIRST SEARCH':
            min_node = None
            min_hn = 100000
            for node in opened:
                  if node.hn  < min_hn:
                        min_hn = node.hn
                        min_node = node

            return min_node

      elif algo == 'HILL CLIMBING':
            try:
                  children = current_node.children
                  node = None
                  min_hn = children[0].hn 
                  for child in children:
                        if child.hn < min_hn:
                              min_hn = child.hn
                              node = child
                  return child
            
            except:
                  plt.title('Goal Not Reachable!')
                  time.sleep(3)
                  plt.close()
                  exit()
      
      elif algo == 'BFS':
            x = opened.popleft()
            opened.appendleft(x)
            return x

      elif algo == 'DFS':
            x = opened.pop()
            opened.append(x)
            return x
      
      elif algo == 'my_algo':
            # bidirectional best first search or a star 
            pass


def show_results():
      global image
      history = [[],[]]
      for node in ancestors:
            x = [node.position[0]]
            y = [node.position[1]]
            history[0].append(x)
            history[1].append(y)
            plt.cla()
            plt.imshow(image,cmap = 'gray')
            plt.plot(history[0],history[1],'r-', linewidth = 7)
            plt.plot(x,y,'bo')
            plt.title("Let's Go!")
            plt.show()
            plt.pause(0.001)

      plt.title('Done!')
      plt.pause(3)
      plt.close()


def start(goal, start):
      global opened,closed,ancestors,image,pixels_per_step, top
      node = top
      while len(opened):
            if np.linalg.norm(np.array(goal) - node.position) < np.max(image.shape)/50:
                  node.record_ancestor() 
                  show_results()
                  return 0
            plt.plot([node.position[0]],[node.position[1]],'b.')
            plt.show()
            plt.pause(0.001)
            node.record_ancestor()
            node.get_child_data()             
            node = ALGORITHM('A-STAR')
            opened.remove(node)
            closed.append(node)
      else:
            plt.title('Goal Not Found !')
            time.sleep(5)
            plt.close()

opened = deque()
closed = deque()
ancestors = deque()

image = plt.imread(filename,0)
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
image = image > 0.5
pixels_per_step = np.max(image.shape) / 40

num_click = 0
start_position = [0,0]
goal_position = [None, None]

def onclick(event):
      global num_click, start_position, goal_position
      num_click += 1

      if num_click == 1:

            start_position = [event.xdata, event.ydata]
            plt.plot([event.xdata], [event.ydata],'go')
            plt.title('Now, click to create a goal position!')

      if num_click == 2:

            goal_position = [event.xdata, event.ydata]
            plt.plot([event.xdata], [event.ydata],'ro')
            plt.title('Loading..')
      

plt.ion()
fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', onclick)
plt.imshow(image,cmap = 'gray')
plt.title('Click to create a start position!')
plt.show()
plt.pause(7)
plt.scatter([start_position[0],goal_position[0]],[start_position[1],goal_position[1]], c = ['g','r'])

top = Node(None)
top.position = start_position
top.hn = top.get_hn(method = 'euclid', goal = goal_position)
top.gn = 0
top.fn = top.hn + top.gn
opened.appendleft(top)
start(goal_position,start_position)
