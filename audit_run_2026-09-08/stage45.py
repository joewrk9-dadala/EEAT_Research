from pathlib import Path
import json,re,copy
R=Path(__file__).resolve().parent
def write(n,t): (R/n).write_text(t.rstrip()+'\n')
def dump(n,o): write(n,json.dumps(o,ensure_ascii=False,indent=2))
def table(h,rs):
    def c(v): return str(v).replace('|','\\|').replace('\n','<br>')
    return '\n'.join('| '+' | '.join(map(c,x))+' |' for x in [h,['---']*len(h),*rs])+'\n'
cs=json.loads((R/'02_claims_V0.json').read_text())
ps={f'P{i:03}':b for i,b in enumerate(re.split(r'\n\s*\n',(R/'article_V0.md').read_text().strip()),1)}
def ids(p,word=''): return ','.join(c['id'] for c in cs if c['paragraph']==p and word in c['claim'])
ev=[
{'id':'E001','title':'證據邊界','publisher':'使用者提供，實際作者未提供','location':'inputs/boundary','published':'未載明','updated':'未載明','accessed':'2026-09-08','scope':'本專案研究前提，台灣網頁玩家情境；非外部事實','support':'僅可使用明示模擬；截圖、紀錄與平台文件不能單獨支持完整個案结論。','locator':'第2節分類表、第3節可描述／不可下結論、第4節待補資料','limit':'已讀內部資料；不是外部證據。E01～E05為原檔缺資料分類。'},
{'id':'E002','title':'情境設計稿','publisher':'使用者提供，實際作者未提供','location':'inputs/user_story','published':'未載明','updated':'未載明','accessed':'2026-09-08','scope':'匿名虛構手機網頁，單局，2026/08/20；版號未載明','support':'示例時間、局號、金額、返還定義、介面設定與未知結局。','locator':'第1～6節；第3節示範表與計算檢查；第7節篇幅','limit':'內部一致性依據，不證明真實事件、實測效果或平台功能。'},
{'id':'E003','title':'建立實用、可靠且以使用者為優先的內容','publisher':'Google 搜尋中心','location':'https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=zh-tw','published':'未載明','updated':'2025-12-18 UTC','accessed':'2026-09-08','scope':'Google搜尋內容指引；繁體中文頁面，非特定平台或台灣法律規範；版號未載明','support':'內容品質、來源及製作方法透明、E-E-A-T與YMYL為審核框架參考。','locator':'品質／專業度、E-E-A-T、製作者／方法；本次讀取行134～153、184～222；更新行235','limit':'不是法律或Google認證；不支持本例個案結論，也不設定本專案字數門檻。'},
{'id':'E004','title':'Page Lifecycle API','publisher':'Chrome for Developers；Philip Walton','location':'https://developer.chrome.com/docs/web-platform/page-lifecycle-api','published':'未載明','updated':'2023-12-01 UTC','accessed':'2026-09-08','scope':'Chrome官方頁面生命週期說明；部分功能段落談Chrome68，非所有瀏覽器通用承諾；地區未限定','support':'Frozen狀態會暫停可凍結任務；可作瀏覽器暫停假設的有限背景。','locator':'States / Frozen及New features added in Chrome68；本次讀取行126～145、188～201；更新行401','limit':'隱藏／凍結狀態描述不能證明本例可見頁面卡頓原因；未提供本例瀏覽器、生命週期或前端紀錄。'}]
dump('04_evidence.json',ev)
checks=[]
for c in cs:
    p=c['paragraph']
    if c['type'].startswith('模擬'):
        result,ee,why,action='直接支持','E002','設計稿支持此模擬設定；僅確認設計範圍。','保留模擬，不標成外部實測'
    elif p=='P030':
        result,ee,why,action='直接支持','E002','依示例定義計算1000-100=900；900+60=960；60-100=-40；內部算術檢查。','保留假設及非完整查核限制'
    elif p=='P048' and '瀏覽器' in c['claim']:
        result,ee,why,action='部分支持','E004','僅提供任務暫停機制背景，非此事件或所有瀏覽器的原因證據。','保留待查假設，不新增已查明結論'
    elif c['type'].startswith('可查核'):
        result,ee,why,action='無法查核','E001,E002','沒有事件原始資料；研究前提不等於技術原因證據。','保留不承擔結論的待查方向'
    elif p=='P016' and '只證明' in c['claim']:
        result,ee,why,action='部分支持','E001','影像可用於核對畫面，但原文「證明」省略來源及時間對應條件。','依I002限定措辭'
    elif c['type']=='主觀評論':
        result,ee,why,action='無法查核','E002','可保留設計評論；沒有可用性測試，不能核實普遍改善效果。','依I003區分建議目的、個人偏好與待測效果；其他有邊界評論保留'
    elif c['type']=='操作建議':
        result,ee,why,action='無法查核','無','這是查核建議，不是假定已存在的平台功能；無特定平台可核對。','保留條件式詢問；不得宣稱平台必定提供'
    else:
        result,ee,why,action='部分支持',c['evidence'],'依研究邊界與設計稿可支持有限推理；沒有原始資料可支持真實事件結論。','保留未知、條件與範圍'
    checks.append([c['id'],ee,result,why,action])
