import pygame, sys, random, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.pantalla.pantalla_victoria import pantalla_victoria
from juego.pantalla.pantalla_muerte import pantalla_fin
from juego.controlador.cargar_config import get_config_sala
config = get_config_sala("general")
ANCHO, ALTO = 1100,600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escape Del Juicio")

clock = pygame.time.Clock()

# === RUTAS ===
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_img = os.path.join(ruta_base, "..", "..", "img")

# === CARGAR IMÁGENES ===
fondo = pygame.image.load(os.path.join(ruta_img, "Fondos", "fondo_final.png")).convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

nave_img = pygame.image.load(os.path.join(ruta_img, "mc", "messi.png")).convert_alpha()
nave_img = pygame.transform.scale(nave_img, (70, 70))

boss_img = pygame.image.load(os.path.join(ruta_img, "saw", "saw.png")).convert_alpha()
boss_img = pygame.transform.scale(boss_img, (150, 150))

corazon_img = pygame.image.load(os.path.join(ruta_img, "mc", "corazones.png")).convert_alpha()
corazon_img = pygame.transform.scale(corazon_img, (40, 40))

laser_grande_img = pygame.image.load(os.path.join(ruta_img, "lasers", "laser_grande.png")).convert_alpha()
laser_chiquito_img = pygame.image.load(os.path.join(ruta_img, "lasers", "laser_chiquito.png")).convert_alpha()

alerta_img = pygame.image.load(os.path.join(ruta_img,  "lasers", "alerta.png")).convert_alpha()
alerta_img = pygame.transform.scale(alerta_img, (80, 80))

# === CÍRCULOS DE PODER ===
ruta_poderes = os.path.join(ruta_img, "poderes")
circulo_auto_img = pygame.image.load(os.path.join(ruta_poderes, "circulo_laser_automatico.png")).convert_alpha()
circulo_grande_img = pygame.image.load(os.path.join(ruta_poderes, "circulo_laser_grande.png")).convert_alpha()
circulo_doble_img = pygame.image.load(os.path.join(ruta_poderes, "circulo_laser_doble.png")).convert_alpha()

# === COLORES ===
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)


