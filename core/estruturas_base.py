# Nesse arquivo estão as classes base para a estrutura utilizada
# no half-edge: vértice, half-edge(aresta) e face.
#   Lógica bem básica, um construtor e getters/setters 
#   para completar as informações após a criação dos objetos.

class Vertex:
    def __init__(self, x, y):
        self.coords = (x, y)
        self.half_edge = None
        self.id = None

    def getCoords(self):
        return self.coords
    
    def setCoords(self, x, y):
        self.coords = (x, y)

    def getHalfEdge(self):
        return self.half_edge
    
    def setHalfEdge(self, half_edge):
        self.half_edge = half_edge

class HalfEdge:
    def __init__(self, start: Vertex, end: Vertex):
        self.start = start
        self.end = end
        self.face = None
        self.next = None
        self.prev = None
        self.twin = None
        self.id = None

    def getFace(self):
        return self.face
    
    def setFace(self, face):
        self.face = face

    def getNext(self):
        return self.next
    
    def setNext(self, next):
        self.next = next

    def getPrev(self):
        return self.prev
    
    def setPrev(self, prev):
        self.prev = prev

    def getTwin(self):
        return self.twin
    
    def setTwin(self, twin):
        self.twin = twin
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

class Face:
    def __init__(self):
        self.half_edge = None
        self.id = None

    def getHalfEdge(self):
        return self.half_edge
    
    def setHalfEdge(self, half_edge):
        self.half_edge = half_edge

    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id