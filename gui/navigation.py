def volver_al_login(ventana_actual):
    ventana_actual.destroy()

    # Import diferido para evitar ciclo
    from gui.login import mostrar_ventana_login  
    mostrar_ventana_login()