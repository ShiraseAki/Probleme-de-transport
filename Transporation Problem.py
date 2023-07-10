from pulp import *

# la taille du probleme est fixé
print("c'est un probleme de transport de taille 3x3 ")


# La saisie des disponobilité

a = int(input("Veuillez entrer la disponibilité 1 :"))
b = int(input("Veuillez entrer la disponibilité 2 :"))
c = int(input("Veuillez entrer la disponibilité 3 :"))

# la saisie des demandes

A = int(input("Veuillez entrer la demande 1 :"))
B = int(input("Veuillez entrer la demande 2 :"))
C = int(input("Veuillez entrer la demande 3 :"))

# La saisie des couts de transport

A1 =int(input("cout de transport de source A au destination 1:"))
A2 =int(input("cout de transport de source A au destination 2:"))
A3 =int(input("cout de transport de source A au destination 3:"))
B1 =int(input("cout de transport de source B au destination 1:"))
B2 =int(input("cout de transport de source B au destination 2:"))
B3 =int(input("cout de transport de source B au destination 3:"))
C1 =int(input("cout de transport de source C au destination 1:"))
C2 =int(input("cout de transport de source C au destination 2:"))
C3 =int(input("cout de transport de source C au destination 3:"))


# Creation d'une liste des sources
warehouses = ["A", "B", "C"]

# creation d'un dictionnaire des disponibilités pour chaque nœuds
supply = {"A": a, "B": b, "C":c}

# Creation d'une liste de tous les nœuds des demandes
projects = ["1", "2", "3"]

# creation d'un dictionnaire pour le nombre d'unités de demande pour chaque nœud de demande
demand = {
    "1": A,
    "2": B,
    "3": C,
}

# Crée une liste des coûts de chaque route
costs = [
    [A1,A2,A3],  # A   entrepôts
    [B1,B2,B3],  # B
    [C1,C2,C3]   # C
]

# Les données de coût sont transformées en dictionnaire
costs = makeDict([warehouses, projects], costs, 0)

# Crée la variable 'prob' pour contenir les données du problème
prob = LpProblem("Material Supply Problem", LpMinimize)

# Crée une liste de tuples contenant tous les itinéraires possibles pour le transport
Routes = [(w, b) for w in warehouses for b in projects]

# Un dictionnaire appelé 'Vars' est créé pour contenir les variables référencées (les routes)
vars = LpVariable.dicts("Route", (warehouses, projects), 0, None, LpInteger)
# La fonction objectif minimum est ajoutée à 'prob' en premier
prob += (
    lpSum([vars[w][b] * costs[w][b] for (w, b) in Routes]),
    "Sum_of_Transporting_Costs",
)


#Les contraintes maximales d'approvisionnement sont ajoutées à prob pour chaque nœud d'approvisionnement (entrepôts)
for w in warehouses:
    prob += (
        lpSum([vars[w][b] for b in projects]) <= supply[w],
        "Sum_of_Products_out_of_warehouses_%s" % w,
    )

# Les contraintes minimales de demande sont ajoutées à prob pour chaque nœud de demande
for b in projects:
    prob += (
        lpSum([vars[w][b] for w in warehouses]) >= demand[b],
        "Sum_of_Products_into_projects%s" % b,
    )

    # Le problème est résolu en utilisant le choix de PuLP du solveur
    prob.solve()

    # Montrer la valeur optimisée des variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # La valeur de la fonction objectif optimisée est montrée à l'écran
    print("Value of Objective Function = ", value(prob.objective))
