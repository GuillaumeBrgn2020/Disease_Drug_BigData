# Déroulement d'une requête

On souhaite :
- à partir d'un symptôme (manifestation ou effet secondaire), renvoyer l'ensemble des maladies et des médicaments qui pourraient la causer
- à partir d'un symptôme causé par une maladie, renvoyer la liste des médicaments qui pourraient traiter la maladie
- à partir d'un symptôme causé par des médicaments, renvoyer la liste des médicaments qui pourraient traiter l'effet secondaire
- dans le cas d'une requête à symptômes multiples, on renvoie l'intersection des résultats pour chaque symptôme

Le déroulement de la requête :
- on reçoit un symptôme
- on cherche sa liste de synonymes ***synonyms*** (*HPO*), soit :
    - le symptôme est listé et on récupère sa liste de synonymes
    - le symptôme est pas listé et on le cherche parmi les listes de synonymes
    ?
- pour chaque synonyme :
    - on rérupère son ***idSymptom*** (*HPO*)
    - grâce à son ***idSymptom*** (*HPO*), on récupère son ***idOmim*** (*HPO Annotation*), s'il existe
    - on fait correspondre son ***idOmim*** (*HPO Annotation*) à son ***FIELD NO*** (*omim.txt*), ce qui permet de faire la liste des maladies génétiques ayant ce synonyme dans son ***FIELD CS*** (*omim.txt*)
    => on obtient la liste des noms de maladies ayant ce symptôme

    - on récupère la liste des ***id*** (*drugbank.xml*) de médicaments pour lesquels le synonyme apparait comme ***indication*** (*drugbank.xml*), c'est alors un médicament de traitement, ou comme ***toxicity*** (*drugbank.xml*), c'est alors un médicament qui a causé l'effet secondaire
    - on faire correspondre l'***id*** (*drugbank*) à l'***idStitch*** (*br08303.keg*) pour récupérer son ***label*** (*br08303.keg*)
    => on obtient la liste des noms de médicaments pour traiter le symptôme
    => on obtient la liste des noms de médicaments qui ont ce symptôme comme effet secondaire

    - on fait correspondre ***idOmim*** (*HPO Annotation*) à l'***FIELD NO*** (*omim.txt*)
    - on fait correspondre ***FIELD NO*** (*omim.txt*) à ***Class ID*** (*omim.csv*) ?
    => ?

    - on trouve le ***CUI*** (*omim.csv*) du synonyme ?
    - on fait correspondre le ***CUI*** (*omim.csv*) au ***CUI*** (*Sider*) pour récupérer l'***idStitch*** (*Sider*) et faire la liste des indications et effets secondaires
    - on fait correspondre chaque ***idStitch*** (*Sider*) à l'***idStitch*** (*br08303.keg*) pour récupérer son ***label*** (*br08303.keg*)
    => on obtient la liste des noms de médicaments pour traiter le symptôme
    => on obtient la liste des noms de médicaments qui ont ce symptôme comme effet secondaire

