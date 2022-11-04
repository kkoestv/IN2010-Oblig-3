from heapq import heappop, heappush
from collections import defaultdict, deque


class Node:
    def __init__(self, nm_id, name):
        self.nm_id = nm_id
        self.name = name
        self.colleagues_dict = {}
        self.number_of_edges = self.get_number_of_edges
        self.visited = False

    
    def add_colleagus(self, colleague_list, movie):
        for i in colleague_list:
            if i.name != self.name:
                self.colleagues_dict[i] = movie
    

    def get_colleagus_name(self): 
        return_list = []   
        for key, val in self.colleagues_dict:
            return_list.append((key, val))
        return return_list

          
    def get_number_of_edges(self):
        return len(self.colleagues_dict)


    def get_edge(self, other):
        return self.colleagues_dict[other].title + " (" + self.colleagues_dict[other].rating + ")"

    
    def calculate_weight(self, other):
        return 10 - self.colleagues_dict[other].get_rating()


    def __lt__(self, other):
        return True


class Movie:

    def __init__(self, tt_id, title, rating):
        self.tt_id = tt_id
        self.title = title
        self.rating = rating
        self.actors = []
        self.visited = set()
        

    def __str__(self):
        return self.title


    def add_actors(self, actor):
        self.actors.append(actor)


    def get_actors(self):
        return self.actors


    def add_edges(self):
        for i in self.actors:
            i.add_colleagus(self.actors, self)


    def get_rating(self):
        return float(self.rating)


class Graph:
    def __init__(self):
        self.graph = {}            # node_object --> {node_object : movie_object}
        self.actor_dict = {}       # node_object name --> {node_object}
        self.movie_dict = {}       # movie_object tt_id --> {movie_object}   
        #self.components_dict = {}  # 'component' int --> {node_object1, node_object2 ..}

    #Leser skuespiller-fil
    def read_actor_file(self, filename):
        lines = []
        with open(filename) as f:
            for line in f:
                l = line.strip().split('\t')
                lines.append(l)
        
        for data in lines:
            data_lenght = len(data)
            nm_id = data[0]
            name = data[1]
            movie_list = data[2:data_lenght]
            movie_obj_list = []

            actor = Node(nm_id, name)
            for movie in movie_list:
                if movie in self.movie_dict:
                    self.movie_dict[movie].add_actors(actor)
                    self.movie_dict[movie].add_edges()

            self.graph[actor] = actor.colleagues_dict
            self.actor_dict[name] = actor


    #Leser film-fil
    def read_movie_file(self, filename):
        lines = []
        with open(filename) as f:
            for line in f:
                l = line.strip().split('\t')
                lines.append(l)

        for data in lines:
            tt_id = data[0]
            title = data[1]
            rating = data[2]

            movie = Movie(tt_id, title, rating)
            self.movie_dict[tt_id] = movie

    

    def bfs(self, nm_id_start, nm_id_end):
        for key in self.graph.keys():
            if key.nm_id == nm_id_start:
                start_node = key
            if key.nm_id == nm_id_end:
                end_node = key
        
        visited = []
        queue = [[start_node]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in visited:
                neighbours = self.graph[node]

                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    if neighbour == end_node:
                        print(new_path[0].name)
                        for i in range(len(new_path) - 1):
                            print("====[ " + str(new_path[i].get_edge(new_path[i+1])) + " ] =====> " + str(new_path[i+1].name))
                        return
                visited.append(node)
        print("Ingen stier funnet")
        return



    def dijkstra(self, nm_id_start, nm_id_end):
        for key in self.graph.keys():
            if key.nm_id == nm_id_start:
                start_node = key 
            if key.nm_id == nm_id_end:
                end_node = key 
        
        queue , visited = [(0, start_node, [])] , set()
        while queue:
            cost, node , path = heappop(queue)
            if node not in visited:
                path = path + [node]
                visited.add(node)

                for (next, c) in self.graph[node].items():
                    heappush(queue, (cost + (node.calculate_weight(next)), next, path))

                if node == end_node:
                    print(path[0].name)
                    for i in range(len(path) - 1):
                        print("====[ " + str(path[i].get_edge(path[i+1])) + " ] =====> " + str(path[i+1].name)) 
                    print("Total weight: " + str(cost))
                    return


    def map_components(self, num):
        components_dict = {}  #Antall noder --> antall komponenter med node-antallet
        visited = set()
        for node in self.graph:
            num_nodes = self._bfs_visit(node, visited)
            if components_dict.get(num_nodes) != None:
                components_dict[num_nodes] += 1
            else:
                components_dict[num_nodes] = 1
        if components_dict.get(num) != None:
            print('There are ' + str(components_dict[num]) + ' of size ' + str(num))
        else:
            print('No components of that size')
             

    def _bfs_visit(self, node, visited):
        queue = deque([node])
        counter = 0

        while queue:
            n = queue.popleft()
            if n not in visited:
                counter += 1
                visited.add(n)
                for neighbour in self.graph[n]:
                    queue.append(neighbour)
        return counter


    def print_graph(self):
        for key, val in self.graph.items():
            print(key.name, " <---------> ", val)


    def get_number_of_edges_total(self):
        list = []
        for i in self.actor_dict:
            list.append(self.actor_dict[i].get_number_of_edges())
        return sum(list)


    def get_number_of_actors_total(self):
        return len(self.graph)



    def print_numbers(self):
        print("--------------------------------------------------------------")
        print("Number of nodes: " + str(self.get_number_of_actors_total()))
        print("Number of edges: " + str(self.get_number_of_edges_total()))
        print("--------------------------------------------------------------")



def main():
    g = Graph()

    #g.read_movie_file("marvel_movies.tsv")
    #g.read_actor_file("marvel_actors.tsv")
    g.read_movie_file("movies.tsv")
    g.read_actor_file("actors.tsv")
    #g.test_print_movie()
    #g.print_graph()
    #g.print_pretty_graph()
    #g.print_numbers()
    #print(g.BFS("nm2255973", "nm0000460"))
    #print(g.dijkstra2("nm2255973","nm0000460"))
    #g.find_num_components(10)
    #print(g.components)
    print(g.map_components(3))
    
    

  
main()
    
    
