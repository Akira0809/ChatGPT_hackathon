from django.shortcuts import render
from .models import Data
import openai

# Create your views here.
def game(request):
    data= Data.objects.order_by("-created_at").filter()
    questions = []
    answer = []
    hints = []
    commentary = []
    for i in range(5):
        questions.append(data[i]["question"])
        answer.append(data[i]["answer"])
        hints.append(data[i]["hints"])
        commentary.append(data[i]["commentary"])
    return render(request, "base.html", context={"text": text})

def difficulty(request):
    data = Data.objects.all()
    with open("../api.text", "r") as f:
        openai.api_key = f.read().strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": """
                以下の条件で文章を生成してください
                ・VOCALOIDに関する文章。
                ・出力する文章の数は5つ。その5つのうち、4つは本当のことしか書かれていない文章にする。残りの1つは嘘の情報が混じった文章にする。嘘の文章の個数と本当の文章の個数を変えてはならない。もしこの個数を守らなかった場合は重い罰が下る。
                ・文章は疑問形で終わってはならない。
                ・それぞれの文章は、その分野の専門家程度の知識を持った人でなければ意味が分からないレベルにする
                ・嘘の文章に混ぜる嘘の内容は、その分野の専門家程度の知識を持った人でなければ見抜けないレベルにする
                ・嘘が混じっている文章の場合は「F」、そうでない場合は「T」をつける
                ・それぞれの文章において、嘘が混じっているかどうかを考えるのに役立つワードを3つ考え、生成する。ワードの数は必ず3つでなければならない。また、「です」「など」のように単語として成り立たないようなワードは除外すること
                ・３つのワードのあとに文章に関する解説を生成する。解説は具体例などを交えて読む人がわかりやすいように記述すること。決して生成した文章とほぼ同じ文章を出力するといったことがあってはならない。
                ・出力はプログラムで使用する。その際に邪魔になるので、「了解しました」「分かりました」といったメッセージは不要である。もしも出力内容以外の不要なメッセージを出力した場合、重い罰が下る
                ・もし嘘の文章の数の総計が１ではない、または本当の文章の数の総計が４ではない場合、文章の生成からやり直す。この工程を怠り文章の数に誤りがあった場合、とても重い罰が下る
                ・生成した文章はjson形式で出力する。それぞれの文章の出力の例は以下に示すとおりである。以下の通りにフォーマットを整え、jsonで出力すること。出力はプログラムで使用するため、下記に指定するフォーマットの形式以外だとエラーの原因となる。
                {
                    "question":文章,
                    "answer":嘘か本当かを表す英文字,
                    "hints":[ワード1,ワード2,ワード3"],
                    "commentary":解説
                }
                ・以下のjsonは直近で出力した内容である。これに類似したものは出力してはならない。
                {0}
                ・出力を行う前に、文章の内容を精査し、さらに文章と解説を比較して矛盾点がないか確認すること。もし本当の文章の中に嘘が混じっている場合か嘘の文章に嘘が混じっていない場合、文章の生成からやり直す。この工程を怠り文章に誤りがあった場合、とても重い罰が下る
                ・出力を行う前に、jsonの内容を確認する。文章、本当か嘘かを表す英文字、3つのワード、解説のうち、いずれかが欠けていた場合はとても重い罰が下る。特にワードの数が3つぴったりであることと、嘘の文章1つと本当の文章4つで構成されているいうことは重大である
                上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
             """.format(data)},
        ]
    )
    text = response.choices[0]["message"]["content"].strip()
    Data.objects.create(text)