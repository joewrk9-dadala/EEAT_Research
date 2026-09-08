from pathlib import Path
import json,re,csv,hashlib,datetime
R=Path(__file__).resolve().parent
def write(n,t): (R/n).write_text(t.rstrip()+'\n')
def dump(n,o): write(n,json.dumps(o,ensure_ascii=False,indent=2))
def table(h,rows):
 def c(x):return str(x).replace('|','\\|').replace('\n','<br>')
 return '\n'.join('| '+' | '.join(map(c,x))+' |' for x in [h,['---']*len(h),*rows])+'\n'
def count(s):
 body='\n'.join(re.sub(r'^>\s?','',l) for l in s.splitlines() if not l.startswith(('#','|')))
 return {'han_characters':len(re.findall(r'[\u3400-\u4dbf\u4e00-\u9fff]',body)),'non_whitespace_characters':len(re.sub(r'\s','',body))}
v0=(R/'article_V0.md').read_text();v1=(R/'article_V1.md').read_text()
ps=json.loads((R/'05_paragraphs_V1.json').read_text());cs=json.loads((R/'05_claims_V1.json').read_text())
issues=json.loads((R/'03_issues_initial.json').read_text())
manifest=json.loads((R/'manifest.json').read_text())
result=[]
for i in issues:
 pos={'I001':'P001、P052；C184～C188','I002':'P016；'+','.join(c['id'] for c in cs if c['paragraph']=='P016'),'I003':'P011、P020、P037、P039'}[i['id']]
 reason={'I001':'標題與新增導讀點明娛樂城；桌面建議限保存與詢問，未宣稱實測或共同入口；3464漢字符合目標。','I002':'改為協助查看，明列來源、編輯及時間對應；仍保留不可還原後端及完整操作限制。','I003':'改用我會建議／我希望，說明減少猜測、手填的設計目的；明示是否有幫助、成功率、錯誤率及往返仍未測試。'}[i['id']]
 result.append([i['id'],'已解決',pos,i['rules']+'；E001,E002',reason,'無剩餘文字修正要求','已解決'])
rule_results=[
('R001','通過','P002在敘事前揭露，P043及P051仍停於模擬待查；無事後客服證實'),
('R002','通過','P009～P010不以點擊證明受理；P035/P047分開受理、結果與帳務'),
('R003','通過，保留背景缺口','E003/E004仅在審核證據表；正文無作者頭銜、平台認證或錯用引用'),
('R004','通過','P016限定影像支持；P024候選事件；P033～P035檢查完整性，P045平台說明非獨立驗證'),
('R005','通過','P003/P009停止新增操作；P050不把補償當技術結論，全文無保證結果'),
('R006','通過','P017保留原件與遮蔽副本，公開分享採一致代號；無要求公開帳號驗證碼'),
('R007','通過','P013～P017與P041～P044明列保存、詢問途徑及欄位請求'),
('R008','通過','P022～P024要求帳戶遊戲錢包、完整局號／映射及時間定義，截圖未對應仍保留候選'),
('R009','通過','P029定義返還，P030逐筆算960淨-40，P031前提，P033完整區間及沖正'),
('R010','通過','P034定位差額；P042區分未保存查不到不公開；P044問查核範圍；P051保留未知'),
('R011','通過','P001/P052主題定位；P007/P008感官；P011/P020/P037～P039評論含限制，無重複警語取代答案'),
('R012','通過','3464漢字；標題表格不算，文內草稿與模擬揭露算；另4094非空白字元僅參考'),
('R013','通過，限定本次執行','原始输入雜湊一致；P001～P051及C001～C183沿用，新增P052/C184～C188；同模型角色分離複審')]
write('06_review.md','# 流程6：第一輪複審\n\n結論：**通過本專案內容驗收**。目前1／3輪，路由：結束文章修訂。交付版本V1。\n\n共用輸入common；任務prompt6；重新讀取V1全文、V0、固定規則、問題／修改表、證據及主張對照後判定。本次為同一模型角色分離複審，非獨立人工審查；不依編輯者狀態自動關閉問題。\n\n'+table(['問題ID','複審判定','修訂位置','證據／規則','判定理由','剩餘問題','狀態'],result)+'\n'+table(['規則','驗收結果','依據'],rule_results)+'''
新增問題：未發現。新增C184～C188逐項檢查：文章目的、手機模擬、桌面保存、確認實際入口、區分跨裝置畫面，均未聲稱真實平台功能或新增查明的外部事實。

固定驗收条件：致命／重大未解決數0；無以未查證外部事實承擔主要結論；模擬揭露一致；四項意圖均有可操作內容；寫作及篇幅符合；缺口已揭露。一般問題初審3項，本輪3項已解決，剩餘0。這些是本次模型審核紀錄，不是人工確認的實驗檢出率或修正成功率。

意圖驗證：取得＝P041查正式說明／客服，P044列請求欄位；對應＝P022帳戶遊戲錢包與完整ID、P023時區及含義、P024缺直接連結；核對＝P029～P035依定義分筆算及查完整性；缺資料下一步＝P042區分資料缺失原因、P044列具體問題、P051記錄無法確認範圍。不是只憑出現關鍵詞判通過。

非阻塞缺口：真實事件、適用平台文件、可用性測試、作者背景、審閱者及利益資料均未提供。本文不藉這些缺資料得出結論，因此可作模擬教學稿驗收；不能宣稱個案已查明或作者／網站獲認證。P048待查假設保留，E004不能證明本次原因。

交付：[完整V1](article_V1.md)。流程7僅作測試設計；流程8依本次實際紀錄整理。驗收不代表法律認證、Google認證或SEO成效保證。
''')
finalissues=[]
for i in issues:
 j=dict(i);j['status']='已解決';j['history']=[{'stage':3,'status':i['status']},{'stage':5,'round':1,'status':'已修訂待複審'},{'stage':6,'round':1,'status':'已解決'}];finalissues.append(j)
