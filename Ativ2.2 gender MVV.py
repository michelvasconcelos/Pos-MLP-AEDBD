import random
import uuid


class Person(object):

    def __init__(self, uid, s_type):
        self._uid = uid
        self._s_type = s_type

    def get_uid(self):
        return self._uid
    
    def get_s_type(self):
        return self._s_type


class FriendNetwork(object):

    def __init__(self, people_num, connections_num):
        self._people_num = people_num
        self._connections_num = connections_num
        self._graph = self._generate_graph()

    def _generate_graph(self):

        people = []
        for person_index in range(self._people_num):
            uid = str(uuid.uuid4())
            s_type = 'female' if person_index < (self._people_num // 2)  else 'male'
            people.append(Person(uid, s_type))

        conn_num = 0
        graph = {}
        graph_aux = {} # criando um grafo auxiliar para agilizar algumas buscas
        while conn_num < self._connections_num:
            person, friend = random.sample(people, 2)
            person_uid = person.get_uid()
            friend_uid = friend.get_uid()

            if person_uid not in graph:
                graph[person_uid] = {
                    'this': person,
                    'friends': []
                }
                # criando um índice auxiliar para os vizinhos de cada vértice inserido no grafo
                graph_aux[person_uid] = {}

            if friend_uid not in graph:
                graph[friend_uid] = {
                    'this': friend,
                    'friends': []
                }
                # criando um índice auxiliar para os vizinhos de cada vértice inserido no grafo
                graph_aux[friend_uid] = {} 

            # if person_uid == friend_uid or \
            #     friend in graph[person_uid]['friends']: # fazer essa verificação em um índice auxiliar
            #     continue
            if person_uid == friend_uid or \
                friend_uid in graph_aux[person_uid]: # fazer essa verificação em um índice auxiliar
                continue

            graph[person_uid]['friends'].append(friend)
            graph[friend_uid]['friends'].append(person)
            # adicionar vizinho também nos índices do grafo auxiliar
            graph_aux[person_uid][friend_uid] = True
            graph_aux[friend_uid][person_uid] = True
            conn_num += 1

        people_to_remove = []
        for person_uid in graph:
            friends_types = [*map(lambda p: p.get_s_type(), graph[person_uid]['friends'])]
            person_type = graph[person_uid]['this'].get_s_type()
            if ('male' not in friends_types or 'female' not in friends_types) and person_type in friends_types:
                people_to_remove.append({'person_uid': person_uid, 'remove_from': graph[person_uid]['friends']})

        for person_props in people_to_remove:
            for friend in person_props['remove_from']:
                person_index = [*map(lambda friend: friend.get_uid(),
                    graph[friend.get_uid()]['friends'])].index(person_props['person_uid'])
                del graph[friend.get_uid()]['friends'][person_index]
            del graph[person_props['person_uid']]

        return graph
    
    def get_person_by_uid(self, uid):
        return self._graph[uid]['this']

    def _search(self, person_uid, friend_uid):

        queue = [[person_uid]]
        visited = set()

        while queue:
            path = queue.pop(0)
            vertex = path[-1]
            if vertex == friend_uid:
                return path
            elif vertex not in visited:
                for current_neighbour in self._graph[vertex].get('friends', []):
                    #a = current_neighbour._uid
                    new_path = list(path)
                    if current_neighbour._s_type != self._graph[vertex]['this']._s_type:
                        new_path.append(current_neighbour._uid)
                        queue.append(new_path)
                visited.add(vertex)
        return path  

    def get_separation_degree(self):
       
        total_paths_len = 0
        for _ in range(100):
            person_uid, friend_uid = random.sample([*self._graph.keys()], 2)
            path = self._search(person_uid, friend_uid)
            total_paths_len += len(path) - 1

        return total_paths_len / 100

if __name__ == '__main__':

    friend_network = FriendNetwork(100, 500)
    separation_degree = friend_network.get_separation_degree()
    print(separation_degree)
