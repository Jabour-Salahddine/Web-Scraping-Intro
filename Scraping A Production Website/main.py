import time
import requests
from bs4 import BeautifulSoup
import os # pour la création d'un dossier où on va stocker les fichiers et chaque fichier contient les info d'offre de trvaille  
import re # Pour nettoyer les noms de fichiers

BASE_URL = 'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation='

OUTPUT_DIR = "offres_emploi_python" # dossier pour sauvegarder les offres

DAYS_FILTER_LIMIT = 10 # n'afficher que les offres publiées il y a x jours ou moins

REQUEST_TIMEOUT = 15 # secondes avant timeout de la requête

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'



def sanitize_filename(filename):
    """Nettoie une chaîne de caractères pour l'utiliser comme nom de fichier."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)




def get_unwanted_skills():
    """Demande à l'utilisateur une liste de compétences à exclure."""
    while True:
        skills_input = input("Entrez les compétences à EXCLURE, séparées par des virgules (ex: java,php,ruby) ou laissez vide pour ne rien exclure : ").strip()
        
        if not skills_input:
            return []
        
        unwanted = [skill.strip().lower() for skill in skills_input.split(',') if skill.strip()]
        
        if unwanted:
            print(f"Les offres contenant l'une de ces compétences seront ignorées : {', '.join(unwanted)}")
            return unwanted
        
        print("Aucune compétence à exclure saisie.")
        
        return []





def scraping_python_jobs(unwanted_skills_list):
    """
    Scrape les offres d'emploi Python, filtre et sauvegarde celles qui correspondent.
    """
    
    print(f"Recherche d'offres sur {BASE_URL}...")
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.get(BASE_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
        html_text = response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return 0 # Retourne 0 offres sauvegardées

    
    soup = BeautifulSoup(html_text, 'lxml')
    jobs_elements = soup.find_all('div', class_='srp-job-bx')

    if not jobs_elements:
        print("Aucune offre d'emploi trouvée sur la page.")
        return 0

    
    # Crée le dossier de sortie s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    saved_jobs_count = 0




    for job_element in jobs_elements:
        
        # --- Extraction de la date de publication et filtrage ---
        published_date_span = job_element.find('span', class_='posting-time')
        
        if not published_date_span:
            
            continue
        
        published_date_text = published_date_span.text.strip()
        
        # Filtre sur la date : n'accepte que "X days ago" et si X <= DAYS_FILTER_LIMIT
        # Ou si c'est "few hours ago", "today", "yesterday" (considérés comme récents)

        is_recent = False
        
        if 'days ago' in published_date_text.lower():
            try:
                days_ago = int(published_date_text.split(' ')[0])
                if days_ago <= DAYS_FILTER_LIMIT:
                    is_recent = True
            except (ValueError, IndexError):
                # print(f"Impossible de parser le nombre de jours pour '{published_date_text}'. Offre considérée comme récente.")
                is_recent = True # Par défaut, si on ne peut pas parser, on la garde (ou on l'ignore)
        
        elif any(keyword in published_date_text.lower() for keyword in ['hour', 'hours', 'today', 'yesterday', 'posted']):
            is_recent = True
        
        
        if not is_recent:
            # print(f"Offre trop ancienne ({published_date_text}), ignorée.")
            continue


        # --- Extraction des autres informations ---
        
        label_tag = job_element.find('div', class_='srp-job-heading')
        job_title = label_tag.h3.text.strip() if label_tag and label_tag.h3 else "N/A"

        company_tag = job_element.find('span', class_='srp-comp-name')
        company_name = company_tag.text.strip() if company_tag else "N/A"

        skills_div = job_element.find('div', class_='srp-keyskills')
        job_skills = []
        
        if skills_div:
            job_skills = [skill.text.strip().lower() for skill in skills_div.find_all('a')]

        # --- Filtrage des compétences indésirables ---
        job_contains_unwanted_skill = False
       
        if unwanted_skills_list: # S'il y a des compétences à exclure
            for unwanted_skill in unwanted_skills_list:
                if unwanted_skill in job_skills:
                    job_contains_unwanted_skill = True
                    # print(f"Offre '{job_title}' chez '{company_name}' ignorée car elle contient la compétence indésirable : {unwanted_skill}")
                    break 
        
        if job_contains_unwanted_skill:
            continue

        
        # --- Sauvegarde de l'offre dans un fichier ---
        filename_base = sanitize_filename(f"{company_name}_{job_title}")
        filepath = os.path.join(OUTPUT_DIR, f"{filename_base}.txt")
        
        # Pour éviter d'écraser des fichiers si plusieurs offres ont le même titre/compagnie (rare mais possible)
        counter = 1
        temp_filepath = filepath
        
        
        while os.path.exists(temp_filepath):
            temp_filepath = os.path.join(OUTPUT_DIR, f"{filename_base}_{counter}.txt")
            counter += 1
        filepath = temp_filepath

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Compagnie: {company_name}\n")
                f.write(f"Poste: {job_title}\n")
                f.write(f"Date de publication: {published_date_text}\n")
                f.write(f"Compétences: {', '.join(job_skills) if job_skills else 'Non spécifiées'}\n")
                
                # Ajout du lien vers l'offre (si disponible et pertinent)
                job_link_tag = job_element.find('a', href=True)
                if job_link_tag:
                    job_url = job_link_tag['href']
                    # S'assurer que le lien est absolu
                    if job_url.startswith('/'):
                        job_url = "https://m.timesjobs.com" + job_url
                    f.write(f"Lien: {job_url}\n")

            # print(f"Offre sauvegardée : {filepath}")
            saved_jobs_count += 1
        except IOError as e:
            print(f"Erreur lors de l'écriture du fichier {filepath}: {e}")
            
    if saved_jobs_count > 0:
        print(f"{saved_jobs_count} nouvelle(s) offre(s) pertinente(s) sauvegardée(s) dans le dossier '{OUTPUT_DIR}'.")
    else:
        print("Aucune nouvelle offre pertinente trouvée correspondant aux critères.")
    return saved_jobs_count


if __name__ == '__main__':
    unwanted_skills = get_unwanted_skills()
    
    while True:
        print("\n--- Lancement d'un nouveau cycle de scraping ---")
        scraping_python_jobs(unwanted_skills)
        
        sleep_duration = 400 # secondes
        print(f"Attente de {sleep_duration // 60} minutes et {sleep_duration % 60} secondes avant le prochain cycle...")
        
        # Afficher un compte à rebours simple
        for i in range(sleep_duration, 0, -60): # Décompte par minute
            minutes_left = i // 60
            if minutes_left > 0 :
                print(f"Prochain scan dans environ {minutes_left} minute(s)...", end="\r")
            time.sleep(min(60, i)) # Attend 60 secondes ou le temps restant s'il est inférieur
        print("                                                         ", end="\r") # Efface la ligne du compte à rebours















