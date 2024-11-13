# youtube-trends

## Propozycja Projektu


24.10.2024

Adam Bednarski, Jan Masłowski, Łukasz Lenkiewicz, Oliwer Krupa

AJLO  


<p align="center">
Propozycja projektu: <b>Analiza migracji trendów zagranicznych na rynek polski </b>
</p>

<br/><br/>
**Tło projektu**  
Na polskiej scenie YouTube można zaobserwować silną inspirację trendami i pomysłami pochodzącymi z amerykańskiego YouTube'a. Nowe formaty, style narracji oraz tematyka często pojawiają się najpierw w USA, a dopiero później są adaptowane przez twórców z Polski. Projekt ma na celu stworzenie narzędzia, które umożliwi wczesne wykrywanie nadchodzących trendów na amerykańskiej platformie, co pozwoli na szybszą adaptację i wykorzystanie ich na polskim rynku. W ten sposób twórcy w Polsce zyskają możliwość wcześniejszego reagowania na zmiany w preferencjach widzów.

<br/><br/>
**Naukowe/technologiczne pytania**  
- Czy polscy twórcy na YouTube faktycznie inspirują się amerykańskimi trendami, a jeśli tak, to w jakim stopniu?  
- Jak silny jest wpływ zagranicznych trendów na polską scenę YouTube?  
- Jakie tematy i formaty najczęściej przenikają między rynkami amerykańskim a polskim?  
- Czy trendy, które zyskują popularność w USA, równie dobrze przyjmują się w Polsce?  
- Czy możliwa jest analiza, która pozwoli na przewidywanie przyszłych trendów na polskim YouTube na podstawie obserwacji amerykańskiego rynku?

- Które elementy treści (np. tytuły, opisy, miniaturki) zawierają najwięcej informacji przydatnych do przewidywania trendów?  
- Jakie algorytmy są najbardziej odpowiednie do przewidywania nadchodzących trendów na platformach wideo?  
- Jakie kryteria należy przyjąć przy wyborze odpowiedniej próbki danych do analizy?  
- Skąd pozyskać dane potrzebne do analizy trendów, zarówno z amerykańskiego, jak i polskiego YouTube'a?  
- Ile danych jest potrzebnych, aby przewidywania były wiarygodne i statystycznie istotne?

<br/><br/>
**Rezultat końcowy**
Celem projektu będzie stworzenie systemu do wczesnego wykrywania trendów na amerykańskim YouTube i przewidywania ich wpływu na polską scenę. Rezultatem końcowym będzie dogłębna analiza, która wskaże, jakie kategorie i formaty treści mają największy potencjał do zdobywania popularności w Polsce, wraz z identyfikacją tych, które generują najwięcej wyświetleń. Dodatkowo, projekt może dostarczyć rekomendacje dla twórców, wskazując, które elementy treści mają największy wpływ na popularność filmów.

<br/><br/>
**Kluczowi interesariusze**  
W poniższej tabeli zidentyfikowani są kluczowi interesariusze projektu, którzy będą bezpośrednio lub pośrednio zaangażowani w jego realizację i korzystanie z wyników:

| Typ interesariusza                  | Nazwa                                                      |
| ----------------------------------- | ---------------------------------------------------------- |
| Twórcy treści na YouTube             | Polscy i amerykańscy twórcy YouTube, poszukujący nowych trendów |
| Platformy analizujące dane internetowe | Firmy i startupy zajmujące się analizą danych i predykcją trendów |
| Managerowie marketingu i contentu   | Osoby odpowiedzialne za strategie contentowe w agencjach digitalowych |
| Zespół badawczy                     | Zespół realizujący projekt, w tym analitycy danych i specjaliści od AI |
| Odbiorcy treści na YouTube           | Widzowie YouTube, na których preferencje będą wpływać przewidywane trendy |
| Potencjalni sponsorzy                | Firmy lub marki, które mogą być zainteresowane inwestowaniem w treści bazujące na przewidywanych trendach |
| Platformy społecznościowe            | YouTube i inne platformy, na których monitorowane będą trendy |



<br/><br/>
**Dane**  
Dane będą pozyskiwane z YouTube za pomocą YouTube Data API, co umożliwi zbieranie informacji o filmach (tytuły, opisy, miniaturki, wyświetlenia itp.) zarówno z polskiej, jak i amerykańskiej platformy. Próbka danych zostanie odpowiednio dobrana, aby reprezentować różnorodne kategorie treści i okresy, zapewniając dokładną analizę trendów.

<br/><br/>
**Plan prac**  
Realizacja projektu zostanie podzielona na kilka kluczowych faz, z jasno określonymi zadaniami w każdej z nich. Struktura prac będzie oparta na metodyce Work Breakdown Structure (WBS):

