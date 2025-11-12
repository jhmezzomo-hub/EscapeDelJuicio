import pygame
import sys
import random
import os

# === INICIALIZACIÓN ===
pygame.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaxy Attack - Sala Final")

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
laser_direcciones_img = pygame.image.load(os.path.join(ruta_img, "lasers", "laser_direcciones.png")).convert_alpha()
laser_chiquito_img = pygame.image.load(os.path.join(ruta_img, "lasers", "laser_chiquito.png")).convert_alpha()
alerta_img = pygame.image.load(os.path.join(ruta_img, "lasers", "alerta.png")).convert_alpha()

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
        self.image = nave_img
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 80))
        self.velocidad = 7
        self.vidas = 3
        self.power = None
        self.power_tiempo = 0
        self.laser_auto_timer = 0
        self.laser_grande = None
        self.tiempo_ultimo_dano = 0  # cooldown de daño

    def recibir_dano(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_dano > 1000:  # 1 segundo invulnerable
            self.vidas -= 1
            self.tiempo_ultimo_dano = ahora

    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

        # Control del poder de tiempo
        if self.power:
            if pygame.time.get_ticks() - self.power_tiempo > self.power["duracion"]:
                self.power = None
                if self.laser_grande:
                    self.laser_grande.kill()
                    self.laser_grande = None

        # Disparo automático
        if self.power and self.power["tipo"] == "auto":
            ahora = pygame.time.get_ticks()
            if ahora - self.laser_auto_timer > 200:
                self.laser_auto_timer = ahora
                bala = Bala(self.rect.centerx, self.rect.top, direccion=-1)
                grupo_balas.add(bala)

        # Actualizar posición del láser grande si está activo
        if self.laser_grande:
            self.laser_grande.rect.midbottom = self.rect.midtop


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion=-1):
        super().__init__()
        self.image = pygame.transform.scale(laser_chiquito_img, (60, 90))
        self.image = pygame.transform.rotate(self.image, 0 if direccion == -1 else 180)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.velocidad = 8 * direccion

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill()


