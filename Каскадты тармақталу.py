#Каскадты тармақталу — бір шартты тексеруден кейін келесі шартты тексеру қажет болғанда қолданылады

"""
if шарт_1:
    # Шарт_1 орындалса орындалатын код
elif шарт_2:
    # Шарт_2 орындалса орындалатын код
elif шарт_3:
    # Шарт_3 орындалса орындалатын код
else:
    # Егер жоғарыдағы шарттардың ешқайсысы орындалмаса, орындалатын код
"""

"""
Мысал 1: Студенттің бағасын анықтау
Оқушының балын енгізіп, сәйкес баға беріңіз:

90-100: "Өте жақсы" 
75-89: "Жақсы"
50-74: "Қанағаттанарлық"
50-ден төмен болса: "Нашар"
"""

baga = int(input("Баға енгіз"))

if 90 <= baga <= 100:
    print("Өте жақсы")
elif 75 <= baga <= 89:
    print("Жақсы")
elif 50 <= baga <= 74:
    print("Қанағаттанарлық")
elif baga < 50:
    print("Нашар")

