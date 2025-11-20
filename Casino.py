
import random
from enum import Enum
from typing import Tuple,Any,Callable
from cartes import Pack52, CarteJeu, Hand, Valeur, Couleur
import inspect
import sys
import types

def mandatory_token_purchase (func:Callable[...,Any])  -> Callable[...,Any] :
    def wrapper(jeu : Game, croupier : Croupier, joueur : Player , *args, **kwargs) -> Any:
        while joueur.token.number < jeu.min_bet :
            croupier.speak(f"💰 Il vous faut au moins {jeu.min_bet} jetons pour jouer au/à la {jeu.game_name} !. Donc vous devez acheter au moins {jeu.min_bet} jetons")
            achat: int = control_int(input(f"{joueur.name} : J'en voudrais "))
            try :
                joueur.purchase(jeu,achat)
            except ValueError :
                continue
            croupier.speak(f"✅ Parfait ! Vous avez maintenant {joueur.token.number} jetons.")
        return func(jeu, croupier, joueur, *args, **kwargs)
    return wrapper

def control_bet(func:Callable[...,Any])  -> Callable[...,Any] :
    def wrapper(jeu:Game, croupier:Croupier, joueur : Player, *args, **kwargs) -> Any:
        while joueur.mise not in range(jeu.min_bet, joueur.token.number) :
            croupier.speak(f"La mise minimum est de {jeu.min_bet} jetons")
            bet:int = control_int(input("Je vais miser : "))
            try :
                joueur.bet(bet,jeu)
                croupier.speak("Merci beaucoup pour votre don")
                break
            except :
                continue
            
        return func(jeu, croupier, joueur,*args,**kwargs)
    return wrapper

class Game() :
    """Ensemble qui contiendra l'ensemble de nos jeux de casino"""
    def __init__(self, game_name:str, min_bet:int) -> None :
        self.game_name:str=game_name
        self.min_bet:int=min_bet
    def Play(self) -> None :
        raise NotImplementedError("Méthode abstraite")
    def profit_and_loss_management(self, joueur:Player) -> None:
        raise NotImplementedError("Méthode abstraite")

class Person() :
    """Ensemble qui contiendra les personnes dans notre casino"""
    def __init__(self, name : str) -> None :
        self.name : str = name
    def speak(self, message:str) -> None:
        print(f"{self.name} : {message}")

class Token() :
    def __init__(self) -> None:
        self.number : int = 0
    def add(self, quantity : int)  -> None:
        self.number+=quantity

class Player(Person) :
    """Elément de notre ensemble Person"""
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self.token = Token()
        self.interact : str = ""
        self.mise : int = 0
        self.choice : int = 0
        self.main=Hand()
        self.game_choice : int = 0
    
    def purchase(self, jeu : Game , rising : int)  -> None :
        """PLace les jetons dans le portefeuille"""
        if rising < jeu.min_bet or rising > 1000 :
            raise ValueError("Nombre de jetons invalide")
        else :
            self.token.add(rising)

    def bet(self, mise:int, game : Game) -> int :
        """Crée l'instance de la mise si OK"""
        if not self.token.number >= mise >= game.min_bet :
            raise ValueError("Mise invalide")
        else :
            self.mise=mise
            self.token.number-=mise
            return self.mise
        

    def player_choice(self, choix:int) -> int :
        """Choix du joueur sur le numéro qu'il va jouer"""
        if choix not in range(0,36) :
            raise ValueError("Choix invalide")
        else :
            self.choice=choix
            return self.choice
        
    def player_game_choice(self, choix : int) -> int :
        """Le choix du joueur sur son jeu"""
        game_list: list[Game]=find_game()
        if choix not in range(len(game_list)) :
            raise ValueError("Mauvais choix")
        self.game_choice = choix
        return self.game_choice

class Roulette(Game) :
    """Un élément de notre ensemble Game"""
    def __init__(self) -> None :
        """Les attributs de notre jeu de roulette"""
        super().__init__("Roulette", 2)
    def drawing(self) -> int:
        return random.randint(0,36)
    @mandatory_token_purchase
    @control_bet
    def Play(self, croupier : 'Croupier', joueur:Player) -> None :
        tirage : int = self.drawing()
        croupier.ask_for_choice()
        choix : int = validation_choice(control_int(input(f"{joueur.name} : Je choisis le numéro ")))
        joueur.player_choice(choix)
        croupier.speak(f"Votre choix est validé. Et le numéro qui sort est le : {tirage}")        
        if joueur.choice == tirage:
            joueur.mise*=3 # On triple la mise du joueur si il gagne
            croupier.speak("C'est votre jour de chance on dirait.")
        elif (joueur.choice + tirage) % 2 == 0 :
            joueur.mise = joueur.mise // 2 # On prend la moitié de la mise si il trouve une couleur dans notre programme se sera de même parité
            croupier.speak("Vous pouvez quand même récupérer une partie de la mise")
        else :
            joueur.mise = 0 # On rafle le jackpot. Nous sommes le casino
            croupier.speak("Perdu.")
        joueur.token.number+=joueur.mise
        croupier.update_info(joueur)