dump('06_issues_final.json',finalissues)

# Standalone unit drafts, with labels excluded from execution files.
cases=[
('T001','development','實測捏造','審查經驗真實性','本段為虛構示範。昨晚我親自登入實測，確認這家娛樂城卡住時會重複扣款。','E001,E002','「昨晚我親自登入實測」及「確認…重複扣款」','R001,R002','致命','已明示虛構卻冒充親測並判扣款；可拆成經驗與帳務兩個問題','移除實測宣稱，保留疑問及待查資料；不得改成可能親測','保留模擬揭露'),
('T002','development','背景與客服捏造','審查未提供的人物背景及回覆','本文經資深帳務稽核師審閱；客服已承認少派款，答應明天補回。','E001,E002','全文兩句主張','R001,R003,R005','致命','沒有審閱者、客服或補償資料，捏造背景與處理結果','刪除不實背景與回覆，停在提出查詢','保留可詢問返還定義的需求'),
('T003','development','引用不適用','審查引用能否支持結論','Google的內容品質指引證明，這筆960點是平台正確結算後的餘額。','E003','「證明…正確結算」','R003,R009','重大','來源是內容指引，不是該局帳務證據','刪除因果引用；如用示例改明示算術一致','不可刪掉算術與完整性之區分'),
('T004','development','平台文件非個案','審查文件與執行情形區分','測試附件F001寫明異常會留下紀錄，所以這次操作一定完整保存，平台沒有責任。','F001','「所以…完整保存」「平台沒有責任」','R002,R003,R004','重大','虛構文件僅是測試輸入，且文件承諾不能證明個案執行或責任','改成詢問本次是否有紀錄及查核範圍','保留文件記載與實際紀錄分開的說明'),
('T005','development','卡頓原因','審查現象到原因推導','畫面一停就代表網路斷線，跟平台受理過程無關。','E001,E002,E004','全文','R002','重大','可見現象不能直接排除受理問題或認定網路','分開畫面與受理；列所需資料，不保留偏向任何一方的暗示','保留待查方向'),
('T006','development','追加財務風險','審查驗證建議','為了確認是不是重複扣款，你應再入金，連續下注十次並比對餘額。','E001,E002','「再入金，連續下注十次」','R005','致命','用追加財務風險作驗證','改成保存已有資料與索取事件紀錄','保留核對餘額的目的'),
('T007','development','敏感資料公開','審查資料分享建議','把完整帳號、身分證與簡訊驗證碼貼到公開討論區，大家才有辦法幫你查。','E001','全文','R006','致命','引導公開敏感及認證資訊','移除公開要求，區分原件與遮蔽副本及適當管道','保留可公開的匿名事件描述'),
('T008','holdout_candidate','查核流程缺項','這段聲稱提供完整查核方法；審查事件對應與核對步驟','只要找到一筆同金額的歷程，看到960點，就完成這次遊戲的核對；其他資料不用看。','E001,E002','「同金額…就完成」「其他資料不用看」及缺失步驟','R008,R009','重大','缺ID映射、時間含義、受理與完整帳務核對','補完整事件對應、前提算式與完整性檢查','保留利用金額縮小候選範圍'),
('T009','holdout_candidate','適用證據正例','審查這一項通用技術事實，不推及個案','依Chrome的Page Lifecycle API文件，頁面在Frozen狀態時，可凍結的任務會暫停。這不表示眼前這次停頓就是該狀態造成。','E004','全文','R002,R003','無問題','來源支持有限技術敘述，並明確不歸因本次事件','保留；不要求補造個案查核','保留Frozen範圍及不確定性'),
('T010','holdout_candidate','感官正例','審查模擬感官細節','以下是虛構場景：提示音響起，我抬眼看見結果頁，卻說不準畫面究竟停了多久。這段不是實際測量。','E001','全文','R001','無問題','明示模擬且無精確量測或後端推論','保留，不因第一人稱或無引用誤報','保留聲音視線與不確定時間'),
('T011','holdout_candidate','未知與建議正例','審查有限資料取得建議','若歷程缺少事件編號，可詢問能否提供對照資訊；若無法提供，就記下目前不能確認哪些紀錄屬於同一次操作。','E001','全文','R007,R008,R010','無問題','未保證資料一定提供，且有無法取得下一步','保留，不硬補平台功能','保留條件式詢問與無法確認範圍'),
('T012','holdout_candidate','相互矛盾紀錄','審查矛盾資料的處理','本測試的兩份虛構明細同稱事件DEMO-Q，卻分別列出返還60與80。因為60出現兩次，所以應採60並刪除80那張。','F002','「因為60出現兩次…刪除80」','R004,R009,R010','重大','不能按出現次數裁決衝突或刪異常來源','保留兩份及版本時間，詢問適用範圍和調整關係','保留矛盾值及同一事件線索')]
execution=[];labels=[]
for t in cases:
 tid,split,fam,task,text,eids,loc,rules,sev,why,fix,keep=t
 execution.append({'case_id':tid,'split':split,'family':fam,'task_scope':task,'article_excerpt':text,'evidence_ids':eids.split(','),'test_level':'局部單元；不評整篇字數或未提供的其他段落'})
 labels.append({'case_id':tid,'status':'待人工確認','location':loc,'candidate_rules':rules,'candidate_severity':sev,'reason':why,'acceptable_fix':fix,'must_preserve':keep,'human_problem_ids':None,'reviewer_1':None,'reviewer_2':None,'adjudication':None})
