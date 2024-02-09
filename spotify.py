try:
	import requests as x, random, os, threading, sys, time
except Exception as e :
	print(" Module belum terinstall\n")

domain = "@shutupfvckup.my.id"  # set domain here
sandi = "@MaterACars"  # set password here
capsolver_key = "" # set capsolver api key here
api_spotify = "142b583129b2df829de3656f9eb484e6" # dont change if u dont know how to get api_spotify

class Spotify:
    def __init__(self):
        self.api = x.Session()

    def user_data(self):
        return self.api.get("http://api.suhu.my.id/v2/faker",headers={"User-Agent": "PanelNewbie/0.2 (Linux; rdhoni;) Termux/0.2"}).json()
	
    def create(self, ua, nama, email, sandi, ttl, gender):
        return self.api.post("https://spclient.wg.spotify.com/signup/public/v2/account/create", json={"account_details":{"birthdate":ttl,"consent_flags":{"eula_agreed":True,"send_email":False,"third_party_email":False},"display_name":nama,"email_and_password_identifier":{"email":email,"password":sandi},"gender":gender},"callback_uri":"","client_info":{"api_key":api_spotify,"app_version":"v2","capabilities":[1],"installation_id":"","platform":""},"tracking":{"creation_flow":"","creation_point":"","referrer":""},"recaptcha_token":"","submission_id":""}, headers={"User-Agent":ua,"Content-Type":"application/json"})

    def get_challege_id(self, ua, session_id):
        return self.api.post("https://challenge.spotify.com/api/v1/get-session", json={"session_id":session_id}, headers={"User-Agent":ua}).json()["in_progress"]["challenge_details"]["challenge_id"]
    
    def get_recaptcha_token(self, clientKey):
        taskId = self.api.post("https://api.capsolver.com/createTask", json={
            "clientKey": clientKey,
            "task": {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://www.spotify.com/id-id/signup",
                "websiteKey": "6LeO36obAAAAALSBZrY6RYM1hcAY7RLvpDDcJLy3",
                "pageAction": "signup"
            }
        }).json()["taskId"]
        while(True):
            gRecaptchaResponse = self.api.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": clientKey,
                "taskId": taskId
            })
            if("RecaptchaResponse" in gRecaptchaResponse.text):
                return gRecaptchaResponse.json()["solution"]
            time.sleep(5)
            
    def bypass_challenge_spotify(self, session_id, challenge_id, solution):
        complete_session = self.api.post("https://challenge.spotify.com/api/v1/invoke-challenge-command", json={"session_id":session_id,"challenge_id":challenge_id,"recaptcha_challenge_v1":{"solve":{"recaptcha_token":solution["gRecaptchaResponse"]}}}, headers={"User-Agent":solution["userAgent"]})
        if("completed" in complete_session.text):
            return self.api.post("https://spclient.wg.spotify.com/signup/public/v2/account/complete-creation", json={"session_id": session_id})

class UserThread:
    def main(self, domain, sandi):
        generate_data = Spotify().user_data()
        ua = generate_data["browser"]["user_agent"]
        nama = generate_data["email"]
        nama = nama.split("@")[0]
        gender = random.randint(1, 4)
        email = f'{nama.replace(" ","")}{domain}'.lower()
        ttl = f"{random.randint(1990, 2002)}-{random.randint(10, 12)}-{random.randint(10, 31)}"
        signup = Spotify().create(ua, nama, email, sandi, ttl, gender)
        # print(signup.text)
        if "login_token" in signup.text:
            print(f" Created : {email}")
            with open('account.txt', 'a') as f:
                f.write(f'Email : {email} | Sandi : {sandi}\n')
        elif "challenge" in signup.text:
            print(" Captcha detected, wait...")
            session_id = signup.json()["challenge"]["session_id"]
            challenge_id = Spotify().get_challege_id(ua, session_id)
            solution = Spotify().get_recaptcha_token(capsolver_key)
            bypass = Spotify().bypass_challenge_spotify(session_id, challenge_id, solution)
            if "login_token" in bypass.text:
                print(f" Created : {email}")
                with open('account.txt', 'a') as f:
                    f.write(f'Email : {email} | Sandi : {sandi}\n')
        else:
            None

    def createThread(self):
        try:
            try:
                amount = input(f' Amount : ')
                if int(amount) > 20:  # jangan diganti biar ga error spam
                    sys.exit(f'\n Sebaiknya jangan gegabah terlalu banyak')
                else:
                    print(f"\n Ready Create Spotify Account\n\n Kata sandi : {sandi}\n")
                threads = []
                count = 0
                try:
                    while count < int(amount):
                        thread = threading.Thread(target=self.main, args=(domain, sandi))
                        threads.append(thread)
                        thread.start()
                        count += 1
                     
                    for thread in threads:
                        thread.join()

                    # Credit jangan dihapus kontol
                    print("\n Support Developer: \n - DANA (Aga): 0895415306281 \n - QRIS (Mater): @paymentmater ") 
                    print("\n Detail: \n - Ch: @chsangkara\n - Tele: @MaterACars|@paymentmater")
                    print("\n Take A note Please: \n The official MaterIsACars channel is not mine (MaterACars) anymore, \n so if you want to join my channel, please join @chsangkara, thank you.")
                except KeyboardInterrupt:
                    pass

            except Exception as r:
                None

        except Exception as r:
            None

    def user_main(self):
        green = "\033[0;32m"
        white = "\033[0;37m"
        os.system('cls' if os.name == "nt" else 'clear')
        print(f"{green}\n\n  ()                       \n  /\\          _/_   /)     \n /  )  _   __ /  o // __  ,\n/__/__/_)_(_)<__<_//_/ (_/_ {white}  Agathasangkara{green}\n     /           />     /  \n    '           </     '   \n{white}\n"); UserThread().createThread()
        
if __name__ == "__main__":
    index = UserThread().user_main()