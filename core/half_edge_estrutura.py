# Nesse arquivo estão as funções responsáveis por criar a 
# estrutura do half-edge, com a adição de vértices, half-edges e faces.

from core.estruturas_base import Vertex, HalfEdge, Face

# Classe para representar a estrutura half-edge e seus métodos de criação e busca
class HalfEdgeStructure:

    def __init__(self):
        self.vertices = []
        self.half_edges = []
        self.faces = []

        # Dicionário para busca rápida de half-edges por seus vértices
        self.edge_dict = {}

    def add_vertex(self, x, y):
        new_vertex = Vertex(x, y)
        new_vertex.id = len(self.vertices)
        self.vertices.append(new_vertex)
    
    def criar_half_edge(self, start: Vertex, end: Vertex):
        new_half_edge = HalfEdge(start, end)
        new_half_edge.id = len(self.half_edges)
        self.half_edges.append(new_half_edge)

        key = (start.id, end.id)
        self.edge_dict[key] = new_half_edge

        twin_key = (end.id, start.id)
        possivel_twin = self.edge_dict.get(twin_key)

        if possivel_twin and possivel_twin.twin is None:
            new_half_edge.setTwin(possivel_twin)
            possivel_twin.setTwin(new_half_edge)

        return new_half_edge

    def buscar_half_edge(self, v_start: Vertex, v_end: Vertex):
        key = (v_start.id, v_end.id)
        return self.edge_dict.get(key, None)

    def criar_face_poligonal(self, vertices_list):
        if(len(vertices_list) < 3):
            raise ValueError("Faces precisam de no mínimo 3 vértices")
        
        face = Face()
        face.setId(len(self.faces))

        half_edges_face = []

        for i in range(len(vertices_list)):
            v_start =  vertices_list[i]
            v_end = vertices_list[(i+1) % len(vertices_list)]

            he = self.buscar_half_edge(v_start, v_end)
            if he is None:
                he = self.criar_half_edge(v_start, v_end)

            half_edges_face.append(he)

        for i in range(len(half_edges_face)):
            current_he = half_edges_face[i]
            next_he = half_edges_face[(i+1) % len(half_edges_face)]
            prev_he = half_edges_face[i-1]

            current_he.setNext(next_he)
            current_he.setPrev(prev_he)
            current_he.setFace(face)

        face.setHalfEdge(half_edges_face[0])

        for i, vertices in enumerate(vertices_list):
            if not vertices.getHalfEdge():
                vertices.setHalfEdge(half_edges_face[i])

        self.faces.append(face)
        return face