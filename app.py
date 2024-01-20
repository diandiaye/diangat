import PyPDF2
import streamlit as st
from io import BytesIO
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import justext
# Liste des thèmes à rechercher
themes_socio_economiques = [
    "Coût de la vie",
    "Logement",
    "Sécurité",
    "Émigration",
    "Numérique",
    "Technologie",
    "Pouvoir d’achat",
    "Aide à l’entreprenariat",
    "Démocratie",
    "Santé publique",
    "Éducation",
    "Infrastructures industrielles",
    "Économie du savoir",
    "Agriculture et souveraineté alimentaire",
    "Emploi et formation",
    "Protection sociale",
    "Énergie et transition énergétique",
    "Sécurité intérieure et relations internationales",
    "Technologies numériques et innovation",
    "Gouvernance et institutions démocratiques",
    "Environnement et développement durable",
    "Équité et inclusion sociale",
    "Commerce international",
    "Investissement étranger",
    "Réformes fiscales",
    "Développement rural",
    "Tourisme et culture",
    "Sports et loisirs",
    "Santé mentale",
    "Égalité des genres",
    "Droits de l'homme",
    "Liberté d'expression",
    "Transparence gouvernementale",
    "Développement urbain",
    "Transport et mobilité",
    "Gestion des déchets",
    "Qualité de l'air et pollution",
    "Conservation de la biodiversité",
    "Gestion des ressources en eau",
    "Résilience aux changements climatiques",
    "Éducation à la citoyenneté",
    "Accès à l'information",
    "Diversité et intégration",
    "Réforme judiciaire",
    "Droits des enfants",
    "Protection des données personnelles",
    "Cybersécurité",
    "Innovation en santé",
    "Énergies renouvelables",
    "Efficacité énergétique",
    "Sécurité alimentaire",
    "Réduction de la pauvreté",
    "Développement des PME",
    "Formation professionnelle",
    "Accessibilité numérique",
    "Inclusion financière",
    "Réseaux de transport public",
    "Développement de la petite enfance",
    "Soutien aux familles",
    "Droits des travailleurs",
    "Réforme des retraites",
    "Sécurité sociale",
    "Prévention de la corruption",
    "Participation citoyenne",
    "Développement des arts et de la culture",
    "Politiques de jeunesse",
    "Accès aux soins de santé",
    "Gestion des crises et des catastrophes",
    "Aménagement territorial",
    "Urbanisme durable",
    "Gestion des ressources naturelles",
    "Efficacité gouvernementale",
    "Réduction des inégalités",
    "Lutte contre le chômage",
    "Développement des compétences",
    "Connectivité rurale",
    "Inclusion numérique",
    "Modernisation de l'administration publique",
    "Soutien à la recherche et au développement",
    "Collaboration internationale",
    "Diplomatie économique",
    "Gestion des frontières",
    "Intégration régionale",
    "Politique de l'immigration",
    "Droits des minorités",
    "Protection de l'enfance",
    "Soutien aux personnes handicapées",
    "Santé reproductive",
    "Prévention des maladies",
    "Réforme de l'éducation",
    "Qualité de vie",
    "Accès à l'énergie",
    "Développement des infrastructures",
    "Stratégies anti-pauvreté",
    "Égalité d'accès aux services",
    "Décentralisation gouvernementale",
    "Promotion de l'économie locale",
    "Conservation du patrimoine",
    "Développement communautaire",
    "Amélioration des services publics",
    "Réforme des systèmes de santé",
    "Gestion durable des forêts",
    "Protection de la faune et de la flore",
    "Prévention de la violence" "Développement durable",
    "Gestion des crises sanitaires",
    "Innovation agricole",
    "Accès à l'eau potable",
    "Réseaux d'assainissement",
    "Politiques migratoires",
    "Lutte contre le terrorisme",
    "Réformes électorales",
    "Gouvernance locale",
    "Transports en commun",
    "Développement des TIC",
    "Économie verte",
    "Droits des peuples autochtones",
    "Patrimoine culturel",
    "Tourisme durable",
    "Éducation aux médias",
    "Lutte contre la désinformation",
    "Accès à Internet",
    "E-commerce",
    "Inclusion des jeunes",
    "Développement des compétences numériques",
    "Économie circulaire",
    "Gestion des ressources halieutiques",
    "Agriculture durable",
    "Sécurité routière",
    "Accès aux soins de santé primaires",
    "Soins de santé mentale",
    "Prévention du VIH/SIDA",
    "Maladies tropicales négligées",
    "Santé maternelle",
    "Nutrition et sécurité alimentaire",
    "Microfinance",
    "Banque mobile",
    "Développement des infrastructures numériques",
    "Éducation financière",
    "Économie collaborative",
    "Espaces verts urbains",
    "Qualité de l'habitat",
    "Réseaux électriques",
    "Développement de l'énergie solaire",
    "Biocarburants",
    "Gestion des déchets électroniques",
    "Réglementations environnementales",
    "Conservation marine",
    "Protection des écosystèmes",
    "Lutte contre la déforestation",
    "Urbanisation et planification",
    "Inclusion des personnes handicapées",
    "Droits des LGBTQ+",
    "Réforme du secteur de la sécurité",
    "Lutte contre les inégalités de genre",
    "Développement de l'économie bleue",
    "Coopération Sud-Sud",
    "Relations internationales",
    "Intégration économique régionale",
    "Soutien à l'entrepreneuriat féminin",
    "Innovation en matière de santé",
    "Télétravail et travail à distance",
    "Équilibre vie professionnelle/vie privée",
    "Éducation bilingue",
    "Langues régionales",
    "Réforme de l'enseignement supérieur",
    "Échanges culturels internationaux",
    "Soutien aux industries créatives",
    "Protection des droits d'auteur",
    "Éducation en environnement",
    "Programmes de reforestation",
    "Développement de l'agroforesterie",
    "Gestion durable des terres",
    "Réduction des émissions de gaz à effet de serre",
    "Adaptation au changement climatique",
    "Prévention des risques naturels",
    "Résilience urbaine",
    "Mobilité durable",
    "Transport aérien",
    "Voies navigables",
    "Développement du commerce équitable",
    "Commerce intra-africain",
    "Relations Afrique-diaspora",
    "Réseaux d'éducation à la paix",
    "Désarmement et non-prolifération",
    "Médiation de conflits",
    "Droits des réfugiés",
    "Intégration des migrants",
    "Prévention de la radicalisation",
    "Lutte contre le trafic d'êtres humains",
    "Réforme de la gouvernance mondiale",
    "Diplomatie climatique",
    "Souveraineté alimentaire",
    "Aide au développement",
    "Partenariats public-privé",
    "Financement du développement",
    "Réduction de la dette",
    "Soutien à la petite enfance",
    "Protection sociale pour tous",
    "Systèmes de santé universels",
    "Accès aux médicaments essentiels",
    "Lutte contre les épidémies",
    "Santé et environnement",
    "Éducation à la sexualité",
    "Droits reproductifs",
    "Planification familiale",
    "Prévention du mariage des enfants",
]