write('04_source_review.md','# 流程4：來源與主張查核\n\n輸入：common＋prompt4＋流程1～3及內部材料。本輪1。讀取兩份內部檔及兩個官方網頁相關原文；下表「直接支持」若來源為E002，只代表支持虛構設定或算術，絕非個案已核實。\n\n'+table(['證據ID','標題／發布者','網址或位置','發布／更新','查閱日期','適用範圍','支持內容','原文定位','限制'],[[e['id'],e['title']+' / '+e['publisher'],e['location'],e['published']+' / '+e['updated'],e['accessed'],e['scope'],e['support'],e['locator'],e['limit']] for e in ev])+'\n'+table(['主張 ID','證據 ID','判定','理由','處理方式'],checks)+'''
引用修正：原稿未附外部引用，無錯誤引用可移除。E003用於審核框架；E004用於檢查P048假設邊界，兩者不插入正文當作本次事件佐證。未取得可比較的同主張衝突來源；這不代表不存在其他來源或分歧。

作者、審閱者、利益關係與外部聲譽均未提供，無法核對；正文沒有虛構聲稱，不添加頭銜、審閱標章或「無利益關係」。本文的出版作者資料仍待實際發布者提供。

| 缺少項目 | 影響位置／問題 | 是否阻塞本次模擬內容驗收 | 取得方式 |
| --- | --- | --- | --- |
| 真實原始影像及事件資料 | P016、P024、P047～P051；I002 | 否，修訂不再讓截圖承擔過量結論；仍阻塞真實事件判定 | 由實際資料持有人提供原件及事件資訊 |
| 適用平台欄位與完整帳務文件 | P029～P035、P041～P044 | 否，本例有獨立虛構定義；真實帳務結論仍不可作 | 確定平台後索取事件版本文件與完整區間明細 |
| 可用性測試 | I003 | 否，改成建議目的，不宣稱實際效益 | 未來以實際介面任務量測錯填、完成率與耗時 |
| 作者、審閱者與利益關係 | R003；文章發布資訊 | 否，僅驗收本文，不認證發布者 | 作者與發布單位提供可核對資料 |

交接流程5：I001補主題及桌面使用建議；I002收斂截圖措辭；I003改成設計目的與角色偏好。不得把E004用來認定本局凍結、網路延遲、扣款正確或平台責任。保留全部核心核對步驟及未查明結尾。
''')

new=copy.deepcopy(ps)
new['P001']='# 娛樂城畫面卡住，餘額剩下 960：我會怎麼核對剛才那一局？'
new['P052']='這篇想回答的是：在娛樂城網頁上，畫面與餘額看起來接不上時，怎麼取得能核對的遊戲歷程？故事以手機瀏覽器為例。若你用的是桌面網頁，也可以先保存完整結果頁，記下裝置、瀏覽器與當時操作，再依下文列出的項目詢問紀錄。不要直接套用故事裡的入口位置；先確認實際平台的說明，再決定去哪裡找。換到另一台裝置查詢時，也請記清楚哪張圖來自發生當下、哪張是後來查看的，別把兩次畫面混在一起。'
new['P016']='我沒有事前錄影，這個缺口無法補拍。現在開始錄，只能保存後續查詢過程；截圖可以協助查看留下的畫面，但還要確認檔案來源、是否經過編輯，以及截取時間能否對應待查事件。即使這些都能交代，單張截圖仍不能完整還原操作順序或伺服器處理。'
new['P011']='這個虛構介面沒有可辨識的等待或處理提示，讓我不知道應該等多久、能不能再次操作。這是操作指引不足的問題，還不是後端失敗的證據。我會建議介面清楚區分送出中、已受理或結果待更新，並依實際狀態提供指引。這項建議要解決的是玩家得靠猜行動的困惑；是否真的有幫助，仍需用實際介面測試。'
new['P020']='入口安排增加了步驟，但沒有可用性測試，我不能說大多數玩家都會找不到。以這個角色的查詢需求來看，我希望結果頁能直接連到該局明細，並保留返回位置，讓查詢有一條清楚的路可走。這是對操作路徑的建議，沒有實測完成速度或成功率。'
new['P037']='局號能關聯是有幫助的，但列表截短讓我得不斷切頁，核對時要留意有沒有抄錯。我希望能完整顯示與複製局號，少一點手動來回抄寫；是否真的降低錯誤率，這份模擬沒有量測。即使介面做到，也只是提供核對條件，不是保證紀錄內容正確。'
new['P039']='這個情境的查詢表單能附圖片，卻不會帶入局號，我得手動填寫。我會建議從該局明細發起查詢時帶入識別資訊，目的是少一道手動填寫步驟；有沒有減少漏填與往返，還需要測試。不過，目前沒有客服回覆，無法評斷處理速度、態度或查核品質。'
order=list(ps)
order.insert(2,'P052')
v1='\n\n'.join(new[p] for p in order)+'\n'
write('article_V1.md',v1)
write('05_numbered_V1.md','# 流程5：V1段落對照\n\nP001～P051沿用，新增P052插在P002後；沒有拆分或合併原段落。\n\n'+'\n\n'.join(f'<!-- {p} -->\n{new[p]}' for p in order))
dump('05_paragraphs_V1.json',[{'id':p,'text':new[p],'previous':ps.get(p),'version':'V1','change':'新增' if p not in ps else '修訂' if ps[p]!=new[p] else '未變'} for p in order])