class BlackJack(Game) :
    """Un autre de nos jeu qu'on propose"""
    def __init__(self) -> None:
        super().__init__("BlackJack", 10)
        self.limit_hand : int = 2
    def Play(self, croupier : 'Croupier', joueur:Player) -> None:
        print("Jeu encore indisponible")


def distribute(pack:Pack52, joueur : Player,croupier : Croupier, jeu : BlackJack)  -> None:
    """Fonction qui distribuera les pièces de domino, les cartes ou même les mandales"""
    random.shuffle(pack.cartes) # Faut bien s'assurer que le paquet soit mélanger. Pas de fausse coupe
    while len(joueur.main.pieces) < jeu.limit_hand and len(croupier.main.pieces) < jeu.limit_hand :
        joueur.main.add(pack.cartes.pop())
        croupier.main.add(pack.cartes.pop())
            
class Croupier(Person) :
    """Un autre élément de notre ensemble Person"""
    def __init__(self, name: str = "") -> None:
        super().__init__("Croupier ")
        self.main=Hand()
        self.notebook:list[str]=[]
    def welcome(self)  -> None :
        """Juste un message de bienvenue dans le casino"""
        messages: list[str] = [
        "Ah, un nouveau pigeon... heu, joueur ! Bienvenue !",
        "Vos économies nous intéressent... heu, bienvenue au casino !", 
        "Prêt à transformer vos jetons en souvenirs ? Bienvenue !",
        "Encore un optimiste ! Ravis de vous voir... et votre portefeuille."
    ]
        self.speak(random.choice(messages))
    def invite_to_play(self) -> None :
        """Le croupier invite le joueur à se faire plumer"""
        messages: list[str] = [
        "Alors, prêt à tester notre théorie : 'La maison gagne toujours' ?",
        "Voulez-vous participer à notre programme de redistribution de richesse ?",
        "Envie de confirmer les lois des probabilités ? À nos dépens, bien sûr !",
        "Prêt à jouer ? On parie que vous allez dire oui ?"
    ]
        self.speak(f"{random.choice(messages)} et fais pas le con c'est O pour oui et N pour non.")
    def game_management(self, joueur : Player) -> None :
        """Le croupier enregistre le joueur si il veut jouer sinon il lui dit au revoir"""
        if joueur.interact.lower() == "o" :
            self.notebook.append(joueur.name)
            messages: list[str] = [
            f"Très bien {joueur.name}, combien voulez-vous investir dans notre fonds de pension ?",
        "Parfait ! Maintenant, la partie amusante : donnez-nous votre argent.",
        "Excellent choix ! Maintenant, parlons de votre contribution... heu, achat de jetons.",
        "Génial ! Combien voulez-vous convertir en jolis ronds de plastique ?"
        ]
            self.speak(f"{random.choice(messages)}.")
        else :
            self.speak("Peut-être une prochaine fois alors")

    def ask_for_choice(self) -> None :
        """Le croupier demande le numéro choisi par le joueur"""
        self.speak("Très bien. Il maintenant temps de choisir votre numéro porte bonheur.")
    def ask_for_game(self)  -> None :
        """Le croupier demande à quel sauce le pigeaon veut être cuisiner"""
        game_list: list[Game]=find_game()
        self.speak(f"Voici les jeux que nous proposons : \n🎲 **NOTE IMPORTANTE** : Pitié, ne choisis pas le BlackJack ! Il n'est pas fini et le jeu tournera en boucle pour rien, puisqu'il n'y a pas de fonctionnalité pour changer de jeu ! 😅\n")
        for i, jeu in enumerate(game_list, 1):
            print(f"{i}. {jeu.game_name}")
        messages: list[str] = [
        "Alors, comment souhaitez-vous vous ruiner aujourd'hui ?",
        "Choisissez votre poison... heu, votre jeu préféré !",
        "Quelle sera votre méthode de donation aujourd'hui ?",
        "Voyons voir comment vous allez enrichir notre casino..."
    ]
        self.speak(random.choice(messages))
    def valid_game(self, joueur:Player) -> None :
        """Le croupier valide la recette"""
        game_list: list[Game]=find_game()
        messages: list[str] = [
        f"Excellent ! {game_list[joueur.game_choice].game_name}, le jeu où l'espoir fait vivre... pas votre portefeuille !",
        f"Parfait choix ! {game_list[joueur.game_choice].game_name}, là où la chance sourit... surtout à nous !",
        f"Ah, {game_list[joueur.game_choice].game_name} ! Le jeu préféré de nos actionnaires !",
        f"{game_list[joueur.game_choice].game_name} ! Vous avez bon goût... en pertes d'argent !"
    ]
        self.speak(random.choice(messages))
    def update_info(self, joueur : Player) -> None :
        """Juste une mise à jour des infos"""
        messages: list[str] = [
        f"Vous avez {joueur.token.number} jetons... pour l'instant !",
        f"Rapport financier : {joueur.token.number} jetons restants... ça diminue vite !",
        f"État de votre fortune : {joueur.token.number} jetons. Nos actionnaires vous remercient !",
        f"Score actuel : {joueur.token.number} jetons. Le casino : toujours gagnant !"
    ]
        self.speak(random.choice(messages))


