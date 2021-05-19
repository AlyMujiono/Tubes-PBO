import pygame as pg  # MENGGUNAKAN FUNGSI IMPORT PYGAME 
import sys  # MENGGUNAKAN FUNGSI IMPORT SYS
import random  # MENGGUNAKAN FUNGSI IMPORT RANDOM


def tabrak(x1, y1, x2, y2, x3, y3, x4, y4):  # BENTUK YG DITABRAK (TEMBOK)
    if (x3+x4) > x1 > x3 and (y3+y4) > y1 > y3 or (x3+x4) > x2 > x3 and (y3+y4) > y2 > y3:
        return True
    else:
        return False


def tabrak2(x1, y1, x2, y2, x3, y3, x4, y4, size):  # BENTUK YG DITABRAK (MAKANANAN)
    if (x3+(11*size)) > x1 > x3-1 and (y3+(11*size)) > y1 > y3-1 or (x3+(11*size)) > x2 > x3-1 and (y3+(11*size)) > y2 > y3-1:
        return True
    else:
        return False


# BENTUK YG DITABRAK (DIRI ULERNYA SENDIRI)
def tabrak3(x1, y1, x2, y2, x3, y3, x4, y4, size):
    if (x3+(10*size)) > x1 > x3 and (y3+(10*size)) > y1 > y3 or (x3+(10*size)) > x2 > x3 and (y3+(10*size)) > y2 > y3:
        return True
    else:
        return False

class Makanan():  # CLASS MAKANAN
    def __init__(self, size):
        self.pos = [random.randrange(10, 780, 10),  # MAKANAN DIACAK
                    random.randrange(10, 430, 10)]  # MAKANAN DI DALAM PAPAN PERMAINAN
        self.gambar = pg.Surface((10*size, 10*size))  # UKURAN MAKANAN
        self.gambar.fill((255, 0, 0))  # WARNA MAKANAN MAKANAN


class Bonus():  # CLASS MAKANAN BONUS
    def __init__(self, size):
        self.pos = [random.randrange(10, 780, 10),  # MAKANAN DIACAK
                    random.randrange(10, 430, 10)]  # MAKANAN DI DALAM PAPAN PERMAINAN
        self.gambar = pg.Surface((15*size, 15*size))  # UKURAN MAKANAN
        self.gambar.fill((0, 0, 0))

class Ular():  # MEMBUAT CLASS SNAKE/ULAR
    def __init__(self, kecepatan, size):
        self.pos = [20, 20]  # POSISI AWAL SI ULAR
        self.gambar = pg.Surface((10*size, 10*size))  # KEPALA PUNYA ULAR
        self.gambar.fill((255, 255, 255))  # WARNA KEPALA ULAR
        self.kecepatan = kecepatan
        self.size = size
        self.gambar2 = []
        self.pos_akhir = [[20, 20]]
        self.arah = [0, 0]
        self.skor = 0
        self.banyakmakan = 0
        self.Makanan = Makanan(size)
        self.Bonus = Bonus(size)
        self.layar = pg.display.set_mode((800, 450))

    def kanan(self):  # ARAH KLIK KEKANAN
        self.arah = [self.kecepatan, 0]

    def kiri(self):  # ARAH KLIK KEKIRI
        self.arah = [-self.kecepatan, 0]

    def atas(self):  # ARAH KLIK KEATAS
        self.arah = [0, -self.kecepatan]

    def bawah(self):  # ARAH KLIK KEBAWAH
        self.arah = [0, self.kecepatan]

    def update(self):  # POSISI TERBARU
        if self.pos_akhir[-1] != self.pos:
            self.pos_akhir.append([self.pos[0], self.pos[1]])
        self.pos[0] += self.arah[0]
        self.pos[1] += self.arah[1]
        a = 1
        for x in self.gambar2:
            x[1] = self.pos_akhir[int(a*((-11*self.size)/self.kecepatan))]
            a += 1

    def periksa_tabrakan(self, x):  # PROSES TABRAKAN SAMA TEMBOK
        c = tabrak(self.pos[0], self.pos[1], self.pos[0]+10,
                   self.pos[1]+10, x[0], x[1], x[0]+10, x[1]+10)
        return c

    def periksa_makanan(self, x):  # PROSES TABRAKAN SAMA MAKANAN
        c = tabrak2(self.pos[0], self.pos[1], self.pos[0]+10,
                    self.pos[1]+10, x[0], x[1], x[0]+10, x[1]+10, self.size)
        return c

    def periksa_tabrakan2(self, x):  # PROSES TABRAKAN SAMA BADAN ULAR
        c = tabrak3(self.pos[0], self.pos[1], self.pos[0]+10,
                    self.pos[1]+10, x[0], x[1], x[0]+10, x[1]+10, self.size)
        return c

    def memakan(self):  # KETIKA MEMAKAN MAKANAN
        self.skor += 1  # PENAMBAHAN SKOR KALO ABIS MAKAN MAKANAN
        # UKURAN BADAN YANG DITAMBAHKAN
        self.banyakmakan += 1
        blok = pg.Surface((10*self.size, 10*self.size))
        blok.fill((0, 255, 0))  # WARNA PENAMBAHAN BADAN
        self.gambar2.append([blok, [10, 10]])  # PENAMBAHAN PANJANG ULAR

    def memakan_bonus(self):  # KETIKA MEMAKAN MAKANAN
        self.skor += 5  # PENAMBAHAN SKOR KALO ABIS MAKAN MAKANAN
        # UKURAN BADAN YANG DITAMBAHKAN
        blok = pg.Surface((10*self.size, 10*self.size))
        blok.fill((0, 255, 0))  # WARNA PENAMBAHAN BADAN
        self.gambar2.append([blok, [10, 10]])  # PENAMBAHAN PANJANG ULAR

    def banyak_makan(self):
        if self.periksa_makanan(self.Makanan.pos) == True:
            self.memakan()
            del self.Makanan
            self.Makanan = Makanan(self.size)
            if self.banyakmakan % 10 == 0:
                self.kecepatan += 0.05
        self.layar.blit(self.Makanan.gambar, self.Makanan.pos)

        if self.banyakmakan % 5 == 0 and self.banyakmakan != 0:
            if self.periksa_makanan(self.Bonus.pos) == True:
                self.memakan_bonus()
                del self.Bonus
                self.Bonus = Bonus(self.size)
            self.layar.blit(self.Bonus.gambar, self.Bonus.pos)