updates={
('P016','截圖只證明截取當下可見內容'):'截圖僅協助查看留下畫面，須確認來源、編輯情況與事件時間對應',
('P011','明確狀態指引能減少靠猜行動的負擔'):'建議狀態指引的目的是減少猜測，實際幫助需介面測試',
('P020','结果頁連到該局並保留返回位置較易核對'):'角色希望該局入口及返回位置清楚，未量測速度或成功率',
('P037','切頁增加抄錯機會'):'切頁核對時應留意是否抄錯',
('P037','完整顯示及複製能降低負擔'):'角色希望減少抄寫；是否降低錯誤率未量測',
('P039','帶入識別資訊可減少漏填往返'):'帶入資訊目的為省去手動步驟，減少漏填往返與否需測試'}
vcs=copy.deepcopy(cs)
for c in vcs:
    c['original_V0']=c['original']
    c['claim_V0']=c['claim']
    c['original']=new[c['paragraph']]
    if (c['paragraph'],c['claim']) in updates:
        c['claim']=updates[(c['paragraph'],c['claim'])]
        c['status']='已修訂待複審；限定為證據邊界／建議目的'
    c['version']='V1'
newunits=[('P052','本文回答娛樂城網頁遊戲歷程核對問題','主觀評論'),('P052','故事僅為手機瀏覽器模擬','模擬情境或感官細節'),('P052','桌面讀者先保存完整頁面及操作環境','操作建議'),('P052','入口須確認實際平台說明，不套用模擬路徑','操作建議'),('P052','區分發生當下與跨裝置後續查詢畫面','操作建議')]
for p,cl,typ in newunits:
    vcs.append({'id':f'C{len(vcs)+1:03}','paragraph':p,'original':new[p],'original_V0':None,'claim':cl,'claim_V0':None,'type':typ,'scope':'本篇定位或有限操作建議','evidence':'E001,E002' if typ!='操作建議' else '無','status':'新增待複審；非新增平台事實','needed':'若改為平台功能或真實事件結論須另取來源','version':'V1'})
dump('05_claims_V1.json',vcs)
write('05_claims_V1.md','# 更新主張與證據對應表\n\n全部主張保留原ID；變更原文與主張原值見05_claims_V1.json。新增C184～C188，無新增待查外部事實。\n\n'+table(['主張ID','段落ID','V0主張','V1主張','類型','證據ID','狀態','證據限制'],[[c['id'],c['paragraph'],c['claim_V0'] or '新增',c['claim'],c['type'],c['evidence'],c['status'],'內部情境或有限建議，不等於真實個案證據'] for c in vcs]))
rows=[]
for issue,positions,reason in [('I001',['P001','P052'],'補主題與桌面使用方式，維持手機模擬範圍'),('I002',['P016'],'交代截圖來源與對應限制'),('I003',['P011','P020','P037','P039'],'將未量測效益改為設計目的與角色偏好')]:
    for p in positions:
        rows.append([issue,p,ids(p) or ','.join(c['id'] for c in vcs if c['paragraph']==p) or '標題，無主張ID',ps.get(p,'原稿無此段'),new[p],'限定範圍／重寫' if p in ps else '補充','E001,E002',reason,'已修訂待複審'])
dump('05_changes.json',rows)
write('05_revision.md','# 流程5：第一輪修訂\n\n共用輸入common；任務prompt5；依流程1固定規則、流程3問題表、流程4證據與保留清單執行。本階段狀態僅為「已修訂待複審」。\n\n完整可閱讀稿：[article_V1.md](article_V1.md)。\n\n'+table(['問題ID','段落ID','主張ID','修改前','修改後','方式','證據ID','理由','狀態'],rows)+'''
更新段落：05_paragraphs_V1.json及05_numbered_V1.md；更新主張：05_claims_V1.json及.md。新增P052；新增C184～C188均為文章定位、模擬範圍與操作建議。未新增外部事實，未添加技術原因、平台流程或作者背景宣稱。I001～I003全部等待流程6判定。

玩家口吻及感官細節保留；四項核心意圖的既有內容保留；客服草稿、示例表及計算完全保留。字數由validation.json及06_review.md記錄實際計數。原稿保持不變，修訂稿未插入審核ID。
''')
print('流程4及流程5檔案已生成；V1待複審。')
