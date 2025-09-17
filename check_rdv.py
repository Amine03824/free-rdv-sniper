import os
import time
import random
import sys
import traceback
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException, WebDriverException
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
load_dotenv()
DATE_LIMITE = int(os.getenv("DATE_LIMITE"))
FREE_USER = os.getenv("FREE_USER")
FREE_PASS = os.getenv("FREE_PASS")
LOGIN_URL = os.getenv("LOGIN_URL")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ---------------- FONCTIONS ----------------
def notifier(message: str):
    """Send Telegram + print console"""
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
        print("Telegram response:", r.status_code, r.text)
    except Exception as e:
        print("Erreur envoi Telegram :", e)
    print(message)

def pause_with_countdown(seconds):
    """Per-second countdown with terminal display"""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rTemps restant avant prochaine tentative : {remaining:3} s")
        sys.stdout.flush()
        time.sleep(1)
    print()

def init_driver():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    return driver, wait

def se_connecter_et_naviguer(driver, wait):
    driver.get(LOGIN_URL)
    print("⚠️ Connexion en cours...")
    time.sleep(5)
    try:
        driver.find_element(By.ID, "login_b").send_keys(FREE_USER)
        driver.find_element(By.ID, "pass_b").send_keys(FREE_PASS)
        driver.find_element(By.ID, "ok").click()
        time.sleep(5)
        mon_assistance_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbtn.monsav"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mon_assistance_btn)
        driver.execute_script("arguments[0].click();", mon_assistance_btn)
        time.sleep(5)
        print("✅ Page Mon Assistance chargée - prêt pour la suite")
    except Exception as e:
        notifier(f"❌ Erreur login/navigation : {e}")
        print(traceback.format_exc())
        input("Connecte-toi manuellement et appuie sur Entrée pour continuer...")

# ---------------- SCRIPT ----------------
notifier("🤖 Bot de surveillance RDV démarré ! Connecte-toi manuellement si nécessaire.")

driver, wait = init_driver()
se_connecter_et_naviguer(driver, wait)

while True:
    try:
        # Refresh page & click "Modifier"
        driver.refresh()
        time.sleep(5)
        bouton = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Modifier')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
        driver.execute_script("arguments[0].click();", bouton)
        print("Bouton 'Modifier' cliqué via JS")

        # ✅ Attente dynamique : modale prête (contenu chargé)
        try:
            jour_centre_btn = WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "div.bg-gray-100")
            )
        except:
            jour_centre_btn = None

        print("Analyse de la modale pour les créneaux disponibles...")

        # 1️⃣ Service indisponible
        try:
            msg_service = driver.find_element(By.CSS_SELECTOR, "p.text-red")
            if "indisponible" in msg_service.text.lower():
                notifier("❌ Service indisponible pour le moment.")
                pause_with_countdown(120)  # 2 minutes
                continue
        except:
            pass

        # 2️⃣ Jour pré-sélectionné seulement
        try:
            if jour_centre_btn:
                numero_jour = jour_centre_btn.find_element(By.TAG_NAME, "p").text.strip()
                if numero_jour.isdigit():
                    num = int(numero_jour)

                    # 🔍 Vérifier s'il existe des créneaux horaires en bas
                    creneaux = driver.find_elements(By.CSS_SELECTOR, "div.w-full.mb-4 button")

                    if creneaux:
                        horaire = creneaux[0].text.strip()
                        if num < DATE_LIMITE:
                            notifier(f"⚡ NOUVEAU CRÉNEAU ! Jour {num} à {horaire}")
                        else:
                            print(f"🔹 Créneau trouvé mais après la limite ({DATE_LIMITE}) : {num} à {horaire}")
                    else:
                        print(f"❌ Aucun créneau dispo pour le jour {num}")
            else:
                print("❌ Aucun jour pré-sélectionné trouvé / modale vide")
        except Exception as e:
            print(f"Erreur récupération du jour/créneaux : {e}")

        # Normal pause before next iteration
        pause_with_countdown(random.randint(60, 280))

    except (InvalidSessionIdException, NoSuchWindowException):
        notifier("⚠️ Session expirée ou fenêtre fermée. Reconnexion...")
        try:
            driver.quit()
        except:
            pass
        driver, wait = init_driver()
        se_connecter_et_naviguer(driver, wait)

    except WebDriverException as e:
        notifier(f"⚠️ WebDriverException détectée : {e}")
        try:
            notifier("⚠️ Relance complète du parcours depuis le login...")
            try:
                driver.quit()
            except:
                pass
            driver, wait = init_driver()
            se_connecter_et_naviguer(driver, wait)
        except Exception as inner_e:
            notifier(f"❌ Erreur lors du traitement de WebDriverException : {inner_e}")
            pause_with_countdown(random.randint(30, 60))

    except Exception as e:
        notifier("❌ Erreur inattendue lors de l'itération principale.")
        notifier(f"Traceback:\n{traceback.format_exc()}")
        try:
            notifier("⚠️ Relance complète du parcours depuis le login...")
            try:
                driver.quit()
            except:
                pass
            driver, wait = init_driver()
            se_connecter_et_naviguer(driver, wait)
        except Exception as inner_e:
            notifier(f"❌ Erreur lors de la relance complète : {inner_e}")
            pause_with_countdown(random.randint(30, 60))
