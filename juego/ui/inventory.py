# juego/ui/inventory.py
import pygame
from dataclasses import dataclass
from typing import Optional, List, Tuple

SLOT_SIZE = 64
SLOT_PADDING = 8

@dataclass
class Item:
    type: str
    count: int = 1
    max_stack: int = 1
    color: Tuple[int,int,int] = (200,200,200)
    image: Optional[pygame.Surface] = None   # sprite opcional (Surface)

Slot = Optional[Item]

def clone_item(it: Item) -> Item:
    # copia los valores; la Surface se comparte (no es necesario duplicarla)
    return Item(type=it.type, count=it.count, max_stack=it.max_stack, color=it.color, image=it.image)

class Inventory:
    """
    Clase modular de inventario.
    Uso:
      inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40,40))
      inv.handle_event(event)
      inv.update(dt)
      inv.draw(surface)
    """
    def __init__(self, rows=1, cols=8, quickbar_slots=8, pos=(40,40)):
        # estado
        self.rows = rows
        self.cols = cols
        self.pos = pos
        self.inventory_slots: List[Slot] = [None] * (rows * cols)
        self.quickbar: List[Slot] = [None] * quickbar_slots
        self.held_item: Optional[Item] = None
        self.held_from = None
        self.is_open = False
        self.context_menu = None

        # asegurar fonts inicializadas (por si crean Inventory antes de pygame.init)
        if not pygame.get_init():
            # no inicializamos todo; dejamos que el main llame a pygame.init() normalmente,
            # pero si alguien instanció antes, intentamos inicializar el módulo de fuentes.
            try:
                pygame.init()
            except Exception:
                pass
        if not pygame.font.get_init():
            pygame.font.init()

        # fuentes/colores
        self.font = pygame.font.SysFont(None, 16)
        self.bigfont = pygame.font.SysFont(None, 20, bold=True)
        self.SLOT_BG = (36,37,41)
        self.SLOT_BORDER = (70,70,78)
        self.HIGHLIGHT = (120,170,255)
        self.TOOLTIP_BG = (12,12,12)
        self.TOOLTIP_BORDER = (200,200,200)

        # demo (puedes quitar/editar esto)
        # self.inventory_slots[0] = clone_item(Item("sword",1,1,(200,200,200), image=None))
        # self.inventory_slots[1] = clone_item(Item("potion",5,20,(172,64,255), image=None))

    # --- rect helpers ---
    def get_inventory_slot_rect(self, index:int) -> pygame.Rect:
        x0,y0 = self.pos
        r = index // self.cols
        c = index % self.cols
        x = x0 + c * (SLOT_SIZE + SLOT_PADDING)
        y = y0 + r * (SLOT_SIZE + SLOT_PADDING)
        return pygame.Rect(x,y,SLOT_SIZE,SLOT_SIZE)

    def get_quickbar_slot_rect(self, index:int) -> pygame.Rect:
        x0,y0 = self.pos
        y = y0 + self.rows * (SLOT_SIZE + SLOT_PADDING) + 24
        x = x0 + index * (SLOT_SIZE + SLOT_PADDING)
        return pygame.Rect(x,y,SLOT_SIZE,SLOT_SIZE)

    def slot_at_pos(self, pos:Tuple[int,int]):
        for i in range(len(self.inventory_slots)):
            if self.get_inventory_slot_rect(i).collidepoint(pos):
                return (False, i)
        for i in range(len(self.quickbar)):
            if self.get_quickbar_slot_rect(i).collidepoint(pos):
                return (True, i)
        return (None, None)

    def merge_or_move(self, src_item:Item, dst_item:Slot, split=False):
        if dst_item is None:
            if split and src_item.count > 1:
                taken = src_item.count // 2
                src_item.count -= taken
                new = clone_item(src_item)
                new.count = taken
                return (src_item if src_item.count>0 else None, new)
            else:
                return (None, src_item)
        if dst_item.type == src_item.type and dst_item.max_stack > 1:
            free = dst_item.max_stack - dst_item.count
            to_move = src_item.count // 2 if split and src_item.count>1 else src_item.count
            moved = min(to_move, free)
            dst_item.count += moved
            src_item.count -= moved
            if src_item.count <= 0:
                return (None, dst_item)
            else:
                return (src_item, dst_item)
        # swap
        return (dst_item, src_item)

    # --- events ---
    def handle_event(self, event):
        # tecla I abre/cierra inventario (si querés otra tecla cambialo)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            self.is_open = not self.is_open
            # cancelar contextmenu al alternar
            self.context_menu = None
            return

        if not self.is_open:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            left = event.button == 1
            right = event.button == 3
            pos = event.pos
            is_q, idx = self.slot_at_pos(pos)
            shift = pygame.key.get_mods() & pygame.KMOD_SHIFT

            if left and is_q is not None:
                source = self.quickbar if is_q else self.inventory_slots
                if source[idx] is not None:
                    if shift and source[idx].count > 1:
                        taken = source[idx].count // 2
                        source[idx].count -= taken
                        self.held_item = clone_item(source[idx])
                        self.held_item.count = taken
                        self.held_from = (is_q, idx)
                        if source[idx].count <= 0:
                            source[idx] = None
                    else:
                        self.held_item = source[idx]
                        self.held_from = (is_q, idx)
                        source[idx] = None

            elif right and is_q is not None:
                arr = self.quickbar if is_q else self.inventory_slots
                if arr[idx] is not None:
                    self.context_menu = {'pos': pos, 'slot':(is_q, idx), 'options': ['Usar','Equipar','Dividir mitad','Tirar']}

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.held_item is not None:
            pos = event.pos
            is_q, idx = self.slot_at_pos(pos)
            split = pygame.key.get_mods() & pygame.KMOD_SHIFT
            if is_q is not None:
                dest = self.quickbar if is_q else self.inventory_slots
                dst_item = dest[idx]
                remaining, new_dst = self.merge_or_move(self.held_item, dst_item, split=bool(split))
                dest[idx] = new_dst
                if remaining is None:
                    self.held_item = None
                    self.held_from = None
                else:
                    self.held_item = remaining
                    if self.held_from:
                        src_q, src_idx = self.held_from
                        src_arr = self.quickbar if src_q else self.inventory_slots
                        if src_arr[src_idx] is None:
                            src_arr[src_idx] = self.held_item
                            self.held_item = None
                            self.held_from = None
            else:
                # soltado fuera -> devolver al origen si es posible, si no intentar primero slot vacío
                if self.held_from:
                    src_q, src_idx = self.held_from
                    src_arr = self.quickbar if src_q else self.inventory_slots
                    if src_arr[src_idx] is None:
                        src_arr[src_idx] = self.held_item
                    else:
                        for i in range(len(self.inventory_slots)):
                            if self.inventory_slots[i] is None:
                                self.inventory_slots[i] = self.held_item
                                break
                self.held_item = None
                self.held_from = None

    def update(self, dt):
        # placeholder para animaciones/timers si los necesitás
        pass

    # --- drawing ---
    def draw_slot(self, surface:pygame.Surface, rect:pygame.Rect, item:Slot, highlight=False):
        pygame.draw.rect(surface, self.SLOT_BG, rect, border_radius=8)
        pygame.draw.rect(surface, self.SLOT_BORDER, rect, width=2, border_radius=8)
        if highlight:
            pygame.draw.rect(surface, self.HIGHLIGHT, rect, width=3, border_radius=8)
        if item:
            inner = rect.inflate(-8, -8)
            # fondo del item (color)
            pygame.draw.rect(surface, item.color, inner, border_radius=6)

            # Si el item tiene imagen, escalar y blitearla centrada
            if getattr(item, "image", None):
                img = item.image
                iw, ih = img.get_size()
                max_w, max_h = inner.width, inner.height
                scale = min(max_w / iw, max_h / ih, 1.0)
                new_w, new_h = int(iw * scale), int(ih * scale)
                img_s = pygame.transform.smoothscale(img, (new_w, new_h))
                img_rect = img_s.get_rect(center=inner.center)
                surface.blit(img_s, img_rect)

            # contador de pila en la esquina inferior derecha
            if item.max_stack > 1:
                cnt_surf = self.font.render(str(item.count), True, (255,255,255))
                surface.blit(cnt_surf, (rect.right - 6 - cnt_surf.get_width(), rect.bottom - 6 - cnt_surf.get_height()))

    def draw(self, surface:pygame.Surface):
        if not self.is_open:
            return

        # dibujar grid
        for i in range(len(self.inventory_slots)):
            r = self.get_inventory_slot_rect(i)
            is_q, idx = self.slot_at_pos(pygame.mouse.get_pos())
            hl = (is_q is False and idx == i)
            self.draw_slot(surface, r, self.inventory_slots[i], highlight=hl)

        # dibujar quickbar
        for i in range(len(self.quickbar)):
            r = self.get_quickbar_slot_rect(i)
            is_q, idx = self.slot_at_pos(pygame.mouse.get_pos())
            hl = (is_q is True and idx == i)
            self.draw_slot(surface, r, self.quickbar[i], highlight=hl)

        # dibujar held_item que sigue al mouse (sin letra)
        if self.held_item:
            mx,my = pygame.mouse.get_pos()
            draw_rect = pygame.Rect(mx - SLOT_SIZE//2, my - SLOT_SIZE//2, SLOT_SIZE, SLOT_SIZE)
            pygame.draw.rect(surface, self.SLOT_BG, draw_rect, border_radius=8)
            inner = draw_rect.inflate(-8, -8)
            pygame.draw.rect(surface, self.held_item.color, inner, border_radius=6)
            if getattr(self.held_item, "image", None):
                img = self.held_item.image
                iw, ih = img.get_size()
                max_w, max_h = inner.width, inner.height
                scale = min(max_w / iw, max_h / ih, 1.0)
                new_w, new_h = int(iw * scale), int(ih * scale)
                img_s = pygame.transform.smoothscale(img, (new_w, new_h))
                img_rect = img_s.get_rect(center=inner.center)
                surface.blit(img_s, img_rect)
            if self.held_item.max_stack > 1:
                cnt_surf = self.font.render(str(self.held_item.count), True, (255,255,255))
                surface.blit(cnt_surf, (draw_rect.right - 6 - cnt_surf.get_width(), draw_rect.bottom - 6 - cnt_surf.get_height()))