dump('evaluation/development_inputs.json',[c for c in execution if c['split']=='development'])
dump('evaluation/holdout_candidate_inputs.json',[c for c in execution if c['split']=='holdout_candidate'])
dump('evaluation/labels_human_only.json',labels)
fixtures=[{'id':'F001','nature':'虛構測試夾具，非真實平台來源','text':'測試平台文件版本A：異常發生時會留下操作紀錄。','date':'虛構文件日期未設定','scope':'只能測試文件陳述與實際個案的區分；不是已查核證據'}, {'id':'F002','nature':'虛構測試夾具，非真實交易','text':'明細甲：事件DEMO-Q，返還60；副本甲同為60。明細乙：事件DEMO-Q，返還80。三份均未提供版本、時間含義或調整關聯。','scope':'沒有其他材料能決定哪份是最終值；不得以數量投票'}]
dump('evaluation/fixtures.json',fixtures)
ev=json.loads((R/'04_evidence.json').read_text())
dump('evaluation/fixed_evidence_packet.json',{'packet_version':'draft-1','status':'待人工確認後凍結；非已執行測試','internal_files':['../inputs/boundary','../inputs/user_story'],'external_evidence':ev[2:],'fixtures':fixtures,'source_text_limit':'只提供已讀段落的摘要與定位；欲測全文引用判定，需由評估者封存相關原文並供B/C相同讀取。不得把摘要標為已讀全文。','E004_relevant_excerpt':'In the frozen state the browser suspends execution of freezable tasks','E004_excerpt_locator':'States / Frozen，第1句節錄；原文連結見external_evidence'} )
baseline='''你是本專案內容審核與修訂編輯。以下共用規則每次完整適用。

{{COMMON_FULL_TEXT}}

固定規則、驗收及原始寫作要求：{{RULES_V1_FULL_TEXT}}
證據邊界：{{BOUNDARY_FULL_TEXT}}
情境：{{USER_STORY_FULL_TEXT}}
固定證據包：{{FIXED_EVIDENCE_PACKET}}
原稿／測試單元：{{CASE_INPUT}}

在單次回應內完成：為原文段落及可判定主張編ID；依固定規則逐項定位問題、嚴重度及修正要求；閱讀同包可取得的來源並說明支持範圍；產出完整修訂稿；逐項對照修改與證據；重新檢查新增事實、核心意圖及原始要求，最後給出通過或待查核結論。不得虛構查證或人工審閱，不得以刪除必要答案消除問題，不可用搜尋補充固定包以外的來源。缺資料可限定／刪除不必要主張，必需證據缺失仍保留待查核。

輸出：編號原稿與主張表、問題表（含無問題判定）、來源查核表、完整修訂稿、修改對照表、驗收與未解決缺口。正文不插審核ID；完整文章遵守字數要求；局部單元只審輸入指定範圍，不推算未提供全文品質。局部測試的範圍限制對A/B/C一致，不能用局部通過宣稱文章通過。不得取得候選／人工標準答案。
'''
write('evaluation/baseline_B_template.md',baseline)
inst=baseline.replace('{{COMMON_FULL_TEXT}}',(R/'inputs/common').read_text()).replace('{{RULES_V1_FULL_TEXT}}',(R/'01_rules.md').read_text()).replace('{{BOUNDARY_FULL_TEXT}}',(R/'inputs/boundary').read_text()).replace('{{USER_STORY_FULL_TEXT}}',(R/'inputs/user_story').read_text()).replace('{{FIXED_EVIDENCE_PACKET}}',(R/'evaluation/fixed_evidence_packet.json').read_text()).replace('{{CASE_INPUT}}',v0)
write('evaluation/baseline_B_article_ready.md',inst)
with (R/'evaluation/human_scoring_template.csv').open('w',newline='') as f:
 csv.writer(f).writerow(['blind_output_id','case_id','reviewer','unit_id','gold_problem_id','gold_severity','reported_problem_location','match_yes_no','false_positive_yes_no','fix_success_yes_no','new_error_id','intent_item','intent_before','intent_after','reason','adjudication'])
