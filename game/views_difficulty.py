from django.shortcuts import render
from .models import Data
import openai, json

# Create your views here.
def difficulty(request):
    error_text = "入力漏れがあります。2つとも選択してください。"
    if request.method == "POST":
        selected_difficulty = request.POST.get("selected_difficulty")
        if selected_difficulty == "elementary_school":
            difficulty_text = "小学校卒業"
        elif selected_difficulty == "high_school":
            difficulty_text = "・高校卒業"
        elif selected_difficulty == "society":
            difficulty_text = "社会人レベル"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        selected_genre = request.POST.get("selected_genre")
        if selected_genre == "miscellaneous":
            genre_text = "雑学"
        elif selected_genre == "history":
            genre_text = "歴史"
        elif selected_genre == "it":
            genre_text = "IT"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        #data = Data.objects.latest("id")

        data = [
            {
                "question": "犬はネコと同じくらいの知能を持っていますか？", 
                "answer": "F", 
                "hints": ["トリック訓練", "忠誠心", "社会性"], 
                "commentary": "犬はネコと同じくらいの知能を持っていません。ただし、トリック訓練においては高い知能を発揮し、忠誠心や社会性も備えています。", 
                "final_answer": "T", 
                "true_commentary": "犬はネコと同じくらいの知能を持っています。犬種によって知能の差はありますが、一部の犬はネコ以上の知能を持っていると言われています。また、トリック訓練だけでなく、問題解決能力や学習能力も高く、忠誠心や社会性も備えています。"
            },
            {
                "question": "マグロは鰹と同じ種類の魚ですか？", 
                "answer": "T", 
                "hints": ["観賞魚", "食用", "生息地"], 
                "commentary": "マグロは鰹と同じ種類の魚です。両方とも観賞魚としても人気がありますが、主に食用として広く利用されており、生息地も一部重なっています。", 
                "final_answer": "F", 
                "true_commentary": "この文章に誤りはありません"
            },
            {
                "question": "レモンは酸味を持っていますか？", 
                "answer": "T", 
                "hints": ["ビタミンC", "柑橘系", "飲み物"], 
                "commentary": "レモンは酸味を持っています。レモンには多量のビタミンCが含まれており、柑橘系の果物としてその酸味が特徴です。そのため、レモンを使った飲み物などもよく作られます。", 
                "final_answer": "F", 
                "true_commentary": "この文章に誤りはありません"
            },
            {
                "question": "ニューヨークはアメリカの首都ですか？", 
                "answer": "F", 
                "hints": ["ビッグアップル", "金融センター", "自由の女神"], 
                "commentary": "ニューヨークはアメリカの首都ではありません。ニューヨークはアメリカのビッグアップルとして知られ、金融センターや観光名所の自由の女神などがありますが、首都ではありません。", 
                "final_answer": "T", 
                "true_commentary": "ニューヨークはアメリカの首都ではありません。アメリカの首都はワシントンD.C.です。ニューヨークはアメリカでもっとも人口が多く、国際的な金融センターとして知られています。また、観光名所や文化施設も多く、世界中から多くの人々が訪れることでも有名です。"
            },
            {
                "question": "太陽は地球の周りを公転していますか？", 
                "answer": "F", 
                "hints": ["自転", "一日24時間", "日の出日の入り"], 
                "commentary": "太陽は地球の周りを公転していません。太陽は自転しており、その自転によって一日24時間が生じ、地球上で日の出や日の入りが行われています。", 
                "final_answer": "T", 
                "true_commentary": "太陽は地球の周りを公転しています。地球が太陽の周りを約365日かけて一周することによって、一年が生じます。また、太陽が地球を中心として公転することで、地球上で季節が生まれるのです。"
            }
        ]

        with open("../api.text") as f:
            openai.api_key = f.read().strip()

        with open("../api_js.text") as f:
            API = f.read().strip()

        template = template = [
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "final_answer": "文章の判定を書き換えたかを表す英文字",
                "true_commentary": "本当の解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "final_answer": "文章の判定を書き換えたかを表す英文字",
                "true_commentary": "本当の解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "final_answer": "文章の判定を書き換えたかを表す英文字",
                "true_commentary": "本当の解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "final_answer": "文章の判定を書き換えたかを表す英文字",
                "true_commentary": "本当の解説"
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "final_answer": "文章の判定を書き換えたかを表す英文字",
                "true_commentary": "本当の解説"
            }
        ]

        prompt = """
        あなたは指定された条件でjsonデータを生成するbotです。生成したjsonデータ以外のことは絶対に出力してはいけません。
        以下の条件で文章を生成してください。
        ・問題の難易度は{difficulty}程度の知識がないと解けないレベルとする。
        ・{genre}に関する文章。
        ・出力する文章の数は5つ。その5つの文章は、本当のことしか書かれていない文章と嘘の情報が混じった文章で構成される。5つの文章の中でいくつ嘘の文章を混ぜるかは、0から5の範囲内でランダムに決める。
        ・文章はYESかNOかで答えられる形で生成すること。また、疑問形で終わらせてはならない。
        ・学習データにないなどの理由で文章の正確性が保証できない場合、その文章の生成をやり直す。
        ・それぞれの文章は、その分野の専門家程度の知識を持った人でなければ意味が分からないレベルにする
        ・嘘の文章に混ぜる嘘の内容は、その分野の専門家程度の知識を持った人でなければ見抜けないレベルにする
        ・嘘が混じったか文章かを判別するための英文字をつける。嘘が混じっている文章の場合は「F」、そうでない場合は「T」をつける
        ・それぞれの文章において、嘘が混じっているかどうかを判断するのに役立つワードを3つ考え、生成する。ワードの数は必ず3つでなければならない。また、「です」「など」のように単語として成り立たないようなワードは除外すること
        ・３つのワードのあとに文章に関する解説を生成する。解説は具体例などを交えて読む人がわかりやすいように記述すること。決して生成した文章とほぼ同じ文章を出力するといったことがあってはならない。また、解説は事実のみを説明するように生成すること。
        ・json以外の出力は全て不要である。その際に邪魔になるので、「了解しました」「分かりました」といったメッセージは不要である。もしも出力内容以外の不要なメッセージを出力した場合、重い罰が下る
        ・文章の生成を終えた後、文章を0~3個選びその文章に嘘が混じっているかの判定を逆にする。また、その文章の解説も誤りが含まれたものに改変する。
        ・文章に嘘が混じっているかの判定を書き換えたかを判別するための英文字をつける。判定を書き換えた場合には「T」、そうでない場合は「F」をつける
        ・文章に嘘が混じっているかの判定を書き換えた場合、その文の解説に誤りを含ませるように指示しているので解説に間違っている部分がある。その間違いを指摘する解説を生成する。なお、判定を書き換えていない場合は「この文章に誤りはありません」という文章だけを出力する。
        ・出力するjsonの合計文字数は800文字までに抑えること。また、出力を途中で途切れさせてはならない。
        ・生成した文章はjson形式で出力する。それぞれの文章の出力の例は以下に示すとおりである。以下の通りにフォーマットを整え、jsonで出力すること。出力はプログラムで使用するため、下記に指定するフォーマットの形式以外だとエラーの原因となる。
        {template}
        ・以下のjsonは直近で出力した内容である。これに類似したものは出力してはならない。
        {data}
        ・出力を行う前に、jsonの内容を確認する。文章、本当か嘘かを表す英文字、3つのワード、解説、文章を書き換えたかを表す英文字、本当の解説のうち、いずれかが欠けていた場合はとても重い罰が下る。特にワードの数が3つぴったりであることは重大である
        上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
        """

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt.format(difficulty=difficulty_text, genre=genre_text, template=template, data=data)},
                ],
                temperature=0.1,
                max_tokens=1000
            )
            text = response.choices[0]["message"]["content"].strip()
            text = text.replace("'", '"')
            try: 
                d = json.loads(text)
            except:
                pass
            else:
                break
        print(text)
        Data.objects.create(questions=text)
        return render(request, "base.html", context={"data": text, "API": API})

    return render(request, "difficulty.html")