Le code lis une musique et la joue sur un buzzer. 
Une bibliotheque de note est declarée.
Dans chaque note le code est le meme.
La frequence de la note est joué.
La fonction get_volule est utilisé a chque fois pour addapter le volume a la lecture du potentiometre.
la valeur est diviser par 10(choisie subjectivement) pour evité la aturation du buzzer.
On va ammumer la led, attendre une demi fois le temps de la note et rallumer la led puis attendre leutre moitier de la note.
Cela fais clignoté la led au rythme de la musique.
Ensuite, une boucle while inclue deux partitions. Celle qui est lue est decider par une varriable global status.
Cette varriable global est modifiée par un listener qui ecoute tout relachement du bouton.
Dans cette configuration la musique n'est modifier que lorsque celle en cour se termine.