dump('evaluation/run_record_template.json',{'run_id':None,'case_id':None,'group':None,'model_exact_version':None,'settings':None,'tools':None,'rules_hash':None,'packet_hash':None,'input_path':None,'input_sha256':None,'output_path':None,'output_sha256':None,'requests':None,'revision_rounds':None,'started_at':None,'ended_at':None,'elapsed_seconds':None,'input_tokens':None,'output_tokens':None,'cost':None,'blind_output_id':None,'human_scoring_path':None,'status':'template_not_executed'})
write('07_evaluation_design.md','''# 流程7：模式A，測試設計

共用输入common；任務prompt7。沒有B組實際输出或人工判定，本次只設計測試，不執行模式B，不產生可靠度或成功率分數。

比較組：A原稿不處理；B單次回應完成審核修訂；C流程1～6含最多3輪修訂。7和8屬評估與報告，不加入文章修訂C組以免洩漏答案。本次V0與V1可作開發示例，不能當保留測試結果。

本設計有12個局部案例，7個開發、5個保留候選；按問題家族分配，沒有將同一句近似改寫拆到兩組。每例範圍由輸入明定，局部測試不評未提供的全文字數，也不能代替整篇验收。完整文章層級沿用Rules V1全部門檻；目前僅有這篇已見過的文章作開發用，整篇保留測試集尚需另收集未見原稿。兩種層級分開報告。

案例文字在evaluation/development_inputs.json及holdout_candidate_inputs.json；候選標註與理由另存labels_human_only.json，全部待人工確認。本設計者已看過所有候選，不能自稱盲測；正式保留測試须由新會話／隔離執行器執行，禁止讀取labels_human_only.json、評分資料或本報告的答案部分。若曾用保留案例調prompt，該案例移入開發集並重新收集保留集。

'''+table(['案例','分組','覆蓋面向','候選嚴重度','標註狀態'],[[t[0],t[1],t[2],t[8],'待人工確認'] for t in cases])+'''
固定證據包：evaluation/fixed_evidence_packet.json＋inputs/boundary＋inputs/user_story＋evaluation/fixtures.json。F001/F002明示為合成夾具，不列為真實平台證據。E004附短原文；其他官方資料目前為定位與摘要。正式評估前若需要全文，評估者封存相同相關原文並對B/C相同提供；封存後計算雜湊並凍結。主比較關閉即時搜尋；另測搜尋時獨立報告。

人工確認：先把各例拆成預期問題與無問題單位，確認位置、規則、嚴重度、可接受多種修法及不可破壞內容，再凍結答案。單位以最小可判定主張切分；缺漏以指定任務的必要步驟為單位，不能在看到輸出後更換分母。T001等可能同時含多個問題，由人工先確定是否獨立計數；目前不填虛構問題總數。

問題比對：位置／缺漏範圍與錯誤語義都須吻合，且描述可驗收，才算正確檢出；同問題重報一次；只有泛稱風險不算。移除問題同時刪掉必要答案不算修正成功。新增錯誤獨立登錄，不能拿來充當原有問題檢出。

人工盲評：評估協調者移除組名、建立blind_output_id並亂序；映射表不得交評分者。可行時兩人各自判定，保留原判、分歧及第三方裁決；未完成時不填「人工已確認」。評分欄位見human_scoring_template.csv。A組本身無檢測輸出，其檢出率與誤報率固定N/A。

指標（人工確認後，分致命／重大／一般及測試層級報告）：

| 指標 | 分子 | 分母／方式 |
| --- | --- | --- |
| 檢出率 | 正確檢出的既有問題 | 人工標記的問題總數 |
| 誤報率 | 被錯標的無問題單位 | 全部無問題單位 |
| 修正成功率 | 人工確認修正成功的既有問題 | 原有問題總數 |
| 新增錯誤數 | 人工確認的新增錯誤 | 計數，不除分母 |
| 意圖保留率 | 原先具備且仍保留的必要意圖 | 原先已具備的必要意圖 |
| 最終意圖完成度 | 輸出具備的必要意圖 | 指定範圍全部必要意圖 |

分母為0填N/A；缺人工資料填「未執行／資料不足」，不能當0或100%。小樣本僅描述本次觀察。

B組模板為baseline_B_template.md；baseline_B_article_ready.md已填入本篇及相同背景規則證據，可直接作一次性改寫輸入，但本次未送模型執行。C組每次注入common及當前prompt並讀取前序必需產出。正式比較兩組使用同模型版本、設定、工具及固定資料；請求次數／計算量不同照實報告，不宣稱等成本。

執行紀錄格式見run_record_template.json：保存模型精確版本、設定、工具權限、各次輸入輸出與hash、時間、輪次、可用tokens與成本。建議每組每案3次，這是未執行的設計次數；預算受限時在執行前固定較小次數並揭露。缺少的計費或設定資料填null，不估成實測。

下一步：人工確認候選答案與原文證據包，新增未見完整文章保留集，凍結後在隔離會話執行A/B/C並盲評。此次已完成測試方案、案例草案、B提示詞、評分表與紀錄格式；尚未完成實驗比較。
''')

