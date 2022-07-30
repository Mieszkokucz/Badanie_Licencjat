import pygame


def WyswietlInstrukcje(sciezka_do_instrukcji):
    instrukcja_ = True
    while instrukcja_:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    instrukcja_ = False
        # wyczysc obecny widok
        gameDisplay.fill(BLACK)

        pozycja_y = 0
        with open(sciezka_do_instrukcji, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                # pierwsza linie jako tytuł
                if line == lines[0]:
                    gameDisplay.blit(tytul.render(line[:-1], True, GREEN),
                                     (1280 / 2 - len(line) * 8, 50))
                else:
                    pozycja_y += 1
                    linijka = styl_1.render(line[:-1], True, GREEN)
                    gameDisplay.blit(linijka, (1280 / 2 - (linijka.get_width()) / 2, 120 + (pozycja_y + 1) * 21))
        przejscie = styl_1.render("Przejdź dalej naciskając 'SPACJE'", True, WHITE)
        gameDisplay.blit(przejscie, (1280 / 2 - (przejscie.get_width()) / 2, 625))
        pygame.display.update()


BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

odpowiedzi_OB = []
pytania_OB = ["Wpisz swoje imię oraz pierwszą literę nazwiska:",
              "Twoja płeć? K/M/Inna",
              "Twój wiek?"]


def metryczka(screen, pytania, odpowiedzi):
    for pytanie in pytania:
        screen.fill(BLACK)

        pytanie_obecne = styl_1.render(pytanie, True, WHITE)
        screen.blit(pytanie_obecne, (1280 / 2 - (pytanie_obecne.get_width()) / 2, 720 / 2 - 40))

        komunikat_1 = styl_2.render("Kliknij w kwadrat, aby wprowadzić dane.", True, WHITE)
        screen.blit(komunikat_1, (1280 / 2 - (komunikat_1.get_width() / 2), 720 / 2 + 45))

        pygame.display.update()

        udzielona_odpowiedz = PoleWprowadzania(screen, 1280 / 2 - 110, 720 / 2)

        if pytanie == pytania[1]:
            while udzielona_odpowiedz.lower() not in ['k', 'm', 'inna']:
                udzielona_odpowiedz = PoleWprowadzania(screen, 1280 / 2 - 110, 720 / 2, udzielona_odpowiedz, "Niepoprawna forma zapisu.")

        odpowiedzi.append(udzielona_odpowiedz)


def PoleWprowadzania(screen, pozycja_x, pozycja_y, odpowiedz='', komunikat=''):
    clock = pygame.time.Clock()

    # utworz prostokat
    input_box = pygame.Rect(pozycja_x, pozycja_y, 0, 0)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    active = False
    user_text = odpowiedz
    zakonczono = False


    while not zakonczono:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN and active == True:
                # zapisz decyzje
                if event.key == pygame.K_RETURN:
                    zakonczono = True

                # uzuwanie wprowadzonych znakow
                elif event.key == pygame.K_BACKSPACE:

                    # tekst bez ostatniego znaku
                    user_text = user_text[:-1]
                    pygame.draw.rect(screen, BLACK, input_box)

                # didawanie nowych znakow
                else:
                    user_text += event.unicode
        # zmiana koloru po kliknieciu na pole
        if active:
            color = color_active
        else:
            color = color_inactive

        # narysuj imput box
        pygame.draw.rect(screen, color, input_box, 2)

        txt_surface = styl_1.render(user_text, True, color)

        # rozszerz pole kwadratu jezeli to konieczne
        input_box.w = max(220, txt_surface.get_width() + 10)
        input_box.h = 32

        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        if komunikat != "":
            komunikat_do_wyswietlenia = styl_1.render(komunikat, False, RED)
            screen.blit(komunikat_do_wyswietlenia, ((1280 / 2 - (komunikat_do_wyswietlenia.get_width()) / 2), 590))

        komunikat_zapisz_decyzje = styl_1.render("Zapisz decyzje naciskając 'ENTER'", False, WHITE)
        screen.blit(komunikat_zapisz_decyzje, ((1280 / 2 - (komunikat_zapisz_decyzje.get_width()) / 2), 665))
        pygame.display.flip()
        clock.tick(30)

    return user_text


def main():
    WyswietlInstrukcje('instrukcja.txt')
    metryczka(gameDisplay, pytania_OB, odpowiedzi_OB)
    WyswietlInstrukcje('instrukcja1.txt')
    WyswietlInstrukcje('instrukcja2.txt')
    WyswietlInstrukcje('instrukcja3.txt')


if __name__ == '__main__':
    # zainicjuj pygame
    pygame.init()
    gameDisplay = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN, 32)
    pygame.font.init()
    styl_1 = pygame.font.SysFont('Arial', 20)
    styl_2 = pygame.font.SysFont('Arial', 17)
    tytul = pygame.font.SysFont('Arial', 40)

    main()
