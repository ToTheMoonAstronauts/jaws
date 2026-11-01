"""Builds the Lithuanian legal pages in website-lt/ (formal "Jūs"). Run after tools/build_lt.py:
   python3 tools/build_legal_lt.py"""
import os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from lt_dict import PAIRS
src = open(os.path.join(HERE, "build_legal.py"), encoding="utf-8").read()
ns = {"__file__": os.path.join(HERE, "build_legal.py")}
exec(src[:src.index("PRELAUNCH = ")], ns)   # reuse shell(), FOOTER, DRAWER
_i = src.index("CSS_EXTRA = ")
exec(src[_i:src.index("BODIES = ", _i)], ns)
OUT = os.path.join(HERE, "..", "website-lt")
UPDATED = "2026 m. lapkričio 1 d."
EMAIL = "[kontaktinis el. paštas]"
ADDR = "[grąžinimo adresas], Lietuva"
OPERATOR = "[valdytojo juridinis pavadinimas]<br>[buveinės adresas]<br>Juridinio asmens kodas: [kodas]<br>PVM mokėtojo kodas: [PVM kodas arba: ne PVM mokėtojas]"

PAGES = [("terms.html","Pirkimo taisyklės"),("returns.html","Grąžinimas"),("withdraw.html","Atsisakyti sutarties"),
         ("shipping.html","Pristatymas ir apmokėjimas"),("privacy.html","Privatumas ir slapukai"),("safety.html","Saugos instrukcija"),("legal.html","Teisinė informacija")]
ns["TOC"] = "".join(f'<a href="{f}">{t}</a>' for f, t in PAGES)

PRELAUNCH = '''<div class="callout"><b>Prieš paleidimą.</b> Cutline dar neparduodama. Jei dabar pateiksite užsakymą, užregistruosime tik <b>išankstinio užsakymo prašymą</b>: pirkimo–pardavimo sutartis nesudaroma, mokėjimas nenuskaitomas ir mokėjimo duomenys nerenkami. Parašysime Jums, kai produktai bus prieinami, ir Jūs galėsite laisvai nuspręsti, ar pirkti.</div>'''

