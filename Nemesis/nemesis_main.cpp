// nemesis_main.cpp - KEIN EXTRA FENSTER
#include <windows.h>
#include <iostream>
#include <string>

void setGreen() { SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 10); }
void setRed() { SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 12); }
void setWhite() { SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 7); }
void setYellow() { SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 14); }

void printLogo() {
    HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(h, 12);
    std::cout << R"(
 _   _ ______ __  __ ______  _____ _____ _____ 
| \ | |  ____|  \/  |  ____|/ ____|_   _/ ____|
|  \| | |__  | \  / | |__  | (___   | || (___  
| . ` |  __| | |\/| |  __|  \___ \  | | \___ \ 
| |\  | |____| |  | | |____ ____) |_| |_ ____) 
|_| \_|______|_|  |_|______|_____/|_____/_____/ 
)" << std::endl;
    SetConsoleTextAttribute(h, 7);
}

void checkUrl(const std::string& url, const std::string& name) { std::string cmd = "curl -s -o nul -w \"%{http_code}\" \"" + url + "\"";FILE* f = _popen(cmd.c_str(), "r");if (f) { char buf[64];std::string code;while (fgets(buf, sizeof(buf), f))code += buf;_pclose(f);std::cout << "  " << name << ": ";if (code == "200") { setGreen();std::cout << "FOUND\n"; } else { setRed();std::cout << "NOT\n"; }setWhite(); } }
void usernameSearch() { system("cls");printLogo();std::string user;std::cout << "\n  Username Search\n\n  Username: ";std::getline(std::cin, user);if (user.empty())return;std::cout << "\n";checkUrl("https://github.com/" + user, "GitHub");checkUrl("https://twitter.com/" + user, "Twitter/X");checkUrl("https://instagram.com/" + user, "Instagram");checkUrl("https://tiktok.com/@" + user, "TikTok");checkUrl("https://snapchat.com/add/" + user, "Snapchat");checkUrl("https://reddit.com/user/" + user, "Reddit");checkUrl("https://youtube.com/@" + user, "YouTube");checkUrl("https://twitch.tv/" + user, "Twitch");checkUrl("https://facebook.com/" + user, "Facebook");checkUrl("https://steamcommunity.com/id/" + user, "Steam");checkUrl("https://pinterest.com/" + user, "Pinterest");checkUrl("https://medium.com/@" + user, "Medium");checkUrl("https://dev.to/" + user, "Dev.to");checkUrl("https://gitlab.com/" + user, "GitLab");checkUrl("https://telegram.me/" + user, "Telegram");checkUrl("https://open.spotify.com/user/" + user, "Spotify");checkUrl("https://soundcloud.com/" + user, "SoundCloud");checkUrl("https://flickr.com/people/" + user, "Flickr");checkUrl("https://patreon.com/" + user, "Patreon");std::cout << "\n  Enter...";std::cin.get(); }
void ipLookup() { system("cls");printLogo();std::string ip;std::cout << "\n  IP Lookup\n\n  IP: ";std::getline(std::cin, ip);if (ip.empty())return;std::string cmd = "curl -s \"http://ip-api.com/json/" + ip + "?fields=country,regionName,city,zip,timezone,isp,org,as,query\"";FILE* f = _popen(cmd.c_str(), "r");if (f) { char buf[4096];std::string json;while (fgets(buf, sizeof(buf), f))json += buf;_pclose(f);auto getVal = [&](std::string key)->std::string {size_t p = json.find("\"" + key + "\":\"");if (p == std::string::npos) { p = json.find("\"" + key + "\":");if (p == std::string::npos)return"N/A";p += key.length() + 3;size_t e = json.find(",", p);if (e == std::string::npos)e = json.find("}", p);return json.substr(p, e - p); }p += key.length() + 4;size_t e = json.find("\"", p);return json.substr(p, e - p);};std::cout << "\n  Country:  " << getVal("country") << "\n  Region:   " << getVal("regionName") << "\n  City:     " << getVal("city") << "\n  ZIP:      " << getVal("zip") << "\n  Timezone: " << getVal("timezone") << "\n  ISP:      " << getVal("isp") << "\n  Provider: " << getVal("org") << "\n  AS:       " << getVal("as") << "\n  IP:       " << getVal("query") << "\n"; }std::cout << "\n  Enter...";std::cin.get(); }
void emailBreach() { system("cls");printLogo();std::string email;std::cout << "\n  Email Breach\n\n  Email: ";std::getline(std::cin, email);if (email.empty())return;std::string cmd = "curl -s \"https://haveibeenpwned.com/api/v3/breachedaccount/" + email + "\" -H \"hibp-api-key: demo\" 2>nul";FILE* f = _popen(cmd.c_str(), "r");if (f) { char buf[8192];std::string json;while (fgets(buf, sizeof(buf), f))json += buf;_pclose(f);std::cout << "\n";if (json.find("[") != std::string::npos) { std::cout << "  Breaches found:\n";size_t pos = 0;while ((pos = json.find("Name\":\"", pos)) != std::string::npos) { pos += 7;size_t end = json.find("\"", pos);std::cout << "  - " << json.substr(pos, end - pos) << "\n";pos = end; } } else { std::cout << "  No breaches found.\n"; } }std::cout << "\n  Enter...";std::cin.get(); }
void phoneLookup() { system("cls");printLogo();std::string phone;std::cout << "\n  Phone Lookup\n\n  Phone: ";std::getline(std::cin, phone);if (phone.empty())return;std::string cmd = "curl -s \"https://api.numlookupapi.io/v1/validate?number=" + phone + "\"";FILE* f = _popen(cmd.c_str(), "r");if (f) { char buf[4096];std::string json;while (fgets(buf, sizeof(buf), f))json += buf;_pclose(f);auto getVal = [&](std::string key)->std::string {size_t p = json.find("\"" + key + "\":\"");if (p == std::string::npos) { p = json.find("\"" + key + "\":");if (p == std::string::npos)return"N/A";p += key.length() + 3;size_t e = json.find(",", p);if (e == std::string::npos)e = json.find("}", p);return json.substr(p, e - p); }p += key.length() + 4;size_t e = json.find("\"", p);return json.substr(p, e - p);};std::cout << "\n  Number  : " << getVal("number") << "\n  Valid   : " << getVal("valid") << "\n  Country : " << getVal("country_name") << "\n  Line    : " << getVal("line_type") << "\n  Carrier : " << getVal("carrier") << "\n"; }std::cout << "\n  Enter...";std::cin.get(); }
void dnsLookup() { system("cls");printLogo();std::string domain;std::cout << "\n  DNS Lookup\n\n  Domain: ";std::getline(std::cin, domain);if (domain.empty())return;std::cout << "\n";system(("nslookup " + domain).c_str());std::cout << "\n  Enter...";std::cin.get(); }
void webhookInfo() { system("cls");printLogo();std::string wh;std::cout << "\n  Webhook Info\n\n  URL: ";std::getline(std::cin, wh);if (wh.empty())return;std::string cmd = "curl -s \"" + wh + "\"";FILE* f = _popen(cmd.c_str(), "r");if (f) { char buf[4096];std::string json;while (fgets(buf, sizeof(buf), f))json += buf;_pclose(f);auto getVal = [&](std::string key)->std::string {size_t p = json.find("\"" + key + "\":\"");if (p == std::string::npos) { p = json.find("\"" + key + "\":");if (p == std::string::npos)return"N/A";p += key.length() + 3;size_t e = json.find(",", p);if (e == std::string::npos)e = json.find("}", p);return json.substr(p, e - p); }p += key.length() + 4;size_t e = json.find("\"", p);return json.substr(p, e - p);};std::cout << "\n  Name    : " << getVal("name") << "\n  ID      : " << getVal("id") << "\n  Channel : " << getVal("channel_id") << "\n  Guild   : " << getVal("guild_id") << "\n  Token   : " << getVal("token") << "\n"; }std::cout << "\n  Enter...";std::cin.get(); }
void portScan() { system("cls");printLogo();std::string ip;std::cout << "\n  Port Scanner\n\n  IP: ";std::getline(std::cin, ip);if (ip.empty())return;std::cout << "\n";int ports[] = { 21,22,25,53,80,110,143,443,445,993,995,3306,3389,5900,8080 };for (int p : ports) { std::string cmd = "curl -s --connect-timeout 1 telnet://" + ip + ":" + std::to_string(p) + " 2>nul 1>nul";int r = system(cmd.c_str());std::cout << "  Port " << p << "  : ";if (r == 0) { setGreen();std::cout << "OPEN\n"; } else { setRed();std::cout << "CLOSED\n"; }setWhite(); }std::cout << "\n  Enter...";std::cin.get(); }

int main() {
    SetConsoleTitleA("NEMESIS");

    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    std::string dir = exePath;
    dir = dir.substr(0, dir.find_last_of("\\/"));

    while (true) {
        system("cls"); printLogo();
        HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
        std::cout << "\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [1] "; SetConsoleTextAttribute(h, 7); std::cout << "Build Stealer\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [2] "; SetConsoleTextAttribute(h, 7); std::cout << "Username Search\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [3] "; SetConsoleTextAttribute(h, 7); std::cout << "IP Lookup\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [4] "; SetConsoleTextAttribute(h, 7); std::cout << "Email Breach\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [5] "; SetConsoleTextAttribute(h, 7); std::cout << "Phone Lookup\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [6] "; SetConsoleTextAttribute(h, 7); std::cout << "DNS Lookup\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [7] "; SetConsoleTextAttribute(h, 7); std::cout << "Webhook Info\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [8] "; SetConsoleTextAttribute(h, 7); std::cout << "Port Scanner\n";
        SetConsoleTextAttribute(h, 14); std::cout << " [9] "; SetConsoleTextAttribute(h, 7); std::cout << "Exit\n";
        std::cout << "\n > ";
        int c; std::cin >> c; std::cin.ignore();
        if (c == 1) {
            ShowWindow(GetConsoleWindow(), SW_MINIMIZE);
            std::string cmd = "python \"" + dir + "\\nemesis_py_builder.py\"";
            system(cmd.c_str());
            ShowWindow(GetConsoleWindow(), SW_RESTORE);
        }
        else if (c == 2)usernameSearch();else if (c == 3)ipLookup();else if (c == 4)emailBreach();else if (c == 5)phoneLookup();
        else if (c == 6)dnsLookup();else if (c == 7)webhookInfo();else if (c == 8)portScan();else if (c == 9)break;
    }
    return 0;
}