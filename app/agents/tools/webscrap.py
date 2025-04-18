from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os


class WebScrap:
    def __init__(self):
        self.options = Options()
        #self.options.headless = True
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
    
    def trip_flights(self, origin, destination):
        
        self.driver.get("https://www.google.com/travel/flights")
        print("Página do Google Flights aberta")
        time.sleep(5)
                
        # Preencher origem
        origin_field = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='De onde?']")
        origin_field.clear()
        origin_field.send_keys(origin)
        origin_field.send_keys(Keys.TAB)  # Pressiona Tab para ir ao próximo campo
        time.sleep(2)
        print("Origem preenchida")
        
        # Preencher destino (agora já deve estar focado neste campo)
        destination_field = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Para onde?']")
        destination_field.clear()
        destination_field.send_keys(destination)
        #destination_field.send_keys(Keys.RETURN)  # Pressiona Tab para ir ao próximo campo
        time.sleep(2)
        print("Destino preenchido")
        # Armazene os valores para uso posterior
        self.origin = origin
        self.destination = destination
        
        time.sleep(10)

    def date_trip(self, ida, volta):
        # Data de ida
        ida_field = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Partida']")
        ida_field = self.driver.find_element(By.CLASS_NAME, "zsRT0d")
        ida_field.send_keys(ida)
        ida_field.send_keys(Keys.TAB)  # Vai para o campo de data de volta
        time.sleep(2)
        print("Data de ida preenchida")
        # Data de volta (já deve estar focado neste campo)
        volta_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Retorno']")
        volta_field.clear()
        volta_field.send_keys(volta)
        volta_field.send_keys(Keys.TAB)  # Vai para o próximo campo
        time.sleep(2)
        print("Data de volta preenchida")
    def search_flights(self):
        # Botão de pesquisa
        try:
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Pesquisar']").click()
            print("Botão de pesquisa clicado")

        except Exception as e:
            print(f"Erro ao clicar no botão de pesquisa: {e}")
            self.driver.save_screenshot("error_search_button.png")
            
            # Aguardar carregamento dos resultados
            print("Aguardando carregamento dos resultados...")
            time.sleep(10)
            
    def capture_content(self):        # Capturar conteúdo da página
            content = self.driver.page_source
            print("Conteúdo da página capturado com sucesso")
            
            # Salvar o conteúdo em um arquivo HTML
            file_name = f"trips/{self.destination.replace(' ', '_')}.html"
            os.makedirs("trips", exist_ok=True)
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(content)
            
            print(f"Conteúdo salvo em '{file_name}'")
            
            # Capturar screenshot dos resultados
            screenshot_name = f"trips/{self.destination.replace(' ', '_')}.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Screenshot salvo em '{screenshot_name}'")
            
            self.driver.quit()
            print("Driver fechado")
            return file_name

def run_webscrap(origin, destination, ida, volta):
    scraper = WebScrap()
    scraper.trip_flights(origin, destination)
    scraper.date_trip(ida, volta)
    scraper.search_flights()
    scraper.capture_content()
    return scraper

# Exemplo de uso
if __name__ == "__main__":
    origin = "Recife"
    destination = "Rio de Janeiro"
    ida = "2025-05-01"  # Define the departure date
    volta = "2025-05-10"  # Define the return date

    run_webscrap(origin, destination, ida, volta)