TERMS = f'''{PRELAUNCH}
<h2>1. Kas mes esame</h2>
<p>Cutline – Lietuvoje veikianti internetinė kietos kramtomosios gumos parduotuvė. Parduotuvę valdantis subjektas nurodytas skiltyje <a href="legal.html">Teisinė informacija</a>. El. paštas: {EMAIL}. Šios taisyklės taikomos visiems šioje svetainėje pateiktiems užsakymams.</p>
<h2>2. Laikotarpis iki paleidimo</h2>
<p>Kol rodomas aukščiau esantis pranešimas, parduotuvė naudojama susidomėjimui įvertinti prieš pradedant prekybą. Pateikus užsakymą sukuriamas išankstinio užsakymo prašymas, o ne pirkimas. Jūsų įvestus duomenis saugome tam, kad galėtume informuoti apie prekių prieinamumą (žr. <a href="privacy.html">Privatumo politiką</a>). Šiuo laikotarpiu jokie pinigai nenuskaitomi. 3–11 punktai taikomi, kai prekyba pradedama ir pranešimas pašalinamas.</p>
<h2>3. Kas gali pirkti</h2>
<p>Užsakymą pateikti gali asmenys nuo 18 metų arba nepilnamečiai, turintys tėvų ar globėjų sutikimą. Mūsų produktai neskirti jaunesniems nei 14 metų vaikams. Parduodame vartotojams Europos Sąjungoje. Už ES ribų kol kas nesiunčiame.</p>
<h2>4. Informacija apie prekes</h2>
<p>Prekes, jų sudėtį, maistinę vertę ir naudojimo instrukcijas aprašome kuo tiksliau. Nuotraukos gali šiek tiek skirtis nuo gautos pakuotės. Mūsų guma yra maisto produktas, skirtas kramtymo pratimams. Tai nėra medicinos priemonė ir ji negydo bei neapsaugo nuo jokių ligų.</p>
<h2>5. Sutarties sudarymas</h2>
<p>Prekių aprašymai yra kvietimas pateikti užsakymą. Paspaudę užsakymo mygtuką, Jūs pateikiate pasiūlymą pirkti. Užsakymo gavimą patvirtiname el. paštu. Sutartis sudaroma, kai išsiunčiame užsakymo patvirtinimą arba prekes, atsižvelgiant į tai, kas įvyksta anksčiau. Prieš pateikdami užsakymą, galite jį peržiūrėti ir pataisyti. Šias taisykles ir užsakymo duomenis atsiunčiame el. paštu, be to, šį puslapį galite išsaugoti arba atsispausdinti.</p>
<h2>6. Kainos ir apmokėjimas</h2>
<p>Kainos nurodytos eurais ir, kai taikoma, su PVM. Pristatymo kaina parodoma prieš pateikiant užsakymą. Mokėjimus apdoroja licencijuoti mokėjimo paslaugų teikėjai – mes niekada nematome ir nesaugome viso Jūsų kortelės numerio. Mokėjimas nuskaitomas pateikus užsakymą. Kai rodome sumažintą kainą, palyginamoji kaina yra mažiausia kaina, taikyta per 30 dienų iki kainos sumažinimo.</p>
<h2>7. Pristatymas</h2>
<p>Prekes pristatome per terminą, nurodytą skiltyje <a href="shipping.html">Pristatymas ir apmokėjimas</a>, ir bet kuriuo atveju ne vėliau kaip per 30 dienų nuo sutarties sudarymo, jei nesusitarta kitaip. Jei prekės negalime pristatyti, nes jos nebeturime, nedelsdami Jums apie tai pranešame ir grąžiname sumokėtus pinigus per 14 dienų. Prekių praradimo rizika Jums pereina, kai prekes gaunate Jūs arba Jūsų nurodytas asmuo.</p>
<h2>8. Teisė atsisakyti sutarties</h2>
<p>Per 14 dienų galite atsisakyti sutarties nenurodydami priežasties. Išsami informacija, išimtys ir prekių grąžinimo tvarka pateikta skiltyje <a href="returns.html">Grąžinimas</a>. Sutarties atsisakyti galite bet kada internetu per formą <a href="withdraw.html">Atsisakyti sutarties čia</a>. Pristatytos ir Jūsų atplėštos gumos pakuotės dėl sveikatos apsaugos ir higienos priežasčių grąžinti negalima.</p>
<h2>9. Teisinė garantija</h2>
<p>Turite įstatymų nustatytas teises dėl sutarties neatitinkančių prekių 2 metus nuo pristatymo. Jei prekė su trūkumais, sugadinta pervežant ar gavote ne tą prekę, parašykite {EMAIL}, nurodykite užsakymo numerį ir pridėkite nuotrauką. Prekę nemokamai pakeisime arba grąžinsime pinigus. Prekes suvartokite iki ant pakuotės nurodytos tinkamumo vartoti datos.</p>
<h2>10. Atsakomybė</h2>
<p>Pagal taikomus įstatymus atsakome už žalą, padarytą tyčia ar dėl didelio neatsargumo, už gyvybės atėmimą ar sveikatos sužalojimą ir pagal atsakomybės už produktus taisykles. Už kitą dėl nedidelio neatsargumo padarytą žalą atsakome tik tiek, kiek ji yra numatoma ir būdinga tokio pobūdžio sutarčiai. Šios taisyklės neriboja Jūsų, kaip vartotojo, teisių. Laikykitės <a href="safety.html">Saugos instrukcijos</a>: žala, atsiradusi naudojant produktą ne pagal ją, nėra produkto trūkumo pasekmė.</p>
<h2>11. Atsiliepimai ir Jūsų pateiktas turinys</h2>
<p>Atsiliepimus mūsų svetainėje skelbia pirkėjai, turintys patvirtintą užsakymą. Neskelbiame atsiliepimų, už kuriuos sumokėjome ar kuriuos parašėme patys, ir nešaliname neigiamų atsiliepimų vien dėl to, kad jie neigiami. Atsiųsdami atsiliepimą ar nuotrauką, leidžiate juos skelbti mūsų svetainėje ir socialiniuose tinkluose kartu su Jūsų vardu. Bet kada galite paprašyti juos pašalinti.</p>
<h2>12. Skundai ir ginčai</h2>
<p>Pirmiausia kreipkitės į mus el. paštu {EMAIL}. Atsakome per 14 dienų. Jei klausimo išspręsti nepavyksta, galite nemokamai kreiptis į Valstybinę vartotojų teisių apsaugos tarnybą, Vilniaus g. 25, 01402 Vilnius, <a href="https://www.vvtat.lt" rel="noopener">www.vvtat.lt</a>, arba į savo šalies vartotojų teisių institucijas ar teismus.</p>
<h2>13. Taikoma teisė</h2>
<p>Šioms taisyklėms taikoma Lietuvos Respublikos teisė. Jei esate vartotojas, gyvenantis kitoje ES valstybėje, Jums išlieka Jūsų šalies imperatyviųjų vartotojų apsaugos normų apsauga.</p>
<h2>14. Pakeitimai</h2>
<p>Šias taisykles galime atnaujinti būsimiems užsakymams. Užsakymui taikoma jo pateikimo metu galiojusi taisyklių redakcija.</p>'''

