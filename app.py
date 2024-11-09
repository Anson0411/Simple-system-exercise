import pymongo
from flask import *
client = pymongo.MongoClient("mongodb+srv://root:root123@cluster0.ol6ob.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.member_system
print("資料庫建立成功")

app = Flask(
    __name__, 
    static_folder="public",
    static_url_path="/"
)
app.secret_key = "any string but secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")
#/error?msg=
@app.route("/error")
def error():
    mess = request.args.get("msg", "發生錯誤請聯繫")
    return render_template("error.html", data=mess)

@app.route("/signup", methods=["POST"])
def sighup():
    # 從前端接收資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    # 根據接收到的資料，和資料庫互動
    collection = db.user
    result=collection.find_one({
        "email":email
    })
    # 檢查會員集合中是否有相同 Email 的文件資料
    if result != None:
        return redirect("/error?msg=信箱已被註冊")
    # 把資料放進資料庫，完成註冊
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者的輸入
    email = request.form["email"]
    password = request.form["password"]
    # 和資料庫互動
    collection = db.user
    # 檢查信箱密碼是否正確
    result = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    # 找不到對應資料，登入失敗，導向錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號或密碼錯誤")
    # 登入成功，在 Session 紀錄會員資訊 導向會員頁面
    session["nickname"] = result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
    # 移除 Sesion 中的會員資訊
    del session["nickname"]
    return redirect("/")


app.run(port=3000)