import pygame
import sys
import time
import random

# --- Configuración ---
pygame.init()
ANCHO, ALTO = 1100, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Code Master: Edition Gold")

# Colores y Estética
FONDO = (10, 12, 20)
PANEL_CODIGO = (22, 25, 33)
TEXTO_COLOR = (171, 178, 191)
ROBOT_COLOR = (0, 200, 255)
META_COLOR = (0, 255, 120)
ESTRELLA_COLOR = (255, 215, 0)
PARTICULA_COLOR = (255, 255, 255)

fuente_puntos = pygame.font.SysFont("Impact", 30)
fuente_main = pygame.font.SysFont("Consolas", 16)

class Robot:
    def __init__(self):
        self.x, self.y = 50, 50
    def reset(self, pos):
        self.x, self.y = pos

class Particula:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-10, -2)
        self.vida = 255
    def mover(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 5

# --- Variables Globales del Jugador ---
puntos_totales = 0
nivel_idx = 0
estrellas_por_nivel = [0] * 12
particulas = []
robot = Robot()

# Niveles (Misma estructura anterior)
niveles = [
    {"reto": "Mueve a la derecha (450px)", "pista": "robot.x += 450", "meta": (500, 300), "pos": (50, 300)},
    {"reto": "Sube el robot (200px)", "pista": "robot.y -= 200", "meta": (50, 100), "pos": (50, 300)},
    {"reto": "Usa un bucle while", "pista": "while robot.x < 500: robot.x += 1", "meta": (500, 300), "pos": (50, 300)},
    # ... (agrega los demás niveles aquí)
]

codigo_usuario = [""]
linea_activa = 0
error_msg = ""
consola_y = ALTO

def calcular_estrellas(lineas_codigo):
    if lineas_codigo <= 3: return 3
    if lineas_codigo <= 6: return 2
    return 1

def celebrar():
    global particulas
    for _ in range(50):
        particulas.append(Particula(550, 350))

def ejecutar_script():
    global error_msg, consola_y, nivel_idx, puntos_totales
    robot.reset(niveles[nivel_idx]["pos"])
    
    # Limpiar líneas vacías para contar eficiencia
    lineas_reales = [l for l in codigo_usuario if l.strip()]
    
    try:
        locales = {"robot": robot}
        exec("\n".join(codigo_usuario), {"__builtins__": __builtins__}, locales)
        
        m = niveles[nivel_idx]["meta"]
        if abs(robot.x - m[0]) < 25 and abs(robot.y - m[1]) < 25:
            # ¡GANASTE EL NIVEL!
            estrellas = calcular_estrellas(len(lineas_reales))
            estrellas_por_nivel[nivel_idx] = estrellas
            puntos_totales += estrellas * 100
            error_msg = f"SUCCESS: +{estrellas * 100} PTS! ({estrellas} Estrellas)"
            celebrar()
            pygame.display.flip()
            time.sleep(1.5)
            nivel_idx = min(nivel_idx + 1, len(niveles)-1)
            reiniciar_nivel()
        else:
            error_msg = "LOGIC_ERROR: No llegaste a la meta."
            consola_y = ALTO - 120
    except Exception as e:
        error_msg = f"SYNTAX_ERROR: {str(e)}"
        consola_y = ALTO - 120

def reiniciar_nivel():
    global codigo_usuario, linea_activa, error_msg, consola_y
    robot.reset(niveles[nivel_idx]["pos"])
    codigo_usuario = [""]
    linea_activa = 0
    error_msg = ""
    consola_y = ALTO

# --- Bucle ---
reloj = pygame.time.Clock()
while True:
    pantalla.fill(FONDO)
    
    # Animación consola
    target_y = ALTO - 120 if error_msg else ALTO
    consola_y += (target_y - consola_y) * 0.1

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN:
            ctrl = pygame.key.get_pressed()[pygame.K_LCTRL]
            if ctrl and ev.key == pygame.K_s: ejecutar_script()
            if ctrl and ev.key == pygame.K_z: reiniciar_nivel()
            elif ev.key == pygame.K_RETURN:
                codigo_usuario.insert(linea_activa + 1, ""); linea_activa += 1
            elif ev.key == pygame.K_BACKSPACE:
                if len(codigo_usuario[linea_activa]) > 0:
                    codigo_usuario[linea_activa] = codigo_usuario[linea_activa][:-1]
                elif linea_activa > 0:
                    codigo_usuario.pop(linea_activa); linea_activa -= 1
            elif ev.key == pygame.K_UP: linea_activa = max(0, linea_activa - 1)
            elif ev.key == pygame.K_DOWN: linea_activa = min(len(codigo_usuario)-1, linea_activa + 1)
            else:
                if ev.unicode.isprintable() and not ctrl:
                    codigo_usuario[linea_activa] += ev.unicode

    # --- DIBUJAR UI ---
    # Barra de Progreso Superior
    progreso_ancho = (nivel_idx + 1) * (700 // len(niveles))
    pygame.draw.rect(pantalla, (40, 40, 60), (0, 0, 700, 5))
    pygame.draw.rect(pantalla, META_COLOR, (0, 0, progreso_ancho, 5))

    # Puntos y Estrellas
    pantalla.blit(fuente_puntos.render(f"SCORE: {puntos_totales}", True, (255, 255, 255)), (20, 20))
    
    # Dibujar Estrellas del nivel actual
    for i in range(3):
        color = ESTRELLA_COLOR if i < estrellas_por_nivel[nivel_idx-1] else (50, 50, 50)
        pygame.draw.circle(pantalla, color, (300 + i*30, 40), 10)

    # Robot y Meta
    m = niveles[nivel_idx]["meta"]
    pygame.draw.rect(pantalla, META_COLOR, (m[0], m[1], 50, 50), 2)
    pygame.draw.rect(pantalla, ROBOT_COLOR, (robot.x, robot.y, 40, 40), border_radius=5)

    # Partículas de victoria
    for p in particulas[:]:
        p.mover()
        if p.vida <= 0: particulas.remove(p)
        else: pygame.draw.circle(pantalla, (255, 255, 0), (int(p.x), int(p.y)), 3)

    # Editor
    pygame.draw.rect(pantalla, PANEL_CODIGO, (700, 0, 400, ALTO))
    for i, l in enumerate(codigo_usuario):
        if i == linea_activa: pygame.draw.rect(pantalla, (40, 45, 60), (705, 50+i*22, 390, 22))
        pantalla.blit(fuente_main.render(l, True, TEXTO_COLOR), (715, 52+i*22))

    # Consola
    pygame.draw.rect(pantalla, (20, 20, 30), (0, consola_y, ANCHO, 120))
    pantalla.blit(fuente_main.render(error_msg, True, (255, 100, 100)), (20, consola_y + 40))

    pygame.display.flip()
    reloj.tick(60)