RETURNS = f'''{PRELAUNCH}
<h2>Teisė atsisakyti sutarties per 14 dienų</h2>
<p>Per 14 dienų galite atsisakyti sutarties nenurodydami jokios priežasties. Terminas baigiasi praėjus 14 dienų nuo tos dienos, kai Jūs arba Jūsų nurodytas asmuo (ne vežėjas) gaunate prekes. Jei užsakėte kelias prekes, pristatomas atskirai, terminas skaičiuojamas nuo paskutinės prekės gavimo.</p>
<h2>Kaip atsisakyti sutarties</h2>
<p>Iki termino pabaigos aiškiai praneškite mums apie savo sprendimą. Greičiausia tai padaryti per internetinę formą <a href="withdraw.html">Atsisakyti sutarties čia</a>. Taip pat galite rašyti el. paštu {EMAIL} arba paštu adresu Cutline, {ADDR}. Galite naudoti žemiau pateiktą pavyzdinę formą, bet tai neprivaloma.</p>
<h2>Prekių grąžinimas</h2>
<p>Prekes grąžinkite nedelsdami ir ne vėliau kaip per 14 dienų nuo pranešimo apie sutarties atsisakymą adresu Cutline, {ADDR}. Nurodykite užsakymo numerį. Tiesiogines prekių grąžinimo išlaidas apmokate Jūs. Atsakote tik už prekių vertės sumažėjimą, atsiradusį dėl elgesio su prekėmis, kuris nebuvo būtinas jų pobūdžiui ir savybėms nustatyti.</p>
<h2>Higienos išimtis gumai</h2>
<p>Mūsų guma tiekiama sandariose pakuotėse. Dėl sveikatos apsaugos ir higienos priežasčių Jūsų po pristatymo atplėštos pakuotės grąžinti negalima – teisė atsisakyti sutarties dėl šios pakuotės baigiasi ją atplėšus. Neatplėštas, sandarias pakuotes per 14 dienų grąžinti galima visada.</p>
<h2>Pinigų grąžinimas</h2>
<p>Visas iš Jūsų gautas įmokas, įskaitant standartinio pristatymo išlaidas, grąžiname nedelsdami ir ne vėliau kaip per 14 dienų nuo pranešimo apie sutarties atsisakymą gavimo. Jei pasirinkote brangesnį nei mūsų standartinis pristatymo būdą, kainų skirtumo negrąžiname. Pinigus grąžiname tuo pačiu mokėjimo būdu, kurį naudojote, nebent susitartume kitaip, ir už tai neimame jokio mokesčio. Pinigų grąžinimą galime sulaikyti, kol gausime prekes arba Jūs pateiksite įrodymą, kad jas išsiuntėte, atsižvelgiant į tai, kas įvyksta anksčiau.</p>
<h2>Prekės su trūkumais, sugadintos ar ne tos</h2>
<p>Tai nesusiję su sutarties atsisakymu – tam taikoma teisinė garantija. Per protingą laiką nuo trūkumo pastebėjimo parašykite {EMAIL}, nurodykite užsakymo numerį ir pridėkite nuotrauką. Atsiųsime naują prekę arba grąžinsime pinigus, o prekės grąžinti ar mokėti už siuntimą nereikės.</p>
<h2>Pavyzdinė sutarties atsisakymo forma</h2>
<div class="formbox">
<p>Kam: Cutline, {ADDR}, {EMAIL}</p>
<p>Aš / Mes (*) pranešu / pranešame (*), kad atsisakau / atsisakome (*) savo sutarties dėl šių prekių pirkimo (*):</p>
<p>Užsakymo data (*) / gavimo data (*):<br>Vartotojo (-ų) vardas, pavardė:<br>Vartotojo (-ų) adresas:<br>Vartotojo (-ų) parašas (tik jei ši forma pateikiama popieriuje):<br>Data:</p>
<p><small>(*) Išbraukite, kas netinka.</small></p>
</div>'''