def extraire_themes_du_pdf(fichier):
    lecteur_pdf = PyPDF2.PdfReader(fichier)

    themes_trouves = {}
    for num_page, page in enumerate(lecteur_pdf.pages):
        texte_page = page.extract_text()

        for theme in themes_socio_economiques:
            if theme.lower() in texte_page.lower():
                if theme not in themes_trouves:
                    themes_trouves[theme] = []
                themes_trouves[theme].append(num_page + 1)

    return themes_trouves

class WebApp:
    def download_transcript(self, video_url, num_keywords):
        # Télécharge la transcription depuis YouTube en utilisant l'URL de la vidéo
        try:
            video_id = YouTube(video_url).video_id
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["fr"])
            transcript_text = "\n".join([entry["text"] for entry in transcript])
            st.subheader("Transcription YouTube:")
            st.write(transcript_text)

        except Exception as e:
            st.error(f"Erreur lors du téléchargement de la transcription : {str(e)}")

    def scrape_content_url(self, url):
        # Grattage du contenu d'une URL donnée en utilisant requests et justext
        try:
            response = requests.get(url)
            paragraphs = justext.justext(response.content, justext.get_stoplist("French"))
            scraped_content = [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]
            content_text = " ".join(scraped_content)
            return content_text
        except Exception as e:
            st.error(f"Erreur lors du grattage du contenu : {str(e)}")
            return None

    def run(self):
        st.markdown("<h1 style='font-size:1.5em;'>Institut des Algorithmes du Sénégal - Jangat Web App</h1>", unsafe_allow_html=True)
        st.info("Bienvenue à l'application \"Jàngat\" de l'Institut des Algorithmes du Sénégal.")

        # Choix de la source de données
        option = st.sidebar.radio("Choisissez la source de données :", ("URL", "PDF", "YouTube"))

        # Boutons de la barre latérale
        action_button = st.sidebar.button("Lancer l'analyse")

        if option == "URL":
            url = st.text_input("Entrez l'URL à gratter :", "")
            if action_button:
                if url:
                    st.info("Grattage du contenu... Veuillez patienter.")
                    scraped_content = self.scrape_content_url(url)
                    if scraped_content:
                        st.subheader("Contenu gratté :")
                        st.write(scraped_content)

        elif option == "Fichier PDF":
            fichier_uploade = st.file_uploader("Téléchargez un fichier PDF", type="pdf")
            if fichier_uploade and action_button:
                # Enregistrez le fichier PDF localement temporairement
                with open("temp.pdf", "wb") as temp_file:
                    temp_file.write(fichier_uploade.read())

                with st.spinner("Analyse en cours..."):
                    themes_trouves = extraire_themes_du_pdf("temp.pdf")
                    st.subheader("Voici une liste non exhaustive des thèmes abordés dans le programme :")
                    for index, (theme, pages) in enumerate(themes_trouves.items(), 1):
                        with st.expander(f"Thème {index}: {theme}"):
                            st.write(f"Pages : {', '.join(map(str, pages))}")

                # Supprimez le fichier temporaire après l'analyse
                os.remove("temp.pdf")

        elif option == "YouTube":
            youtube_url = st.text_input("Entrez l'URL YouTube :", "")
            if action_button:
                if youtube_url:
                    st.info("Téléchargement de la transcription... Veuillez patienter.")
                    self.download_transcript(youtube_url, 20)

if __name__ == "__main__":
    web_app = WebApp()
    web_app.run()