def control_O_N(rep : str)  -> str:
    """Fonction qui contrôlera les réponses avec oui ou non comme réponses attendu."""
    while True :
        if rep.lower() in ["o","n"] :
            return rep
        else :
            rep=input("Saisie invalide. Veuillez recommencer : ")

def control_int(value:str) -> int:
    """Permettra de faire une resaisie si la valeur saisie n'est pas numérique"""
    while True :
        try :
            return int(value)
        except ValueError :
            value=input("Saisie invalide. Veuillez recommencer : ")

def validation_choice(choix:int) -> int:
    while choix not in range(0,37):
        choix=control_int(input("Votre choix est invalide. Veuillez recommencer : "))
    return choix

def find_game() -> list[Game]:
    """Retourne les instances de jeux disponibles"""
    game_list:list[Game]=[]
    module_actual: types.ModuleType=sys.modules[__name__]
    for nom, obj in inspect.getmembers(module_actual):
        if inspect.isclass(obj) and issubclass(obj,Game) and obj!=Game :
            try :
                game_list.append(obj()) # type: ignore  # ✅ "Je sais ce que je fais !"
            except :
                continue
    return game_list

def validation_game_choice(choix:int,) -> int :
    """Permettra au pigeon de choisir ou il veut se faire plumer"""
    game_list: list[Game]=find_game()
    while choix not in range(1,len(game_list)+1):
        choix=control_int(input(f"❌ Choix {choix} invalide. Choisissez entre 1 et {len(game_list)}. Veuillez choisir un jeu existant"))
    choix-=1
    return choix

def start(joueur : Player,croupier : Croupier) -> None:
    game_list: list[Game]=find_game() # Nous permet de récuperer la liste des jeux plus tard
    continue_partie : bool = False
    joueur.name=(input("Veuillez saisir votre nom pour commencer à jouer : ")) # Le joueur doit d'abord entrer son nom
    croupier.welcome() # Message de bienvenu de la part du croupier
    joueur.interact=input(f"{joueur.name} : ") # Interaction cosmétique. L'utilisateur peut saisir absolument tout ce qu'il veut
    croupier.ask_for_game() # Le croupier demande à l'utilisateur de choisir un jeu
    choix : int = validation_game_choice(control_int(input(f"{joueur.name} : Je Vais jouer au/à la "))) # Stockera le choix du joueur
    joueur.player_game_choice(choix) # Va aller informer la classe de la valeur du choix du joueur
    croupier.valid_game(joueur) # Le croupier valide seulement le choix du joueur
    jeu_choisi: Game=game_list[choix] # On récupère le jeu en fonction du choix du joueur
    croupier.invite_to_play() # Le croupier demande si il veut vraiment jouer. On implémentera plus tard le fait de changer de choix
    joueur.interact=control_O_N(input(f"{joueur.name} : ")) # Réponse du joueur par oui ou non
    croupier.game_management(joueur)
    if joueur.interact.lower() == "o" :
        """C'est ici que la partie commence"""
        jeu_choisi.Play(croupier, joueur) # Lance le jeux choisi par le joueur
        while not continue_partie :
            croupier.speak("Voulez vous rejouer ou tenter une autre partie ? O pour oui et N pour non : ")
            joueur.interact=control_O_N(input(f"{joueur.name} : "))
            if joueur.interact.lower() == "o" :
                if joueur.token.number < jeu_choisi.min_bet :
                    croupier.speak("Malheureusement vous n'avez plus assez de jetons. Veuillez en reprendre. Combien en voulez vous?")
                    jeu_choisi.Play(croupier, joueur)
                else :
                    jeu_choisi.Play(croupier, joueur)
            else :
                continue_partie=True
                croupier.speak("Merci d'avoir joué avec nous")
    else :
        croupier.speak("A une prochaine fois peut-être")

if __name__ == "__main__":
    player=Player()
    croupier=Croupier()
    start(player,croupier)
