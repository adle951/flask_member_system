import pymongo
from flask import *
from pymongo.mongo_client import MongoClient

# 初始化資料庫連線
uri = "mongodb+srv://leo:1qaz2wsx@cluster0.im14enu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.member_system
print("資料庫連線成功")
# 初始化 Flask 伺服器
app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key = "any"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" not in session:
        return redirect("/")
    return render_template("member.html",nickname=session["nickname"] )

@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤，請聯繫客服人員")
    return render_template("error.html", message=message)

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]
    collection = db.users
    result = collection.find_one({
        "$and" : [
            {"email" : email},
            {"password" : password}
        ]
    })
    if result == None:
        return redirect("/error?msg=帳號或密碼錯誤")
    session["nickname"] = result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")

@app.route("/signup", methods=["POST"])
def signup():
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    collection = db.users
    result = collection.find_one({
        "email" : email
    })
    if result != None:
        return redirect("/error?msg=信箱已被註冊")
    collection.insert_one({
        "nickname" : nickname,
        "email" : email,
        "password" : password
    })
    return redirect("/")
app.run(port=3000)