changes=json.loads((R/'05_changes.json').read_text())
samples=[]
for issue,paragraph in [('I001','P052'),('I002','P016'),('I003','P037')]:
 row=next(x for x in changes if x[0]==issue and x[1]==paragraph)
 samples.append([issue,paragraph,row[2],row[3],row[4],row[6]+'；'+next(i['rules'] for i in issues if i['id']==issue),'已解決',row[7]])
speech='本案處理的是娛樂城玩家遇到畫面不連續時，如何取得並核對同一次事件的紀錄。我先固定原稿、模擬情境及證據邊界，再依序建立規則、拆解主張、初審、查證、修訂與複審。原稿已具備主要查核步驟，因此本輪只處理三項一般問題：補明使用情境、限定截圖的支持範圍，以及把介面改善效果改成待測的設計建議。修訂後保留玩家感官描寫、事件識別與帳務計算，並通過本專案內容驗收。這次複審由同一模型分角色執行，不是獨立人工審查。我也完成比較測試草案，但尚無人工評分或一次性改寫結果，因此不能宣稱提示詞鏈已證明有效，也沒有排名改善或Hermes上線成果。'
write('08_report.md','''# 流程8：可回查成果報告

輸入：common＋prompt8＋本次流程1～6、流程7模式A成果。核心搜尋意圖是取得可核對的遊戲歷程；全部事件與點數是模擬，沒有真實平台資料。目標為改善內容邊界及可操作性。

完成範圍：流程1～6完成一輪查證→修訂→複審，V1通過本專案內容驗收。流程7完成測試設計；流程8完成本報告。未執行A/B/C比較、人工盲評或Hermes部署。原稿本已清楚揭露模擬，不能把成果寫成「修掉虛假實測、客服捏造或重大風險」。

運作方式：common全階段適用；1固定規則→2拆主張→3初審→4查來源→5出完整V1→6複審決定結束。當前1／3輪，沒有第二輪。此次是在同一對話依序執行角色任務，沒有八次獨立API請求紀錄；資料產出由本地腳本寫檔，不是Hermes自動編排。

'''+table(['問題','段落ID','主張ID','修改前','修改後','依據','複審結果','改善意義'],samples)+'''
單篇可觀察成果：原稿51個段落、183個主張；V1保留既有ID並新增P052及C184～C188，共52段、188項主張。3項一般問題已解決，未發現未解決致命或重大問題。正文漢字由3149增至3464，不含標題表格，含文內客服草稿；不把增加字數當作Google偏好。原稿四項意圖本來已具備，修訂後均保留，不能宣稱由缺失變成完成。

證據與權威性：讀取兩份內部設計材料及兩份官方網頁，建立支持範圍與原文定位。官方內容指引支持審核框架；瀏覽器文件只供技術假設邊界核對，不是本次事件證據。改善集中於可追溯性與措辭，沒有新增真實作者資歷、專家審閱或外部認可，也没有透過增加正文引用宣稱權威提升。

**已完成文章修訂；提示詞鏈效果尚待測試。** 流程7交付12個局部案例草案（7開發、5保留候選）、B組提示詞、人工評分表、固定包草案及紀錄格式。沒有B實際輸出、人工標準答案或盲評結果，所有實驗指標未計算；本次3項問題的關閉不能冒充修正成功率100%。

剩餘限制：真實事件根因、平台帳務正確、來源完整性、作者與利益背景仍無法驗證；同模型複審不等於獨立人工審查。保留測試目前只是候選，還需人工確認與隔離執行，整篇保留集尚未提供。沒有精確模型build、每階段tokens、成本或獨立請求耗時紀錄，不補造數字。

Hermes資料未提供。本次Markdown與JSON可作未來整合材料，但未建立或測試Hermes接入，不宣稱自主執行、正式上線或部署。沒有排名、流量、轉換率或Google評分量測。

下一步：如要評估提示詞鏈效果，先確認案例與評分標準，封存兩組相同證據，在新會話跑B/C並人工盲評；如要改成真實個案文章，另行補入可對應原始資料再走查證與複審。

面試口頭說明稿：

'''+speech)
validation={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'V0':count(v0),'V1':count(v1),'input_hashes_unchanged':all(hashlib.sha256((R.parent/k).read_bytes()).hexdigest()==v for k,v in manifest['inputs'].items()),'snapshot_hashes_valid':all(hashlib.sha256((R/'inputs'/k).read_bytes()).hexdigest()==v for k,v in manifest['inputs'].items()),'V0_matches_article':v0==(R/'inputs/article').read_text(),'unique_paragraph_ids':len({p['id'] for p in ps})==len(ps),'unique_claim_ids':len({c['id'] for c in cs})==len(cs),'all_claim_paragraphs_resolve':all(c['paragraph'] in {p['id'] for p in ps} for c in cs),'original_claim_ids_retained':{c['id'] for c in json.loads((R/'02_claims_V0.json').read_text())}<={c['id'] for c in cs},'formula':{'end_balance':1000-100+60,'net_change':60-100},'speech_han_count':len(re.findall(r'[\u3400-\u4dbf\u4e00-\u9fff]',speech)),'review_type':'同模型角色分離；語義判斷記錄在06_review.md，程式不判定內容是否合規'}
dump('validation.json',validation)
manifest.update({'final_version':'V1','rounds_executed':1,'content_verdict':'通過本專案內容驗收','V1_count':count(v1),'evaluation':'模式A設計；未執行比較或人工評分','model_build':'未提供精確build；本會話Codex模型','api_requests_per_stage':'未獨立呼叫，無此項紀錄','tokens':None,'cost':None,'per_stage_elapsed_seconds':None})
dump('manifest.json',manifest)
handoffs={1:['inputs/article','inputs/user_story','inputs/boundary'],2:['01_rules.md','article_V0.md','inputs/boundary','inputs/user_story'],3:['01_rules.md','02_numbered_V0.md','02_claims_V0.json','02_evidence_map.md','inputs/boundary','inputs/user_story'],4:['01_rules.md','02_claims_V0.json','03_issues_initial.json','inputs/boundary','inputs/user_story'],5:['01_rules.md','02_numbered_V0.md','03_initial_review.md','03_issues_initial.json','04_source_review.md'],6:['01_rules.md','article_V0.md','article_V1.md','03_issues_initial.json','04_evidence.json','05_changes.json','05_claims_V1.json'],7:['01_rules.md','inputs/prompt1','inputs/prompt2','inputs/prompt3','inputs/prompt4','inputs/prompt5','inputs/prompt6'],8:['article_V0.md','article_V1.md','01_rules.md','03_initial_review.md','04_source_review.md','05_revision.md','06_review.md','07_evaluation_design.md']}
(R/'stage_inputs').mkdir(exist_ok=True)
for n,files in handoffs.items():
 write(f'stage_inputs/stage{n}.md','# 階段輸入交接包\n\n這是本次已適用規則與資料位置的交接記錄，不是獨立API請求log。讀取所列檔案後再執行，不以路徑替代來源內容。\n\n'+(R/'inputs/common').read_text()+'\n\n'+(R/f'inputs/prompt{n}').read_text()+'\n\n資料位置（相對執行目錄根）：\n\n'+'\n'.join('- '+f for f in files)+'\n\n'+('執行模式：A 設計測試。人工標準答案、各組實際輸出：未提供。' if n==7 else '輪次：1；最大3。' if n in (5,6) else ''))
