#include <windows.h>
#include <filesystem>
#include <tlhelp32.h>
#include <string.h>
#include <iostream>
#include <string>
namespace fs = std::filesystem;
DWORD GetProccesIdByName(const char* processname) {
    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(PROCESSENTRY32);
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);
    if (Process32First(snapshot, &entry)== TRUE){
        while (Process32Next(snapshot, &entry) == TRUE) {
            if (_stricmp(entry.szExeFile, processname) == 0) {
                DWORD procId = entry.th32ProcessID;
                return procId;
            }
        }
    }
    CloseHandle(snapshot);
    return 0;
}
int main (int argc,char* argv[]) {
    if (IsDebuggerAttached()) {
        MessageBox(NULL,"Debugger founded","aborting",MB_OK | MB_ICONERROR);
        return 1;
    }
    std::string target_process_name;
    std::string dll_path;
    std::cout << "enter target process name" << "\n";
    std::cin >> target_process_name;
    std::cout << "Enter the full path to your dll";
    std::cin.ignore();
    std::getline(std::cin, dll_path);
    std::cout << "trying ot find process " << target_process_name << "\n";
    DWORD pid = GetProccesIdByName(target_process_name.c_str());
    if (pid == 0) {
        std::cout << "process " << target_process_name << " was not found\n";
    } else {
        std::cout << "process id is" << pid;
        return 0;
    }
}
