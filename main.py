import pygame
import os
import sys

# --- COMPATIBILIDAD CON RI ---
# Si el RI inyectó la ruta, la usamos; si no, buscamos la de por defecto
if 'RI_ASSETS' not in globals():
    RI_ASSETS = os.path.join(os.getenv('APPDATA'), "MiGranJuego", "assets")

def iniciar_juego():
    pygame.init()
    
    # Configuración de la ventana
    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Ventana Cargada desde GitHub")
    
    # Colores
    COLOR_FONDO = (30, 30, 30) # Gris oscuro
    
    reloj = pygame.time.Clock()
    corriendo = True
    
    print("🚀 Ventana de Pygame abierta con éxito.")

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        # Dibujo
        pantalla.fill(COLOR_FONDO)
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# Ejecución automática al ser cargado por el RI
if __name__ == "__main__":
    iniciar_juego()
else:
    iniciar_juego()