from tkinter import *
from tkinter import messagebox
from time import sleep, strftime
import config
import threading
from win10toast import ToastNotifier
import winsound


root = Tk()
toaster = ToastNotifier()

win_w = 300
win_h = 200


#-CONFIG-WINDOW-------------------------------
# agarra las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# pone la ventana en las coordenadas
root.geometry(f'{win_w}x{win_h}+{50}+{50}')

# no se puede cambiar de tamaño
root.resizable(False, False)
#---------------------------------------------


# reloj que cambia el atributo de la etiqueta mostrada
def clock():
    string = strftime('%H:%M:%S %p')
    clocklbl.config(text=string)
    clocklbl.after(1000, clock)



# Hilo de contador
class Thread1():
    def __init__(self):
        counterTread = threading.Thread(target=Thread1.start_session)
        
        # inicio contador
        counterTread.start()

        # desactiva el boton
        startButton["state"]="disabled"

    #inicia la sesion de trabajo al presionar start
    def start_session():

        sessions = config.session_stack
        while sessions:
        
            # cuenta atras durante el tiempo de trabajar indicado en el archivo de configuracion
            # notifica al terminar
            estado.config(text="Trabajando")
            Thread1.countDown(config.session_time)

            # si es la ultima sesion se salta para dar un descanso largo
            if sessions > 1:
                #toaster.show_toast("Felicidades!","Hora de tomar un descanso",duration=5)

                # aviso de descanso
                toaster.show_toast("Felicidades!","Hora de tomar un descanso",duration=5)
    
                # cuenta atras durante el tiempo de descanso indicado en el archivo de configuracion
                # notifica al terminar
                estado.config(text="Descansando")
                Thread1.countDown(config.rest_time)
                toaster.show_toast("Descanso terminado","Hay que volver al trabajo!",duration=5)

            sessions-= 1

        # descanso largo
        toaster.show_toast("Has terminado las {0} sesiones".format(config.session_stack),"Ganaste un descanso largo",duration=5)
        
        estado.config(text="Descansando Largo")
        Thread1.countDown(config.long_rest_time)

        toaster.show_toast("Descanso terminado","Hay que volver al trabajo!",duration=5)

        # vuelve a activar el boton
        startButton["state"]="normal"

    def countDown(time):
        # mientras el tiempo no sea 0 sigue restando y actualiza la etiqueta
        while time:
            counter.config(text= "{0}:{1}".format(time//60,time%60))
            time-=1
            sleep(1)
        counter.config(text= "00:00")
        winsound.Beep(2500, 500)


if __name__ == "__main__":
    # reloj
    clocklbl = Label(root)
    clocklbl.pack()

    # contador
    counter = Label(root)
    counter.pack()
    
    # estado (trabajo - descanso)
    estado = Label(root)
    estado.pack()

    #empezar a trabajar
    startButton = Button(root,text="Start" , command=Thread1)
    startButton.pack()

    clock()

    root.mainloop()