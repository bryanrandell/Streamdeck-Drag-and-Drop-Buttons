# Research for Sony Venice Multi Control
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

number_of_cameras = 1

#drivers_instances = [webdriver.Chrome().get("http://192.168.0.{}/rmt.html".format(i + 1)) for i in range(number_of_cameras)]
drivers_instances = []
camera_urls_list = []
for i in range(number_of_cameras):
    drivers_instances.append(webdriver.Chrome().get("http://192.168.0.{}/rmt.html".format(i + 1)))

    / html / head / script[32]

* @brief constructeur
 * @param [in] type Direction du curseur
 * Curseur vertical @arg'V'
 * Curseur horizontal @arg'H'
 * @param [in] buttonId ID de l'élément HTML à traiter comme un bouton coulissant
 * La plage de mouvement du bouton se trouve dans la zone de la partie parent spécifiée en HTML.
 * @param [in] convertTable Un tableau qui convertit les positions du curseur en valeurs (spécifiez null si non utilisé)
 * @param [in] Rappel lorsque le bouton cbPress est enfoncé, spécifiez null si aucun rappel n'est requis.
 * @param [in] cbRelease Callback lorsque le bouton est relâché, spécifiez null si aucun rappel n'est requis.
 * @param [in] Rappel lorsque le bouton cbMove est déplacé, spécifiez null si aucun rappel n'est requis.
 * / /

('H', "IMAGE_LENS_IRIS_KNOB", null, null, null, null)

rec = driver.find_element_by_id("BUTTON_REC_BUTTON")
iris = driver.find_element_by_id("BASE_LENS_IRIS_SLIDER_MOVABLE_SCOPE")
move = ActionChains(driver)
move.drag_and_drop_by_offset(iris, -15, 0).perform()

from selenium import webdriver
from selenium import ActionChains

driver = webdriver.Chrome()
# driver.get("http://admin:admin111@192.168.0.1/rmt.html")
driver.get('https://www.sony.net/Products/Cinematography/Venice/Camera_simulator/')
move = ActionChains(driver)

rec = driver.find_element_by_id("BUTTON_REC_BUTTON")
iris = driver.find_element_by_id("BASE_LENS_IRIS_SLIDER_MOVABLE_SCOPE")
move.drag_and_drop_by_offset(iris, -20, 0).perform()
"""