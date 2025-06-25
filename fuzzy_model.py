import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variables de entrada
acidez = ctrl.Antecedent(np.arange(4.0, 7.1, 0.1), 'acidez')
cafeina = ctrl.Antecedent(np.arange(0.5, 2.1, 0.1), 'cafeina')
humedad = ctrl.Antecedent(np.arange(5.0, 13.0, 0.1), 'humedad')
aroma = ctrl.Antecedent(np.arange(1, 11, 1), 'aroma')

# Salida
calidad = ctrl.Consequent(np.arange(0, 11, 1), 'calidad')

# Funciones de membresía
acidez['baja'] = fuzz.trimf(acidez.universe, [4.0, 4.5, 5.0])
acidez['media'] = fuzz.trimf(acidez.universe, [4.8, 5.5, 6.2])
acidez['alta'] = fuzz.trimf(acidez.universe, [5.8, 6.5, 7.0])

cafeina['baja'] = fuzz.trimf(cafeina.universe, [0.5, 0.7, 1.0])
cafeina['media'] = fuzz.trimf(cafeina.universe, [0.9, 1.2, 1.5])
cafeina['alta'] = fuzz.trimf(cafeina.universe, [1.4, 1.7, 2.0])

humedad['baja'] = fuzz.trimf(humedad.universe, [5.0, 6.0, 7.0])
humedad['media'] = fuzz.trimf(humedad.universe, [6.5, 8.0, 9.5])
humedad['alta'] = fuzz.trimf(humedad.universe, [9.0, 11.0, 13.0])

aroma['débil'] = fuzz.trimf(aroma.universe, [1, 2, 4])
aroma['medio'] = fuzz.trimf(aroma.universe, [3, 5, 7])
aroma['intenso'] = fuzz.trimf(aroma.universe, [6, 8, 10])

calidad['baja'] = fuzz.trimf(calidad.universe, [0, 0, 4])
calidad['media'] = fuzz.trimf(calidad.universe, [3, 5, 7])
calidad['alta'] = fuzz.trimf(calidad.universe, [6, 10, 10])

# Reglas
regla1 = ctrl.Rule(aroma['intenso'] & humedad['baja'], calidad['alta'])
regla2 = ctrl.Rule(acidez['media'] & cafeina['media'] & aroma['medio'], calidad['media'])
regla3 = ctrl.Rule(acidez['baja'] | cafeina['alta'] | humedad['alta'], calidad['baja'])
regla4 = ctrl.Rule(aroma['medio'] & humedad['media'], calidad['media'])
regla5 = ctrl.Rule(acidez['alta'] & cafeina['baja'] & aroma['intenso'], calidad['alta'])

# Sistema y simulador
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
simulador = ctrl.ControlSystemSimulation(sistema_control)

# Función para usar desde Flask
def clasificar_calidad(acidez_val, cafeina_val, humedad_val, aroma_val):
    simulador.input['acidez'] = acidez_val
    simulador.input['cafeina'] = cafeina_val
    simulador.input['humedad'] = humedad_val
    simulador.input['aroma'] = aroma_val
    simulador.compute()
    valor = simulador.output['calidad']
    if valor < 4:
        return f"{valor:.2f} → Baja"
    elif valor < 7:
        return f"{valor:.2f} → Media"
    else:
        return f"{valor:.2f} → Alta"
