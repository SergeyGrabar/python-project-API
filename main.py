import requests
import json
import datetime
from tabulate import tabulate

API_KEY = "9e5b707b2d96dad45953a0e75652a1a0"

class SaveToFile:
    def save(self, obj, file):
        with open(file, "w") as file:
            json.dump(obj, file, indent=4, ensure_ascii=False)

class GenerateUserData:
    def __init__(self):
        self.userData = self.getUserData()

    def getUserData(self):

        url = "https://randomuser.me/api"

        params = {
            "nat": "UA",
            "inc": "name,location,email,phone"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)

    def getCoordinates(self):
        data = self.userData
        sityName = data["results"][0]["location"]["city"]

        url = "http://api.openweathermap.org/geo/1.0/direct"

        param = {
            "q": sityName,
            "appid": API_KEY
        }

        response = requests.get(url, params=param)
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
        
    def currentWeatherData(self):
        data = self.userData
        sityName = data["results"][0]["location"]["city"]
        coord = self.getCoordinates()
        for i in coord:
            lat = i["lat"]
            lon = i["lon"]

            url = "https://api.openweathermap.org/data/3.0/onecall"

            params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": API_KEY,
                    "units": "metric",
                    "lang": "ua"
                }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                response = response.json()
                temp = response["hourly"][0]["temp"]
                date = response["hourly"][0]["dt"]
                date_time = datetime.datetime.fromtimestamp(date)
                self.userData["results"][0]["weather"] = {"sity": sityName, "date": f"{date_time}", "temp": temp}
                return f"Температура в місті {sityName} {temp}C"
            else:
                return response.text

    def historicalWeatherData(self, date):
        data = self.userData
        sityName = data["results"][0]["location"]["city"]
        coord = self.getCoordinates()
        for i in coord:
                lat = i["lat"]
                lon = i["lon"]

                url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"

                params = {
                    "lat": lat,
                    "lon": lon,
                    "date": date,
                    "appid": API_KEY,
                    "units": "metric",
                    "lang": "ua"
                }

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    response = response.json()
                    temp = response["temperature"]["afternoon"]
                    return f"Температура в місті {sityName} за {date} {temp}C"
                else:
                    return response.text

class Edit(GenerateUserData):
    def editData(self):
        data = self.userData
        results = data["results"][0]
        try:
            while True:
                print("Меню редагування".center(50, "="))

                infoInput = ""
                for value in results.keys():
                    infoInput += f"{value.title()}\n"
                section = input(f"\n{infoInput}Choice: ")

                if section in results:
                    if isinstance(results[section], str):
                        results[section] = input("Введіть: ")
                        self.userData["results"][0] = results
                    else:
                        listSercion = ["first", "last", "city", "state", "country"]
                        infoInput = ""
                        for value in results[section].keys():
                            if value not in listSercion:
                                continue
                            infoInput += f"{value.title()}\n"
                        subsection = input(f"\n{infoInput}Choice: ")

                        if subsection in results[section]:
                            if isinstance(results[section][subsection], str):
                                results[section][subsection] = input("Введіть: ")
                                self.userData["results"][0] = results
                        else:
                            print("Поле відсутне!")
                else:
                    print("Поле відсутне!")

                choice = input("Вийти? [y/n]: ")
                if choice == "y":
                    break
        except ValueError:
            print("Помилка")

    def __str__(self):
        table = []
        for result in self.userData['results']:
            row = [
                result['name']['first'],
                result['name']['last'],
                result['email'],
                result['phone'],
                result['location']['city'],
                result['location']['state'],
                result['location']['country']
            ]
            table.append(row)
        
        return tabulate(
            tabular_data=table,
            headers=['First Name', 'Last Name', 'Email', 'Phone', 'City', 'State', 'Country'],
            tablefmt="fancy_grid"
        )

class App(SaveToFile, Edit):
    def run(self):
        while True:
            print("Головне меню".center(50, "="))
            try:
                choice = int(input("[1]Показати данні\n[2]Редагувати данні\n[3]Зберегти данні\n[4]Поточна погода в місті\n[5]Історичні данні погоди в місті\n[6]Вихід\nВибір: "))
                match choice:
                    case 1:
                        print(app)
                    case 2:
                        self.editData()
                    case 3:
                        self.save(self.userData, "randomuser.json")
                    case 4:
                        print(self.currentWeatherData())
                    case 5:
                        print(self.historicalWeatherData(input("Введіть дату(РРРР-ММ-ДД): ")))
                    case 6:
                        break
                    case _:
                        print(f"п.{choice} в меню нема")
            except ValueError:
                print("Не вірний ввід")

app = App()
app.run()