import instaloader
from pymongo import MongoClient


class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()

        # Connecter à MongoDB
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['database']
        self.collection = self.db['collection']
        
    def login(self, username, password):
        self.L.login(username, password)
 
    def download_hashtag_posts(self, hashtag):
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            try:
                images = []
                comments = []
    
                # Télecharger l'image
                self.L.download_post(post, target=f"images")
                images.append(f"images/{post.shortcode}.jpg")

                # captions
                caption = post.caption

    
                # commentaires
                for comment in post.get_comments():
                    comments.append(comment.text)
                
        
                # Créer a document avec images,caption et commentaires
                post_data = {
                    'image': images[0],
                    'caption': caption,
                    'comments': comments
                }

                # Stocker dans MongoDB
                self.collection.insert_one(post_data)

                

            except Exception as e:
                print(f"Error downloading post {post.shortcode}: {str(e)}")

    def close_connection(self):
        self.client.close()



if __name__=="__main__":
    cls = GetInstagramProfile()
    username= "" #Entrer instagram username
    password= "" #Entrer instagram password
    cls.login(username,password)
    hashtag="PrésidentJacquesChirac" #Entrer hashtag
    cls.download_hashtag_posts(hashtag)
    


    #Afficher la collection qui contienne les images leurs captions et leurs commentaires
    cursor = cls.collection.find()
    for document in cursor:
        print(document)
    
        
    cls.close_connection()


