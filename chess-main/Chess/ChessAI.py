import random
import os
import json
# Depth of the algorithm determining AI moves. Higher set_depth == harder AI. Lower if engine is too slow.
set_depth = 4

# // FEN stands for Forsyth-Edwards Notation.
# // It is a standard notation for describing a particular board position in chess.
# // A FEN string contains six fields, separated by spaces:

# // Piece placement (from White's 8th rank to 1st, using letters for pieces and numbers for empty squares)
# // Active color (w for White, b for Black)
# // Castling availability (KQkq for both sides, - if none)
# // En passant target square (- if none)
# // Halfmove clock (for the fifty-move rule)
# // Fullmove number (starts at 1, increments after Black's move)

# Load opening book (FEN -> UCI move)
_opening_book = {}
_transposition_table = {}
try:
    _book_path = os.path.join(os.path.dirname(__file__), 'ChessOpenings.json')
    with open(_book_path, 'r', encoding='utf-8') as _f:
        _opening_book = json.load(_f)
except Exception:
    _opening_book = {}
# ...existing code...

# Positive values are good for white, negative for black. i.e. black checkmate = -1000
checkmate_points = 1000
stalemate_points = 0

piece_scores = {'K': 200.0, 'Q': 9.0, 'R': 5.0, 'B': 3.3, 'N': 3.2, 'P': 1.0}
piece_positions = {
    'wP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'bP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 5.0, -30],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 5.0, -30],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'bN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'wB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'bB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'wR': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]],
    'bR': [
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wQ': [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    "bQ": [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    'wK': [  # Uses chessprogramming.org King middle game values
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]],
    'bK': [  # Uses chessprogramming.org King middle game values
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]]}


def find_random_move(valid_moves):
    return random.choice(valid_moves)


def find_best_move(game_state, valid_moves):
    """Helper method to make first recursive call"""
    global next_move
    next_move = None

    # Try opening book first
    fen = _game_state_to_fen(game_state)
    if fen in _opening_book:
        uci = _opening_book[fen]
        book_move = _uci_to_move(uci, game_state, valid_moves)
        if book_move is not None:
            return book_move

    random.shuffle(valid_moves)
    find_negamax_move_alphabeta(game_state, valid_moves, set_depth, -checkmate_points, checkmate_points,
                                1 if game_state.white_to_move else -1)
    return next_move


def _uci_to_move(uci, game_state, valid_moves):
    """
    Convert UCI string like 'e2e4' (or 'e7e8q') to a Move object by
    creating a Move and matching it against valid_moves.
    """
    from Chess import ChessEngine
    if uci is None or len(uci) < 4:
        return None
    file_to_col = lambda f: ord(f) - ord('a')
    try:
        start_col = file_to_col(uci[0])
        start_row = 8 - int(uci[1])
        end_col = file_to_col(uci[2])
        end_row = 8 - int(uci[3])
    except Exception:
        return None

    # Create a candidate move and compare with valid_moves (Move.__eq__ is used by engine)
    candidate = ChessEngine.Move((start_row, start_col), (end_row, end_col), game_state.board)
    # handle promotion UCI like e7e8q by checking piece type if necessary
    for mv in valid_moves:
        if candidate == mv:
            return mv
    return None

def _game_state_to_fen(game_state):
    """
    Build a FEN string for the given game_state.
    If GameState provides get_fen(), use it; otherwise build a minimal FEN:
    piece placement + side-to-move + default castling '-' + en-passant '-' + '0 1'
    """
    # Prefer game_state.get_fen() if it exists
    get_fen = getattr(game_state, 'get_fen', None)
    if callable(get_fen):
        try:
            return get_fen()
        except Exception:
            pass

    # Build piece placement from game_state.board
    rows = []
    for r in range(8):
        empty_count = 0
        fen_row = ''
        for c in range(8):
            piece = game_state.board[r][c]
            if piece == '--':
                empty_count += 1
            else:
                if empty_count:
                    fen_row += str(empty_count)
                    empty_count = 0
                # piece already in form 'wP' or 'bK' -> convert to fen letter
                color = piece[0]
                p_type = piece[1]
                fen_char = p_type.lower() if color == 'b' else p_type.upper()
                fen_row += fen_char
        if empty_count:
            fen_row += str(empty_count)
        rows.append(fen_row)
    placement = '/'.join(rows)

    side = 'w' if getattr(game_state, 'white_to_move', True) else 'b'

    # Default castling/en-passant and move counters if not present on GameState
    castling = getattr(game_state, 'castling_rights', '-')  # if engine stores different name, adjust
    # Normalize castling to a string if it's an object
    if not isinstance(castling, str):
        # try common attributes
        try:
            castling = ''.join([
                'K' if getattr(castling, 'white_kingside', False) else '',
                'Q' if getattr(castling, 'white_queenside', False) else '',
                'k' if getattr(castling, 'black_kingside', False) else '',
                'q' if getattr(castling, 'black_queenside', False) else ''
            ]) or '-'
        except Exception:
            castling = '-'
    en_passant = getattr(game_state, 'en_passant_possible', '-')  # if stored differently, adjust
    if en_passant is True:
        en_passant = '-'  # unknown square -> fallback
    # halfmove and fullmove fallback
    halfmove = getattr(game_state, 'halfmove_clock', 0)
    fullmove = getattr(game_state, 'fullmove_number', 1)
    return f'{placement} {side} {castling} {en_passant} {halfmove} {fullmove}'