class LaserGrandeJugador(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.image_original = pygame.transform.scale(laser_grande_img, (180, ALTO))
        self.image = self.image_original.copy()
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(midbottom=jugador.rect.midtop)
        self.jugador = jugador
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 2000  # 2 segundos

    def update(self):
        self.rect.midbottom = self.jugador.rect.midtop
        if pygame.time.get_ticks() - self.tiempo_inicio > self.duracion:
            self.kill()
            self.jugador.laser_grande = None


class LaserGrandeBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_original = pygame.transform.scale(laser_grande_img, (180, ALTO))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(midtop=(x, y - 20))
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
                self.tiempo_inicio = pygame.time.get_ticks()
        elif self.estado == "disparando":
            if tiempo_transcurrido >= self.duracion_disparo:
                self.kill()

    def hace_dano(self):
        return self.estado == "disparando"


class LaserDireccionalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = pygame.transform.scale(laser_direcciones_img, (100, 400))
        self.image = pygame.transform.rotate(self.image, direccion)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 7
        self.direccion = direccion
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 3000

    def update(self):
        if self.direccion == 90:
            self.rect.x += self.velocidad
        elif self.direccion == -90:
            self.rect.x -= self.velocidad
        if pygame.time.get_ticks() - self.tiempo_inicio > self.duracion:
            self.kill()


class CirculoPoder(pygame.sprite.Sprite):
    def __init__(self, tipo, imagen):
        super().__init__()
        self.image = pygame.transform.scale(imagen, (80, 80))
        self.rect = self.image.get_rect(midtop=(random.randint(100, ANCHO - 100), -50))
        self.tipo = tipo
        self.velocidad = 3

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect(center=(ANCHO // 2, 100))
        self.vida_max = 1000
        self.vida = self.vida_max
        self.velocidad = 3
        self.direccion = 1
        self.tiempo_disparo = 0
        self.tiempo_ataque = 0
        self.estado = "normal"
        self.ultimo_poder = "laser_direccional"
        self.atacando = False

    def update(self):
        if self.estado == "normal" and not self.atacando:
            self.rect.x += self.velocidad * self.direccion
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.direccion *= -1

    def preparar_ataque(self, tipo):
        self.estado = tipo
        self.tiempo_ataque = 60
        self.atacando = True
        self.velocidad = 0

    def ejecutar_ataque(self, grupo_lasers):
        if self.ultimo_poder == "laser_grande":
            # alterna a direccional
            laser_izq = LaserDireccionalBoss(self.rect.centerx, self.rect.bottom, -90)
            laser_der = LaserDireccionalBoss(self.rect.centerx, self.rect.bottom, 90)
            grupo_lasers.add(laser_izq, laser_der)
            self.ultimo_poder = "laser_direccional"
        else:
            # alterna a grande
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


# === CREAR SPRITES ===
jugador = Nave()
boss = Boss()

grupo_jugador = pygame.sprite.GroupSingle(jugador)
grupo_balas = pygame.sprite.Group()
grupo_boss = pygame.sprite.GroupSingle(boss)
grupo_balas_boss = pygame.sprite.Group()
grupo_lasers_boss = pygame.sprite.Group()
grupo_poderes = pygame.sprite.Group()
grupo_laser_jugador = pygame.sprite.Group()


# === BUCLE PRINCIPAL ===
def iniciar_galaxy_attack():
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

        jugador.update(teclas)
        boss.update()
        grupo_balas.update()
        grupo_balas_boss.update()
        grupo_lasers_boss.update()
        grupo_poderes.update()
        grupo_laser_jugador.update()

        # === Spawnear poderes ===
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

        # === IA del Boss ===
        if boss.estado == "normal":
            boss.tiempo_disparo += 1
            if boss.tiempo_disparo % 42 == 0:
                boss.disparar_chico(grupo_balas_boss)
            if boss.tiempo_disparo > 240:
                boss.tiempo_disparo = 0
                boss.preparar_ataque("alerta_laser")

        elif "alerta" in boss.estado:
            boss.tiempo_ataque -= 1
            if boss.tiempo_ataque <= 0:
                boss.estado = "laser"
                boss.ejecutar_ataque(grupo_lasers_boss)
        elif boss.estado == "quieto":
            boss.tiempo_ataque -= 1
            if boss.tiempo_ataque <= 0:
                boss.continuar()

        # === Colisiones ===
        if pygame.sprite.spritecollide(jugador, grupo_balas_boss, True):
            jugador.recibir_dano()

        for laser in grupo_lasers_boss:
            # Láser grande
            if hasattr(laser, "hace_dano") and laser.hace_dano() and jugador.rect.colliderect(laser.rect):
                jugador.recibir_dano()
                break
            # Láser direccional
            elif isinstance(laser, LaserDireccionalBoss) and jugador.rect.colliderect(laser.rect):
                jugador.recibir_dano()
                break

        for bala in grupo_balas:
            if pygame.sprite.spritecollide(bala, grupo_boss, False):
                boss.vida -= 10
                bala.kill()

        for laser in grupo_laser_jugador:
            if pygame.sprite.spritecollide(boss, grupo_laser_jugador, False):
                boss.vida -= 2
                break

        col_poder = pygame.sprite.spritecollide(jugador, grupo_poderes, True)
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

        # === Derrota o victoria ===
        if jugador.vidas <= 0:
            en_juego = False
        if boss.vida <= 0:
            en_juego = False

        # === Dibujar ===
        pantalla.blit(fondo, (0, 0))
        grupo_balas.draw(pantalla)
        grupo_balas_boss.draw(pantalla)
        grupo_lasers_boss.draw(pantalla)
        grupo_poderes.draw(pantalla)
        grupo_laser_jugador.draw(pantalla)
        grupo_jugador.draw(pantalla)
        grupo_boss.draw(pantalla)
        dibujar_vidas(jugador.vidas)
        dibujar_barra_boss(boss.vida, boss.vida_max)
        pygame.display.flip()

    # Pantalla final
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 80)
    texto = "¡VICTORIA!" if boss.vida <= 0 else "GAME OVER"
    color = (0, 255, 0) if boss.vida <= 0 else (255, 0, 0)
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, ALTO // 2 - render.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    iniciar_galaxy_attack()
