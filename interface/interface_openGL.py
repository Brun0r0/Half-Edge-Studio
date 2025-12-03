from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLU import * 

class Janela_OpenGL(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.estruturas = []
        self.window_w = 800
        self.window_h = 600
        self.margin = 0.3
        self.algDesenho = True  # True = Bresenham, False = Wu
        self.bbox = None

    def set_estrutura(self, estrutura):
        self.estruturas.append(estrutura)
        self.bbox = self.compute_bbox(self.estruturas)

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

    def set_algoritmo(self, algoritmo):
        # True = Bresenham, False = Wu
        self.algDesenho = algoritmo 

    # Função que utilizo para calcular o bounding box e fazer todas estrutura caber na tela
    def compute_bbox(self, estrutura):
        xs = []
        ys = []
        
        for estrutura in self.estruturas:
            for v in estrutura.vertices:
                x, y = v.getCoords()
                xs.append(x)
                ys.append(y)

        # Calcular os valores mínimos e máximos de uma vez
        xs_minimo, xs_maximo = min(xs), max(xs)
        ys_minimo, ys_maximo = min(ys), max(ys)

        return xs_minimo, xs_maximo, ys_minimo, ys_maximo
    
    # Converte coordenadas do mundo real para coordenadas de tela
    def world_to_screen(self, x, y):
        if self.bbox is None:
            return 0, 0

        minx, maxx, miny, maxy = self.bbox
        # prevenir divisão por zero
        ret_x = maxx - minx if maxx - minx != 0 else 1.0
        ret_y = maxy - miny if maxy - miny != 0 else 1.0
        
        sx = (x - minx) / ret_x
        sy = (y - miny) / ret_y
        # manter aspecto
        sx = self.margin + sx * (1 - 2*self.margin)
        sy = self.margin + sy * (1 - 2*self.margin)
        screen_x = int(sx * (self.window_w - 1))
        screen_y = int(sy * (self.window_h - 1))
        return screen_x, screen_y
    
    # Utilizei o algoritmo de Bresenham's como passado no vídeo
    def desenharSegmento(self, x1, y1, x2, y2):
        if self.algDesenho:
            # Bresenham
            if(abs(x2-x1) > abs(y2-y1)):
                self.desenharSegmentoH(x1, y1, x2, y2)
            else:
                self.desenharSegmentoV(x1, y1, x2, y2)
        else:
            # Wu
            self.desenharSegmentoWu(x1, y1, x2, y2)
        
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

    def desenharSegmentoWu(self, x1, y1, x2, y2):

        def putPixel(x, y, opacidade):
            glColor4f(r, g, b, opacidade)
            glVertex2f(x, y)

        r, g, b, _ = glGetFloatv(GL_CURRENT_COLOR)
        glBegin(GL_POINTS)
        

        if abs(y2 - y1) < abs(x2 - x1):
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
        
            dx = x2 - x1
            dy = y2 - y1
            m = dy/dx


            overlap = 1 - ((x1 + 0.5) - int(x1 + 0.5))
            distStart = y1 - int(y1)
            putPixel(int(x1 + 0.5), int(y1), (1-distStart) * overlap)
            putPixel(int(x1 + 0.5), int(y1) + 1, distStart * overlap)

            overlap = 1 - ((x1 - 0.5) - int(x1 - 0.5))
            distEnd = y1 - int(y1)
            putPixel(int(x1 + 0.5), int(y1), (1-distStart) * overlap)
            putPixel(int(x1 + 0.5), int(y1) + 1, distStart * overlap)

            for i in range(1, round(dx+0.5)):
                y = y1 + i * m
                ix = int(x1 + i)
                iy = int(y)
                dist = y - iy
                putPixel(ix, iy, 1 - dist)
                putPixel(ix, iy + 1, dist)
        
        else:
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            dx = x2 - x1
            dy = y2 - y1
            m = dx/dy

            overlap = 1 - ((y1 + 0.5) - int(y1 + 0.5))
            distStart = y1 - int(y1)
            putPixel(int(x1 + 0.5), int(y1), (1-distStart) * overlap)
            putPixel(int(x1 + 0.5), int(y1) + 0.5, distStart * overlap)

            overlap = ((y2 - 0.5) - int(y2 - 0.5))
            distEnd = y2 - int(y2)
            putPixel(int(x2), int(y2 + 0.5), (1-distEnd) * overlap)
            putPixel(int(x2) + 1, int(y2 + 0.5), distEnd * overlap)

            for i in range(1, round(dy+0.5)):
                x = x1 + i * m
                ix = int(x)
                iy = int(y1 + i)
                dist = x - ix
                putPixel(ix, iy, 1 - dist)
                putPixel(ix + 1, iy, dist)

        glEnd()
    
    # Desenha todas as arestas da estrutura
    def desenhar_tudo(self):
        glColor3f(1,1,1)
        glPointSize(1)
        drawn = set()

        for idx_estrutura, estrutura in enumerate(self.estruturas):
            for he in estrutura.half_edges:
                twin = he.twin
                if twin:
                    key = tuple(sorted((
                        (idx_estrutura, he.start.id), 
                        (idx_estrutura, he.end.id)
                    )))
                    if key in drawn:
                        continue
                    drawn.add(key)
                else:
                    key = (idx_estrutura, he.start.id, he.end.id)
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
        
        if self.estruturas:
            self.window_w = self.width
            self.window_h = self.height
            self.desenharEixos()
            self.desenhar_tudo()


        glFlush()

    def desenharEixos(self):
        glColor3f(1, 0, 0)
        if self.bbox:
            _, y_center = self.world_to_screen(0, 0)
            self.desenharSegmento(0, y_center, self.window_w - 1, y_center)
            
            x_center, _ = self.world_to_screen(0, 0)
            self.desenharSegmento(x_center, 0, x_center, self.window_h - 1)