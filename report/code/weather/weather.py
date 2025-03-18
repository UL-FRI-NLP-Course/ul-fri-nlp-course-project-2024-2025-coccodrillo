import requests
from bs4 import BeautifulSoup
import os



def get_parameters(hourly,day):
    output = f"Previsioni meteo per {day}" +  "\n" 
    for forecast in hourly:
        ora = forecast.find('td').text.strip()
        temp = forecast.find('td', {'data-value': 'temperatura'}).text.strip()
        prec_elem = forecast.find_all('td')[3]
        prec_text = prec_elem.find('span').text.strip() if prec_elem.find('span') else "0 mm"
        vento_elem = forecast.find_all('td')[5]
        vento_info = vento_elem.text.strip().replace("\n", " ")
        quota_elem = forecast.find_all('td')[6]
        quota_info = quota_elem.text.strip().replace("\n", " ")
        visib_elem = forecast.find_all('td')[7]
        visibilita = visib_elem.text.strip().replace("\n", " ")
        pressione = forecast.find_all('td')[8].text.strip()
        umidita = forecast.find_all('td')[9].text.strip()
        temp_perc = forecast.find_all('td')[10].text.strip()
        uv_elem = forecast.find_all('td')[-1]
        indice_uv = uv_elem.text.strip() if uv_elem.text.strip() else "N/A"

        output += f"Time: {ora}:00" + "\n" +  \
                  f"Temperatura: {temp}°C" + "\n" +  \
                  f"Precipitazioni: {prec_text}"  + "\n" +  \
                  f"Wind: {vento_info}"  + "\n" +  \
                  f"Quota neve: {quota_info}"  + "\n" +  \
                  f"Visibilità: {visibilita}"  + "\n" +  \
                  f"Pressione: {pressione} mbar"  + "\n" +  \
                  f"Umidity: {umidita}%"  + "\n" +  \
                  f"Temperatura percepita: {temp_perc}°C"  + "\n" +  \
                  f"UV index: {indice_uv}"  + "\n" +  \
                   "-" * 50 + "\n"
    return output


def analize_url(url,headers,file):
    global long_term_link
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        forecast_days = soup.find_all('li', class_='forecast_day_selector__list__item')
        for day in forecast_days:
            date_element = day.find('span', class_='forecast_day_selector__list__item__link__date')
            if date_element:
                giorno_settimana = date_element.contents[0].strip()  # Es. "Lun"
                giorno_numero = date_element.find('span').text.strip()  # Es. "10"
                giorno_completo = f"{giorno_settimana} {giorno_numero}"
                
            else:
                long_term_forecast = soup.find('a', href=True, title=lambda x: x and "Previsioni fino al" in x)
                if long_term_forecast:
                    long_term_link = long_term_forecast['href']
                else:
                    continue
            link = day.find('a', href=True)
            link_url = link['href'] if link else None
            if link_url:
                
                daily_response = requests.get(link_url, headers=headers)
                if daily_response.status_code == 200:
                    daily_soup = BeautifulSoup(daily_response.text, 'lxml')
                    weather_tables = daily_soup.find_all('table', class_='weather_table')
                    if weather_tables:
                        hourly_forecasts = daily_soup.find_all('tr', class_=['dialog-open forecast_3h',
                                                                             'dialog-open hidden forecast_3h ok_temperatura',
                                                                             'dialog-open hidden forecast_1h ok_temperatura'])
                        if (hourly_forecasts != []):
                            parameters = get_parameters(hourly_forecasts,giorno_completo)
                            fp = open(file,"a")
                            fp.write(parameters)
                            fp.close()

                            


    else:
         print("Error")


citta = "torino"
url = f'https://www.ilmeteo.it/meteo/{citta}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


long_term_link = ""
path_file = citta + "_meteo.txt"
if os.path.exists(path_file):
    with open(path_file, "w") as fp:
        pass  

analize_url(url,headers,path_file)
if (long_term_link != ""):
    analize_url(long_term_link,headers,path_file)