WITHDRAW = f'''<p>Šia forma galite atsisakyti sutarties per 14 dienų sutarties atsisakymo terminą. Prisijungti ar nurodyti priežastį nereikia. Patvirtinę matysite patvirtinimą su sutarties atsisakymo gavimo data ir laiku. Išsaugokite jį arba padarykite ekrano nuotrauką; be to, per 2 darbo dienas patvirtinsime el. paštu.</p>
<div class="callout"><b>Prieš paleidimą:</b> pirkimo–pardavimo sutarčių dar nėra, todėl jokie pinigai negali būti nuskaityti. Jei pateikėte išankstinio užsakymo prašymą ir norite, kad jį ištrintume, galite naudoti šią formą arba parašyti {EMAIL}.</div>
<form id="wForm" class="wform" novalidate>
  <div class="step" id="wStep1">
    <h2>1 žingsnis: Jūsų duomenys</h2>
    <div class="f-grid2">
      <div class="field"><label for="wName">Vardas ir pavardė</label><input id="wName" autocomplete="name" required><span class="err" id="wNameErr"></span></div>
      <div class="field"><label for="wEmail">Užsakymo el. paštas</label><input id="wEmail" type="email" autocomplete="email" required><span class="err" id="wEmailErr"></span></div>
      <div class="field"><label for="wOrder">Užsakymo numeris (jei turite)</label><input id="wOrder" placeholder="pvz., #1042"></div>
      <div class="field"><label for="wDate">Užsakymo data (jei žinote)</label><input id="wDate" type="date"></div>
      <div class="field full"><label for="wItems">Kurios prekės? (palikite tuščią, jei visas užsakymas)</label><input id="wItems" placeholder="pvz., Kieta guma, Mėtų, 6 mėnesių atsargos"></div>
    </div>
    <button class="btn big" type="button" id="wNext">Tęsti</button>
  </div>
  <div class="step" id="wStep2" hidden>
    <h2>2 žingsnis: patvirtinimas</h2>
    <div class="formbox" id="wSummary"></div>
    <div class="cta-row"><button class="btn big" type="submit" id="wSubmit">Patvirtinti sutarties atsisakymą</button><button class="btn ghost" type="button" id="wBack">Taisyti duomenis</button></div>
  </div>
  <div class="step" id="wDone" hidden>
    <h2>Sutarties atsisakymas gautas</h2>
    <div class="callout ok" id="wReceipt"></div>
    <p>Išsaugokite šį patvirtinimą. Jei jau gavote prekes, neatplėštas pakuotes grąžinkite per 14 dienų, kaip nurodyta skiltyje <a href="returns.html">Grąžinimas</a>.</p>
  </div>
  <p class="err" id="wErr"></p>
</form>'''

