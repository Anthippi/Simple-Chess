import pygame
import chess
from game.board_renderer import WIDTH, HEIGHT, SQUARE_SIZE, load_images, draw_board, choose_promotion_piece
from game.chess_game import ChessGame

# Συνάρτηση που μετατρέπει τις συντεταγμένες του ποντικιού σε τετράγωνο της σκακιέρας (0-63)
def get_square_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)  # Η σκακιέρα ξεκινά από κάτω (λευκά)
    return chess.square(col, row)

# Κύρια συνάρτηση εκκίνησης του παιχνιδιού
def main():
    pygame.init()  # Εκκίνηση του pygame
    win = pygame.display.set_mode((WIDTH, HEIGHT))  # Παράθυρο με διαστάσεις σκακιέρας
    pygame.display.set_caption("Chess")  # Τίτλος παραθύρου
    clock = pygame.time.Clock()  # Χρήση για τον έλεγχο FPS

    load_images()  # Φόρτωση των PNG εικόνων των κομματιών
    game = ChessGame()  # Δημιουργία αντικειμένου παιχνιδιού (π.χ. board, σειρά κλπ)

    running = True
    while running:
        clock.tick(60)  # Μέγιστο 60 FPS

        # Σχεδίαση της σκακιέρας και των κομματιών
        draw_board(win, game.board)
        pygame.display.flip()  # Ενημέρωση της οθόνης

        # Έλεγχος συμβάντων pygame (κλικ, quit, κλπ)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Τερματισμός παιχνιδιού

            # Κλικ με το ποντίκι κατά τη διάρκεια του παιχνιδιού
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.is_game_over():
                square = get_square_from_mouse(pygame.mouse.get_pos())  # Από θέση -> τετράγωνο
                # Επιλογή κομματιού και πιθανή μετακίνηση (με υποστήριξη promotion)
                game.select_square(
                    square,
                    promotion_choice_callback=lambda color: choose_promotion_piece(color, win) # Επιστροφή χρώματος παίκτη
                )

        # Αν έχει τελειώσει η παρτίδα, τερμάτισε το loop
        if game.result:
            print("Game Over:", game.result)
            running = False

    pygame.quit()  # Κλείσιμο pygame και παραθύρου

# Εκτέλεση της main αν τρέχει απευθείας το αρχείο
if __name__ == "__main__":
    main()
