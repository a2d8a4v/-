# -
此為使用python 3語言所寫的api串接示範，並且利用matplt繪製圖片，讓大家瞭解現在市場的牛蒡價量與產銷價差情形。

@使用方式：

所有檔案請按照上面放的方式放在電腦裡面

要跑ipynb格式，請先下載jupyter notebook使用，或是ipython notebook

@注意事項

要跑py，請記得先在電腦裡面安裝python3，我使用的版本是python 3.5

另外我寫py的話會使用sublime text 3，關於python3的build檔案我也放在這裡了

下載後請把當中的“Python3.sublime-build”檔案放在：/library/Applicaiton Support/Sublime text 3/Packages/User/

# -

@參考資源：

http://data.coa.gov.tw/Query/ServiceDetail.aspx?id=037

資料從100年到至今

http://m.coa.gov.tw/outside/transaction/View.aspx?productCateCode=N04&productCode=SM1&YYYYMMDD=20160401

這裡可以分類查詢

http://data.coa.gov.tw/Query/AdvSearch.aspx?id=037

若想要用json來做apo串聯，可以在這裡新增條件之後在思考要怎麼用

http://amis.afa.gov.tw/others/iii2.htm

農產品市場交易站說明

http://data.gov.tw/node/8066#comment-6241

關於api的說明



@資料

提供資料包含：交易日期、作物代號、作物名稱、市場代號、市場名稱、上價(元/公斤)、中價(元/公斤)、下價(元/公斤)、平均價(元/公斤) 、交易量(公斤)等欄位資料。

原始資料長的樣子：{ “date”:”104.12.28","作物代號":"rest","作物名稱":"休市","市場代號":"109","市場名稱":"台北一","上價":"0","中價":"0","下價":"0","平均價":"0","交易量":"0"}

注意只查一天可能會查到休市的情況，這樣會沒有資料跑出來，變成空集合。



@關於資料：

a.當天若是休市，會變成這樣子的資料型態

{ "交易日期":"104.12.28","作物代號":"rest","作物名稱":"休市","市場代號":"109","市場名稱":"台北一","上價":"0","中價":"0","下價":"0","平均價":"0","交易量":"0"}

b.作物代號和作物名稱的關聯

"作物代號":"SM1","作物名稱":"牛蒡"

"作物代號":"SM9”,”作物名稱":"牛蒡-進口"

c.每個市場有其代碼

台北二：104

台北一：109

三重市：241

宜蘭市：260

豐原鄉：420

永靖鄉：512

溪湖鎮：514

南投市：540

西螺鎮：648

屏東市：900

台中市：400

高雄市：800

鳳山區：830

桃園縣：338

台東市：930

花蓮市：950

d.資料不會一次都顯示出來，需要有變數控制來控制要取多少筆資料

＊＊建議一次取得一個月的資料量即可，再聚集成一年的資料

e.名詞定義

上價：以當日該農產品總交易量中最高價格之20%，加權平均計算得之。 

下價：以當日該農產品總交易量中最低價格之20%，加權平均計算得之。 

中價：以當日該農產品總交易量中扣除最高最低價格各20%剩餘之60%，加權平均計算得之。

簡單來說就是，因為從產地把東西分級上中下運送到批發市場拍賣，批發市場會看東西的等級所拍賣出來的價錢當然就不一樣。

而你去市場買東西，為什麼每個攤販所賣同樣的東西，價錢卻都不一樣，就是因為去批發時貨色不同(等級) 。



@關於存檔（重新定義名稱）

交易日期：dat

作物代號：crs

作物名稱：cro

市場名稱：mar

市場代號：mas

上價：pru

中價：pro

下價：prd

平均價：prm

交易量：trv



@圖表繪製：

總交易量170157 公斤 總平均價23.84 元/公斤 平均交易量204.76 公斤/日

個別市場的不同天的「交易量」圖表

個別市場的不同天的「價格」圖表

所有市場的「總交易」量圖表

所有市場的「每天價格」圖表

不同市場的交易狀況

產季時的價量

全時間當中最高行情為

全時間檔中最低行情為

每天的總交易量

每年總交易量

市場價格和銷售量之間的關係

@參考範例：

價格的和狀圖 http://matplotlib.org/examples/pylab_examples/boxplot_demo2.html

疊層圖http://matplotlib.org/examples/api/filled_step.html

價格折線圖http://matplotlib.org/examples/api/date_index_formatter.html

不同月份和不同年份的折線圖疊合http://matplotlib.org/examples/showcase/bachelors_degrees_by_gender.html
