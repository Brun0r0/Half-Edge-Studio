from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import * 

class Janela_OpenGL(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.estrutura = None
        self.window_w = 800
        self.window_h = 600
        self.bbox_inicial = None

        self.pos_x = 0
        self.pos_y = 0
        self.escala = 0

    def set_estrutura(self, estrutura):
        self.estrutura = estrutura
        self.bbox = self.compute_bbox(estrutura)
        self.bbox_inicial = self.bbox 

        self.after(10, self.redraw)

    def initgl(self):
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # Função que utilizo para calcular o bounding box e fazer todas estrutura caber na tela
    def compute_bbox(self, estrutura):
        xs = [v.getCoords()[0] for v in estrutura.vertices]
        ys = [v.getCoords()[1] for v in estrutura.vertices]

        return (min(xs), max(xs), min(ys), max(ys))
    
    # Converte coordenadas do mundo real para coordenadas de tela
    def world_to_screen(self, x, y):
        if self.bbox is None:
            return (int(x), int(y))

        minx, maxx, miny, maxy = self.bbox
        # prevenir divisão por zero
        ret_x = maxx - minx if maxx - minx != 0 else 1.0
        ret_y = maxy - miny if maxy - miny != 0 else 1.0
        # Margem para evitar que a estrutura fique junta da borda
        margin = 0.3
        sx = (x - minx) / ret_x
        sy = (y - miny) / ret_y
        # manter aspecto
        sx = margin + sx * (1 - 2*margin)
        sy = margin + sy * (1 - 2*margin)
        screen_x = int(sx * (self.window_w - 1))
        screen_y = int(sy * (self.window_h - 1))
        return screen_x, screen_y
    
    # Utilizei o algoritmo de Bresenham's como passado no vídeo
    def desenharSegmento(self, x1, y1, x2, y2):
        if(abs(x2-x1) > abs(y2-y1)):
            self.desenharSegmentoH(x1, y1, x2, y2)
        else:
            self.desenharSegmentoV(x1, y1, x2, y2)
    
    def desenharSegmentoH(self, x1, y1, x2, y2):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1

        dir = -1 if dy < 0 else 1
        dy *= dir

        glBegin(GL_LINES)

        if dx != 0:
            y = y1
            p = 2*dy - dx
            for i in range(dx+1):
                glVertex2f(x1+i, y)
                
                if p >= 0:
                    y += dir
                    p = p - 2*dx
                p = p + 2*dy

        glEnd()

    def desenharSegmentoV(self, x1, y1, x2, y2):
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1

        dir = -1 if dx < 0 else 1
        dx *= dir

        glBegin(GL_LINES)

        if dy != 0:
            x = x1
            p = 2*dx - dy
            for i in range(dy+1):
                glVertex2f(x, y1 + i)
                
                if p >= 0:
                    x += dir
                    p = p - 2*dy
                p = p + 2*dx

        glEnd()
    
    # Desenha todas as arestas da estrutura
    def desenhar_tudo(self):

        glColor3f(1,1,1)
        glPointSize(1)
        drawn = set()

        for he in self.estrutura.half_edges:
            # Evitar desenhar a mesma aresta duas vezes
            twin = he.twin
            if twin:
                key = tuple(sorted((he.start.id, he.end.id)))
                if key in drawn:
                    continue
                drawn.add(key)
            else:
                key = (he.start.id, he.end.id)
                if key in drawn:
                    continue
                drawn.add(key)

            x1w, y1w = he.start.getCoords()
            x2w, y2w = he.end.getCoords()

            x1, y1 = self.world_to_screen(x1w, y1w)
            x2, y2 = self.world_to_screen(x2w, y2w)

            self.desenharSegmento(x1, y1, x2, y2)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        if self.estrutura:
            self.window_w = self.width
            self.window_h = self.height
            self.desenhar_tudo()

        glFlush()