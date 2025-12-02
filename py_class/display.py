import xlwings as xw

def afficher_arbre_et_proba(arbre):
    wb = xw.Book.caller()

    app = wb.app
    app.api.ScreenUpdating = False
    app.api.Calculation = -4135  # xlCalculationManual
    app.api.EnableEvents = False


    # Underlying
    ws_arbre = wb.sheets["Arbre"]
    ws_arbre.clear()
    
    # Three probability blocks
    ws_proba = wb.sheets["Proba"]
    ws_proba.clear()

    N = arbre.n_steps + 1

    # Display node values
    node_mid = arbre.racine
    for k in range(N):
        ws_arbre.range("A1").offset(N, k).value = node_mid.p_up
        node = node_mid.voisin_up
        i = 1
        while node is not None:
            ws_arbre.range("A1").offset(N - i, k).value = node.p_up
            i += 1
            node = node.voisin_up
        node = node_mid.voisin_down
        i = 1
        while node is not None:
            ws_arbre.range("A1").offset(N + i, k).value = node.p_up
            i += 1
            node = node.voisin_down
        node_mid = node_mid.next_mid
    #ws_arbre.range("A1").offset(N, N + 2).value = "Underlying price"

    app.api.ScreenUpdating = True
    app.api.Calculation = -4105  # xlCalculationAutomatic
    app.api.EnableEvents = True


"""
    # Block for proba_next_up
    node_mid = arbre.racine
    for k in range(N):
        ws_proba.range("A1").offset(N, k).value = node_mid.p_up
        node = node_mid.voisin_up
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(N - i, k).value = node.p_up
            i += 1
            node = node.voisin_up
        node = node_mid.voisin_down
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(N + i, k).value = node.p_up
            i += 1
            node = node.voisin_down
        node_mid = node_mid.next_mid
    ws_proba.range("A1").offset(N, N + 2).value = "Proba next up"
    
    # Block for proba_next_down
    node_mid = arbre.racine
    for k in range(N):
        ws_proba.range("A1").offset(3 * N, k).value = node_mid.p_down
        node = node_mid.voisin_up
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(3 * N - i, k).value = node.p_down
            i += 1
            node = node.voisin_up
        node = node_mid.voisin_down
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(3 * N + i, k).value = node.p_down
            i += 1
            node = node.voisin_down
        node_mid = node_mid.next_mid
    ws_proba.range("A1").offset(3 * N, N + 2).value = "Proba next down"
    
    # Block for proba_next_mid
    node_mid = arbre.racine
    for k in range(N):
        ws_proba.range("A1").offset(5 * N, k).value = node_mid.p_mid
        node = node_mid.voisin_up
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(5 * N - i, k).value = node.p_mid
            i += 1
            node = node.voisin_up
        node = node_mid.voisin_down
        i = 1
        while node is not None:
            ws_proba.range("A1").offset(5 * N + i, k).value = node.p_mid
            i += 1
            node = node.voisin_down
        node_mid = node_mid.next_mid
    ws_proba.range("A1").offset(5 * N, N + 2).value = "Proba next mid"
    
    


"""
