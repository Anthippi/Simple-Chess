import chess

class ChessGame:
    def __init__(self):
        # Δημιουργεί νέο πίνακα σκακιού με την αρχική τοποθέτηση
        self.board = chess.Board()

        # Το τετράγωνο που έχει επιλεγεί από τον παίκτη (πρώτο click)
        self.selected_square = None

        # Το αποτέλεσμα του παιχνιδιού όταν ολοκληρωθεί (π.χ. 1-0, 0-1, 1/2-1/2)
        self.result = None

    def select_square(self, square, promotion_choice_callback=None):
        """
        Καλείται όταν γίνεται click σε ένα τετράγωνο της σκακιέρας.
        Χειρίζεται:
        - Επιλογή κομματιού (πρώτο κλικ)
        - Επιλογή κίνησης (δεύτερο κλικ)
        - Αν είναι πιόνι στην 8η ή 1η γραμμή → κάνει promote
        """

        print(f"Selected: {square}")  # Debug

        # Πρώτο click: επιλογή κομματιού
        if self.selected_square is None:
            piece = self.board.piece_at(square)

            # Ελέγχει ότι υπάρχει κομμάτι στο τετράγωνο και είναι της σειράς του παίκτη
            if piece and piece.color == self.board.turn:
                print(f"Selected piece: {piece}")
                self.selected_square = square
            else:
                print("No valid piece selected.")

        # Δεύτερο click: προσπάθεια για κίνηση
        else:
            if square == self.selected_square:
                print("Deselected same square.")
                self.selected_square = None
                return

            piece = self.board.piece_at(self.selected_square)
            move = chess.Move(self.selected_square, square)

            # Έλεγχος για promotion πιόνιου
            if piece and piece.piece_type == chess.PAWN:
                rank = chess.square_rank(square)
                if (piece.color == chess.WHITE and rank == 7) or (piece.color == chess.BLACK and rank == 0):
                    if promotion_choice_callback:
                        promotion_piece = promotion_choice_callback(self.board.turn)
                        move = chess.Move(self.selected_square, square, promotion=promotion_piece)

            print(f"Trying move: {self.selected_square} → {square}")
            if move in self.board.legal_moves:
                self.board.push(move)
                print("Move successful.")
                if self.board.is_game_over():
                    self.result = self.board.result()
            else:
                print("Illegal move.")

            self.selected_square = None

    def is_game_over(self):
        # Επιστρέφει True αν έχει τελειώσει η παρτίδα
        return self.board.is_game_over()