WITHDRAW_JS = '''
<script>
const v=id=>document.getElementById(id).value.trim();
const esc=s=>s.replace(/</g,"&lt;");
const okEmail=e=>/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(e);
$("wNext").addEventListener("click",()=>{
  let ok=true;
  $("wNameErr").textContent=v("wName")?"":(ok=false,"Įveskite vardą ir pavardę.");
  $("wEmailErr").textContent=okEmail(v("wEmail"))?"":(ok=false,"Įveskite teisingą el. pašto adresą.");
  if(!ok)return;
  $("wSummary").innerHTML=`<p>Atsisakau sutarties dėl: <b>${esc(v("wItems"))||"viso užsakymo"}</b>.</p><p>Vardas, pavardė: <b>${esc(v("wName"))}</b><br>El. paštas: <b>${esc(v("wEmail"))}</b><br>Užsakymas: <b>${esc(v("wOrder"))||"nenurodytas"}</b>, užsakyta <b>${v("wDate")||"data nenurodyta"}</b></p>`;
  $("wStep1").hidden=true;$("wStep2").hidden=false;$("wSubmit").focus();
});
$("wBack").addEventListener("click",()=>{$("wStep2").hidden=true;$("wStep1").hidden=false});
$("wForm").addEventListener("submit",async e=>{
  e.preventDefault();$("wSubmit").disabled=true;$("wErr").textContent="";
  const ok=await sbInsert("withdrawals",{full_name:v("wName").slice(0,200),email:v("wEmail").slice(0,254),order_ref:v("wOrder").slice(0,100)||null,order_date:v("wDate")||null,items:v("wItems").slice(0,1000)||null,lang:"lt"});
  if(!ok){$("wSubmit").disabled=false;$("wErr").textContent="Nepavyko išsiųsti. Bandykite dar kartą arba parašykite mums el. paštu – toks pranešimas taip pat galioja.";return}
  const t=new Date();
  $("wReceipt").innerHTML=`Jūsų sutarties atsisakymą gavome <b>${t.toLocaleDateString("lt-LT",{year:"numeric",month:"long",day:"numeric"})}</b>, <b>${t.toLocaleTimeString("lt-LT",{hour:"2-digit",minute:"2-digit"})}</b> (${Intl.DateTimeFormat().resolvedOptions().timeZone}). Per 2 darbo dienas patvirtinsime el. paštu ${esc(v("wEmail"))}.`;
  $("wStep2").hidden=true;$("wDone").hidden=false;
});
</script>'''

SHIPPING = f'''{PRELAUNCH}
<h2>Kur siunčiame</h2>
<p>Siunčiame į visas ES šalis iš Lietuvos. Už ES ribų kol kas nesiunčiame. Kadangi ES viduje muitų nėra, pristatant nereikės mokėti jokių importo muitų ar papildomų mokesčių.</p>
<h2>Kainos ir pristatymo terminai</h2>
<div class="table-scroll"><table class="compare">
<thead><tr><th>Šalis</th><th>Standartinis pristatymas</th><th>Įprastas terminas</th></tr></thead>
<tbody>
<tr><td>Lietuva, Latvija, Estija</td><td>4,95 € · nemokamai nuo 49 €</td><td>1–3 darbo dienos</td></tr>
<tr><td>Lenkija, Suomija, Vokietija, Šiaurės šalys</td><td>4,95 € · nemokamai nuo 49 €</td><td>2–5 darbo dienos</td></tr>
<tr><td>Kitos ES šalys</td><td>4,95 € · nemokamai nuo 49 €</td><td>3–7 darbo dienos</td></tr>
</tbody></table></div>
<p>Užsakymus išsiunčiame per 1–2 darbo dienas. Pristatymo terminai skaičiuojami nuo išsiuntimo ir yra preliminarūs. Kai siunta bus išsiųsta, el. paštu gausite sekimo nuorodą.</p>
<h2>Adreso klaidos ir grąžintos siuntos</h2>
<p>Užsakydami patikrinkite adresą ir telefono numerį. Jei siunta grįžta mums dėl neišsamaus adreso ar neatsiimta, susisieksime su Jumis ir, sumokėjus naujo siuntimo kainą, išsiųsime ją pakartotinai arba grąžinsime pinigus, atskaičiavę patirtas siuntimo išlaidas.</p>
<h2>Pamestos ar vėluojančios siuntos</h2>
<p>Jei siuntos būsena nesikeičia 7 darbo dienas arba rodo „pristatyta“, bet jos negavote, parašykite {EMAIL}. Pradėsime tyrimą su vežėju ir, jei siunta pamesta, atsiųsime naują arba grąžinsime visus pinigus. Kol prekės Jūsų nepasiekė, rizika tenka mums.</p>
<h2>Apmokėjimas</h2>
<p>Pradėjus prekybą, priimsime mokėjimo korteles (Visa, Mastercard, American Express), PayPal, Apple Pay, Google Pay ir Klarna – mokėjimus apdoros licencijuoti mokėjimo paslaugų teikėjai. Mokėjimas nuskaitomas pateikus užsakymą. Visos kainos nurodytos eurais ir, kai taikoma, su PVM.</p>
<h2>Siuntimas už ES ribų</h2>
<p>Ateityje planuojame siųsti į JK ir JAV. Visoms siuntoms į JAV dabar taikomi importo muitai, todėl ten siųsime tik muitus ir mokesčius surinkę apmokėjimo metu (DDP), kad pristatant nereikėtų nieko primokėti.</p>'''

