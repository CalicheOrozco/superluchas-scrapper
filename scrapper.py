import requests
import lxml.html as html
import os
import datetime
# URL de la pagina principal
HOME_URL = 'https://superluchas.com/'
# links de xpath
XPATH_LINK_TO_ARTICLE = '//h2[@class="entry-title"]/a/@href'
XPATH_TITLE = '//div[@class="inside-page-hero grid-container grid-parent"]/h1/text()'
XPATH_BODY =  '//div[@class="entry-content"]/p//text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            # Decodifica en utf-8 para evitar errores
            notice = response.content.decode('utf-8')
            # Convierte el contenido de string a html
            parsed = html.fromstring(notice)
            
            try:
                # Obtiene el titulo
                title = parsed.xpath(XPATH_TITLE)[0]
                # Elimina las comillas dobles del titulo
                title = title.replace('\"', '')
                title = title.replace('|', '')
                title = title.replace('\n', '')
                # Imprime el titulo
                print(title)
                # Obtiene el  cuerpo
                
                body = parsed.xpath(XPATH_BODY)
                
            # Si no se encuentra alguno, solo retorna
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)

                f.write('\n\n')
                for p in body:
                    p = p.replace('.', '.\n')
                    p = p.replace('«', '\"')
                    p = p.replace('»', '\"')  
                    print(p)
                    f.write(p)
                    
        else:
            # Imprine el error
            raise ValueError(response.status_code)
    
    except ValueError as ve:
        # Imprine el error
        print(ve)

# Funcion que va a conseguir los links
def parse_home():

    try:
        # Obtiene el html del link
        response = requests.get(HOME_URL)
        # Si el estatus es OK 
        if response.status_code == 200:
            # Decodifica en utf-8 para evitar errores
            home = response.content.decode('utf-8')
            # Convierte el contenido de string a html
            parsed = html.fromstring(home)
            # Obtiene los links de las noticias
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # Los imprime
            # print(links_to_notices)
            # Guarda la fecha de hoy en str
            today = datetime.date.today().strftime('%d-%m-%Y')
            # Si no existe una carpeta con el nombre de la variable today
            if not os.path.isdir(today):
                # Crea una carpeta con el nombre de la variable today
                os.mkdir(today)
            # Por cada link en los links de noticia
            for link in links_to_notices:
                # Ejecuta la funcion de extracion
                # Imprime el link
                print(link)
                parse_notice(link,today)
        else:
            # Imprine el error
            raise ValueError(f'Error: {response.status_code}')
    # Imprine el error
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()