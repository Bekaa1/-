"""
Шартты операторлар — шарттарды тексеріп, нәтиже бойынша әртүрлі әрекеттер орындауға мүмкіндік береді.
Ең негізгі шартты операторлар:

if — егер шарт орындалса, әрекетті орында.
elif — қосымша шарттарды тексеру үшін қолданылады.
else — егер барлық шарттар жалған болса, соңғы әрекетті орында
"""


#Күрделі шарттар логикалық операторлар арқылы бірнеше шарттарды бір уақытта тексеруге мүмкіндік береді. Мысалы:


#Оқушыдан бір санды енгізіп, оның жұп немесе тақ екенін анықтаңыз

#Оқушыдан үш санды енгізіп, олардың ішінен ең үлкенін табыңыз.



#Оқушыдан ай нөмірін енгізіп, сол айдың қай мезгілге жататынын анықтаңыз (қыс, көктем, жаз, күз).

# ai_nomeri = int(input("Ай нөмерін енгіз"))
#
# if ai_nomeri == 3 or ai_nomeri == 4 or ai_nomeri == 5:
#     print("Бұл көктем")
# elif ai_nomeri == 6 or ai_nomeri == 7 or ai_nomeri == 8:
#     print("Бұл Жаз")
# elif ai_nomeri == 9 or ai_nomeri == 10 or ai_nomeri == 11:
#     print("Бұл Күз")
# elif ai_nomeri == 12 or ai_nomeri == 1 or ai_nomeri == 2:
#     print("Бұл Қыс")
# else:
#     print("Дұрыс сан енгіз")

#Сабақта өткен калькулятор есебін қайта жазып көрейік

symbol = input("Символ енгіз! (+,-,*,/)")
san1 = int(input("San1 engiz"))
san2 = int(input("San2 engiz"))

if symbol == '+':
    print(san2 + san1)
elif symbol == '-':
    print(san1 - san2)
elif symbol == '*':
    print(san2 * san1)
elif symbol == '/':
    print(san1 / san2)
else:
    print("Аман енгізсейш!")
