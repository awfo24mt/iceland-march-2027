from pathlib import Path
import json,csv,base64,re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'trip.json').read_text())
with (ROOT/'costs.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['Item','Unit CAD','Quantity','Total CAD','Evidence','Optional']);w.writerows([r['title'],r['amount'],r['qty'],r['amount']*r['qty'],r['status'],r['optional']] for r in d['ledger'])
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='TitleGreen',fontName='Helvetica-Bold',fontSize=30,leading=36,textColor=HexColor('#184b43'),spaceAfter=20));styles['BodyText'].leading=15;styles['BodyText'].spaceAfter=10
story=[]
def p(text,style='BodyText'):story.append(Paragraph(escape(text),styles[style]))
p('ICELAND / MARCH 2027','TitleGreen');p('March 13-18 | Four travellers | Two rooms | Four nights','Heading2');p('Planning edition checked October 16, 2026. User-supplied flights and hotel have not been independently re-quoted or confirmed booked. All daily times are suggestions; verify issued flight and tour vouchers.');story.append(Image(str(ROOT/'assets/hotel.png'),width=420,height=275));p('Standard room photo: Center Hotels. Illustrative property image; room type unconfirmed.');p('Flights + hotel: C$7,915 for four / C$1,978.75 each. Core allowances add C$3,760 for four. Baseline C$11,675 / C$2,918.75 each before contingency and optional items. With 10% contingency: C$12,842.50 / C$3,210.63 each.');p('Reykjavik base, no rental car. Retain March 17 as a weather buffer before adding another long excursion.');story.append(PageBreak())
for day in d['days']:
 p('Day '+str(day['n'])+' | '+day['date']+' | '+day['city'],'Heading1');p('Local timezone: '+day['timezone']+'. Overnight: '+('Thingholt, two rooms' if day['hotel'] else 'No hotel night'))
 for e in day['events']:p(e['time']+' | '+e['title'])
 p('Personal notes: ____________________________________________________');p('________________________________________________________________')
 story.append(PageBreak())
p('Flights, hotel & practical checks','TitleGreen');p('FI602: YYZ March 13 19:40 - KEF March 14 06:25, 5h45 supplied. FI603: KEF March 18 17:00 - YYZ 19:15, 6h15 supplied. Economy Light, non-refundable; user-supplied C$200/person checked bag add-on needs return-basis verification. Flight clocks are local.');p('Thingholt by Center Hotels: March 14-18, four nights, two rooms, C$2,534 user Expedia.ca quote. Non-refundable. Upgrade C$49 per room, assumed per stay: verify. Confirm taxes, breakfast, twin beds, luggage storage and checkout. Early arrival does not include early check-in.');p('Flybus reference: about 45 minutes airport-BSI; hotel transfer adds time. Plan hotel pickup around 13:00 March 18 for 17:00 departure and verify voucher. Aim KEF 14:00-14:30; earlier if weather deteriorates.');p('Check passport-specific entry rules. Pack waterproof layers and suitable footwear. Follow guide, SafeTravel and weather alerts, including current Reynisfjara access. Aurora not guaranteed. No glacier hike included. Restaurant ratings and specific menus remain unresearched.');p('Booking checklist','Heading2')
for t in ['Re-quote flights and hotel; confirm baggage and seats','Confirm cancellation terms, taxes and breakfast','Book Flybus with correct pickup stop and buffer','Check each passport entry requirement','Book Golden Circle and South Coast with cancellation terms','Choose one lagoon; preserve a weather-swap day','Review insurance, data, weather and SafeTravel']:p('[  ] '+t)
story.append(PageBreak());p('Cost ledger | CAD','TitleGreen')
for r in d['ledger']:p(f"{r['title']}: ${r['amount']:,.2f} x {r['qty']} = ${r['amount']*r['qty']:,.2f}. {r['status']}. {'Optional; excluded.' if r['optional'] else 'Included in baseline.'}")
p('FX display uses illustrative C$0.01/ISK; no live conversion. Meals C$80/person/day for five days until breakfast inclusions known. Insurance/data reserve is an allowance. Baseline PDF does not contain subsequent browser edits.');story.append(PageBreak());p('Sources & evidence','TitleGreen')
for s in d['sources']:p(s['title'],'Heading3');p(s['url']);
p('Fare-watch text was supplied in the brief; automation existence/status has not been checked. No fare watch is created by this guide.')
def footer(c,doc):c.setFont('Helvetica',9);c.setFillColor(HexColor('#184b43'));c.drawString(45,25,'Iceland 2027 | Planning edition | '+str(doc.page))
SimpleDocTemplate(str(ROOT/'iceland-guide.pdf'),pagesize=(595,842),rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
h=(ROOT/'index.html').read_text()
for path in ['styles.css','assets/leaflet.css']:h=h.replace(f'<link rel="stylesheet" href="{path}">','<style>'+(ROOT/path).read_text()+'</style>')
for path in ['data.js','assets/leaflet.js','assets/outline.js','app.js']:h=h.replace(f'<script src="{path}"></script>','<script>'+(ROOT/path).read_text().replace('</script','<\\/script')+'</script>')
img='data:image/png;base64,'+base64.b64encode((ROOT/'assets/hotel.png').read_bytes()).decode();h=h.replace('assets/hotel.png',img)
# Rendered card images are inserted by inline app JS, whose paths are replaced above too.
(ROOT/'offline-guide.html').write_text(h)
print('PDF, CSV and standalone HTML exported')
