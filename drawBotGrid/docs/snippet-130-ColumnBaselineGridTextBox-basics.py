from drawBot import *
import pathlib

# <include> ----------------------------------------
from drawBotGrid import BaselineGrid, columnBaselineGridTextBox

newPage("A4Landscape")

# </include> ----------------------------------------
fill(1, 1, 1, .5)
rect(0, 0, width(), height())
# <include> ----------------------------------------

fill(0)
font("Georgia")
fontSize(8)
lineHeight(10)
hyphenation(True)

baselines = BaselineGrid.from_margins((0, -50, 0, -50), 10)
baselines.draw()

text = """Longtemps, je me suis couché de bonne heure. Parfois, à peine ma bougie éteinte, mes yeux se fermaient si vite que je n’avais pas le temps de me dire: «Je m’endors.» Et, une demi-heure après, la pensée qu’il était temps de chercher le sommeil m’éveillait; je voulais poser le volume que je croyais avoir encore dans les mains et souffler ma lumière; je n’avais pas cessé en dormant de faire des réflexions sur ce que je venais de lire, mais ces réflexions avaient pris un tour un peu particulier; il me semblait que j’étais moi-même ce dont parlait l’ouvrage: une église, un quatuor, la rivalité de François Ier et de Charles Quint. Cette croyance survivait pendant quelques secondes à mon réveil; elle ne choquait pas ma raison mais pesait comme des écailles sur mes yeux et les empêchait de se rendre compte que le bougeoir n’était plus allumé. Puis elle commençait à me devenir inintelligible, comme après la métempsycose les pensées d’une existence antérieure; le sujet du livre se détachait de moi, j’étais libre de m’y appliquer ou non; aussitôt je recouvrais la vue et j’étais bien étonné de trouver autour de moi une obscurité, douce et reposante pour mes yeux, mais peut-être plus encore pour mon esprit, à qui elle apparaissait comme une chose sans cause, incompréhensible, comme une chose vraiment obscure. Je me demandais quelle heure il pouvait être; j’entendais le sifflement des trains qui, plus ou moins éloigné, comme le chant d’un oiseau dans une forêt, relevant les distances, me décrivait l’étendue de la campagne déserte où le voyageur se hâte vers la station prochaine; et le petit chemin qu’il suit va être gravé dans son souvenir par l’excitation qu’il doit à des lieux nouveaux, à des actes inaccoutumés, à la causerie récente et aux adieux sous la lampe étrangère qui le suivent encore dans le silence de la nuit, à la douceur prochaine du retour. J’appuyais tendrement mes joues contre les belles joues de l’oreiller qui, pleines et fraîches, sont comme les joues de notre enfance. Je frottais une allumette pour regarder ma montre. Bientôt minuit. C’est l’instant où le malade, qui a été obligé de partir en voyage et a dû coucher dans un hôtel inconnu, réveillé par une crise, se réjouit en apercevant sous la porte une raie de jour. Quel bonheur, c’est déjà le matin! Dans un moment les domestiques seront levés, il pourra sonner, on viendra lui porter secours. L’espérance d’être soulagé lui donne du courage pour souffrir. Justement il a cru entendre des pas; les pas se rapprochent, puis s’éloignent. Et la raie de jour qui était sous sa porte a disparu. C’est minuit; on vient d’éteindre le gaz; le dernier domestique est parti et il faudra rester toute la nuit à souffrir sans remède. Je me rendormais, et parfois je n’avais plus que de courts réveils d’un instant, le temps d’entendre les craquements organiques des boiseries, d’ouvrir les yeux pour fixer le kaléidoscope de l’obscurité, de goûter grâce à une lueur momentanée de conscience le sommeil où étaient plongés les meubles, la chambre, le tout dont je n’étais qu’une petite partie et à l’insensibilité duquel je retournais vite m’unir. Ou bien en dormant j’avais rejoint sans effort un âge à jamais révolu de ma vie primitive, retrouvé telle de mes terreurs enfantines comme celle que mon grand-oncle me tirât par mes boucles et qu’avait dissipée le jour,--date pour moi d’une ère nouvelle,--où on les avait coupées. J’avais oublié cet événement pendant mon sommeil, j’en retrouvais le souvenir aussitôt que j’avais réussi à m’éveiller pour échapper aux mains de mon grand-oncle, mais par mesure de précaution j’entourais complètement ma tête de mon oreiller avant de retourner dans le monde des rêves."""*2
columnBaselineGridTextBox(text, (50, 50, width()-100, height()-100), baselines, subdivisions=4, gutter=40, draw_grid=True)

# </include> ----------------------------------------

fill(None)
stroke(.5)
rect(0, 0, width(), height())
out_path = pathlib.Path(__file__).with_suffix(".png")
saveImage(out_path, imageResolution=144)