PRIVACY = f'''<h2>1. Kas atsakingas už Jūsų duomenis</h2>
<p>Duomenų valdytojas yra Cutline valdantis subjektas, nurodytas skiltyje <a href="legal.html">Teisinė informacija</a>. Visais privatumo klausimais rašykite {EMAIL}. Duomenų apsaugos pareigūno nesame paskyrę.</p>
<h2>2. Kokius duomenis renkame ir kodėl</h2>
<div class="table-scroll"><table class="compare">
<thead><tr><th>Duomenys</th><th>Tikslas</th><th>Teisinis pagrindas (BDAR)</th><th>Saugojimo terminas</th></tr></thead>
<tbody>
<tr><td>Užsakymas: el. paštas, vardas, pavardė, šalis, pasirinktas mokėjimo būdas, krepšelio turinys ir suma</td><td>Tvarkyti Jūsų išankstinio užsakymo prašymą ar užsakymą ir susisiekti dėl jo</td><td>6 str. 1 d. b p., Jūsų prašymu atliekami veiksmai prieš sudarant sutartį</td><td>Išankstiniai užsakymai: iki paleidimo + 6 mėn. arba kol paprašysite ištrinti. Užsakymai: tiek, kiek reikalauja mokesčių ir apskaitos teisės aktai (iki 10 metų)</td></tr>
<tr><td>Rinkodaros laiškai (tik jei pažymite varnelę arba užsiregistruojate naujienlaiškiui)</td><td>Siųsti treniruočių patarimus ir pasiūlymus</td><td>6 str. 1 d. a p., Jūsų sutikimas, kurį galite bet kada atšaukti</td><td>Kol atsisakysite</td></tr>
<tr><td>Naudojimosi analitika (tik jei sutinkate su analitikos slapukais): atsitiktinis naršyklės identifikatorius, peržiūrėti puslapiai, krepšelio ir apmokėjimo žingsniai, nukreipusi svetainė ir kampanijos žymos</td><td>Suprasti, kiek lankytojų domisi mūsų produktu, ir tobulinti parduotuvę</td><td>6 str. 1 d. a p., sutikimas</td><td>24 mėnesiai</td></tr>
<tr><td>Sutarties atsisakymo prašymai: vardas, pavardė, el. paštas, užsakymo duomenys</td><td>Įvykdyti sutarties atsisakymą ir išsaugoti įrodymą</td><td>6 str. 1 d. c p., teisinė prievolė</td><td>3 metai</td></tr>
<tr><td>Serverio žurnalai (IP adresas, naršyklė, laikas), kuriuos saugo svetainės talpintojas</td><td>Saugiai teikti svetainę</td><td>6 str. 1 d. f p., teisėtas interesas užtikrinti svetainės saugumą</td><td>Nustato talpintojas, paprastai kelios dienos</td></tr>
</tbody></table></div>
<p>Mokėjimo kortelių numerių nerenkame. Mokėjimus tiesiogiai apdoros mokėjimo paslaugų teikėjai pagal savo privatumo sąlygas. Jūsų duomenų neparduodame ir nenaudojame automatizuotiems sprendimams, turintiems teisinių pasekmių.</p>
<h2>3. Slapukai ir naršyklės atmintis</h2>
<p>Reklaminių slapukų nenaudojame. Jūsų naršyklėje saugome: krepšelį (būtina parduotuvės veikimui, sutikimo nereikia), Jūsų slapukų pasirinkimą ir, tik jei sutinkate su analitika, atsitiktinį identifikatorių, siejantį Jūsų apsilankymus. Pasirinkimą bet kada galite pakeisti skiltyje <a href="#" data-cookie-settings>Slapukų nustatymai</a>. Jei ateityje naudosime reklamos pikselius (pvz., Meta ar Google), pirmiausia paprašysime atskiro sutikimo ir atnaujinsime šią politiką.</p>
<h2>4. Kas tvarko duomenis mūsų vardu</h2>
<ul>
<li><b>Supabase</b> (Supabase Inc., JAV): užsakymų, išankstinių užsakymų ir analitikos duomenų bazė. Duomenys saugomi ES (Airijoje).</li>
<li><b>GitHub Pages</b> (GitHub Inc., JAV): svetainės talpinimas.</li>
<li><b>Google Fonts</b> (Google Ireland Ltd.): svetainės šriftai; Jūsų naršyklė jungiasi prie Google serverių.</li>
</ul>
<p>Kai paslaugų teikėjas yra už ES ribų, duomenys perduodami remiantis ES ir JAV duomenų privatumo sistema arba Europos Komisijos patvirtintomis standartinėmis sutarčių sąlygomis (BDAR 45–46 str.).</p>
<h2>5. Jūsų teisės</h2>
<p>Galite prašyti susipažinti su savo duomenimis, juos ištaisyti ar ištrinti, apriboti jų tvarkymą ar nesutikti su juo, gauti juos perkeliamu formatu ir bet kada atšaukti sutikimą (tai neturi įtakos ankstesniam tvarkymui). Rašykite {EMAIL} – atsakysime per vieną mėnesį. Taip pat galite pateikti skundą Valstybinei duomenų apsaugos inspekcijai, L. Sapiegos g. 17, 10312 Vilnius, <a href="https://vdai.lrv.lt" rel="noopener">vdai.lrv.lt</a>, arba savo šalies priežiūros institucijai.</p>
<h2>6. Vaikai</h2>
<p>Mūsų parduotuvė neskirta vaikams. Sąmoningai nerenkame jaunesnių nei 16 metų asmenų duomenų.</p>
<h2>7. Pakeitimai</h2>
<p>Pasikeitus duomenų tvarkymui, atnaujinsime šį puslapį ir viršuje nurodysime datą.</p>'''

