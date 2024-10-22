# START
import requests
import GetToken as gt
from colorCHECK import colorCHECK
import users
import numpy as np
from tensorflow import keras

# data
TOKEN = gt.get_token()
# data

def get_posts_photo(user_id: str, token):
    res_photos = [[],[]]
    count_posts = 50
    filter = "owner"
    offset = 0
    urlWallGetById = 'https://api.vk.com/method/wall.get'
    paramsForWallGetById = {
        'access_token': token,
        'owner_id': f'{user_id}',
        'offset': f'{offset}',
        'count': f'{count_posts}',
        'filter': f'{filter}',
        'v': '5.131'  # Версия API
    }
    responseForWallGetById = requests.get(urlWallGetById, params=paramsForWallGetById)
    dataForWallGetById = responseForWallGetById.json()
    for elements in dataForWallGetById['response']['items']:
        for element in elements['attachments']:  # Указываем параметр, который нас интересует в посте
            if('photo' in element):
                print(element['photo'])
                photo = element['photo']['orig_photo']['url']
                photoId = element['photo']['id']
                res_photos[0].append(photo)
                res_photos[1].append(photoId)
    return res_photos


def userGetInfo(user_id: str, token, choice):
    count_posts = 50
    filter = "owner"
    offset = 0
    urlWallGetById = 'https://api.vk.com/method/wall.get'
    paramsForWallGetById = {
        'access_token': token,
        'owner_id': f'{user_id}',
        'offset': f'{offset}',
        'count': f'{count_posts}',
        'filter': f'{filter}',
        'v': '5.131'  # Версия API
    }
    responseForWallGetById = requests.get(urlWallGetById, params=paramsForWallGetById)
    dataForWallGetById = responseForWallGetById.json()
    if (choice == "text"):
        print(f"Проверка на {choice}")
        for elements in dataForWallGetById['response']['items']:
            if (elements['text'] != ""):
                print("--------------------------------------")
                print(f"id => {elements['id']}")
                print(elements['text'])
                print("--------------------------------------\n")
            else:
                print("--------------------------------------")
                print(f"id => {elements['id']}")
                print("Текста нет")
                print("--------------------------------------\n")

    if (choice == "photo"):
        print(f"Проверка на {choice}")
        for elements in dataForWallGetById['response']['items']:
            for element in elements['attachments']:  # Указываем параметр, который нас интересует в посте
                photo = element['photo']['orig_photo']
                # print(photo)
                if (photo['url'] != ""):
                    print("--------------------------------------")
                    print(f"id => {elements['id']}")
                    print(f"Size original photo: {photo['width']}x{photo['height']}")
                    print(f"Type => {element['type']}")
                    print(f"Photo url => {photo['url']}")
                    print("--------------------------------------\n")

                else:
                    print("--------------------------------------")
                    print(f"id => {elements['id']}")
                    print("фото нет")
                    print("--------------------------------------\n")


# Функция для установки цвета текста с использованием ANSI escape codes
def print_rgb(r, g, b, text):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")


def whatIsColorMean(indexLargeElement):
    if indexLargeElement == 0:
        return (
            "Синий и его оттенки доминируют"
            "Это означает, что:\n"
            "Синий тип - спокойный и уверенный в себе человек. Таким людям важно чувствовать себя в безопасности, быть всегда защищенными."
        )

    if indexLargeElement == 1:
        return (
            "Желтый доминирует\n"
            "Это означает, что:\n"
            "Желтый тип - общительный, отзывчивый человек. Им хорошо подходят широкие социальные контакты."
        )

    if indexLargeElement == 2:
        return (
            "Зеленый доминирует\n"
            "Это означает, что:\n"
            "Зеленый тип - настойчивый, но робкий человек. Ему комфортно в условиях, которые дают ощущение значимости и достоинства."
        )

    if indexLargeElement == 3:
        return (
            "Красный доминирует\n"
            "Это означает, что:\n"
            "Красный тип - энергичный человек. Такие люди чувствуют себя комфортно в активной деятельности."
        )

    return "Некорректный индекс цвета."



def testLusher(x):
    modelBlue = keras.models.load_model('AiModel/my_model.keras')
    modelYellow = keras.models.load_model('AiModel/my_modelYELLOW.keras')
    modelGreen = keras.models.load_model('AiModel/my_modelGREEN.keras')
    modelRed = keras.models.load_model('AiModel/my_modelRED.keras')
    # model.summary()

    predictionBlue = modelBlue.predict(x)
    predictionYellow = modelYellow.predict(x)
    predictionGreen = modelGreen.predict(x)
    predictionRed = modelRed.predict(x)

    sumPrediction = [sum(predictionBlue), sum(predictionYellow), sum(predictionGreen), sum(predictionRed)]
    indexLargeElement = sumPrediction.index(max(sumPrediction))
    testResult = whatIsColorMean(indexLargeElement)

    return testResult

    # print("Вывод для наглядного просмотра")
    #
    # print("For Blue")
    # InputDatasize = x.size
    # counter = 0
    # for i in predictionBlue:
    #     if (counter < InputDatasize):
    #         print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
    #         counter += 1
    #
    # print("For Yellow")
    # InputDatasize = x.size
    # counter = 0
    # for i in predictionYellow:
    #     if (counter < InputDatasize):
    #         print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
    #         counter += 1
    #
    # print("For Green")
    # InputDatasize = x.size
    # counter = 0
    # for i in predictionGreen:
    #     if (counter < InputDatasize):
    #         print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
    #         counter += 1
    #
    # print("For Red")
    # InputDatasize = x.size
    # counter = 0
    # for i in predictionRed:
    #     if (counter < InputDatasize):
    #         print_rgb(x[counter][0], x[counter][1], x[counter][2], i)
    #         counter += 1


def startTestLusher(user_id: str):
    testResult = []
    result = get_posts_photo(user_id,TOKEN)
    print(result)

    indexPhoto = 0
    for i in result[0]:
        print("New url => " + i)
        string = ("Индекс поста: " + str(result[1][indexPhoto]) + "\nНейросеть определила, что в данной фотографии ")
        testResult.append(string + testLusher(np.array(colorCHECK(i,3))))
        indexPhoto+=1


    # print(testResult)
    return testResult