1. **Faza 1: Pobranie danych**
   - Zadanie 1.1: Research dostępnych źródeł danych na YouTube (polska i amerykańska scena).
   - Zadanie 1.2: Uzyskanie dostępu do YouTube Data API.
   - Zadanie 1.3: Pobieranie danych o filmach (tytuły, opisy, miniaturki, wyświetlenia itp.).

2. **Faza 2: Obróbka danych**
   - Zadanie 2.1: Wstępne oczyszczenie i przetwarzanie danych (usuwanie duplikatów, filtrowanie).
   - Zadanie 2.2: Klasyfikacja treści na kategorie (np. tematyka, formaty).
   - Zadanie 2.3: Przygotowanie zbioru danych do analizy.

3. **Faza 3: Tworzenie modelu**
   - Zadanie 3.1: Wybór odpowiednich algorytmów do przewidywania trendów i migracji trendów między rynkami.
   - Zadanie 3.2: Trening modeli na zebranych danych (testowanie i fine-tuning).

4. **Faza 4: Analiza i wizualizacja efektów**
   - Zadanie 4.1: Badanie czy jeśli tak to które trendy posłużyły za inspiracje na innym rynku.
   - Zadanie 4.2: Analiza wyników modelu w kontekście polskiego i amerykańskiego YouTube.
   - Zadanie 4.3: Wizualizacja wyników (dashboard, wykresy trendów).
   - Zadanie 4.4: Przygotowanie końcowego raportu i rekomendacji dla twórców.

Każda faza zakończy się sprawdzeniem postępów, co umożliwi wczesne wykrycie ewentualnych problemów i dostosowanie dalszych działań.

<br/><br/>
**Kluczowe wskaźniki efektywności (KPI)**  
Wskaźniki efektywności projektu zostaną oparte na kluczowych celach poszczególnych faz projektu. Każdy KPI będzie spełniał kryteria SMART – będzie konkretny, mierzalny, osiągalny, realistyczny i osadzony w czasie. Prowadzący zajęcia będzie mógł ocenić postęp na podstawie tych wskaźników, monitorując kluczowe etapy projektu.

Przykładowe KPI:

1. **Faza 1: Pobranie danych**
   - **KPI 1.1**: Pozyskanie co najmniej 20 000 unikalnych rekordów z YouTube Data API do 2024-11-01.
   - **KPI 1.2**: Dane z co najmniej 100 najpopularniejszych kanałów w Polsce i USA do 2024-11-01.

2. **Faza 2: Obróbka danych**
   - **KPI 2.1**: Oczyszczenie danych i podział na kategorie (np. tematyka, format) do 2024-11-08.
   - **KPI 2.2**: Gotowy zestaw danych do analizy z poprawnie zaklasyfikowanymi treściami do 2024-11-08.

3. **Faza 3: Tworzenie modelu**
   - **KPI 3.1**: Wytrenowanie modelu predykcyjnego z co najmniej 80% dokładnością na zbiorze testowym do 2024-11-15.
   - **KPI 3.2**: Osiągnięcie poziomu F1=0.85 w modelu przewidującym popularność trendów do 2024-11-15.

4. **Faza 4: Analiza i wizualizacja**
   - **KPI 4.1**: Stworzenie dashboardu wizualizującego najczęściej przewidywane trendy do 2024-11-20.
   - **KPI 4.2**: Raport końcowy z wynikami analizy i rekomendacjami dla twórców YouTube, gotowy do prezentacji do 2024-11-22.

Te KPI pozwolą na systematyczne monitorowanie postępów oraz będą podstawą do ewaluacji wyników na dwóch terminach prezentacyjnych – 2024-11-08 oraz 2024-11-22, w których powinien być gotowy plakat z wynikami całego projektu.

<br/><br/>
**Powiązane prace**  
Podaj, skąd będziesz czerpać wiedzę. Bazując zarówno na literaturze naukowej, jak i kodzie open source, przedstaw:
1. Youtube API - https://developers.google.com/youtube/v3/docs
2. Strona z danymi analitycznymi m.in. YouTube'a - https://socialblade.com/youtube/
3. Mostafa, M.M., Feizollah, A. & Anuar, N.B. Fifteen years of YouTube scholarly research: knowledge structure, collaborative networks, and trending topics. Multimed Tools Appl 82, 12423–12443 (2023). https://doi.org/10.1007/s11042-022-13908-7
4. Choe, M.G., Park, J.H., Seo, D.W. (2019). How Long Will Your Videos Remain Popular? Empirical Study of the Impact of Video Features on YouTube Trending Using Deep Learning Methodologies. In: Xu, J., Zhu, B., Liu, X., Shaw, M., Zhang, H., Fan, M. (eds) The Ecosystem of e-Business: Technologies, Stakeholders, and Connections. WEB 2018. Lecture Notes in Business Information Processing, vol 357. Springer, Cham. https://doi.org/10.1007/978-3-030-22784-5_19