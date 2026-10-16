from pathlib import Path
import json,csv,base64,re,mimetypes
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'trip.json').read_text())
# Keep the deployment build dependency-free: PDF is generated before committing.
for name,file in [('Guide','DejaVuSans.ttf'),('GuideBold','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
styles=getSampleStyleSheet()
for name in ['BodyText','Normal']:styles[name].fontName='Guide';styles[name].fontSize=8.7;styles[name].leading=12;styles[name].spaceAfter=6
for name in ['Title','Heading1','Heading2','Heading3']:
 styles[name].fontName='GuideBold';styles[name].textColor=HexColor('#184b43');styles[name].spaceAfter=10
styles['Title'].fontSize=27;styles['Title'].leading=33
styles['Heading2'].fontSize=12;styles['Heading2'].leading=15;styles['Heading2'].spaceBefore=9;styles['Heading2'].spaceAfter=6
styles['Heading3'].fontSize=10;styles['Heading3'].leading=13;styles['Heading3'].spaceBefore=7;styles['Heading3'].spaceAfter=4
styles.add(ParagraphStyle(name='SmallGuide',fontName='Guide',fontSize=7,leading=10,spaceAfter=5))
story=[]
def p(t,style='BodyText'):story.append(Paragraph(escape(t).replace('–','-').replace('—','-'),styles[style]))
def link(url,label):story.append(Paragraph('<a color="#184b43" href="'+escape(url,{'"':'&quot;'})+'">'+escape(label)+'</a>',styles['SmallGuide']))
def source(i):return next(x for x in d['sources'] if x['id']==i)
sub=sum(x['amount']*x['qty'] for x in d['ledger'] if not x['optional'])
p('ICELAND / MARCH 2027','Title');p('March 13-18 | Four travellers | Two rooms | Four nights','Heading2');p('Research edition - checked October 16, 2026. Four adults assumed. Dated flight and hotel quotes observed around 21:30 UTC; nothing reserved. Tours are published starting fares with March availability unverified. All timeline clocks are targets except the dated airline schedule.')
story.append(Image(str(ROOT/'assets/hotel.png'),width=420,height=275));p('Illustrative standard room photo: Center Hotels. No room booked.','SmallGuide')
p('Flights + hotel: C$8,058.48 for four / C$2,014.62 each. Core plan: C$'+f'{sub:,.2f}'+' / C$'+f'{sub/4:,.2f}'+' each before optional extras. With 10% contingency: C$'+f'{sub*1.1/4:,.2f}'+' each.');p('Reykjavík base, no car. Keep March 17 for weather swaps. The C$1,500/person target is exceeded by the flight and hotel alone.');p(d['research']['fxNote']);story.append(PageBreak())
for day in d['days']:
 p('Day '+str(day['n'])+' | '+day['date'],'Heading1');p(day['city'],'Heading2');p('Local timezone: '+day['timezone']+'. Overnight: '+('Þingholt, two rooms' if day['hotel'] else 'No hotel night'))
 for e in day['events']:p(e['time']+' | '+e['title']);p('Evidence: '+e['status'],'SmallGuide')
 for x in day.get('links',[]):link(x['url'],x['title']+' - details / availability')
 p('Personal notes: ____________________________________________________');story.append(PageBreak())
p('Flights and hotel quotes','Title');p('Icelandair FI602: YYZ Terminal 3 March 13, 19:40 -> KEF March 14, 06:25 (5h45). FI603: KEF March 18, 17:00 -> YYZ Terminal 3, 19:15 (6h15). Both nonstop, local clocks. Economy Light return for four adults C$5,380.48: airfare C$4,888 + taxes and fees C$492.48. No checked bag, no included seat selection, non-refundable, no ticket changes.');p('Summary offered +C$460 total to upgrade all four on both flights to Economy Standard: C$5,840.48 including a checked bag and basic seat selection. Still non-refundable; changes for fee. Recheck weight/size limits. Earlier C$200/person bag estimate is superseded.');link(source('air-quote')['url'],'Search Icelandair with the exact dates and four adults')
p('Þingholt by Center Hotels','Heading2');p('March 14-18; two Standard Double queen rooms; four nights: C$2,678 including taxes, no breakfast, non-refundable. Breakdown C$2,343 rooms + C$260 taxes + C$75 estimated local tax due at property in ISK (6,400).');p('Alternative observed totals: C$2,832 for Standard Double or Twin rooms; C$3,138 for refundable queen rooms (before March 12 shown; check deadline); C$3,151 for non-refundable queen rooms with breakfast. Those are total stay prices. Supplements in the selector are nightly. Breakfast upgrade C$473 for the group: reduce ordinary food budget if choosing it. Arrival breakfast still separate.');p('Published check-in 15:00, checkout 11:00. Request bag storage on arrival and departure; early room access not assured. Verify bed allocation and rate conditions before paying. Expedia property score observed 9.0/10, 1,001 reviews.');link(source('hotel-quote')['url'],'Dated Expedia room search')
p('Flybus and buffers','Heading2');p('Current hotel/stop fare ISK 5,299 one way. Two one-ways per adult ISK 10,598 (~C$124): planning allowance before group/return discounts. Published return pattern: hotel/stop pickup 12:30, BSÍ 13:00, KEF 13:45 for a 17:00 flight. Reconfirm the March voucher and leave earlier if weather requires. Arrival transfer follows formalities, not a fixed reserved 08:00 departure.');link('https://flybus.is/book/','Book Flybus - compare the final four-person return total');story.append(PageBreak())
p('Tour selection','Title');p(d['research']['bookingGap']);p('Select English morning Golden Circle for Kerið. Follow operator-assigned pickup stop and voucher. Optional outings do not add a second hotel stay or a rental car.')
for t in d['tourOptions']:
 p('Day '+str(t['day'])+' | '+t['title'],'Heading2');p(t['duration']+' | '+t['price']);p(t['description']);p(t['status'],'SmallGuide');link(source(t['source'])['url'],'Operator information / availability')
p('Optional lagoon and aurora','Heading2');p('Sky Lagoon Saman from ISK 14,990 (~C$175) entry, plus separate C$50/person transport allowance. Confirm slot, transfer schedule/fare and ages. Northern Lights coach from ISK 9,990 + 1,590 pickup (~C$135.49/person), about four hours. First clear, rested evening gives more retry opportunities than waiting until the final night. Reconfirm exact terms; sightings never guaranteed.');link(source('sky-price')['url'],'Sky Lagoon admission');link(source('aurora')['url'],'Northern lights coach');story.append(PageBreak())
p('Restaurants and food','Title');p('Official menu references checked October 16, 2026. No reservations made. Hours and prices can change before March. Budget C$100/person/day for five days, all these meals within the allowance; alcohol excluded. Walking times are estimates. Tour lunches follow coach stops: Geysir and Vík; carry snacks and do not arrange a conflicting restaurant booking.')
for r in d['dining']:
 p(r['name']+' | '+r['address'],'Heading2');p(r['price']);p(r['plan']);p(r['hours']+' '+r['note']);link(source(r['source'])['url'],'Official menu / information')
p('Before travel','Heading2')
for t in ['Recheck and book flights / hotel; quotes are not reservations','Confirm ages, queen vs twin beds, breakfast and cancellation deadline','Compare Economy Standard upgrade with separate baggage needs','Book two core coach tours and their pickup; preserve March 17','Check passport-specific entry / transit requirements','Book return Flybus, verify exact stop and departure buffer','Reserve Messinn only if the city evening remains free','Review insurance, weather and SafeTravel; follow beach/path closures']:p('[  ] '+t,'SmallGuide')
story.append(PageBreak());p('Cost ledger | CAD','Title');p('CAD snapshot equivalents at rounded C$0.0117 per ISK. Rows rounded individually; small conversion differences are possible. Optional rows excluded by default. No extra restaurant charges are added on top of food. Baseline PDF does not contain later browser edits.')
for r in d['ledger']:
 p(r['title'],'Heading3');p(f"C${r['amount']:,.2f} x {r['qty']} = C${r['amount']*r['qty']:,.2f}. {r['unit']}. {r['status']}. "+('Optional.' if r['optional'] else 'Included.'))
 if r.get('sourceAmount'):p('Operator reference: ISK '+f"{r['sourceAmount']:,}"+' per unit.','SmallGuide')
 if r.get('note'):p(r['note'],'SmallGuide')
 if r.get('source'):link(source(r['source'])['url'],'Source')
p(f'Core C${sub:,.2f}; with 10% contingency C${sub*1.1:,.2f}; C${sub*1.1/4:,.2f}/person.','Heading2');story.append(PageBreak());p('Sources and open checks','Title')
for s in d['sources']:
 start=len(story);p(s['title'],'Heading3');link(s['url'],s['url']);p('Checked '+s['checked']+('. '+s['note'] if s.get('note') else ''),'SmallGuide');block=story[start:];del story[start:];story.append(KeepTogether(block))
p('Live booking access confirmed only for flight and hotel room selection. Tour dates/times remain to check. Menu prices do not establish future availability. Fare-watch automation existence/status has not been verified. External booking and detailed map tiles require internet; offline website includes the map outline.')
def footer(c,doc):c.setFont('Guide',8);c.setFillColor(HexColor('#184b43'));c.drawString(45,25,'Iceland 2027 | Research edition | '+str(doc.page))
SimpleDocTemplate(str(ROOT/'iceland-guide.pdf'),pagesize=(595,842),rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
with (ROOT/'costs.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Item','Unit CAD','Quantity','Total CAD','Evidence','Optional','Source ISK per unit','Source URL','Notes']);w.writerows([r['title'],r['amount'],r['qty'],round(r['amount']*r['qty'],2),r['status'],r['optional'],r.get('sourceAmount',''),source(r['source'])['url'] if r.get('source') else '',r.get('note','')] for r in d['ledger'])
h=(ROOT/'index.html').read_text()
def css(m):
 path=m.group(1);return '<style>'+(ROOT/path).read_text()+'</style>'
h=re.sub(r'<link rel="stylesheet" href="([^"?]+)">',css,h)
def js(m):return '<script>'+(ROOT/m.group(1)).read_text().replace('</script','<\\/script')+'</script>'
h=re.sub(r'<script src="([^"?]+)"></script>',js,h)
for path in (ROOT/'assets').rglob('*'):
 if path.is_file() and path.suffix.lower() in ['.jpg','.jpeg','.png','.svg','.gif','.webp','.avif']:
  rel=path.relative_to(ROOT).as_posix();h=h.replace(rel,'data:'+str(mimetypes.guess_type(str(path))[0])+';base64,'+base64.b64encode(path.read_bytes()).decode())
(ROOT/'offline-guide.html').write_text(h)
print('Updated PDF, cost CSV and full standalone website')
