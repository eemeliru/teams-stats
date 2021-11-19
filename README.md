# Teams palaveri statistiikat

Työkalu yhdistää kansiosta löytyvät Teamsin luomat kokousraportit hienoiksi tilastoiksi/graafeiksi. 

Vaatii: 
Pythonin toimiakseen (testattu versiolla 3.8.7.)
Teams asetettu englannin kielelle

[DEMOPAGE](http://teams-stats-anon.herokuapp.com/)
u: teams
pw: stats@nonymis3D!

### Käyttöohje:  
1. Lataa Teamsin luomat kokouksen osallistumisraportit (löytyvät kokouksen chatista)
2. Siirrä raportit samaan kansioon näiden koodien kanssa
3. Avaa kansioon komentorivi/Powershell & syötä komento: ``pip install -r requirements.txt``
4. Aja CSV2XLSXrunner.py , joka muuttaa Teamsin luomat pseudo-csv -tiedostot .xlsx -muotoon
5. Aja ExcelCombiner.py, joka tekee raporteille esikäsittelyt ja yhdistää ne yhteen .csv -tiedostoon
   1. (Datasetin anonymisointia varten aja anonGen.py tässä kohtaa)
6. Aja app.py, joka tekee graafit + avaa osoitteeseen 127.0.0.1:8050 -Dash serverin, josta voit katsoa tilastoja. Jos haluat paikallisen .html -tiedoston, paina sivun vasemmasta alanurkasta löytyvää "Download HTML" -nappia.

Enjoy :)