SAFETY = '''<p>Cutline guma gerokai kietesnė už paprastą kramtomąją gumą. Tai treniruočių produktas: tinkamai naudojamas, jis saugus sveikiems suaugusiesiems. Prieš pirmą treniruotę perskaitykite šią instrukciją.</p>
<h2>Kam negalima naudoti</h2>
<ul>
<li>Jaunesniems nei 14 metų vaikams. Laikykite mažiems vaikams nepasiekiamoje vietoje – gali užspringti.</li>
<li>Asmenims, jaučiantiems žandikaulio sąnario skausmą, spragsėjimą, strigimą ar ribotą burnos atvėrimą.</li>
<li>Asmenims, turintiems klibančių dantų, atsilaisvinusių plombų, vainikėlių, laminačių, tiltų ar implantų arba neseniai gydžiusiems dantis. Ypač kietos gumos negalima naudoti su jokiais dantų protezais ar restauracijomis.</li>
<li>Nešiojantiems breketus ar kapas.</li>
</ul>
<p>Jei abejojate, prieš pradėdami pasitarkite su odontologu ar gydytoju.</p>
<h2>Kaip saugiai naudoti</h2>
<ul>
<li>Laikykitės 30 dienų plano: vieną dieną pilna treniruotė (iki 15 minučių), kitą – vienas ratas (apie 8 minutes). Niekada nekramtykite ilgiau kaip 15 minučių per dieną. Daugiau kramtymo nereiškia greitesnio progreso.</li>
<li>Jei kitą rytą žandikaulį skauda labiau nei įprastas raumenų maudimas, padarykite dienos pertrauką.</li>
<li>Pirmiausia sušildykite gabalėlį burnoje ir sukąskite palaipsniui. Staigiai sukandus šaltą, kietą gumą, ji gali suskilti arba pažeisti dantis.</li>
<li>Kramtykite galiniais krūminiais, ne priekiniais dantimis. Tolygiai keiskite puses.</li>
<li>Niekada neryk gumos.</li>
<li>Kiekvienai treniruotei naudokite naują gabalėlį, o panaudotą išmeskite. Sukramtytos gumos nelaikykite vėlesniam kartui.</li>
</ul>
<h2>Nutraukite ir pasitarkite su specialistu, jei</h2>
<ul>
<li>Jaučiate aštrų danties ar žandikaulio sąnario skausmą.</li>
<li>Kitą dieną žandikaulis spragsi, stringa ar skauda labiau nei įprastas raumenų maudimas.</li>
<li>Po treniruotės skauda galvą ar ausis.</li>
</ul>
<p>Raumenų maudimas, praeinantis per dieną, yra normalu. Skausmas – ne.</p>
<h2>Sudėtis ir mityba</h2>
<p>Kietoje ir ypač kietoje gumoje yra poliolių saldiklių. Vartojant per daug, gali sukelti laisvinamąjį poveikį. Visa sudėtis ir maistinė vertė nurodyta kiekvieno produkto puslapyje ir ant pakuotės. Jei turite konkrečių klausimų dėl alergijų, susisiekite su mumis prieš užsakydami.</p>
<h2>Ko tikėtis</h2>
<p>Kieta guma treniruoja kramtymo raumenis. Kaip atrodo žandikaulio linija, taip pat priklauso nuo riebalų kiekio, genetikos ir kaulų sandaros. Nežadame jokio konkretaus vizualinio rezultato, o produktas nėra skirtas jokiai ligai diagnozuoti, gydyti ar jos išvengti.</p>'''.replace("Niekada neryk gumos.","Niekada nenurykite gumos.")