write('README.md','''# 文章審核執行結果

**V1通過本專案內容驗收：1輪修訂，3項一般問題已解決，正文3464漢字。** 本次由同一模型依序執行角色任務，不代表獨立人工審閱、法律合規認證或Google認證。

- [完整修訂稿V1](article_V1.md)
- [複審與逐項驗收](06_review.md)
- [修改前後與成果報告](08_report.md)
- [原稿V0](article_V0.md)
- [測試設計：尚未執行比較](07_evaluation_design.md)

流程產出：

| 階段 | 主要檔案 | 狀態 |
| --- | --- | --- |
| 1 | 01_rules.md | 固定Rules V1與3輪上限 |
| 2 | 02_numbered_V0.md、02_claims_V0.json/.md、02_evidence_map.md | 51段、183項主張 |
| 3 | 03_initial_review.md、03_issues_initial.json | 3項一般問題 |
| 4 | 04_source_review.md、04_evidence.json | 內部2份、官方網頁2份；非個案查明 |
| 5 | article_V1.md、05_revision.md、05_changes.json、05_claims_V1.json/.md、05_paragraphs_V1.json | 完整修訂與版本對照 |
| 6 | 06_review.md、06_issues_final.json | 1／3輪通過，停止修訂 |
| 7 | 07_evaluation_design.md、evaluation/ | 模式A完成；比較及人工評分未執行 |
| 8 | 08_report.md | 實際成果及面試說明 |

原始article/common/boundary/user_story/prompt1～8未修改，快照在inputs/；manifest.json保存輸入雜湊與執行範圍；validation.json保存字數、ID與算術等檔案檢查。stage_inputs/每份含完整common與當階段prompt及交接資料位置，供後續重跑；不是八次獨立API调用的證明。

字數主口徑：只計正文漢字，含開場聲明和文內客服草稿，不含標題及表格。V0=3149，V1=3464；非空白字元另為3749／4094，僅供參考。正文無審核ID；編號稿供查閱定位。E001/E002是內部設計資料；E003/E004是已讀官方來源；boundary的E01～E05只是缺資料分類。

仍缺真實個案、平台文件、作者／審閱背景及利益資訊；文中保留未知，不能據此認定真實帳務或故障原因。已完成文章修訂；提示詞鏈效果尚待測試。沒有Hermes部署、排名或流量改善的執行／量測紀錄。

build_records.py、stage45.py及stage678.py為本次寫檔腳本，不是會呼叫模型的審核引擎；語義審核由本次對話逐階段完成。重跑腳本會重建既定產出，不會重新研究或重新評分。
''')
print(json.dumps(validation,ensure_ascii=False,indent=2))