class Permainan():  # CLASS PERMAINAN
    def __init__(self, kecepatan, size=1):
        # UKURAN BACKGROUND WAKTU PERMAINAN DIMULAI
        self.layar = pg.display.set_mode((800, 450))
        pg.display.set_caption('Game Snake Optimus')
        self.Ular = Ular(kecepatan, size)
        self.blok2 = []
        self.skor = 0
        self.size = size
        self.kiri, self.kanan, self.atas, self.bawah = False, False, False, False
        self.hover = False
        self.click0 = False
        warna = (0, 0, 0)
        for x in range(0, 800, 10):  # UKURAN DINDING ATAS
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [x, 0]])
        for x in range(0, 800, 10):  # UKURAN DINDING BAWAH
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [x, 440]])
        for x in range(0, 450, 10):  # UKURAN DINDING KIRI
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [0, x]])
        for x in range(0, 450, 10):  # UKURAN DINDING KANAN
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [790, x]])

    def over(self):  # KETIKA PERMAINAN BERAKHIR
        while 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            for x in self.blok2:
                self.layar.blit(x[0], x[1])
            txts = pg.font.SysFont('Courier New', 40).render(
                'Game Berakhir    Skor:', True, (255, 255, 255))  # TAMPILAN KETIKA PERMAINAN SELESAI DENGAN FONT COURIER
            txtrect = txts.get_rect()
            # JARAK TULISAN POSISI DARI KIRI DAN ATAS
            txtrect.topleft = (20, 150)
            self.layar.blit(txts, txtrect)
            txts = pg.font.SysFont('Courier New', 50).render(
                str(self.Ular.skor), True, (255, 255, 255))  # UNTUK TAMPILAN NILAI SKOR
            txtrect = txts.get_rect()
            # JARAK TULISAN POSISI DARI KIRI DAN ATAS
            txtrect.topleft = (600, 150)
            self.layar.blit(txts, txtrect)
            pg.display.update()
            self.tombol((153, 300, 130, 50), 'Ulang Lagi', [  # JARAK DAN UKURAN (KIRI, ATAS, LEBAR, TINGGI)
                (255, 255, 255), (150, 150, 150)], action=lambda: ulang())
            if self.hover == True:
                click = pg.mouse.get_pressed()
                if click[0] == 1:
                    self.click0 = True
                if self.click0 == True:
                    if click[0] == 0:
                        self.tombol_klik()
                        self.click0 = False

    # PEMBUATAN TAMPILAN TOMBOL DAN KETIKA TOMBOL DI KLIK
    def tombol(self, pos, teks, warna, action=None, ukuran_teks=20):
        mouse = pg.mouse.get_pos()
        pos_akhir = pos
        rect = pg.Rect(pos)
        pos = rect.topleft
        rect.topleft = 0, 0
        persegi_panjang = pg.Surface(rect.size, pg.SRCALPHA)

        circle = pg.Surface([min(rect.size)*3]*2, pg.SRCALPHA)
        pg.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pg.transform.smoothscale(
            circle, [int(min(rect.size)*0.5)]*2)

        radius = persegi_panjang.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        persegi_panjang.blit(circle, radius)
        radius.topright = rect.topright
        persegi_panjang.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        persegi_panjang.blit(circle, radius)

        persegi_panjang.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        persegi_panjang.fill((0, 0, 0), rect.inflate(0, -radius.h))
        pos = pos_akhir
        if (pos[0]+pos[2]) > mouse[0] > pos[0] and (pos[1]+pos[3]) > mouse[1] > pos[1]:
            self.hover = True
            self.tombol_klik = action
            warna = pg.Color(*warna[1])
            alpha = warna.a
            warna.a = 0
        else:
            warna = pg.Color(*warna[0])
            alpha = warna.a
            warna.a = 0
            self.hover = False
        persegi_panjang.fill(warna, special_flags=pg.BLEND_RGBA_MAX)
        persegi_panjang.fill((255, 255, 255, alpha),
                             special_flags=pg.BLEND_RGBA_MIN)
        self.layar.blit(persegi_panjang, pos)
        txts = pg.font.SysFont('Courier New', ukuran_teks).render(
            teks, True, (0, 0, 0))
        txtrect = txts.get_rect()
        txtrect.center = (pos[0]+pos[2]/2), (pos[1]+pos[3]/2)
        self.layar.blit(txts, txtrect)

    def reset(self):  # UNTUK MERESET FUNGSI TOMBOL KEAWAL
        self.kiri, self.kanan, self.atas, self.bawah = False, False, False, False

    def loop(self):
        self.permainan_selesai = False
        while self.permainan_selesai != True:
            # WARNA BACKGROUND SAAT GAME DIMULAI
            self.layar.fill((35, 38, 117))
            self.Ular.update()
            self.Ular.banyak_makan()
            for x in self.blok2:
                # KONDISI JIKA ULAR MENABRAK DINDING
                if self.Ular.periksa_tabrakan(x[1]) == True:
                    self.over()
                self.layar.blit(x[0], x[1])
            a = 0
            for x in self.Ular.gambar2:
                if a != 0:
                    if self.Ular.periksa_makanan(x[1]) == True:
                        self.over()
                self.layar.blit(x[0], x[1])
                a += 1

            ## MEMUSINGKAN ##     
            self.layar.blit(self.Ular.gambar, self.Ular.pos)
            for event in pg.event.get():  # MENGARAHKAN ULAR DI DALAM PERMAINAN
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        if self.kiri == False:
                            self.reset()
                            self.Ular.kanan()
                            self.kanan = True
                    if event.key == pg.K_LEFT:
                        if self.kanan == False:
                            self.reset()
                            self.Ular.kiri()
                            self.kiri = True
                    if event.key == pg.K_UP:
                        if self.bawah == False:
                            self.reset()
                            self.Ular.atas()
                            self.atas = True
                    if event.key == pg.K_DOWN:
                        if self.atas == False:
                            self.reset()
                            self.Ular.bawah()
                            self.bawah = True
            pg.display.update()


