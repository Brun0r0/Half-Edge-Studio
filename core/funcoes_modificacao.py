import math

def modificar_estrutura(estrutura, tx=0, ty=0, sx=1, sy=1, cis_x=0, cis_y=0, angulo = 0):

    for vertex in estrutura.vertices:
        x, y = vertex.getCoords()

        x, y = escalar_ponto(x, y, sx, sy)

        x, y = rotacionar_ponto(x, y, angulo)
        x, y = cisalhar_ponto(x, y, cis_x, cis_y)

        x, y = transladar_ponto(x, y, tx, ty)

        vertex.setCoords(x, y)

def calcular_centro(estrutura):
    if not estrutura.vertices:
        return 0, 0
    
    xs = [v.getCoords()[0] for v in estrutura.vertices]
    ys = [v.getCoords()[1] for v in estrutura.vertices]

    return (
        (max(xs) + min(xs)) / 2,
        (max(ys) + min(ys)) / 2
    )

def transladar_ponto(x, y, tx, ty):

    trans_x = x + tx
    trans_y = y + ty

    return trans_x, trans_y

def escalar_ponto(x, y, sx, sy):

    esc_x = x * sx
    esc_y = y * sy

    return esc_x, esc_y

def reflex_ponto(estrutura, eixo):

    sinal_x = 0
    sinal_y = 0

    if eixo == 'x':
        sinal_x = -1
        sinal_y = 1
    else:
        sinal_x = 1
        sinal_y = -1

    for vertex in estrutura.vertices:
        x, y = vertex.getCoords()

        reflex_x = x * sinal_x
        reflex_y = y * sinal_y

        vertex.setCoords(reflex_x, reflex_y)

def cisalhar_ponto(x, y, sh_x, sh_y):

    x_cis = x + sh_x * y
    y_cis = y + sh_y * x

    return x_cis, y_cis

def rotacionar_ponto(x, y, angulo_graus):

    # Converter ângulo de graus para radianos
    angulo_rad = math.radians(angulo_graus)
    
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)
    
    x_rot = x * cos_a - y * sin_a
    y_rot = x * sin_a + y * cos_a
    
    return x_rot, y_rot