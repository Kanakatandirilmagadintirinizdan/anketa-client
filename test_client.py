import client

ankety = client.vzyat_ankety()
print("пришло анкет:", len(ankety))

print("статистика:", client.vzyat_statistiku())

print("почта верная:", client.proverit_pochtu("ivanov@mail.ru"))