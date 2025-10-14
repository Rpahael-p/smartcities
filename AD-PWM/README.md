Le code lis une musique et la joue sur un buzzer. \r
Une bibliotheque de note est declarée. \r
Dans chaque note le code est le même. \r
La frequence de la note est joué. \r
La fonction get_volule est utilisé a chque fois pour addapter le volume a la lecture du potentiometre. \r
la valeur est diviser par 10(choisie subjectivement) pour evité la aturation du buzzer. \r
On va ammumer la led, attendre une demi fois le temps de la note et rallumer la led puis attendre leutre moitier de la note. \r
Cela fais clignoté la led au rythme de la musique. \r
Ensuite, une boucle while inclue deux partitions. Celle qui est lue est decider par une varriable global status. \r
Cette varriable global est modifiée par un listener qui ecoute tout relachement du bouton. \r
Dans cette configuration la musique n'est modifier que lorsque celle en cour se termine. \r