LEGAL = f'''<h2>Valdytojas</h2>
<p>Cutline valdo:<br>{OPERATOR}<br>El. paštas: {EMAIL}</p>
<p>Maisto tvarkymo subjekto registracija Valstybinėje maisto ir veterinarijos tarnyboje (VMVT): [registracijos numeris, iki prekybos pradžios].</p>
<h2>Vartotojų ginčai</h2>
<p>ES elektroninio ginčų sprendimo platforma uždaryta 2025 m. liepos 20 d. Kilus ginčui, pirmiausia kreipkitės į mus; vėliau galite kreiptis į Valstybinę vartotojų teisių apsaugos tarnybą, Vilniaus g. 25, 01402 Vilnius, <a href="https://www.vvtat.lt" rel="noopener">www.vvtat.lt</a>. Ginčų nagrinėjimas ne teismo tvarka vartotojams nemokamas, ir mes jame dalyvaujame.</p>
<h2>Svetainės turinys</h2>
<p>Informaciją šioje svetainėje, įskaitant treniruočių rekomendacijas, rengiame atidžiai, tačiau tai bendra informacija, o ne medicininė ar odontologinė konsultacija. Neatsakome už išorinių svetainių, į kurias pateikiame nuorodas, turinį; sužinoję, kad nuorodos puslapis pažeidžia teisę, nuorodą pašaliname.</p>
<h2>Autorių teisės ir prekių ženklai</h2>
<p>Tekstai, grafika, Cutline pavadinimas ir logotipas priklauso Cutline valdytojui, jei nenurodyta kitaip. Kai kurios nuotraukos naudojamos pagal Unsplash licenciją. Mūsų turinio nekopijuokite komerciniais tikslais be rašytinio leidimo.</p>'''

EXTRA = [
 ('<html lang="en">','<html lang="lt">'),
 ('<p class="updated">Last updated 1 November 2026</p>',f'<p class="updated">Atnaujinta {UPDATED}</p>'),
 ('aria-label="Legal pages"','aria-label="Teisiniai puslapiai"'),
 ('<a href="index.html#faq">FAQ</a>','<a href="index.html#faq">DUK</a>'),
 ('<span id="cartTotal">€0,00</span>','<span id="cartTotal">0,00 €</span>'),
]
BODIES = {"terms.html":("Taisyklės",TERMS,""),"returns.html":("Taisyklės",RETURNS,""),"withdraw.html":("Jūsų 14 dienų teisė",WITHDRAW,WITHDRAW_JS),
          "shipping.html":("Taisyklės",SHIPPING,""),"privacy.html":("Taisyklės",PRIVACY,""),"safety.html":("Prieš pradedant",SAFETY,""),"legal.html":("Rekvizitai",LEGAL,"")}
shell_pairs = sorted(PAIRS + EXTRA, key=lambda x: -len(x[0]))
for f, title in PAGES:
    eyebrow, body, js = BODIES[f]
    page = ns["shell"](title, eyebrow, "@@BODY@@", ns["CSS_EXTRA"], "@@JS@@").replace("index-v2.html", "index.html")
    page = page.replace("<title>"+title+" · Cutline</title>", "<title>"+title+" · Cutline</title>")
    for en, lt in shell_pairs:
        page = page.replace(en, lt)
    page = page.replace("@@BODY@@", body).replace("@@JS@@", js)
    page = page.replace(f'<a href="{f}">', f'<a href="{f}" aria-current="page">', 1)
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(page)
    print("wrote", f)
