import time
import datetime
from pynput.keyboard import Key, Controller
import pywhatkit as kit

def send_message_via_whatsapp(numero_telephone, message):
    # Obtenez l'heure actuelle
    now = datetime.datetime.now()
    # numero_telephone = "+212644054404"  # Remplacez par le numéro au format international
    # message = "Bonjour, ceci est un message envoyé automatiquement depuis Python !"

    # Envoyer le message via pywhatkit pour ouvrir WhatsApp Web
    kit.sendwhatmsg(numero_telephone, message, now.hour, now.minute + 2, wait_time=20)

    # Attendre que WhatsApp Web soit prêt
    print("Vous avez 5 secondes pour passer à WhatsApp Web...")
    time.sleep(5)

    # Initialiser le contrôleur de clavier
    keyboard = Controller()

    # Taper le message
    for character in message:
        keyboard.press(character)
        keyboard.release(character)
        time.sleep(0.1)  # Délai pour simuler la saisie humaine

    # Appuyer sur 'Entrée' pour envoyer le message
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    print("Message envoyé avec succès !")

if __name__ == "__main__":
    # send_message_via_whatsapp()
    for i in range(10): print(i); print('hi')