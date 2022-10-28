class Node:
    def __init__(self, nm_id, name):
        self.nm_id = nm_id
        self.name = name
        self.colleagues_dict = {}
        self.number_of_edges = self.get_number_of_edges
    
   
    def add_colleagus(self, colleague_list, movie):
        for i in colleague_list:
            if i.name != self.name:
                self.colleagues_dict[i.name] = movie.title
    
    def get_colleagus_name(self): 
        return_list = []   
        for key, val in self.colleagues_dict:
            return_list.append((key, val))
        return return_list
          
    def get_number_of_edges(self):
        return len(self.colleagues_dict)

class Movie:

    def __init__(self, tt_id, title, rating):
        self.tt_id = tt_id
        self.title = title
        self.rating = rating
        self.actors = []
        
    def __str__(self):
        return self.title

    def add_actors(self, actor):
        self.actors.append(actor)

    def get_actors(self):
        return self.actors

    def add_edges(self):
        for i in self.actors:
            i.add_colleagus(self.actors, self)

class Graph:
    def __init__(self):
        self.graph = {}            # node_object --> {node_object : movie_object}
        self.actor_dict = {}       # node_object name --> {node_object}
        self.movie_dict = {}       # movie_object tt_id --> {movie_object}   
        self.number_of_edges_total = self.get_number_of_edges_total()
        self.number_of_actors_total = 0

              
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
            self.number_of_actors_total += 1

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

    
    def DFS(self, nm_id_start, nm_id_end):
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
                        print("Korteste sti = ")
                        for i in new_path:
                            print(i.name)
                        return
                visited.append(node)
        print("Ingen stier funnet")
        return
        
                     
                          
    #Hjelpe-metode
    def test_print_movie(self):
        for key, val in self.movie_dict.items():
            print(key.name, " : ", val.get_actors())

    #Printer ut grafen
    def print_pretty_graph(self):
        for key, val in self.actor_dict.items():
            print(key, " <---------> ", val)

    def print_graph(self):
        for key, val in self.graph.items():
            print(key.name, " <---------> ", val.name)

    def get_number_of_edges_total(self):
        list = []
        for i in self.actor_dict:
            list.append(self.actor_dict[i].get_number_of_edges())
        return sum(list)


    def print_numbers(self):
        print("--------------------------------------------------------------")
        print("Number of nodes: " + str(self.number_of_actors_total))
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
    g.print_numbers()
    #print(g.DFS("nm0000288", "nm0001401"))

  
main()
    
    



