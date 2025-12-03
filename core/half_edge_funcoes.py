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
