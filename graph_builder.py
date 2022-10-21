
class Node:
    def __init__(self, mn_id, name, movie_list):
        self.mn_id = mn_id
        self.name = ' '.join([str(item) for item in name])
        self.movie_list = movie_list

    def __str__(self):
        #return f"Id: {self.mn_id}  Name: {self.name}   Movies: {self.movie_list}"
        return self.name

    def compareMovies(self, other):
        for m in other.movie_list:
            if m in self.movie_list:
                return m
        return False


class Movie:
    def __init__(self, tt_id, title, rating):
        self.tt_id = tt_id
        self.title = ' '.join([str(item) for item in title])
        self.rating = float(' '.join([str(item) for item in rating]))

    def __str__(self):
        #return f"Id: {self.tt_id}  Titlee: {self.title}   Rating: {self.rating}"
        return self.title
        
class Graph:
    def __init__(self):
        self.graph = dict()
        self.actor_node_list = []
        self.movie_dict = {}
        self.number_of_egdes = 0
    
    #Oppretter kanter mellom noder
    def _addEdges(self):
        for i in range(len(self.actor_node_list)):
            for j in range(i + 1, len(self.actor_node_list)):
                if self.actor_node_list[i].compareMovies(self.actor_node_list[j]) != False:
                    movie = self.actor_node_list[i].compareMovies(self.actor_node_list[j])
                    self.graph[self.actor_node_list[i]].append((self.actor_node_list[j].name, self.movie_dict.get(movie).rating))
                    self.graph[self.actor_node_list[j]].append((self.actor_node_list[i].name, self.movie_dict.get(movie).rating))
                    self.number_of_egdes += 1
                    
    #Leser skuespiller-fil
    def read_actor_file(self, filename):
        for lines in open(filename):
            lines = lines.strip()
            data = lines.split()
            data_lenght = len(data)
            mn_id = data[0]
            
            for i in range(data_lenght):
                new_list = []
                name_list = data[1:data_lenght]
                for i in name_list:
                    if i[0] != 't':
                        new_list.append(i)
        
            for i in range(data_lenght):
                tt_id_list = data[3:data_lenght]
                for i in tt_id_list:
                    if i[0] != 't':
                        tt_id_list.remove(i)

            movie_star = Node(mn_id, new_list, tt_id_list)
            if movie_star not in self.graph:
                self.graph[movie_star] = []
            if movie_star not in self.actor_node_list:
                self.actor_node_list.append(movie_star)
        
        self._addEdges()

    #Leser film-fil
    def read_movie_file(self, filename):
        for lines in open(filename):
            lines = lines.strip()
            data = lines.split()
            data_lenght = len(data)
            tt_id = data[0]

            for i in range(data_lenght):
                title = []
                rating = []
                name_list = data[1:data_lenght]
                for j in name_list:
                    if j[0].isdigit() == False:
                        title.append(j)
                    elif j[0].isdigit() and len(j) < 4:
                        rating.append(j)
                
            movie = Movie(tt_id, title, rating)
            if movie not in self.movie_dict:
                self.movie_dict[tt_id] = movie
                   
                    
    #Skriver ut grafen
    def printGraph(self):
        for keys, values in self.graph.items():
            print(keys, " <------> ", values)

    def print_numbers(self):
        print("Number of nodes: " + str(len(self.actor_node_list)))
        print("Number of egdes: " + str(self.number_of_egdes))
                    

def main():
    g = Graph()

    g.read_movie_file("movies.tsv")
    g.read_actor_file("actors.tsv")
    g.print_numbers()
  

main()
    
    



