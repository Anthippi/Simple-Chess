import pygame
import os
import chess

# Ρυθμίσεις παραθύρου και τετραγώνων
SQUARE_SIZE = 80  # Πλάτος/ύψος κάθε τετραγώνου
WIDTH = HEIGHT = SQUARE_SIZE * 8  # Διαστάσεις παραθύρου (8x8 σκακιέρα)

# Λεξικό για αποθήκευση των εικόνων των κομματιών
PIECE_IMAGES = {}

# Φόρτωση εικόνων από τον φάκελο assets/images/
def load_images():
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K']  # Τύποι κομματιών
    colors = ['w', 'b']  # w = λευκά, b = μαύρα
    for color in colors:
        for piece in pieces:
            name = color + piece  # Π.χ. wP, bK
            path = os.path.join("", "assets", "images", f"{name}.png")  # Σχετικό μονοπάτι εικόνας
            image = pygame.image.load(path)  # Φόρτωση εικόνας από αρχείο
            PIECE_IMAGES[name] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))  # Κλιμάκωση και αποθήκευση

# Σχεδίαση σκακιέρας και κομματιών
def draw_board(win, board):
    # Χρώματα τετραγώνων
    light = pygame.Color(240, 217, 181)  # Ανοιχτό καφέ
    dark = pygame.Color(181, 136, 99)    # Σκούρο καφέ

    # Σχεδίαση τετραγώνων (σαν σκακιέρα)
    for row in range(8):
        for col in range(8):
            color = light if (row + col) % 2 == 0 else dark
            pygame.draw.rect(win, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Αν ο βασιλιάς είναι σε σαχ, σχεδίασε κόκκινο περίγραμμα γύρω του
    if board.is_check():
        king_square = board.king(board.turn)  # Τρέχων βασιλιάς
        if king_square is not None:
            col = chess.square_file(king_square)
            row = 7 - chess.square_rank(king_square)
            highlight_rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, pygame.Color("red"), highlight_rect, 4)  # Κόκκινο περίγραμμα πάχους 4

    # Σχεδίαση κομματιών πάνω στα τετράγωνα
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                name = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
                win.blit(PIECE_IMAGES[name], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Γραφικό μενού επιλογής κομματιού για promotion
def choose_promotion_piece(turn_color, win):
    choices = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]  # Επιλογές προαγωγής
    labels = ['Q', 'R', 'B', 'N']  # Εμφανιζόμενα γράμματα
    font = pygame.font.SysFont(None, 48)  # Γραμματοσειρά pygame

    # Διαστάσεις και θέση του μενού
    box_width = 60
    spacing = 20
    total_width = (box_width + spacing) * len(choices) - spacing
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT // 2 - 30  # Κέντρο κατακόρυφα

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, _ = event.pos
                for i in range(len(choices)):
                    box_x = start_x + i * (box_width + spacing)
                    if box_x <= x <= box_x + box_width:
                        return choices[i]  # Επιστροφή του κομματιού που επέλεξε

        # Σχεδίαση του γκρι φόντου μενού
        pygame.draw.rect(win, pygame.Color("gray"), (start_x - 10, y - 10, total_width + 20, box_width + 20))

        # Σχεδίαση επιλογών κομματιών (Q, R, B, N)
        for i, label in enumerate(labels):
            box_x = start_x + i * (box_width + spacing)
            rect = pygame.Rect(box_x, y, box_width, box_width)
            pygame.draw.rect(win, pygame.Color("white"), rect)
            pygame.draw.rect(win, pygame.Color("black"), rect, 2)
            text = font.render(label, True, pygame.Color("black"))
            text_rect = text.get_rect(center=rect.center)
            win.blit(text, text_rect)

        pygame.display.flip()  # Ενημέρωση οθόνης μενού