# ...existing code...

def find_negamax_move_alphabeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    """
    NegaMax algorithm with alpha beta pruning.

    Alpha beta pruning eliminates the need to check all moves within the game_state tree when
    a better branch has been found or a branch has too low of a score.

    alpha: upper bound (max possible); beta: lower bound (min possible)
    If max score is greater than alpha, that becomes the new alpha value.
    If alpha becomes >= beta, break out of branch.

    White is always trying to maximise score and black is always
    trying to minimise score. Once the possibility of a higher max or lower min
    has been eliminated, there is no need to check further branches.
    """
    fen_key = _game_state_to_fen(game_state)
    tt_entry = _transposition_table.get(fen_key)
    original_alpha = alpha
    if tt_entry is not None and tt_entry.get('depth', -1) >= depth:
        tt_score = tt_entry['score']
        flag = tt_entry.get('flag')
        if flag == 'EXACT':
            return tt_score
        elif flag == 'LOWER':
            alpha = max(alpha, tt_score)
        elif flag == 'UPPER':
            beta = min(beta, tt_score)
        if alpha >= beta:
            return tt_score

    if depth == 0:
        return score_board(game_state) * turn_multiplier

    max_score = -checkmate_points
    best_move_local = None

    # Move ordering: try TT best move first if available
    if tt_entry is not None:
        tt_best = tt_entry.get('best_move')
        if tt_best is not None and tt_best in valid_moves:
            try:
                valid_moves.remove(tt_best)
                valid_moves.insert(0, tt_best)
            except Exception:
                pass

    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        score = -find_negamax_move_alphabeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            best_move_local = move
            if depth == set_depth:
                next_move = move
        game_state.undo_move()

        # alpha-beta pruning updates
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    # Determine TT flag relative to original_alpha and beta
    if max_score <= original_alpha:
        store_flag = 'UPPER'
    elif max_score >= beta:
        store_flag = 'LOWER'
    else:
        store_flag = 'EXACT'

    # Store in transposition table (score is in the same convention returned by this function)
    _transposition_table[fen_key] = {
        'depth': depth,
        'score': max_score,
        'flag': store_flag,
        'best_move': best_move_local
    }
    return max_score

def score_board(game_state):
    """Positive score is good for white; negative score is good for black.

    - Uses piece values + piece-square-tables (PST).
    - Adds small bonuses for advanced pawns, rooks on open files, and centralization.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -checkmate_points  # Black wins
        else:
            return checkmate_points  # White wins
    elif game_state.stalemate:
        return stalemate_points

    score = 0.0
    board = game_state.board
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 8

    for r in range(rows):
        for c in range(cols):
            piece = board[r][c]
            if piece == '--':
                continue
            color = piece[0]
            ptype = piece[1]

            # base material value
            base_val = piece_scores.get(ptype, 0.0)

            # PST value (if available)
            pst_table = piece_positions.get(piece)
            pst_val = pst_table[r][c] if pst_table is not None else 0.0

            # small bonus for advanced pawns (encourage forward play)
            adv_bonus = 0.0
            if ptype == 'P':
                if color == 'w':
                    # white pawns advance as row decreases from 6 -> 0
                    adv_bonus = max(0.0, (6 - r)) * 0.08
                else:
                    # black pawns advance as row increases from 1 -> 7
                    adv_bonus = max(0.0, (r - 1)) * 0.08

            # rook on open file bonus (no pawns on that file)
            open_file_bonus = 0.0
            if ptype == 'R':
                pawn_on_file = False
                for rr in range(rows):
                    sq = board[rr][c]
                    if sq != '--' and sq[1] == 'P':
                        pawn_on_file = True
                        break
                if not pawn_on_file:
                    open_file_bonus = 0.45

            # centralization bonus for knights/bishops/queens/king (encourage center control)
            central_bonus = 0.0
            if ptype in ('N', 'B', 'Q', 'K'):
                center_r, center_c = 3.5, 3.5
                dist = abs(r - center_r) + abs(c - center_c)
                central_bonus = (3.5 - dist) * 0.06  # positive closer to center

            piece_value = base_val + pst_val + adv_bonus + open_file_bonus + central_bonus

            if color == 'w':
                score += piece_value
            else:
                score -= piece_value

    return score