# Neste arquivo é aplicada a lógica estrutural do half-edge e 
# contém as funções demandadas no enunciado para visualização 
# das estruturas pela lógica do half-edge.

from core import half_edge_estrutura

def criar_estrutura_half_edge(conteudo_obj):
    estruturaObjeto = half_edge_estrutura.HalfEdgeStructure()

    for linha in conteudo_obj:
        linhaAtual = linha.strip().split()

        if not linhaAtual:
            continue

        if(linhaAtual[0] == 'v'):
            x = float(linhaAtual[1])
            y = float(linhaAtual[2])
            estruturaObjeto.add_vertex(x, y)
            
        elif(linhaAtual[0] == 'f'):
            indices = []
            for i in range(1, len(linhaAtual)):
                indices.append(int(linhaAtual[i].split('/')[0]) - 1)

            if(len(indices) >= 3):  
                vertices_face = [estruturaObjeto.vertices[idx] for idx in indices]
                estruturaObjeto.criar_face_poligonal(vertices_face)

    return estruturaObjeto

def visualizar_estrutura_half_edge(estrutura):

    estrutura_text = "Vertices:\n"
    for v in estrutura.vertices:
        estrutura_text +=f"\tID: {v.id}, Coords: {v.getCoords()}\n"

    estrutura_text += "\nHalf-Edges:\n"
    for he in estrutura.half_edges:
        twin_id = he.twin.id if he.twin else None
        face_id = he.face.id if he.face else None
        next_id = he.next.id if he.next else None
        prev_id = he.prev.id if he.prev else None
        estrutura_text += f"\tID: {he.id}, Start: {he.start.id}, End: {he.end.id}, Face: {face_id}, Next: {next_id}, Prev: {prev_id}, Twin: {twin_id}\n"

    estrutura_text += "\nFaces:\n"
    for f in estrutura.faces:
        half_edge_id = f.half_edge.id if f.half_edge else None
        estrutura_text += f"\tID: {f.id}, Half-Edge: {half_edge_id}\n"

    return estrutura_text

def listar_faces_adjacentes_face(estrutura, face_id):
    face = estrutura.faces[face_id]
    if not face:
        print(f"Face com ID {face_id} não encontrada")
        return
    
    print(f"Faces adjacentes à face {face_id}:")
    start_he = face.getHalfEdge()
    he = start_he
    visited_faces = set()
    while True:
        twin = he.getTwin()
        if twin and twin.getFace() and twin.getFace().id not in visited_faces:
            visited_faces.add(twin.getFace().id)
            print(f"\tFace ID: {twin.getFace().id}")
        he = he.getNext()
        if he == start_he:
            break

def listar_faces_adjacentes_aresta(estrutura, half_edge_id):
    he = estrutura.half_edges[half_edge_id]
    if not he:
        print(f"Half-edge com ID {half_edge_id} não encontrada")
        return
    
    print(f"Faces adjacentes à half-edge {half_edge_id}:")
    if he.getFace():
        print(f"\tFace ID: {he.getFace().id}")
    twin = he.getTwin()
    if twin and twin.getFace():
        print(f"\tFace ID: {twin.getFace().id}")


def listar_faces_compartilham_vertice(estrutura, vertex_id):
    vertices = estrutura.vertices[vertex_id]
    if not vertices:
        print(f"Vértice com ID {vertex_id} não encontrado")
        return
    
    print(f"Faces que compartilham o vértice {vertex_id}:")
    start_he = vertices.getHalfEdge()
    he = start_he
    visited_faces = set()
    while True:
        if he.getFace() and he.getFace().id not in visited_faces:
            visited_faces.add(he.getFace().id)
            print(f"\tFace ID: {he.getFace().id}")
        twin = he.getTwin()
        if twin:
            he = twin.getNext()
        else:
            break
        if he == start_he:
            break

def listar_arestas_compartilham_vertice(estrutura, vertex_id):
    vertices = estrutura.vertices[vertex_id]
    if not vertices:
        print(f"Vértice com ID {vertex_id} não encontrado")
        return
    
    arestas_encontradas = []
    
    print(f"Arestas que compartilham o vértice {vertex_id}:")

    for he in estrutura.half_edges:
        if he.start.id == vertex_id or he.end.id == vertex_id:
            arestas_encontradas.append(he)

    arestas_unicas = []
    arestas_processadas = set()

    for he in arestas_encontradas:
        edge_key =  tuple(sorted([he.start.id, he.end.id]))

        if edge_key not in arestas_processadas:
            arestas_processadas.add(edge_key)
            arestas_unicas.append(he)

    for he in arestas_unicas:
        print(f"\tHalf-Edge ID: {he.id} (Start: {he.start.id}, End: {he.end.id})")