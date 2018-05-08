import glob
import json
import os

pattern1 = {"name": "File System Permissions Weakness", "description": "Processes may automatically execute specific binaries as part of their functionality or to perform other actions. If the permissions on the file system directory containing a target binary, or permissions on the binary itself, are improperly set, then the target binary may be overwritten with another binary using user-level permissions and executed by the original process. If the original process and thread are running under a higher permissions level, then the replaced binary will also execute under higher-level permissions, which could include SYSTEM.\n\nAdversaries may use this technique to replace legitimate binaries with malicious ones as a means of executing code at a higher permissions level. If the executing process is set to run at a specific time or during a certain event (e.g., system bootup) then this technique can also be used for persistence.\n\n===Services===\n\nManipulation of Windows service binaries is one variation of this technique. Adversaries may replace a legitimate service executable with their own executable to gain persistence and/or privilege escalation to the account context the service is set to execute under (local/domain account, SYSTEM, LocalService, or NetworkService). Once the service is started, either directly by the user (if appropriate access is available) or through some other means, such as a system restart if the service starts on bootup, the replaced executable will run instead of the original service executable.\n\n===Executable Installers===\n\nAnother variation of this technique can be performed by taking advantage of a weakness that is common in executable, self-extracting installers. During the installation process, it is common for installers to use a subdirectory within the <code>%TEMP%</code> directory to unpack binaries such as DLLs, EXEs, or other payloads. When installers create subdirectories and files they often do not set appropriate permissions to restrict write access, which allows for execution of untrusted code placed in the subdirectories or overwriting of binaries used in the installation process. This behavior is related to and may take advantage of DLL Search Order Hijacking. Some installers may also require elevated privileges that will result in privilege escalation when executing adversary controlled code. This behavior is related to Bypass User Account Control. Several examples of this weakness in existing common installers have been reported to software vendors. (Citation: Mozilla Firefox Installer DLL Hijack) (Citation: Seclists Kanthak 7zip Installer)\n\nDetection: Look for changes to binaries and service executables that may normally occur during software updates. If an executable is written, renamed, and/or moved to match an existing service executable, it could be detected and correlated with other suspicious behavior. Hashing of binaries and service executables could be used to detect replacement against historical data.\n\nLook for abnormal process call trees from typical processes and services and for execution of other commands that could relate to Discovery or other adversary techniques.\n\nPlatforms: Windows\n\nData Sources: File monitoring, Process command-line parameters, Services\n\nEffective Permissions: User, Administrator, SYSTEM\n\nPermissions Required: User, Administrator\n\nContributors: Stefan Kanthak, Travis Smith, Tripwire", "kill_chain_phases": [{"kill_chain_name": "mitre-attack", "phase_name": "persistence"}, {"kill_chain_name": "mitre-attack", "phase_name": "privilege-escalation"}], "external_references": [{"url": "https://attack.mitre.org/wiki/Technique/T1044", "source_name": "mitre-attack", "external_id": "T1044"}, {"description": "Kugler, R. (2012, November 20). Mozilla Foundation Security Advisory 2012-98. Retrieved March 10, 2017.", "source_name": "Mozilla Firefox Installer DLL Hijack", "url": "https://www.mozilla.org/en-US/security/advisories/mfsa2012-98/"}, {"description": "Kanthak, S. (2015, December 8). Executable installers are vulnerable^WEVIL (case 7): 7z*.exe\tallows remote code execution with escalation of privilege. Retrieved March 10, 2017.", "source_name": "Seclists Kanthak 7zip Installer", "url": "http://seclists.org/fulldisclosure/2015/Dec/34"}], "object_marking_refs": ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"], "created": "2017-05-31T21:30:43.063Z", "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5", "id": "attack-pattern--0ca7beef-9bbc-4e35-97cf-437384ddce6a", "modified": "2018-04-18T17:59:24.739Z", "type": "attack-pattern"}

attack_patterns = [pattern1]
def load_attack_patterns():
    attack_pat = []
    filepath_read = './static/modified-attack-patterns/*.json'
    files = glob.glob(filepath_read)
    print("Loaded attack patterns...")
    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            try:
                attack_pat.append(data)
            except:
                print("Could not append." + doc)

    print(attack_pat)
    return attack_pat

#load_attack_patterns()

def get_search_pattern(attack_patterns):
    for pattern in attack_patterns:
        print(pattern['name'])

def search_attack_patterns(search_string, attack_patterns):
    search_str = search_string.lower()
    if not search_str:
        return ""
    for pattern in attack_patterns:
        name = pattern['name'].lower()
        if name == search_str:
            return pattern
    return None