# === CLASES ===
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nave_img.copy()  # Crear copia independiente
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 80))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidad = 7
        self.vidas = 3
        self.power = None
        self.power_tiempo = 0
        self.laser_auto_timer = 0
        self.laser_grande = None
        self.tiempo_ultimo_dano = 0
        # Sistema de invulnerabilidad visual
        self.invulnerable = False
        self.duracion_invulnerabilidad = 1000  # 1 segundo
        self.alpha_original = 255
        self.alpha_parpadeo = 100

    def recibir_dano(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_dano > self.duracion_invulnerabilidad:
            self.vidas -= 1
            self.tiempo_ultimo_dano = ahora
            self.invulnerable = True

    def update(self, teclas, grupo_balas=None):
        # Manejar efecto visual de invulnerabilidad
        if self.invulnerable:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_ultimo_dano
            if tiempo_transcurrido >= self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.image.set_alpha(self.alpha_original)  # Restaurar opacidad normal
            else:
                # Efecto de parpadeo rápido (cada 100ms)
                parpadeo_intervalo = 100
                ciclo = (tiempo_transcurrido // parpadeo_intervalo) % 2
                alpha = self.alpha_parpadeo if ciclo == 0 else self.alpha_original
                self.image.set_alpha(alpha)
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

        if self.power:
            if pygame.time.get_ticks() - self.power_tiempo > self.power["duracion"]:
                self.power = None
                if self.laser_grande:
                    self.laser_grande.kill()
                    self.laser_grande = None

        if self.power and self.power["tipo"] == "auto" and grupo_balas is not None:
            ahora = pygame.time.get_ticks()
            if ahora - self.laser_auto_timer > 200:
                self.laser_auto_timer = ahora
                bala = Bala(self.rect.centerx, self.rect.top, direccion=-1)
                grupo_balas.add(bala)

        if self.laser_grande:
            self.laser_grande.rect.midbottom = self.rect.midtop


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion=-1):
        super().__init__()
        self.image = pygame.transform.scale(laser_chiquito_img, (30, 50))
        self.image = pygame.transform.rotate(self.image, 0 if direccion == -1 else 180)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidad = 8 * direccion

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill()


class LaserGrandeJugador(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.image_original = pygame.transform.scale(laser_grande_img, (120, ALTO))
        self.image = self.image_original.copy()
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(midbottom=jugador.rect.midtop)
        self.mask = pygame.mask.from_surface(self.image)
        self.jugador = jugador
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 2000

    def update(self):
        self.rect.midbottom = self.jugador.rect.midtop
        if pygame.time.get_ticks() - self.tiempo_inicio > self.duracion:
            self.kill()
            self.jugador.laser_grande = None


class LaserGrandeBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = pygame.transform.scale(laser_grande_img, (120, ALTO))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(midtop=(x, y - 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_alpha(50)
        self.estado = "cargando"
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion_carga = 1000
        self.duracion_disparo = 500

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio

        if self.estado == "cargando":
            alpha = 50 + int((tiempo_transcurrido / self.duracion_carga) * (220 - 50))
            self.image.set_alpha(min(alpha, 220))
            if tiempo_transcurrido >= self.duracion_carga:
                self.estado = "disparando"
                self.image.set_alpha(255)
                # Actualizar máscara cuando el alfa cambia significativamente
                self.mask = pygame.mask.from_surface(self.image)
                self.tiempo_inicio = pygame.time.get_ticks()
        elif self.estado == "disparando":
            if tiempo_transcurrido >= self.duracion_disparo:
                self.kill()

    def hace_dano(self):
        return self.estado == "disparando"


class CirculoPoder(pygame.sprite.Sprite):
    def __init__(self, tipo, imagen):
        super().__init__()
        self.image = pygame.transform.scale(imagen, (80, 80))
        self.rect = self.image.get_rect(midtop=(random.randint(100, ANCHO - 100), -50))
        self.mask = pygame.mask.from_surface(self.image)
        self.tipo = tipo
        self.velocidad = 3

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


class AlertaLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, duracion=1000):
        super().__init__()
        self.image = alerta_img
        self.rect = self.image.get_rect(midtop=(x, y))
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = duracion

    def update(self):
        if pygame.time.get_ticks() - self.tiempo_inicio > self.duracion:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img.copy()  # Crear copia independiente
        self.rect = self.image.get_rect(center=(ANCHO // 2, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.vida_max = 1000
        self.vida = self.vida_max
        self.velocidad = 3
        self.direccion = 1
        self.tiempo_disparo = 0
        self.tiempo_ataque = 0
        self.estado = "normal"
        self.ultimo_poder = "laser_grande"
        self.atacando = False
        # Efecto visual de parpadeo (sin invulnerabilidad)
        self.parpadeando = False
        self.tiempo_ultimo_hit = 0
        self.duracion_parpadeo = 500  # 0.5 segundos de parpadeo visual
        self.alpha_original = 255
        self.alpha_parpadeo = 100

    def update(self):
        # Manejar efecto visual de parpadeo cuando recibe daño
        if self.parpadeando:
            tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_ultimo_hit
            if tiempo_transcurrido >= self.duracion_parpadeo:
                self.parpadeando = False
                self.image.set_alpha(self.alpha_original)  # Restaurar opacidad normal
            else:
                # Efecto de parpadeo rápido (cada 80ms)
                parpadeo_intervalo = 80
                ciclo = (tiempo_transcurrido // parpadeo_intervalo) % 2
                alpha = self.alpha_parpadeo if ciclo == 0 else self.alpha_original
                self.image.set_alpha(alpha)
        
        if self.estado == "normal" and not self.atacando:
            self.rect.x += self.velocidad * self.direccion
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.direccion *= -1

    def recibir_hit_visual(self):
        """Activa el efecto visual de parpadeo cuando recibe daño"""
        self.parpadeando = True
        self.tiempo_ultimo_hit = pygame.time.get_ticks()

    def preparar_ataque(self, tipo):
        self.estado = tipo
        self.tiempo_ataque = 60
        self.atacando = True
        self.velocidad = 0

    def ejecutar_ataque(self, grupo_lasers):
        laser = LaserGrandeBoss(self.rect.centerx, self.rect.bottom - 100)
        grupo_lasers.add(laser)
        self.ultimo_poder = "laser_grande"
        self.estado = "quieto"
        self.tiempo_ataque = 120

    def continuar(self):
        self.estado = "normal"
        self.velocidad = 3
        self.atacando = False

    def disparar_chico(self, grupo_balas_boss):
        bala = Bala(self.rect.centerx, self.rect.bottom - 10, direccion=1)
        grupo_balas_boss.add(bala)


# === FUNCIONES AUXILIARES ===
def dibujar_vidas(vidas):
    for i in range(vidas):
        pantalla.blit(corazon_img, (10 + i * 45, 10))


def dibujar_barra_boss(vida_actual, vida_max):
    ancho_barra = 300
    alto_barra = 25
    x = ANCHO - ancho_barra - 20
    y = 20
    ratio = vida_actual / vida_max
    pygame.draw.rect(pantalla, ROJO, (x, y, ancho_barra, alto_barra))
    pygame.draw.rect(pantalla, (int((1 - ratio) * 255), int(ratio * 255), 0),
                     (x, y, ancho_barra * ratio, alto_barra))
    pygame.draw.rect(pantalla, BLANCO, (x, y, ancho_barra, alto_barra), 2)


# === BUCLE PRINCIPAL ===
def iniciar_sala7():
    # === CREAR SPRITES (dentro de la función para reiniciar estado) ===
    jugador = Nave()
    boss = Boss()

    grupo_jugador = pygame.sprite.GroupSingle(jugador)
    grupo_balas = pygame.sprite.Group()
    grupo_boss = pygame.sprite.GroupSingle(boss)
    grupo_balas_boss = pygame.sprite.Group()
    grupo_lasers_boss = pygame.sprite.Group()
    grupo_poderes = pygame.sprite.Group()
    grupo_laser_jugador = pygame.sprite.Group()
    grupo_alertas = pygame.sprite.Group()

    en_juego = True
    ultimo_poder_spawn = pygame.time.get_ticks()

    while en_juego:
        clock.tick(60)
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                if jugador.power and jugador.power["tipo"] == "doble":
                    bala1 = Bala(jugador.rect.centerx - 20, jugador.rect.top, -1)
                    bala2 = Bala(jugador.rect.centerx + 20, jugador.rect.top, -1)
                    grupo_balas.add(bala1, bala2)
                elif not jugador.power or jugador.power["tipo"] != "auto":
                    bala = Bala(jugador.rect.centerx, jugador.rect.top, -1)
                    grupo_balas.add(bala)

        jugador.update(teclas, grupo_balas)
        boss.update()
        grupo_balas.update()
        grupo_balas_boss.update()
        grupo_lasers_boss.update()
        grupo_poderes.update()
        grupo_laser_jugador.update()
        grupo_alertas.update()

        ahora = pygame.time.get_ticks()
        if ahora - ultimo_poder_spawn > 5000:
            ultimo_poder_spawn = ahora
            tipo = random.choice(["auto", "grande", "doble"])
            if tipo == "auto":
                poder = CirculoPoder("auto", circulo_auto_img)
            elif tipo == "grande":
                poder = CirculoPoder("grande", circulo_grande_img)
            else:
                poder = CirculoPoder("doble", circulo_doble_img)
            grupo_poderes.add(poder)

        if boss.estado == "normal":
            boss.tiempo_disparo += 1
            if boss.tiempo_disparo % 42 == 0:
                boss.disparar_chico(grupo_balas_boss)
            if boss.tiempo_disparo > 240:
                boss.tiempo_disparo = 0
                boss.preparar_ataque("alerta_laser")

        elif "alerta" in boss.estado:
            boss.tiempo_ataque -= 1
            if boss.tiempo_ataque == 59:
                alerta = AlertaLaser(boss.rect.centerx, boss.rect.bottom + 10)
                grupo_alertas.add(alerta)
            if boss.tiempo_ataque <= 0:
                boss.estado = "laser"
                boss.ejecutar_ataque(grupo_lasers_boss)

        elif boss.estado == "quieto":
            boss.tiempo_ataque -= 1
            if boss.tiempo_ataque <= 0:
                boss.continuar()

        # Colisión jugador con balas del boss usando máscaras
        for bala in grupo_balas_boss:
            if pygame.sprite.collide_mask(jugador, bala):
                jugador.recibir_dano()
                bala.kill()

        # Colisión jugador con láser del boss usando máscaras
        for laser in grupo_lasers_boss:
            if hasattr(laser, "hace_dano") and laser.hace_dano() and pygame.sprite.collide_mask(jugador, laser):
                jugador.recibir_dano()
                break

        # Colisión balas del jugador con boss usando máscaras
        for bala in grupo_balas:
            if pygame.sprite.collide_mask(bala, boss):
                boss.vida -= 10
                boss.recibir_hit_visual()  # Activar efecto visual
                bala.kill()

        # Colisión láser grande del jugador con boss usando máscaras
        hit_laser = False
        for laser in grupo_laser_jugador:
            if pygame.sprite.collide_mask(laser, boss):
                boss.vida -= 2
                hit_laser = True
                break
        
        # Activar parpadeo solo una vez por frame si hay colisión con láser
        if hit_laser and not boss.parpadeando:
            boss.recibir_hit_visual()

        # Colisión jugador con círculos de poder usando máscaras
        col_poder = []
        for poder in grupo_poderes:
            if pygame.sprite.collide_mask(jugador, poder):
                col_poder.append(poder)
                poder.kill()
        for poder in col_poder:
            if poder.tipo == "auto":
                jugador.power = {"tipo": "auto", "duracion": 3000}
            elif poder.tipo == "grande":
                jugador.power = {"tipo": "grande", "duracion": 2000}
                laser = LaserGrandeJugador(jugador)
                grupo_laser_jugador.add(laser)
                jugador.laser_grande = laser
            elif poder.tipo == "doble":
                jugador.power = {"tipo": "doble", "duracion": 3000}
            jugador.power_tiempo = pygame.time.get_ticks()

        if jugador.vidas <= 0:
            en_juego = False
        if boss.vida <= 0:
            en_juego = False

        pantalla.blit(fondo, (0, 0))
        grupo_balas.draw(pantalla)
        grupo_balas_boss.draw(pantalla)
        grupo_lasers_boss.draw(pantalla)
        grupo_poderes.draw(pantalla)
        grupo_laser_jugador.draw(pantalla)
        grupo_alertas.draw(pantalla)
        grupo_jugador.draw(pantalla)
        grupo_boss.draw(pantalla)
        dibujar_vidas(jugador.vidas)
        dibujar_barra_boss(boss.vida, boss.vida_max)
        pygame.display.flip()

    # Manejar resultado del juego
    if boss.vida <= 0:
        resultado = pantalla_victoria()
        if resultado == 'replay':
            return 'sala7'  # Reiniciar sala 7
        elif resultado == 'menu_victoria':  # Cambio aquí
            return 'menu_victoria'  # Volver al menú desde victoria
        else:
            return None  # Salir del juego
    else:
        resultado = pantalla_fin()
        if resultado == 'replay':
            return 'sala7'  # Reiniciar sala 7
        elif resultado == 'menu':
            return 'inicio'  # Volver al menú principal
        else:
            return None  # Salir del juego


if __name__ == "__main__":
    iniciar_sala7()