class MenuAwal():
    def __init__(self):
        # UKURAN TAMPILAN PADA MENU AWAL
        self.layar = pg.display.set_mode((800, 450))
        self.b1 = '(150, 300,190,50),"Permainan Baru", [(0,255,0), (0,150,0)], action = self.mulai'
        self.b2 = '(550, 300,100,50),"Keluar", [(255,0,0), (150,0,0)], action = self.exit'
        self.tombol2 = [self.b1, self.b2]
        self.blok2 = []
        self.size = 1
        self.click0, self.loads = False, False
        warna = (0, 0, 0)
        for x in range(0, 800, 10):  # UKURAN DINDING ATAS
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [x, 0]])
        for x in range(0, 800, 10):  # UKURAN DINDING BAWAH
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [x, 440]])
        for x in range(0, 450, 10):  # UKURAN DINDING KIRI
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [0, x]])
        for x in range(0, 450, 10):  # UKURAN DINDING KANAN
            t = pg.Surface((10, 10))
            t.fill(warna)
            self.blok2.append([t, [790, x]])

    # TAMPILAN TEKS PADA MENU AWAL
    def membuat_teks(self, x, y, teks, size=20, warna=(0, 0, 0), a=False):
        txts = pg.font.SysFont('Courier New', size).render(teks, True, warna)
        txtrect = txts.get_rect()
        txtrect.topleft = (x, y)
        if a == True:
            txtrect.center = (x, y)
        self.layar.blit(txts, txtrect)

    # PEMBUATAN TAMPILAN TOMBOL DAN KETIKA TOMBOL DI KLIK PADA MENU AWAL
    def tombol(self, pos, teks, warna, action=None, ukuran_teks=20):
        mouse = pg.mouse.get_pos()
        pos_akhir = pos
        rect = pg.Rect(pos)
        pos = rect.topleft
        rect.topleft = 0, 0
        persegi_panjang = pg.Surface(rect.size, pg.SRCALPHA)

        circle = pg.Surface([min(rect.size)*3]*2, pg.SRCALPHA)
        pg.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pg.transform.smoothscale(
            circle, [int(min(rect.size)*0.5)]*2)

        radius = persegi_panjang.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        persegi_panjang.blit(circle, radius)
        radius.topright = rect.topright
        persegi_panjang.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        persegi_panjang.blit(circle, radius)

        persegi_panjang.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        persegi_panjang.fill((0, 0, 0), rect.inflate(0, -radius.h))
        pos = pos_akhir
        if (pos[0]+pos[2]) > mouse[0] > pos[0] and (pos[1]+pos[3]) > mouse[1] > pos[1]:
            self.hover = True
            self.tombol_klik = action
            warna = pg.Color(*warna[1])
            alpha = warna.a
            warna.a = 0
        else:
            warna = pg.Color(*warna[0])
            alpha = warna.a
            warna.a = 0
            self.hover = False
        persegi_panjang.fill(warna, special_flags=pg.BLEND_RGBA_MAX)
        persegi_panjang.fill((255, 255, 255, alpha),
                             special_flags=pg.BLEND_RGBA_MIN)
        self.layar.blit(persegi_panjang, pos)
        self.membuat_teks((pos[0]+pos[2]/2), (pos[1]+pos[3]/2),
                          teks, a=True, size=ukuran_teks)

    def mainloop(self):
        while 1:
            self.layar.fill((35, 38, 117))  # WARNA BACKGROUND MENU AWAL
            self.membuat_teks(400, 150, 'Game Snake Optimus',  # JARAK TULISAN
                              warna=(255, 255, 255), size=50, a=True)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            for x in self.blok2:
                self.layar.blit(x[0], x[1])
            for x in self.tombol2:
                exec('self.tombol(' + x + ')')
                if self.hover == True:
                    click = pg.mouse.get_pressed()
                    if click[0] == 1:
                        self.click0 = True
                    if self.click0 == True:
                        if click[0] == 0:
                            self.tombol_klik()
                            self.click0 = False
            pg.display.update()

    def mulai(self):  # Menu pilihan untuk tampilan size permainan
        self.b1 = '(150, 300,100,50),"Normal", [(0,255,0), (0,150,0)], action = self.mulai3'
        self.b2 = '(550, 300,100,50),"Besar", [(0,255,0), (0,150,0)], action = self.mulai4'
        self.tombol2 = [self.b1, self.b2]

    def mulai3(self):  # Menu pilihan untuk level permainan pada pilihan Normal
        self.b1 = '(150, 300,100,50),"Mudah", [(0,255,0), (0,150,0)], action = self.m'
        self.b2 = '(550, 300,100,50),"Susah", [(0,255,0), (0,150,0)], self.s'
        self.tombol2 = [self.b1, self.b2]

    def mulai4(self):  # Menu pilihan untuk level permainan pada pilihan Besar
        self.size = 2
        self.b1 = '(150, 300,100,50),"Mudah", [(0,255,0), (0,150,0)], action = self.m'
        self.b2 = '(550, 300,100,50),"Susah", [(0,255,0), (0,150,0)], self.s'
        self.tombol2 = [self.b1, self.b2]

    def m(self):  # KECEPATAN MODE EASY
        mulai(0.1, self.size)

    def s(self):  # KECEPATAN MODE NORMAL
        mulai(0.2, self.size)

    def exit(self):  # KELUAR
        sys.exit()


def mulai(kecepatan, size):  # FUNGSI START PADA GAME YANG MENGGUNAKAN FUNGSI GLOBAL
    global g, m
    del m

    g = Permainan(kecepatan, size)
    g.loop()


def ulang():  # FUNGSI RESTART YANG MENGGUNAKAN FUNGSI GLOBAL
    global g
    del g
    menu()


def menu():  # FUNGSI MENU YANG MENGGUNAKAN FUNGSI GLOBAL
    global m
    pg.init()
    m = MenuAwal()
    m.mainloop()


menu()
