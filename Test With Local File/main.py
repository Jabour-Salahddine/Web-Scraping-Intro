from bs4 import BeautifulSoup 

'''
But : analyser et extraire des données à partir du HTML, 

 Utilise le HTML récupéré par requests pour le transformer en structure navigable (DOM).

 Tu peux alors chercher des balises, récupérer du texte, des attributs (comme href, src, etc.).
'''


''' Comme juste introduction on va lire à partir d'un fichier
 un code html comme si on l'extrait à partir d'un site web'''


with open('Test With Local File/home.html','r') as html_file:
    content = html_file.read()
     
    soup = BeautifulSoup(content,'lxml')

    courses_carts= soup.find_all('div',class_='card-body') # une liste de cartes.
        
    for course_cart in courses_carts:
        course_name = course_cart.h5.text
        course_prince = course_cart.a.text.split(' ')
 
        print(f'{course_name}, Costs {course_prince[-1]}')
